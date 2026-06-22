#!/usr/bin/env python3
"""Reconcile Run-the-Docs media: EXPECTED (lines.json) vs ON-R2 vs IN-CATALOG.

Pure and secret-free, so it is CI-testable and never touches credentials or the
network. The orchestrator gathers the authenticated R2 object listing via the
Cloudflare MCP (`r2_list_objects`) and feeds it in as JSON; this tool computes the
drift and an updated catalogue. The orchestrator then acts on the report: open a
run-the-docs/website PR for the healed catalogue, and/or alert on byte-gaps.

Drift classes:
  wiring-drift   916 present on R2 but catalog v916 missing  -> self-heal: set v916
  wired-but-404  catalog v916 set but 916 absent on R2        -> self-heal: strip v916
  needs-upload   an expected key is absent on R2              -> ALERT (only the Mac Mini
                                                                can produce the bytes)
  missing-card   expected/on-R2 episode has no catalog entry  -> flag (editorial)

Usage:
  reconcile-media.py --catalog catalog.json --r2-json r2.json --lines-dir DIR \
                     [--public-base URL] [--write OUT_CATALOG] [--report OUT_JSON]
  --r2-json : JSON; either the raw Cloudflare `r2_list_objects` response ({"result":[...]})
              or a bare array of {key,size,etag}.
Exit: 0 = clean · 2 = action needed (wiring healed and/or byte-gaps) · 1 = error.
"""
import argparse, json, os, re, sys, glob, copy

DEFAULT_PUBLIC_BASE = "https://pub-8745206116f440c6b36f5e6bd0eb1905.r2.dev"

LINES_RE = re.compile(r"^ep(.+)\.lines\.json$")
KEY_RE = re.compile(r"^claude-ep(.+?)-(45|916)\.mp4$")
FILE_ID_RE = re.compile(r"claude-ep(.+?)-45\.mp4")


def load_r2_keys(r2_json):
    """Accept either {'result':[...]} (raw MCP response) or a bare [...] list."""
    data = json.loads(r2_json) if isinstance(r2_json, str) else r2_json
    items = data.get("result", data) if isinstance(data, dict) else data
    keys = {}
    for it in items:
        k = it.get("key") if isinstance(it, dict) else it
        if k:
            keys[k] = it if isinstance(it, dict) else {}
    return keys


def expected_ids(lines_dir):
    """Map episode id -> published(bool) for every ep*.lines.json."""
    out = {}
    for path in sorted(glob.glob(os.path.join(lines_dir, "ep*.lines.json"))):
        m = LINES_RE.match(os.path.basename(path))
        if not m:
            continue
        eid = m.group(1)
        published = True
        try:
            d = json.load(open(path, encoding="utf-8"))
            if isinstance(d, dict) and d.get("published") is False:
                published = False
        except Exception:
            pass
        out[eid] = published
    return out


def catalog_episode_id(ep):
    m = FILE_ID_RE.search(ep.get("file", ""))
    return m.group(1) if m else None


def reconcile(catalog, r2_keys, expected, public_base):
    report = {"wiring_drift": [], "wired_404": [], "needs_upload": {},
              "missing_card": [], "summary": {}}
    updated = copy.deepcopy(catalog)
    eps = updated.get("claude_code", {}).get("episodes", [])

    # 1) self-heal the catalogue's wiring against R2 truth
    for ep in eps:
        cid = catalog_episode_id(ep)
        if cid is None:
            continue
        has916 = f"claude-ep{cid}-916.mp4" in r2_keys
        if has916 and not ep.get("v916"):
            ep["v916"] = f"{public_base}/claude-ep{cid}-916.mp4"
            report["wiring_drift"].append(cid)
        elif ep.get("v916") and not has916:
            ep["v916"] = None
            report["wired_404"].append(cid)

    catalog_ids = {catalog_episode_id(e) for e in eps}

    # 2) byte-gaps + missing cards, from EXPECTED
    for eid, published in expected.items():
        if not published:
            continue
        missing = [fmt for fmt in ("45", "916")
                   if f"claude-ep{eid}-{fmt}.mp4" not in r2_keys]
        if missing:
            report["needs_upload"][eid] = missing
        if eid not in catalog_ids:
            report["missing_card"].append(eid)

    present_eps = sorted({eid for eid in expected
                          if f"claude-ep{eid}-916.mp4" in r2_keys
                          and f"claude-ep{eid}-45.mp4" in r2_keys})
    report["summary"] = {
        "expected_episodes": len(expected),
        "fully_on_r2": len(present_eps),
        "wiring_healed": len(report["wiring_drift"]) + len(report["wired_404"]),
        "needs_upload_episodes": len(report["needs_upload"]),
        "missing_cards": len(report["missing_card"]),
    }
    report["clean"] = not (report["wiring_drift"] or report["wired_404"]
                           or report["needs_upload"] or report["missing_card"])
    catalog_changed = bool(report["wiring_drift"] or report["wired_404"])
    return report, updated, catalog_changed


def _idkey(e):
    return (0, int(e)) if e.isdigit() else (1, e)


def human(report):
    s = report["summary"]
    lines = [
        f"expected={s['expected_episodes']}  fully-on-R2={s['fully_on_r2']}  "
        f"wiring-healed={s['wiring_healed']}  needs-upload={s['needs_upload_episodes']}  "
        f"missing-cards={s['missing_cards']}",
    ]
    if report["wiring_drift"]:
        lines.append(f"  SELF-HEAL set v916 for: {', '.join(report['wiring_drift'])}")
    if report["wired_404"]:
        lines.append(f"  SELF-HEAL stripped v916 (R2 404) for: {', '.join(report['wired_404'])}")
    nu = set(report["needs_upload"])
    mc = set(report["missing_card"])
    # carded episodes (have a catalog card => already rendered) only need uploading;
    # un-carded ones were never rendered => build-ep.sh first.
    upload_ready = sorted(nu - mc, key=_idkey)
    render_first = sorted(nu & mc, key=_idkey)
    if upload_ready:
        lines.append("  UPLOAD (cuts rendered, just push to R2): "
                     + ", ".join("ep" + e for e in upload_ready))
        lines.append("    -> on the Mac Mini: bash series/claude-code/production/r2-sync.sh "
                     + " ".join(upload_ready))
    if render_first:
        lines.append("  RENDER+UPLOAD (no card/cuts yet — build-ep.sh first, then r2-sync): "
                     + ", ".join("ep" + e for e in render_first))
    if report["clean"]:
        lines.append("  CLEAN — every expected episode is on R2 and correctly wired.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--r2-json", required=True)
    ap.add_argument("--lines-dir", required=True)
    ap.add_argument("--public-base", default=DEFAULT_PUBLIC_BASE)
    ap.add_argument("--write", help="write the reconciled catalog here if wiring changed")
    ap.add_argument("--report", help="write the JSON report here")
    args = ap.parse_args(argv)

    catalog = json.load(open(args.catalog, encoding="utf-8"))
    r2_keys = load_r2_keys(open(args.r2_json, encoding="utf-8").read())
    expected = expected_ids(args.lines_dir)

    report, updated, changed = reconcile(catalog, r2_keys, expected, args.public_base)
    print(human(report))
    if args.report:
        json.dump(report, open(args.report, "w", encoding="utf-8"), indent=2)
    if args.write and changed:
        json.dump(updated, open(args.write, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"  wrote reconciled catalog -> {args.write}")
    return 0 if report["clean"] else 2


if __name__ == "__main__":
    sys.exit(main())

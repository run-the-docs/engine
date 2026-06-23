#!/usr/bin/env python3
"""Auth-free R2 presence probe — the scheduled media-reconcile routine's R2-list source.

HEAD-probes every EXPECTED Claude Code cut on the public r2.dev domain and emits the
present ones as the `[{key,bytes,etag}]` JSON that `reconcile-media.py --r2-json` accepts.

Why this exists: the Cloudflare MCP `r2_list_objects` caps at ~20 objects/call with no
cursor input (can't reliably list the full bucket), and the in-bucket `manifest.json`
(Phase 2) only appears after a Mac-Mini `r2-sync.sh` run. Probing the *known* expected keys
sidesteps both — it always works, is complete for the keys we care about, and needs no
credentials. Key derivation is pure (unit-tested); network lives only at the edge.

Usage:
  r2-probe.py --lines-dir series/claude-code/production [--public-base URL] > r2.json
"""
import argparse, glob, json, os, re, sys, urllib.request

DEFAULT_PUBLIC_BASE = "https://pub-8745206116f440c6b36f5e6bd0eb1905.r2.dev"
LINES_RE = re.compile(r"^ep(.+)\.lines\.json$")
# Cloudflare's WAF 403s the default python-urllib User-Agent; a named UA is allowed.
UA = "rtd-reconcile/1.0 (run-the-docs media reconciler)"


def expected_keys(lines_dir):
    """Every claude-ep<ID>-{45,916}.mp4 expected from a *published* ep*.lines.json
    (mirrors reconcile-media.py: skips published:false; ID 'fable5' from epfable5.lines.json)."""
    keys = []
    for path in sorted(glob.glob(os.path.join(lines_dir, "ep*.lines.json"))):
        m = LINES_RE.match(os.path.basename(path))
        if not m:
            continue
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            d = {}
        if isinstance(d, dict) and d.get("published") is False:
            continue
        for fmt in ("45", "916"):
            keys.append(f"claude-ep{m.group(1)}-{fmt}.mp4")
    return keys


def probe(keys, base):
    """HEAD each key on r2.dev; return [{key,bytes,etag}] for the live (HTTP 200) ones."""
    base = base.rstrip("/")
    present = []
    for k in keys:
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(f"{base}/{k}", method="HEAD",
                                           headers={"User-Agent": UA}), timeout=15) as r:
                if r.status != 200:
                    continue
                size = r.headers.get("Content-Length")
                present.append({"key": k,
                                "bytes": int(size) if size and size.isdigit() else None,
                                "etag": (r.headers.get("ETag") or "").strip('"') or None})
        except Exception:
            continue  # absent / private / unreachable -> not present
    return present


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines-dir", required=True)
    ap.add_argument("--public-base", default=DEFAULT_PUBLIC_BASE)
    args = ap.parse_args(argv)
    json.dump(probe(expected_keys(args.lines_dir), args.public_base),
              sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Turn a reconcile-media.py report into Discord-ready alerts + a green heartbeat.

Phase 4 of epic #40. The media reconciler runs orchestrator-side (claude-3 via the
Cloudflare MCP — zero new secret). This pure, secret-free helper converts its
`--report` JSON into the two-tier alert text the orchestrator posts via the Discord MCP,
plus the weekly green heartbeat. The orchestrator owns the side effects (Discord post,
deadline-tracker dead-man's-switch); this file owns only the decision + wording, so it is
unit-testable.

Two-tier severity escalates with `--occurrences` (how many consecutive reconcile ticks the
same gap has persisted — the orchestrator tracks this in the deadline-tracker, the durable
cross-run state):
  1–2 consecutive  -> ⚠️  WARN  (#admin)
  >=3 consecutive  -> 🚨  URGENT (#admin) + escalate=true (raise a deadline-tracker entry)

Self-healed drift (wiring-drift / wired-404) is reported as context, not an action item —
the reconciler fixes those itself via the website PR.

Usage:
  reconcile-alert.py --report report.json [--occurrences N] [--heartbeat-due]
Emits a JSON decision to stdout:
  {clean, escalate, occurrences, admin_alert|null, heartbeat|null}
Exit: 0 always (it's a formatter; the orchestrator decides what to send).
"""
import argparse, json, sys

PUBLIC_HINT = "series/claude-code/production/r2-sync.sh"


def _idkey(e):
    return (0, int(e)) if str(e).isdigit() else (1, str(e))


def build(report, occurrences, heartbeat_due):
    clean = report.get("clean", False)
    s = report.get("summary", {})
    nu = set(report.get("needs_upload", {}))
    mc = set(report.get("missing_card", []))
    drift = report.get("wiring_drift", []) or []
    dead = report.get("wired_404", []) or []

    escalate = (not clean) and occurrences >= 3
    out = {"clean": clean, "escalate": escalate, "occurrences": occurrences,
           "admin_alert": None, "heartbeat": None}

    if not clean:
        sev = "🚨 URGENT" if escalate else "⚠️"
        nth = f" ({occurrences}× consecutive)" if occurrences > 1 else ""
        lines = [f"{sev} RtD media reconcile: gap detected{nth}.",
                 f"   on-R2 {s.get('fully_on_r2','?')}/{s.get('expected_episodes','?')} expected episodes."]
        upload_ready = sorted(nu - mc, key=_idkey)   # carded -> cuts rendered -> just upload
        render_first = sorted(nu & mc, key=_idkey)   # no card -> build-ep.sh first
        if upload_ready:
            lines.append("   UPLOAD (rendered, push to R2): "
                         + " ".join("ep" + e for e in upload_ready))
            lines.append("     → on the Mac Mini: bash " + PUBLIC_HINT + " "
                         + " ".join(upload_ready))
        if render_first:
            lines.append("   RENDER+UPLOAD (no card/cuts — build-ep.sh first): "
                         + " ".join("ep" + e for e in render_first))
        if report.get("missing_card"):
            lines.append("   missing card (editorial): "
                         + " ".join("ep" + e for e in sorted(mc, key=_idkey)))
        if drift or dead:
            lines.append(f"   (self-healed wiring: {len(drift)} set, {len(dead)} stripped — PR opened)")
        if escalate:
            lines.append("   ↑ 3rd+ consecutive tick — raising a deadline-tracker entry.")
        out["admin_alert"] = "\n".join(lines)

    if clean and heartbeat_due:
        out["heartbeat"] = (
            f"✅ RtD media reconcile green — {s.get('fully_on_r2','?')}/"
            f"{s.get('expected_episodes','?')} expected episodes on R2, wiring correct. "
            f"(weekly heartbeat / dead-man's-switch renewed)")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--occurrences", type=int, default=1,
                    help="consecutive reconcile ticks this gap has persisted (orchestrator-tracked)")
    ap.add_argument("--heartbeat-due", action="store_true",
                    help="a weekly green heartbeat is due (emit it when clean)")
    args = ap.parse_args(argv)
    report = json.load(open(args.report, encoding="utf-8"))
    json.dump(build(report, args.occurrences, args.heartbeat_due),
              sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

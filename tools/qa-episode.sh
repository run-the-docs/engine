#!/usr/bin/env bash
# qa-episode.sh — Layout verification wrapper for Run the Docs episodes
#
# Usage: qa-episode.sh <html-file> <timing.json>
#
# Runs verify-layout.js and outputs a clear PASS/FAIL report.
# Returns exit code 0 on pass, 1 on any violation (CI-safe).

set -euo pipefail

NODE=/opt/homebrew/bin/node
SCRIPT="$(cd "$(dirname "$0")" && pwd)/verify-layout.js"

# ── Arg validation ────────────────────────────────────────────────────────────
if [[ $# -lt 2 ]]; then
  echo "Usage: qa-episode.sh <html-file> <timing.json>"
  exit 1
fi

HTML_FILE="$1"
TIMING_FILE="$2"

if [[ ! -f "$HTML_FILE" ]]; then
  echo "ERROR: HTML file not found: $HTML_FILE"
  exit 1
fi

if [[ ! -f "$TIMING_FILE" ]]; then
  echo "ERROR: Timing file not found: $TIMING_FILE"
  exit 1
fi

if [[ ! -f "$NODE" ]]; then
  echo "ERROR: Node not found at $NODE"
  exit 1
fi

# ── Run verification ──────────────────────────────────────────────────────────
echo ""
echo "┌─────────────────────────────────────────────┐"
echo "│       RUN THE DOCS — EPISODE QA CHECK       │"
echo "└─────────────────────────────────────────────┘"
echo ""
echo "  HTML   : $HTML_FILE"
echo "  Timing : $TIMING_FILE"
echo "  Node   : $NODE"
echo ""

START_TIME=$(date +%s)

set +e
"$NODE" "$SCRIPT" "$HTML_FILE" "$TIMING_FILE"
EXIT_CODE=$?
set -e

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "  Elapsed: ${ELAPSED}s"
echo ""

if [[ $EXIT_CODE -eq 0 ]]; then
  echo "┌─────────────────────────────────────────────┐"
  echo "│              ✅  QA PASSED                  │"
  echo "└─────────────────────────────────────────────┘"
else
  echo "┌─────────────────────────────────────────────┐"
  echo "│              ❌  QA FAILED                  │"
  echo "│    Review violations above before render    │"
  echo "└─────────────────────────────────────────────┘"
fi

echo ""
exit $EXIT_CODE

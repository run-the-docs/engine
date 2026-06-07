#!/bin/bash
# Self-test for the COMPOSE GUARD (rc 2026-06-07). Simulates the exact bug: make rec/narration.json
# be EP5's while composing as ep1, and assert compose REFUSES (non-zero + "COMPOSE GUARD").
# Then assert a matching episode passes the guard. Restores narration.json on exit.
set -u
DEMO=~/runthedocs/series/claude-code/demo; REC=$DEMO/rec
VVPY=~/voicebox-venv/bin/python
BK=$(mktemp)
[ -f "$REC/narration.json" ] && cp "$REC/narration.json" "$BK"
restore(){ [ -s "$BK" ] && cp "$BK" "$REC/narration.json"; rm -f "$BK"; }
trap restore EXIT

fail=0

# --- Case 1: mismatch must be REJECTED ---
cp "$REC/narration-ep5.json" "$REC/narration.json"
OUT=$(CC_TERM="claude-ep1-term.mp4" CC_OUT="claude-ep1-45.mp4" "$VVPY" "$DEMO/compose_45.py" 2>&1)
rc=$?
if [ $rc -ne 0 ] && echo "$OUT" | grep -q "COMPOSE GUARD"; then
  echo "PASS case1: mismatch rejected (rc=$rc)"
else
  echo "FAIL case1: mismatch NOT rejected (rc=$rc)"; echo "$OUT" | tail -3; fail=1
fi

# --- Case 2: matching episode must PASS the guard (we only check it gets PAST the guard,
#     not a full render — kill it right after the guard by pointing at a bogus term so it
#     fails LATER with a non-guard error). Simpler: assert the guard message is absent. ---
cp "$REC/narration-ep1.json" "$REC/narration.json"
OUT=$(CC_TERM="claude-ep1-term.mp4" CC_OUT="claude-ep1-45.mp4" "$VVPY" "$DEMO/compose_45.py" 2>&1)
rc=$?
if echo "$OUT" | grep -q "COMPOSE GUARD"; then
  echo "FAIL case2: matching episode wrongly blocked by guard"; fail=1
else
  echo "PASS case2: matching episode passed the guard (rc=$rc)"
fi

[ $fail -eq 0 ] && echo "GUARD_SELFTEST_OK" || echo "GUARD_SELFTEST_FAILED"
exit $fail

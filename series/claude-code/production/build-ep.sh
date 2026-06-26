#!/bin/bash
# Build one Claude Code LinkedIn episode (both 4:5 and 9:16) from its lines.json + terminal recording.
# Usage:  bash build-ep.sh <N>
#         RENDER_ONLY=1 bash build-ep.sh <N>   # reuse cached narration (no TTS re-roll), re-render only
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
export PYTORCH_ENABLE_MPS_FALLBACK=1
N=$1
DEMO=~/runthedocs/series/claude-code/demo; REPO=$DEMO/cc-demo-repo; REC=$DEMO/rec
CVPY=~/chatterbox-venv/bin/python; VVPY=~/voicebox-venv/bin/python; PY=/opt/homebrew/bin/python3
LOG=~/ep${N}build.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1

# rc(2026-06-07 ep1-card fix): reset the demo repo to THIS episode's starting commit BEFORE
# rendering assets, so the file-card (make_assets_45 reads the live file) reflects the episode's
# own file state — not whatever a later episode's build/recording left behind.
# KEEP THESE COMMITS IN SYNC WITH recd.sh's per-episode RESET= values.
case "$N" in
  1) RESET=5411d3b ;;
  2) RESET=5411d3b ;;
  3) RESET=6a8d07c ;;
  4) RESET=29299f9 ;;
  5) RESET=0b6488a ;;
  8) RESET=15ca978 ;;
  10) RESET=b4bc357 ;;
  7) RESET=d3c3da0 ;;
  9) RESET=ec4eb0e ;;
  6) RESET=5411d3b ;;
  11) RESET=9e97a74 ;;
  fable5) RESET=0a11b0a ;;
  29) RESET=5411d3b ;;
  28) RESET=5411d3b ;;
  30) RESET=6a8d07c ;;
  31) RESET=5411d3b ;;
  26) RESET=5411d3b ;;
  32) RESET=5411d3b ;;
  33) RESET=6a8d07c ;;
  34) RESET=5411d3b ;;
  35) RESET=5411d3b ;;
  36) RESET=5411d3b ;;
  *) RESET="" ;;
  22) RESET=5411d3b ;;
  27) RESET=5411d3b ;;
  18) RESET=5411d3b ;;
  25) RESET=5411d3b ;;
  38) RESET=5411d3b ;;
esac
if [ -n "$RESET" ]; then
  git -C "$REPO" reset --hard "$RESET" >/dev/null 2>&1 && git -C "$REPO" clean -fdq >/dev/null 2>&1 \
    && echo "repo reset to $RESET (ep$N)" || echo "WARN: repo reset to $RESET failed"
fi

# ep17 (/init): the artifact card is the GENERATED CLAUDE.md, which lives in the synthetic stand-in
# scratch repo (NOT cc-demo-repo). CC_REPO redirects make_assets's artifact lookup there.
if [ "$N" = "17" ]; then
  export CC_REPO=~/runthedocs/scratch/cc-ep17-demo
  echo "ep17: artifact card sourced from $CC_REPO (synthetic stand-in)"
fi

if [ "$RENDER_ONLY" = "1" ] && [ -f "$REC/narration-ep${N}.json" ]; then
  echo "=== RENDER_ONLY: reuse cached narration-ep$N (no TTS re-roll) ==="
  cp "$REC/narration-ep${N}.json" "$REC/narration.json"; cp "$REC/narration-ep${N}.wav" "$REC/narration.wav"
else
  echo "=== narration ep$N ==="; $CVPY "$DEMO/narrate_chatterbox.py" "$DEMO/ep${N}.lines.json" || { echo FATAL narrate; exit 1; }
  cp "$REC/narration.json" "$REC/narration-ep${N}.json"; cp "$REC/narration.wav" "$REC/narration-ep${N}.wav"  # cache for render-only reruns
fi

# rc(2026-06-07): assert the ACTIVE narration really is this episode's before it is baked into
# assets+audio. Defence-in-depth against a stale rec/narration.json (the EP1/EP2-titled-as-EP5 bug).
T_SRC=$($PY -c "import json;print(json.load(open('$DEMO/ep${N}.lines.json'))['title'])" 2>/dev/null)
T_NAR=$($PY -c "import json;print(json.load(open('$REC/narration.json')).get('title',''))" 2>/dev/null)
if [ "$T_SRC" != "$T_NAR" ]; then
  echo "FATAL narration mismatch: ep${N}.lines.json title='$T_SRC' but rec/narration.json title='$T_NAR'"; exit 9
fi
echo "narration OK: '$T_NAR'"

echo "=== assets 4:5 ==="; $VVPY "$DEMO/make_assets_45.py" || { echo FATAL assets; exit 2; }
echo "=== compose 4:5 (term=claude-ep${N}-term.mp4) ==="; CC_TERM="claude-ep${N}-term.mp4" CC_OUT="claude-ep${N}-45.mp4" $VVPY "$DEMO/compose_45.py" || { echo FATAL compose45; exit 3; }
echo "=== assets 9:16 ==="; $VVPY "$DEMO/make_assets_916.py" || { echo FATAL assets916; exit 4; }
echo "=== compose 9:16 ==="; CC_TERM="claude-ep${N}-term.mp4" CC_OUT="claude-ep${N}-916.mp4" $VVPY "$DEMO/compose_916.py" || { echo FATAL compose916; exit 5; }
ls -la "$REC/claude-ep${N}-45.mp4" "$REC/claude-ep${N}-916.mp4"
echo "EP${N}BUILD_OK"

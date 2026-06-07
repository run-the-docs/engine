#!/bin/bash
# Render-only (no re-narrate): restores cached per-episode narration, then assets + compose.
# Usage: bash render45.sh <N>   (requires a prior build-ep.sh run to have cached narration-ep<N>.*)
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
N=$1
DEMO=~/runthedocs/series/claude-code/demo; REC=$DEMO/rec; VVPY=~/voicebox-venv/bin/python
[ -f "$REC/narration-ep${N}.json" ] || { echo "FATAL: no cached narration-ep${N}.json (run build-ep.sh $N first)"; exit 1; }
cp "$REC/narration-ep${N}.json" "$REC/narration.json"
cp "$REC/narration-ep${N}.wav" "$REC/narration.wav"
echo "=== assets 4:5 ep$N ==="; $VVPY "$DEMO/make_assets_45.py" || { echo FATAL assets45; exit 2; }
echo "=== compose 4:5 ep$N ==="; CC_TERM="claude-ep${N}-term.mp4" CC_OUT="claude-ep${N}-45.mp4" $VVPY "$DEMO/compose_45.py" || { echo FATAL compose45; exit 3; }
echo "=== assets 9:16 ep$N ==="; $VVPY "$DEMO/make_assets_916.py" || { echo FATAL assets916; exit 4; }
echo "=== compose 9:16 ep$N ==="; CC_TERM="claude-ep${N}-term.mp4" CC_OUT="claude-ep${N}-916.mp4" $VVPY "$DEMO/compose_916.py" || { echo FATAL compose916; exit 5; }
ffprobe -v error -show_entries format=duration -of csv=p=0 "$REC/claude-ep${N}-45.mp4"
echo "RENDER45_OK ep$N (4:5 + 9:16)"

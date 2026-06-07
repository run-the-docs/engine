#!/bin/bash
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
export PYTORCH_ENABLE_MPS_FALLBACK=1
N=$1
DEMO=~/runthedocs/series/claude-code/demo; CVPY=~/chatterbox-venv/bin/python; VVPY=~/voicebox-venv/bin/python
LOG=~/ep${N}build.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1
echo "=== narration ep$N ==="; $CVPY "$DEMO/narrate_chatterbox.py" "$DEMO/ep${N}.lines.json" || { echo FATAL narrate; exit 1; }
echo "=== assets ==="; $VVPY "$DEMO/make_assets_45.py" || { echo FATAL assets; exit 2; }
echo "=== compose (term=claude-ep${N}-term.mp4) ==="; CC_TERM="claude-ep${N}-term.mp4" CC_OUT="claude-ep${N}-45.mp4" $VVPY "$DEMO/compose_45.py" || { echo FATAL compose; exit 3; }
ls -la "$DEMO/rec/claude-ep${N}-45.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$DEMO/rec/claude-ep${N}-45.mp4" 2>/dev/null
echo "EP${N}BUILD_OK"

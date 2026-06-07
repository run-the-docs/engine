#!/bin/bash
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
LOG=~/ep3rec.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1
TM=/opt/homebrew/bin/tmux; TOKEN=~/.config/claude/oauth-token
DEMO=~/runthedocs/series/claude-code/demo; REPO=$DEMO/cc-demo-repo; REC=$DEMO/rec; W=110; H=30
# --- scenario: project conventions in CLAUDE.md; clean slate for the new helper ---
cat > "$REPO/CLAUDE.md" <<'CMD'
# Project conventions

- String utilities are plain functions, one feature per module file.
- Every function has a matching test in `test_<name>.py` using the `check(got, want)` assertion helper.
- Run a test with: `python3 test_<name>.py`
- Keep functions small and pure; no external dependencies.
CMD
rm -f "$REPO/titlecase.py" "$REPO/test_titlecase.py"
( cd "$REPO" && git add -A && git -c user.email=demo@local -c user.name=demo commit -q -m "add CLAUDE.md conventions" 2>/dev/null )
sleep 1.5
sleep 1.5
$TM kill-session -t ccrec2 2>/dev/null   # stop recorder at result frame (no exit tail)
sleep 1
$TM kill-session -t cclive 2>/dev/null
$TM new-session -d -s cclive -x $W -y $H; $TM set-option -t cclive status off
$TM send-keys -t cclive "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; export CLAUDE_CODE_OAUTH_TOKEN=\$(cat $TOKEN); cd $REPO; clear" Enter
sleep 1
$TM send-keys -t cclive "claude --allowedTools Read Edit Write \"Bash(python3 *)\" --disallowedTools WebFetch WebSearch" Enter
sleep 12
$TM new-session -d -s ccrec2 -x $W -y $H; $TM set-option -t ccrec2 status off
$TM send-keys -t ccrec2 "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; asciinema rec $REC/claude-ep3.cast --overwrite --idle-time-limit 1.2 --command 'tmux attach -t cclive -r'" Enter
sleep 3
$TM send-keys -t cclive "Add a titlecase(text) helper and a test for it, following our conventions."
sleep 1; $TM send-keys -t cclive Enter; echo "prompt sent"
prev=""; stable=0
for i in $(seq 1 60); do
  sleep 3; pane=$($TM capture-pane -pt cclive 2>/dev/null); h=$(echo "$pane"|md5)
  [ "$h" = "$prev" ] && stable=$((stable+1)) || stable=0; prev=$h
  [ $i -ge 5 ] && [ $stable -ge 3 ] && { echo "stable iter $i"; break; }
done
grep -qiE 'sk-ant|oat01' "$REC/claude-ep3.cast" && { echo FATAL token; exit 3; }
echo "--- did claude create titlecase + test? ---"; ls "$REPO"/titlecase.py "$REPO"/test_titlecase.py 2>/dev/null; ( cd "$REPO" && python3 test_titlecase.py 2>&1 | tail -1 )
agg "$REC/claude-ep3.cast" "$REC/claude-ep3.gif" --theme asciinema --font-size 22 2>&1 | tail -1
ffmpeg -y -i "$REC/claude-ep3.gif" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos" -pix_fmt yuv420p -movflags +faststart "$REC/claude-ep3-term.mp4" 2>/dev/null
echo "term dur:"; ffprobe -v error -show_entries format=duration -of csv=p=0 "$REC/claude-ep3-term.mp4" 2>/dev/null
echo "EP3REC_OK"

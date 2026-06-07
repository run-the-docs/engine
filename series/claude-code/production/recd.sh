#!/bin/bash
# Unified detail-recorder: shows the artifact file (cat) before launching claude.
# Usage: EP=<n> bash recd.sh   (scenario files must be staged beforehand)
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
LOG=~/rec_${EP}.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1
TM=/opt/homebrew/bin/tmux; TOKEN=~/.config/claude/oauth-token
DEMO=~/runthedocs/series/claude-code/demo; REPO=$DEMO/cc-demo-repo; REC=$DEMO/rec; W=110; H=30
case "$EP" in
 1) ARTIFACTS="slugify.py"; CLAUDE='claude --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="What does this project do, and what is the bug in slugify.py? Explain briefly. Do not change any files."; COMPLETE=stable ;;
 2) ARTIFACTS="test_slugify.py slugify.py"; CLAUDE='claude --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Fix slugify.py so the failing test passes, then run it."; COMPLETE=testpass ;;
 3) ARTIFACTS="CLAUDE.md"; CLAUDE='claude --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Add a titlecase(text) helper and a test for it, following our conventions."; COMPLETE=stable ;;
 4) ARTIFACTS="slugify.py titlecase.py"; CLAUDE='claude --permission-mode plan --effort low --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Plan how to reorganize slugify and titlecase into one shared textkit module with a single test file. Just the plan, do not edit."; COMPLETE=menu ;;
 5) ARTIFACTS=".claude/commands/test.md"; CLAUDE='claude --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch --effort low'; MODE=slash; TEXT="/test"; COMPLETE=stable ;;
esac
$TM kill-session -t cclive 2>/dev/null; $TM kill-session -t ccrec2 2>/dev/null
$TM new-session -d -s cclive -x $W -y $H; $TM set-option -t cclive status off
$TM send-keys -t cclive "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; export CLAUDE_CODE_OAUTH_TOKEN=\$(cat $TOKEN); cd $REPO; clear" Enter
sleep 1
# recorder FIRST so it captures the shell + the artifact + claude launch
$TM new-session -d -s ccrec2 -x $W -y $H; $TM set-option -t ccrec2 status off
$TM send-keys -t ccrec2 "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; asciinema rec $REC/claude-ep${EP}.cast --overwrite --idle-time-limit 1.0 --command 'tmux attach -t cclive -r'" Enter
sleep 3
# show the artifact(s) — the "more detail"
for a in $ARTIFACTS; do $TM send-keys -t cclive "cat $a" Enter; sleep 3.5; done
# launch claude
$TM send-keys -t cclive "$CLAUDE" Enter
sleep 9
$TM send-keys -t cclive "$TEXT"; sleep 1; $TM send-keys -t cclive Enter; echo "action sent ($MODE)"
case "$COMPLETE" in
 testpass) for i in $(seq 1 40); do sleep 3; ( cd "$REPO" && python3 test_slugify.py >/dev/null 2>&1 ) && { echo "testpass $i"; break; }; done; sleep 5 ;;
 menu) for i in $(seq 1 30); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "keep planning|auto-accept|manually approve|Yes, and|proceed\?" && { echo "menu $i"; break; }; done; sleep 1.5 ;;
 *) prev="";st=0; for i in $(seq 1 50); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); h=$(echo "$p"|md5); [ "$h" = "$prev" ]&&st=$((st+1))||st=0; prev=$h; [ $i -ge 6 ]&&[ $st -ge 3 ]&&{ echo "stable $i"; break; }; done; sleep 1 ;;
esac
$TM kill-session -t ccrec2 2>/dev/null; sleep 1; $TM kill-session -t cclive 2>/dev/null   # recorder stops at result, then close claude
grep -qiE "sk-ant|oat01" "$REC/claude-ep${EP}.cast" && { echo FATAL token; exit 3; }
agg "$REC/claude-ep${EP}.cast" "$REC/claude-ep${EP}.gif" --theme asciinema --font-size 22 2>&1 | tail -1
ffmpeg -y -i "$REC/claude-ep${EP}.gif" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos" -pix_fmt yuv420p -movflags +faststart "$REC/claude-ep${EP}-term.mp4" 2>/dev/null
echo "dur:"; ffprobe -v error -show_entries format=duration -of csv=p=0 "$REC/claude-ep${EP}-term.mp4" 2>/dev/null
echo "RECD_OK ep=$EP"

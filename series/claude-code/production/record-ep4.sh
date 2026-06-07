#!/bin/bash
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
LOG=~/ep4rec.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1
TM=/opt/homebrew/bin/tmux; TOKEN=~/.config/claude/oauth-token
DEMO=~/runthedocs/series/claude-code/demo; REPO=$DEMO/cc-demo-repo; REC=$DEMO/rec; W=110; H=30
# fix slugify so there's no bug for claude to ask about mid-plan
cat > "$REPO/slugify.py" <<'PYF'
import re
def slugify(text):
    return re.sub(r"\s+", "-", text.strip().lower())
PYF
( cd "$REPO" && git add -A && git -c user.email=demo@local -c user.name=demo commit -q -m "pre-ep4: slugify fixed" 2>/dev/null )
$TM kill-session -t cclive 2>/dev/null; $TM kill-session -t ccrec2 2>/dev/null
$TM new-session -d -s cclive -x $W -y $H; $TM set-option -t cclive status off
$TM send-keys -t cclive "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; export CLAUDE_CODE_OAUTH_TOKEN=\$(cat $TOKEN); cd $REPO; clear" Enter
sleep 1
$TM send-keys -t cclive "claude --permission-mode plan --effort low --allowedTools Read \"Bash(python3 *)\" --disallowedTools WebFetch WebSearch" Enter
sleep 12
$TM new-session -d -s ccrec2 -x $W -y $H; $TM set-option -t ccrec2 status off
$TM send-keys -t ccrec2 "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; asciinema rec $REC/claude-ep4.cast --overwrite --idle-time-limit 1.0 --command 'tmux attach -t cclive -r'" Enter
sleep 3
$TM send-keys -t cclive "Plan how to reorganize slugify and titlecase into one shared textkit module with a single test file. Just the plan, do not edit."
sleep 1; $TM send-keys -t cclive Enter; echo "prompt sent"
for i in $(seq 1 30); do
  sleep 3; pane=$($TM capture-pane -pt cclive 2>/dev/null)
  if echo "$pane" | grep -qiE "keep planning|auto-accept|manually approve|Yes, and|proceed\?"; then echo "approve menu shown (iter $i)"; break; fi
done
sleep 1.5
$TM kill-session -t ccrec2 2>/dev/null   # stop recorder at the plan/menu frame (no exit tail)
sleep 1
$TM kill-session -t cclive 2>/dev/null
grep -qiE "sk-ant|oat01" "$REC/claude-ep4.cast" && { echo FATAL token; exit 3; }
echo "--- read-only? ---"; ( cd "$REPO" && git status --porcelain | head )
agg "$REC/claude-ep4.cast" "$REC/claude-ep4.gif" --theme asciinema --font-size 22 2>&1 | tail -1
ffmpeg -y -i "$REC/claude-ep4.gif" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos" -pix_fmt yuv420p -movflags +faststart "$REC/claude-ep4-term.mp4" 2>/dev/null
echo "term dur:"; ffprobe -v error -show_entries format=duration -of csv=p=0 "$REC/claude-ep4-term.mp4" 2>/dev/null
echo "EP4REC_OK"

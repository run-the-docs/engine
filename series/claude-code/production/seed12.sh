#!/bin/bash
# Seed an INTERACTIVE claude session in cc-demo-repo so `claude --continue` resumes it.
# (claude --continue ignores headless `-p` sessions, so the seed must be interactive.)
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
T=/opt/homebrew/bin/tmux
REPO="$HOME/runthedocs/series/claude-code/demo/cc-demo-repo"
TOKEN="$HOME/.config/claude/oauth-token"
$T kill-session -t ccseed 2>/dev/null
$T new-session -d -s ccseed -x 110 -y 30
$T set-option -t ccseed status off
$T send-keys -t ccseed "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; export CLAUDE_CODE_OAUTH_TOKEN=\$(cat $TOKEN); cd $REPO; clear" Enter
sleep 1
$T send-keys -t ccseed "claude --strict-mcp-config --allowedTools Read --disallowedTools WebFetch WebSearch" Enter
sleep 22
$T send-keys -t ccseed "I am refactoring slugify.py. In one sentence, what does it currently do?"
sleep 1
$T send-keys -t ccseed Enter
# wait for the answer to finish
for i in $(seq 1 16); do
  sleep 3
  p=$($T capture-pane -pt ccseed 2>/dev/null)
  echo "$p" | grep -qiE "esc to interrupt" || { [ $i -ge 3 ] && break; }
done
sleep 2
$T send-keys -t ccseed "/exit" Enter
sleep 3
$T kill-session -t ccseed 2>/dev/null
echo "seed12 done (interactive slugify session created)"

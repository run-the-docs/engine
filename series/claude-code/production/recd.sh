#!/bin/bash
# Unified detail-recorder: shows the artifact file (cat) before launching claude.
# Usage: EP=<n> bash recd.sh   (scenario files must be staged beforehand)
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
LOG=~/rec_${EP}.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1
TM=/opt/homebrew/bin/tmux; TOKEN=~/.config/claude/oauth-token
DEMO=~/runthedocs/series/claude-code/demo; REPO=$DEMO/cc-demo-repo; REC=$DEMO/rec; W=110; H=30
case "$EP" in
 1) RESET=5411d3b; ARTIFACTS="slugify.py"; CLAUDE='claude --strict-mcp-config --effort low --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="In two sentences: what does this repo do, and what is the bug in slugify.py? Do not change any files."; COMPLETE=stable ;;
 2) RESET=5411d3b; ARTIFACTS="test_slugify.py slugify.py"; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Fix slugify.py so the failing test passes, then run it."; COMPLETE=testpass ;;
 3) RESET=6a8d07c; ARTIFACTS="CLAUDE.md"; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Add a titlecase(text) helper and a test for it, following our conventions."; COMPLETE=stable ;;
 4) RESET=29299f9; ARTIFACTS="slugify.py titlecase.py"; CLAUDE='claude --strict-mcp-config --permission-mode plan --effort low --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Plan how to reorganize slugify and titlecase into one shared textkit module with a single test file. Just the plan, do not edit."; COMPLETE=menu ;;
 5) RESET=0b6488a; ARTIFACTS=".claude/commands/test.md"; CLAUDE='claude --strict-mcp-config --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch --effort low'; MODE=slash; TEXT="/test"; COMPLETE=stable ;;
 8) RESET=15ca978; ARTIFACTS=".claude/settings.json"; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Add a hook to .claude/settings.json: a PostToolUse hook with an Edit|Write matcher that runs npx prettier --write on the file I just edited. Keep my existing permissions."; COMPLETE=hookwrite ;;
 fable5) RESET=0a11b0a; ARTIFACTS="date_range.py"; CLAUDE='claude --model claude-fable-5 --strict-mcp-config --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="The test is failing. Find the root cause and fix it, then run the test."; PRECMD='python3 test_date_range.py'; COMPLETE=f5test ;;
 11) RESET=9e97a74; ARTIFACTS="context-cheat.txt"; CLAUDE='claude --strict-mcp-config --allowedTools Read --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Read CLAUDE.md and slugify.py and give me a one-line summary of this project."; COMPLETE=ctxdemo ;;
 6) RESET=5411d3b; ARTIFACTS="slugify.py"; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Rewrite slugify in slugify.py to lowercase, strip, and collapse whitespace into single hyphens. Edit the file directly."; COMPLETE=rewind ;;
 9) RESET=ec4eb0e; ARTIFACTS=".mcp.json"; CLAUDE='claude --allowedTools Read --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Use the claude-code-docs MCP to look up what Plan Mode does, and answer in one sentence."; PRESTEP='claude mcp remove claude-code-docs --scope local >/dev/null 2>&1; true'; PRECMD='claude mcp list'; COMPLETE=skill ;;
 7) RESET=d3c3da0; ARTIFACTS=".claude/agents/module-researcher.md"; CLAUDE='claude --strict-mcp-config --allowedTools Read Grep Glob Task --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Use the module-researcher subagent to investigate the auth, db, and api modules in parallel, then give a one-line summary of each."; COMPLETE=skill ;;
 10) RESET=b4bc357; ARTIFACTS=".claude/skills/summarize-changes/SKILL.md"; CLAUDE='claude --strict-mcp-config --allowedTools Read "Bash(git *)" --disallowedTools WebFetch WebSearch --effort low'; MODE=slash; TEXT="/summarize-changes"; PRESTEP='printf "\ndef get_limit():\n    return 100  # TODO: make configurable\n" >> "$REPO/slugify.py"'; COMPLETE=skill ;;
 12) RESET=5411d3b; ARTIFACTS="slugify.py"; PRESTEP='bash "$DEMO/seed12.sh"'; CLAUDE='claude --strict-mcp-config --continue --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT="Which file did I say I am refactoring? Answer in one word."; COMPLETE=stable ;;
 13) RESET=5411d3b; ARTIFACTS=""; CLAUDE='git log --oneline -10 | claude --strict-mcp-config -p "Summarize what these commits changed, in 3 short bullets." --disallowedTools WebFetch WebSearch'; MODE=prompt; TEXT=""; COMPLETE=stable ;;
 14) RESET=5411d3b; ARTIFACTS="slugify.py"; CLAUDE='claude --strict-mcp-config --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="What does @slugify.py do, in one sentence?"; COMPLETE=stable ;;
 15) RESET=5411d3b; ARTIFACTS="slugify.py"; PRESTEP='bash "$DEMO/codereview-prep.sh"'; CLAUDE='claude --strict-mcp-config --allowedTools Read Grep Glob Task "Bash(git *)" --disallowedTools WebFetch WebSearch --effort low'; MODE=slash; TEXT="/code-review"; COMPLETE=skill ;;
 16) RESET=5411d3b; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Read --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="I want to add rate limiting to our API. Interview me about the design using the AskUserQuestion tool. Dig into the hard tradeoffs I might not have considered, not the obvious stuff."; COMPLETE=stable ;;
 17) STANDIN_DIR=~/runthedocs/scratch/cc-ep17-demo; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Read Write Edit Glob Grep "Bash(ls *)" "Bash(find *)" "Bash(cat *)" "Bash(git *)" --disallowedTools WebFetch WebSearch'; MODE=slash; TEXT="/init"; PRECMD="ls"; COMPLETE=init ;;
 24) RESET=5411d3b; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Read "Bash(python3 *)" --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="! python3 test_slugify.py"; FOLLOWUP="Why did that test fail? Answer in one sentence."; COMPLETE=shellmode ;;
 19) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch'; MODE=slash; TEXT="/goal test_slugify.py passes when run"; COMPLETE=testpass ;;
 21) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --disallowedTools WebFetch WebSearch'; MODE=slash; TEXT="/sandbox"; SBCMD="Run python3 test_slugify.py and tell me in one line whether it passes"; COMPLETE=sandbox ;;
 23) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write "Bash(*)" --disallowedTools WebFetch WebSearch'; MODE=slash; TEXT="/statusline show the model, the git branch, and the context percentage"; COMPLETE=skill ;;
 25) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Read --disallowedTools WebFetch WebSearch'; MODE=slash; TEXT="/fast"; FOLLOWUP="What does slugify.py do? Answer in one sentence."; COMPLETE=shellmode ;;
 29) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS="test_slugify.py slugify.py"; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write "Bash(python3 *)" --disallowedTools WebFetch WebSearch --effort high'; MODE=prompt; TEXT="ultrathink: fix slugify.py so the failing test passes, then run it."; COMPLETE=testpass ;;
 28) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS=""; PRESTEP='mkdir -p "$REPO/.claude" && cp "$DEMO/ep28-settings.json" "$REPO/.claude/settings.local.json"'; CLAUDE='claude --strict-mcp-config --allowedTools Read Grep Glob --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Explain what slugify.py does today and where it falls short for real-world titles."; COMPLETE=stable ;;
 30) RESET=6a8d07c; LAUNCH_FIRST=1; ARTIFACTS="CLAUDE.md"; CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Always run python3 -m pytest before committing. Add this to CLAUDE.md."; COMPLETE=memwrite ;;
 26) RESET=5411d3b; ARTIFACTS=""; PRECMD='claude plugin marketplace add anthropics/claude-code'; CLAUDE=':'; MODE=bash; TEXT='claude plugin install commit-commands@claude-code-plugins'; COMPLETE=plugininstall ;;
 31) RESET=5411d3b; LAUNCH_FIRST=1; ARTIFACTS=""; CLAUDE='claude --strict-mcp-config --allowedTools Bash Read --disallowedTools WebFetch WebSearch --effort low'; MODE=prompt; TEXT="Run the test suite (python3 test_slugify.py) in the background so you do not block, tell me the background task ID, then read the output and report pass or fail."; COMPLETE=stable ;;
esac
# reset the demo repo to this episode's correct starting state (so file cards + claude see the right files)
if [ -n "$STANDIN_DIR" ]; then
  # ep17 / synthetic stand-in: rebuild a fresh clean repo (NO CLAUDE.md yet) from the committed fixture.
  # NEVER points at the real gran-canaria-plan repo — only $DEMO/ep17-standin/ (verified PII-clean).
  REPO="$STANDIN_DIR"; rm -rf "$REPO"; mkdir -p "$REPO"; cp "$DEMO/ep17-standin/"* "$REPO/"
  git -C "$REPO" init -q
  git -C "$REPO" -c user.email=demo@local -c user.name=demo add -A
  git -C "$REPO" -c user.email=demo@local -c user.name=demo commit -qm "synthetic ep17 demo project" >/dev/null 2>&1
  echo "standin rebuilt at $REPO (no CLAUDE.md yet)"
else
  git -C "$REPO" reset --hard "$RESET" >/dev/null 2>&1 && git -C "$REPO" clean -fdq >/dev/null 2>&1 && echo "repo reset to $RESET"
fi
[ -n "$PRESTEP" ] && eval "$PRESTEP" && echo "prestep done"
$TM kill-session -t cclive 2>/dev/null; $TM kill-session -t ccrec2 2>/dev/null
$TM new-session -d -s cclive -x $W -y $H; $TM set-option -t cclive status off
$TM set-option -g focus-events on 2>/dev/null; $TM set-option -g mouse on 2>/dev/null   # suppress claude's tmux hint chrome
$TM send-keys -t cclive "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; export CLAUDE_CODE_OAUTH_TOKEN=\$(cat $TOKEN); export PROMPT='\$ '; cd $REPO; clear" Enter
sleep 1
if [ -n "$STANDIN_DIR" ] || [ -n "$LAUNCH_FIRST" ]; then
  # ep17 clean-launch (also LAUNCH_FIRST=1 non-standin episodes): claude's startup prints a transient account toast with the logged-in
  # email/org (e.g. "<acct>'s Organization /release-notes"). It auto-dismisses in ~14s. Launch
  # claude FIRST, let the toast clear, THEN start the recorder so the email never enters the
  # cast or the rendered video (RtD is a neutral brand; Invotek stays the silent owner).
  # Trade-off: no pre-claude shell/ls shot for ep17 — the recording opens on the clean claude prompt.
  $TM send-keys -t cclive "$CLAUDE" Enter
  sleep 16
  $TM new-session -d -s ccrec2 -x $W -y $H; $TM set-option -t ccrec2 status off
  $TM send-keys -t ccrec2 "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; asciinema rec $REC/claude-ep${EP}.cast --overwrite --idle-time-limit 1.0 --command 'tmux attach -t cclive -r'" Enter
  sleep 3
else
  # recorder FIRST so it captures the shell + the artifact + claude launch
  $TM new-session -d -s ccrec2 -x $W -y $H; $TM set-option -t ccrec2 status off
  $TM send-keys -t ccrec2 "export PATH=/opt/homebrew/bin:\$HOME/.local/bin:\$PATH; asciinema rec $REC/claude-ep${EP}.cast --overwrite --idle-time-limit 1.0 --command 'tmux attach -t cclive -r'" Enter
  sleep 3
  # show the artifact(s) — the "more detail"
  for a in $ARTIFACTS; do $TM send-keys -t cclive "cat $a" Enter; sleep 3.5; done
  # launch claude
  [ -n "$PRECMD" ] && { $TM send-keys -t cclive "$PRECMD" Enter; sleep 9; }
  if [ "$MODE" != "bash" ]; then $TM send-keys -t cclive "$CLAUDE" Enter; sleep 22; fi
fi
if [ "$MODE" = "slash" ]; then
  rest="${TEXT#/}"
  $TM send-keys -t cclive "/"; sleep 3                                   # reveal the slash-command menu on screen
  $TM send-keys -t cclive "$rest"; sleep 1; $TM send-keys -t cclive Enter
else
  $TM send-keys -t cclive "$TEXT"; sleep 1; $TM send-keys -t cclive Enter
fi
echo "action sent ($MODE)"
case "$COMPLETE" in
 hookwrite) for i in $(seq 1 40); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "Do you want to|1\. Yes|allow Claude to edit" && $TM send-keys -t cclive "1"; grep -q "PostToolUse" "$REPO/.claude/settings.json" 2>/dev/null && { echo "hookwrite $i"; break; }; done; sleep 3 ;;
 skill) prev="";st=0; for i in $(seq 1 40); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "Do you want|1\. Yes|1\. Use|trust this|allow|proceed|Run this" && $TM send-keys -t cclive "1"; h=$(echo "$p"|md5); [ "$h" = "$prev" ]&&st=$((st+1))||st=0; prev=$h; [ $i -ge 6 ]&&[ $st -ge 3 ]&&{ echo "skill stable $i"; break; }; done; sleep 1 ;;
 rewind) for i in $(seq 1 26); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "Do you want|1\. Yes|allow|proceed" && $TM send-keys -t cclive "1"; if grep -qiE "lower|strip|sub\(" "$REPO/slugify.py" 2>/dev/null && ! echo "$p"|grep -qiE "esc to interrupt"; then echo "idle $i"; break; fi; done; sleep 3; $TM send-keys -t cclive "/rewind"; sleep 1.6; $TM send-keys -t cclive Enter; sleep 1; $TM send-keys -t cclive Enter; sleep 7 ;;
 ctxdemo) for i in $(seq 1 16); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "1\. Yes|Do you want|allow" && $TM send-keys -t cclive "1"; if [ $i -ge 3 ] && ! echo "$p"|grep -qiE "esc to interrupt"; then echo "read done $i"; break; fi; done; sleep 2; $TM send-keys -t cclive "/"; sleep 2; $TM send-keys -t cclive "context"; sleep 1; $TM send-keys -t cclive Enter; sleep 6; $TM send-keys -t cclive "/compact focus on the slugify code"; sleep 1.5; $TM send-keys -t cclive Enter; sleep 13; $TM send-keys -t cclive "/clear"; sleep 1.2; $TM send-keys -t cclive Enter; sleep 4 ;;
 f5test) for i in $(seq 1 40); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "Do you want|1\. Yes|allow|proceed" && $TM send-keys -t cclive "1"; ( cd "$REPO" && python3 test_date_range.py >/dev/null 2>&1 ) && { echo "f5test pass $i"; break; }; done; sleep 4 ;;
 testpass) for i in $(seq 1 40); do sleep 3; ( cd "$REPO" && python3 test_slugify.py >/dev/null 2>&1 ) && { echo "testpass $i"; break; }; done; sleep 5 ;;
 menu) for i in $(seq 1 30); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "keep planning|auto-accept|manually approve|Yes, and|proceed\?" && { echo "menu $i"; break; }; done; sleep 1.5 ;;
 init) for i in $(seq 1 50); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qE "Do you want to|❯ 1\. Yes" && $TM send-keys -t cclive "1"; if [ -f "$REPO/CLAUDE.md" ] && ! echo "$p"|grep -qiE "esc to interrupt"; then echo "init done $i (CLAUDE.md written)"; break; fi; done; sleep 4 ;;
 shellmode) sleep 6; $TM send-keys -t cclive "$FOLLOWUP"; sleep 1; $TM send-keys -t cclive Enter; prev="";st=0; for i in $(seq 1 30); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); h=$(echo "$p"|md5); [ "$h" = "$prev" ]&&st=$((st+1))||st=0; prev=$h; [ $i -ge 4 ]&&[ $st -ge 3 ]&&{ echo "shellmode stable $i"; break; }; done; sleep 1 ;;
 sandbox) sleep 2; $TM send-keys -t cclive "1"; sleep 3; $TM send-keys -t cclive Escape; sleep 2; $TM send-keys -t cclive "$SBCMD"; sleep 1; $TM send-keys -t cclive Enter; prev="";st=0; for i in $(seq 1 30); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); h=$(echo "$p"|md5); [ "$h" = "$prev" ]&&st=$((st+1))||st=0; prev=$h; [ $i -ge 4 ]&&[ $st -ge 3 ]&&{ echo "sandbox stable $i"; break; }; done; sleep 1 ;;
 memwrite) for i in $(seq 1 40); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "Do you want to|1\. Yes|allow Claude to edit" && $TM send-keys -t cclive "1"; grep -qi "pytest" "$REPO/CLAUDE.md" 2>/dev/null && { echo "memwrite $i"; break; }; done; sleep 3 ;;
 plugininstall) for i in $(seq 1 40); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); echo "$p"|grep -qiE "Successfully installed plugin|already installed" && { echo "plugininstall $i"; break; }; done; sleep 3 ;;
 *) prev="";st=0; for i in $(seq 1 50); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); h=$(echo "$p"|md5); [ "$h" = "$prev" ]&&st=$((st+1))||st=0; prev=$h; [ $i -ge 6 ]&&[ $st -ge 3 ]&&{ echo "stable $i"; break; }; done; sleep 1 ;;
esac
sleep 4; $TM kill-session -t ccrec2 2>/dev/null; sleep 1; $TM kill-session -t cclive 2>/dev/null   # recorder stops at result, then close claude
grep -qiE "sk-ant|oat01|invotek|hasleveien|f(ø|o)dselsnummer|brønnøysund|skattemelding|\bNHN\b|godøya|1bedrift" "$REC/claude-ep${EP}.cast" && { echo FATAL secret-or-PII-in-cast; exit 3; }
agg "$REC/claude-ep${EP}.cast" "$REC/claude-ep${EP}.gif" --theme asciinema --font-size 22 2>&1 | tail -1
~/voicebox-venv/bin/python "$DEMO/fix_term.py" "$REC/claude-ep${EP}.gif" "$REC/claude-ep${EP}-term.mp4"   # auto-drop tmux-teardown [terminated] frame
echo "dur:"; ffprobe -v error -show_entries format=duration -of csv=p=0 "$REC/claude-ep${EP}-term.mp4" 2>/dev/null
echo "RECD_OK ep=$EP"

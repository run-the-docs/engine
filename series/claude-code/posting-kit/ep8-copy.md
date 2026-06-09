# Ep 8 — Auto-format every file Claude edits
**Suggested slot:** Wed 2026-06-17 · 09:00 CET   |   **Topic:** A PostToolUse hook runs your formatter automatically on every file Claude edits.

**Files in this folder:**
- `ep8-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep8-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep8-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep8-linkedin-4x5.mp4` natively — no link in the post body)
Still reformatting every file Claude touches by hand?

Stop. Let your formatter run itself.

Claude Code has hooks — shell commands that fire at points in its lifecycle. Add a PostToolUse hook with an "Edit|Write" matcher to `.claude/settings.json`, and after every edit it runs your formatter on the exact file that changed:

`jq -r '.tool_input.file_path' | xargs npx prettier --write`

Deterministic, not "maybe the model remembers." Formatting just stays consistent — no prompting, no nagging. Don't want to hand-write the JSON? Ask Claude to add the hook for you, then run `/hooks` to confirm it's registered.

What's the first thing you'd auto-run on every edit — Prettier, Black, or your test suite?

▶ Full series + episode links in the first comment.

#ClaudeCode #AICoding #DevTools #DeveloperProductivity #Automation

**First comment (post yourself within ~1 min):**
> Pro-tip: PostToolUse fires *after* the edit, so the hook can't undo a bad change — it cleans up, it doesn't gate. And the `Edit|Write` matcher only catches Claude's Edit/Write tools, not files changed via shell. For per-call coverage of Bash-written files too, also match `Bash` and have your script diff `git status --porcelain`. (Prettier needs `jq` installed — `brew install jq`.) Full series: https://code.claude.com/docs/en/hooks-guide

---
## TikTok / Instagram Reels  (upload `ep8-vertical-9x16.mp4`)
stop hand-formatting every file claude edits. add a posttooluse hook in .claude/settings.json with an edit|write matcher, and your formatter runs itself the instant claude saves. prettier, black, your tests — pick one. ask claude to write the hook, then /hooks to confirm. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep8-vertical-9x16.mp4`)
**Title:** Auto-format every file Claude edits (Claude Code hooks)
**Description:** Add a PostToolUse hook with an Edit|Write matcher to .claude/settings.json and your formatter runs on every file Claude edits — no prompting. Ask Claude to write the hook, then run /hooks to confirm.
Run the Docs — Claude Code series. Full series: https://code.claude.com/docs/en/hooks-guide
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep8-linkedin-4x5.mp4`)
Stop reformatting Claude's edits by hand. A PostToolUse hook with an "Edit|Write" matcher in .claude/settings.json runs your formatter on every file Claude saves. Don't fancy the JSON? Ask Claude to write the hook, then /hooks to confirm. #ClaudeCode #AIcoding

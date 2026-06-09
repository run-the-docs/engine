# Ep 8 — Auto-format every file Claude edits
**Suggested slot:** Wed 2026-06-17 · 09:00 CET   |   **Topic:** A PostToolUse hook runs your formatter automatically on every file Claude edits.

**Files in this folder:**
- `ep8-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep8-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep8-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep8-linkedin-4x5.mp4` natively — no link in the post body)
I stopped reformatting every file Claude touches by hand. Now my formatter runs itself.

Claude Code has hooks — shell commands that fire at points in its lifecycle. I added a PostToolUse hook with an "Edit|Write" matcher to `.claude/settings.json`, and after every edit it runs my formatter on the exact file that changed:

`jq -r '.tool_input.file_path' | xargs npx prettier --write`

It's deterministic — not "maybe the model remembers." Formatting just stays consistent, no prompting, no nagging. If you don't feel like hand-writing the JSON, ask Claude to add the hook for you, then run `/hooks` to confirm it's registered.

What's the first thing you'd auto-run on every edit — Prettier, Black, or your test suite?

**First comment (post yourself within ~1 min):**
> Demo: [YouTube link]
>
> I write up one Claude Code tip every weekday — [newsletter link]
>
> One gotcha: PostToolUse fires *after* the edit, so the hook can't undo a bad change — it cleans up, it doesn't gate. And the `Edit|Write` matcher only catches Claude's Edit/Write tools, not files changed via shell. For per-call coverage of Bash-written files too, also match `Bash` and have your script diff `git status --porcelain`. (Prettier needs `jq` — `brew install jq`.)
>
> I'm Stig; I build dev/AI tooling at Invotek — DM me if you want something like this built.
>
> #ClaudeCode #AICoding #DevTools #DeveloperProductivity #Automation

---
## TikTok / Instagram Reels  (upload `ep8-vertical-9x16.mp4`)
i stopped hand-formatting every file claude edits. i added a posttooluse hook in .claude/settings.json with an edit|write matcher, and my formatter runs itself the instant claude saves. prettier, black, your tests — pick one. don't want to write the json? ask claude to do it, then /hooks to confirm. follow for a claude code tip a day. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep8-vertical-9x16.mp4`)
**Title:** Auto-format every file Claude edits (Claude Code hooks)
**Description:** I stopped reformatting Claude's edits by hand. A PostToolUse hook with an Edit|Write matcher in .claude/settings.json runs my formatter on every file Claude saves — no prompting. Don't want the JSON? Ask Claude to write the hook, then /hooks to confirm.
[newsletter link]
Run the Docs — Claude Code series. A project by Invotek.
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep8-linkedin-4x5.mp4`)
I stopped reformatting Claude's edits by hand. A PostToolUse hook with an "Edit|Write" matcher in .claude/settings.json runs my formatter on every file Claude saves. Don't fancy the JSON? Ask Claude to write the hook, then /hooks to confirm. (link in reply) #ClaudeCode #AIcoding

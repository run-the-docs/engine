# Ep 10 — Turn any workflow into a reusable skill
**Suggested slot:** Fri 2026-06-19 · 09:00 CET   |   **Topic:** Package a repeatable workflow as a reusable Claude Code skill — one SKILL.md file

**Files in this folder:**
- `ep10-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep10-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep10-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep10-linkedin-4x5.mp4` natively — no link in the post body)
Still pasting the same multi-step instructions into Claude every session?

Package that workflow once as a skill. It's a single file: `.claude/skills/<name>/SKILL.md`.

The YAML frontmatter `description` tells Claude when to use it. The markdown body says what to do. The folder name becomes the command — so `summarize-changes/` gives you `/summarize-changes`.

Drop a `` !`git diff HEAD` `` line in the body and Claude Code runs it first, inlining your live diff before Claude even reads the skill. Then just ask "what did I change?" — Claude matches the description and loads the skill on its own. No `/` required.

One file. Reused every session, by you or by Claude.

▶ Full series + episode links in the first comment.

#ClaudeCode #AIcoding #DeveloperTools #Productivity #SoftwareEngineering

**First comment (post yourself within ~1 min):**
> Pro-tip: keep the SKILL.md body short — once a skill loads it stays in context for the rest of the session, so every line is a recurring token cost. Push long reference material into separate files in the skill folder and link them; they only load when needed. And if a workflow has side effects (deploy, commit), add `disable-model-invocation: true` so only you can trigger it with `/name`.

---
## TikTok / Instagram Reels  (upload `ep10-vertical-9x16.mp4`)
stop pasting the same instructions into claude every session. package the workflow once as a skill — one SKILL.md file in .claude/skills/. the description tells claude when to use it, the folder name becomes the slash command, and a `!git diff HEAD` line pulls your live diff in automatically. then just ask "what changed?" and claude loads it on its own. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep10-vertical-9x16.mp4`)
**Title:** Turn any repeatable workflow into a reusable Claude Code skill
**Description:** Package a workflow once as a SKILL.md file in .claude/skills/ — the folder name becomes the slash command, the description lets Claude load it automatically, and a `!git diff HEAD` line inlines your live data before Claude reads it.
Run the Docs — Claude Code series. Docs: https://code.claude.com/docs/en/skills
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep10-linkedin-4x5.mp4`)
Stop re-pasting the same instructions into Claude. Package the workflow once: one SKILL.md in .claude/skills/. Folder name = the slash command, description = when Claude auto-loads it, `!git diff HEAD` = your live data inlined before Claude reads it.
#ClaudeCode #AIcoding

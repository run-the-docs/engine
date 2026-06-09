# Ep 10 — Turn any workflow into a reusable skill
**Suggested slot:** Fri 2026-06-19 · 09:00 CET   |   **Topic:** Package a repeatable workflow as a reusable Claude Code skill — one SKILL.md file

**Files in this folder:**
- `ep10-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep10-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep10-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep10-linkedin-4x5.mp4` natively — no link in the post body)
I kept pasting the same multi-step instructions into Claude every single session. So I stopped.

Now I package that workflow once as a skill. It's a single file: `.claude/skills/<name>/SKILL.md`.

The YAML frontmatter `description` tells Claude when to use it. The markdown body says what to do. The folder name becomes the command — so `summarize-changes/` gives me `/summarize-changes`.

I drop a `` !`git diff HEAD` `` line in the body and Claude Code runs it first, inlining my live diff before Claude even reads the skill. Then I just ask "what did I change?" — Claude matches the description and loads the skill on its own. No `/` required.

One file. Reused every session, by me or by Claude.

What's the workflow you re-type the most? That's the one to package first.

**First comment (post yourself within ~1 min):**
> Watch the full thing here: `[YouTube link]`
>
> I write up one Claude Code tip every weekday — `[newsletter link]`
>
> Pro-tip: keep the SKILL.md body short — once a skill loads it stays in context for the rest of the session, so every line is a recurring token cost. Push long reference material into separate files in the skill folder and link them; they only load when needed. And if a workflow has side effects (deploy, commit), add `disable-model-invocation: true` so only you can trigger it with `/name`.
>
> I'm Stig; I build dev/AI tooling at Invotek — DM me if you want something like this built.
>
> #ClaudeCode #AIcoding #DeveloperTools #Productivity #SoftwareEngineering

---
## TikTok / Instagram Reels  (upload `ep10-vertical-9x16.mp4`)
i stopped pasting the same instructions into claude every session. now i package the workflow once as a skill — one SKILL.md file in .claude/skills/. the description tells claude when to use it, the folder name becomes the slash command, and a `!git diff HEAD` line pulls my live diff in automatically. then i just ask "what changed?" and claude loads it on its own. follow for a Claude Code tip a day. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep10-vertical-9x16.mp4`)
**Title:** Turn any repeatable workflow into a reusable Claude Code skill
**Description:** I package a workflow once as a SKILL.md file in .claude/skills/ — the folder name becomes the slash command, and a `!git diff HEAD` line inlines my live data before Claude reads it. Then Claude loads it on its own from the description.
More tips: `[newsletter link]`
Run the Docs — Claude Code series. A project by Invotek.
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep10-linkedin-4x5.mp4`)
I stopped re-pasting the same instructions into Claude. Now I package the workflow once: one SKILL.md in .claude/skills/. Folder name = the slash command, description = when Claude auto-loads it, `!git diff HEAD` = my live data inlined before Claude reads it.
#ClaudeCode #AIcoding

(reply with: `[YouTube link]`)

# Ep 7 — Claude runs a team of subagents in parallel
**Suggested slot:** Tue 2026-06-16 · 09:00 CET   |   **Topic:** Subagents — spin up parallel agents, each with its own context window and tools

**Files in this folder:**
- `ep7-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep7-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep7-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep7-linkedin-4x5.mp4` natively — no link in the post body)
When I kick off a big refactor, I don't want one Claude reading my whole codebase just to get started. It's slow, and it fills the chat with search results I'll never look at again.

So I lean on subagents. Each one runs in its own context window, with its own tools and its own system prompt.

I define one as a tiny file in `.claude/agents/` (or run `/agents`), then ask Claude to research the auth, database, and API modules in parallel. It spawns a subagent per module — they run at once and report back a short summary.

The noisy exploration stays in their context, so my main chat stays clean.

Two honest caveats I've hit: subagents can't spawn more subagents, and a pile of detailed results still costs you main-context tokens — so I keep what they return tight.

What would you parallelize first?

**First comment (post yourself within ~1 min):**
> Pro-tip: give research subagents read-only tools (`tools: Read, Grep, Glob`) and put them on `model: haiku` — fast, cheap, and they can't touch your files. Ask each one to "report only a one-line summary" so three parallel results don't flood your main context. Full episode: [YouTube link]
>
> I write up one Claude Code tip every weekday — [newsletter link]
>
> I'm Stig; I build dev/AI tooling at Invotek — DM me if you want something like this built.

#ClaudeCode #AICoding #DevTools #DeveloperProductivity #Coding

---
## TikTok / Instagram Reels  (upload `ep7-vertical-9x16.mp4`)
one claude, three modules, all at the same time. i give each subagent its own context window + tools, define one tiny file in .claude/agents, then say "research auth, db and api in parallel." the messy searching stays in their context, my chat stays clean. (heads up — they can't spawn more subagents) follow for a claude code tip a day. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep7-vertical-9x16.mp4`)
**Title:** Claude Code runs a team of subagents in parallel
**Description:** I use subagents to make Claude Code work on several parts of my codebase at once — each in its own context window, with its own tools. I define one in `.claude/agents/`, then run them in parallel so the noisy searching stays out of my main chat.
[newsletter link]
Run the Docs — Claude Code series. A project by Invotek.
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep7-linkedin-4x5.mp4`)
One Claude, three modules, all at once. I give each subagent its own context window + tools, so the noisy searching stays out of my main chat. I define one file in `.claude/agents/`, then say "research these in parallel."
(link in reply)
#ClaudeCode #AIcoding

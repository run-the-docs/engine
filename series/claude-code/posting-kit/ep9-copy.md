# Ep 9 — Give Claude a new superpower in one command (MCP)
**Suggested slot:** Thu 2026-06-18 · 09:00 CET   |   **Topic:** Connect external tools to Claude Code with MCP

**Files in this folder:**
- `ep9-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep9-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep9-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep9-linkedin-4x5.mp4` natively — no link in the post body)
Claude Code is sharp inside my repo. But on its own it can't see my issue tracker, my browser, or my internal docs — so I started wiring those in.

That's what MCP is for. One command bolts an external tool onto Claude Code:

`claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp`

I run `claude mcp list`, wait for the green ✓ Connected, then ask Claude to use it by name. The first call asks permission — I approve it once and the new tool is live.

When I want the whole team to have it, I commit a `.mcp.json` to the repo and it ships as configuration-as-code.

One thing I learned the hard way: each connected server costs a little context, so I rip out the ones I'm not actually using.

What tool would you bolt onto Claude first — Sentry, Linear, a browser?

**First comment (post yourself within ~1 min):**
> Watch it here: [YouTube link]
> One more thing I do: for tools behind a login (Sentry, Linear, Notion), add the URL the same way, then run `/mcp` inside a session, pick the server, and choose Authenticate to sign in via browser. For token-based ones like GitHub, pass it at add time with `--header "Authorization: Bearer <token>"`.
> I write up one Claude Code tip every weekday — [newsletter link]
> I'm Stig; I build dev/AI tooling at Invotek — DM me if you want something like this built.

#ClaudeCode #MCP #AICoding #DevTools #DeveloperProductivity

---
## TikTok / Instagram Reels  (upload `ep9-vertical-9x16.mp4`)
i gave claude a new superpower in one command. `claude mcp add` connects an external tool — docs, browser, issue tracker — then i ask claude to use it by name and watch the tool call show up labeled with the server. commit a .mcp.json and the whole team gets it. follow for a Claude Code tip a day. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep9-vertical-9x16.mp4`)
**Title:** Give Claude Code a new superpower in one command (MCP)
**Description:** I connect external tools to Claude Code with one command: `claude mcp add`, check `claude mcp list` for ✓ Connected, then ask Claude to use the server by name. Commit a `.mcp.json` and the whole team gets it.
[newsletter link]
Run the Docs — Claude Code series. A project by Invotek.
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep9-linkedin-4x5.mp4`)
I gave Claude Code a new superpower in one command:
`claude mcp add --transport http claude-code-docs <url>` → `claude mcp list` (✓ Connected) → ask it by name.
Commit a `.mcp.json` to share with the team.
(link in reply)
#ClaudeCode #AIcoding

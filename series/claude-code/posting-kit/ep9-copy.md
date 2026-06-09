# Ep 9 — Give Claude a new superpower in one command (MCP)
**Suggested slot:** Thu 2026-06-18 · 09:00 CET   |   **Topic:** Connect external tools to Claude Code with MCP

**Files in this folder:**
- `ep9-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep9-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep9-cover.jpg` — thumbnail / cover frame

---
## LinkedIn  (upload `ep9-linkedin-4x5.mp4` natively — no link in the post body)
Claude Code is great in your repo. But it can't see your issue tracker, your browser, or your internal docs — until you connect them.

That's what MCP is for. One command bolts an external tool onto Claude Code:

`claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp`

Run `claude mcp list`, wait for the green ✓ Connected, then ask Claude to use it by name. The first call asks permission — approve it once and the new tool is live.

Want the whole team to have it? Commit a `.mcp.json` to the repo and it ships as configuration-as-code.

One tip: each connected server costs a little context, so remove the ones you don't use.

What tool would you bolt onto Claude first — Sentry, Linear, a browser?

▶ Full series + episode links in the first comment.

#ClaudeCode #MCP #AICoding #DevTools #DeveloperProductivity

**First comment (post yourself within ~1 min):**
> Pro-tip: for tools behind a login (Sentry, Linear, Notion), add the URL the same way, then run `/mcp` inside a session, pick the server, and choose Authenticate to sign in via browser. For token-based ones like GitHub, pass it at add time with `--header "Authorization: Bearer <token>"`.

---
## TikTok / Instagram Reels  (upload `ep9-vertical-9x16.mp4`)
give claude a new superpower in one command. `claude mcp add` connects an external tool — docs, browser, issue tracker — then ask claude to use it by name and watch the tool call show up labeled with the server. commit a .mcp.json to share it with your team. #claudecode #aicoding #devtok #coding #programming #devtools

---
## YouTube Shorts  (upload `ep9-vertical-9x16.mp4`)
**Title:** Give Claude Code a new superpower in one command (MCP)
**Description:** Connect external tools to Claude Code with MCP: `claude mcp add`, check `claude mcp list` for ✓ Connected, then ask Claude to use the server by name. Commit a .mcp.json to share with your team.
Run the Docs — Claude Code series. Full series: https://code.claude.com/docs/en/mcp-quickstart
#Shorts #ClaudeCode #AICoding #DevTools

---
## X / Twitter  (upload `ep9-linkedin-4x5.mp4`)
Give Claude Code a new superpower in one command:
`claude mcp add --transport http claude-code-docs <url>` → `claude mcp list` (✓ Connected) → ask it by name.
Commit a .mcp.json to share with the team.
#ClaudeCode #AIcoding

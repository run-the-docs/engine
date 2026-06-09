# Long-form EP 1 — "What Claude Code Actually Is"

**The first weekly long-form, and the front door to the Claude Code series.** This is the *monetizable* asset (watch-hours → YPP, sponsor-evaluable, hosts the newsletter CTA) — shorts feed discovery into it.

| | |
|---|---|
| **Docs source (1:1)** | `https://code.claude.com/docs/en/overview` |
| **Format** | Long-form, 16:9 1920×1080, canvas pipeline (Kokoro TTS → HTML canvas anim → render → ffmpeg) — same rig as the K8s/React series |
| **Target length** | ~8 min |
| **Accent / font** | clay `#da7756` on `#0a0a0a`, JetBrains Mono |
| **Series slot** | Saturday (long-form), 1/week |
| **Real-terminal inserts** | Yes — short recorded `claude` clips for the capability demos (reuse the shorts terminal pipeline as B-roll) |

## Docs-fidelity checklist (every heading / code / note → a scene)
- [ ] Definition: agentic coding tool — reads codebase, edits files, runs commands, integrates with dev tools; terminal/IDE/desktop/browser
- [ ] Get started: Terminal (native `curl`, Homebrew, WinGet, Linux apt/dnf/apk), VS Code, Desktop, Web, JetBrains; `cd project && claude`; first-login; auto-update note (native) vs manual (Homebrew/WinGet)
- [ ] What you can do (all 9): automate tedious work; build features / fix bugs; commits & PRs (+CI); MCP; customize (CLAUDE.md + auto memory, skills, hooks); agent teams & custom agents (subagents, background agents, Agent SDK); pipe/script CLI (`claude -p`); schedule (Routines / desktop tasks / `/loop`); work from anywhere
- [ ] Every code example: `claude "write tests for the auth module..."`, `claude "commit my changes..."`, the 3 `claude -p` pipe examples
- [ ] Use everywhere: same engine across surfaces; the "I want to…" integration table
- [ ] Next steps links

## Scene outline (~8 min)
1. **Cold hook (0:00–0:12).** Real terminal: one prompt → claude reads files, edits, runs the test, it passes. Line: *"This isn't autocomplete. It's an agent that works across your whole codebase — and it runs in your terminal, your IDE, your desktop, and your browser."*
2. **What it actually is (0:12–1:00).** The mental model: read codebase → plan → edit across files → run commands → verify. Canvas: the agent loop ring (think → act → observe).
3. **Get started (1:00–2:30).** Environment cards (Terminal / VS Code / Desktop / Web / JetBrains). Terminal install methods on screen (`curl … | bash`, `brew install --cask claude-code`, `winget …`, Linux pkgs). Then `cd your-project && claude` + "you'll be prompted to log in." Note: native auto-updates; Homebrew/WinGet are manual.
4. **What you can do (2:30–6:00).** Nine tool-call cards, each ~20–25s, with the doc's own example:
   - Automate the tedious — `claude "write tests for the auth module, run them, and fix any failures"`
   - Build features / fix bugs — plain language → plan → multi-file → verify; paste an error, it traces the root cause
   - Commits & PRs — `claude "commit my changes with a descriptive message"`; CI via GitHub Actions / GitLab
   - Connect tools with MCP — Drive/Jira/Slack; "MCP quickstart connects your first server end to end"
   - Customize — CLAUDE.md (read every session) + auto memory; skills (`/review-pr`); hooks (auto-format on edit)
   - Agent teams & custom agents — subagents in parallel; background agents; Agent SDK
   - Pipe / script the CLI — the 3 `claude -p` examples (tail logs → Slack anomalies; CI translations → PR; `git diff` → security review)
   - Schedule — Routines (Anthropic infra, run when your computer's off), desktop scheduled tasks, `/loop`
   - Work from anywhere — Remote Control, Dispatch, web/iOS + `claude --teleport`, `/desktop`, `@Claude` in Slack
5. **Use it everywhere (6:00–6:50).** One engine, many surfaces — CLAUDE.md/settings/MCP carry across. Render the "I want to…" table.
6. **Recap + CTA (6:50–8:00).** Recap the loop + the surfaces. CTA model (NO hard sell): *"That's the map — the series goes deep on each piece, one a week. Subscribe, and grab the free Claude Code cheat-sheet — link below."* Card: **Subscribe to Run the Docs** + `[newsletter link]` lead magnet ("the Claude Code cheat-sheet"). Footer, soft: *"Made by Stig · Run the Docs · a project by Invotek."*

## Production notes
- Reuse recorded `claude` clips from the shorts for the capability B-roll (automate/build/commit/MCP/skills) — incremental cost, not greenfield.
- Outcome-led, searchable title for YouTube SEO (e.g. "What Claude Code Actually Is — the whole map in 8 minutes").
- Description: lead-magnet `[newsletter link]` first, then chapters (timestamps per scene), then "Run the Docs — Claude Code series · a project by Invotek."
- Pin a first comment: cheat-sheet `[newsletter link]` + "what should the next deep-dive cover?"
- Chapters/timestamps in the description (watch-time + retention lever).

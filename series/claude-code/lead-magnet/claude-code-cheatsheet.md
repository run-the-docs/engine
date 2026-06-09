# Run the Docs · Claude Code Cheat-Sheet

*The one-page reference for working with Claude Code in the terminal. Docs-faithful — every command checked against code.claude.com/docs.*

## Start in 30 seconds
```
curl -fsSL https://claude.ai/install.sh | bash    # native install (auto-updates)
# or:  brew install --cask claude-code   |   winget install Anthropic.ClaudeCode
cd your-project && claude                          # start — you'll log in on first run
```
Also runs in VS Code, JetBrains, the Desktop app, the web (claude.ai/code), and Slack.

## The mental model
Claude Code is an **agent**, not autocomplete. Each turn it loops: **gather context → plan → act with tools (read, edit, run) → verify → repeat.** It works across many files and runs commands, so you describe the **outcome**, not the steps.

## Everyday moves
| You want | Do this |
|---|---|
| Understand a codebase | Just ask: "what does this repo do? where's the auth?" |
| Build or fix | Describe it in plain language, or paste an error message |
| Commit / PR | `claude "commit my changes with a good message"` |
| One-off, scripted | `tail -200 app.log \| claude -p "flag anything weird"` |
| Stop it mid-thought | `Esc` |
| Undo its edits | `/rewind` (or `Esc` `Esc` on an empty prompt) |

## The `.claude/` directory (your project's brain)
| Path | What it does |
|---|---|
| `CLAUDE.md` | Read at the **start of every session** — your stack, conventions, commands, "never do X". Run `/init` to draft one from your repo. |
| `.claude/settings.json` | Permissions, model, env, and **hooks** |
| `.claude/commands/<name>.md` | A custom `/name` slash command |
| `.claude/agents/<name>.md` | A **subagent** definition |
| `.claude/skills/<name>/SKILL.md` | A **skill** (reusable, auto-loaded by its description) |

## Power features
**Checkpointing** — `/rewind` or `Esc Esc` on an empty prompt. Claude checkpoints your code before every edit; restore the **code**, the **conversation**, or **both**. *Caveat:* it tracks Claude's file edits only — **not** `bash`/`rm` changes or edits made outside the session. Keep Git for permanent history.

**Plan mode** — `Shift+Tab` cycles permission modes (default → accept-edits → **plan** → bypass). In plan mode Claude researches and proposes a plan but makes **no edits** until you approve.

**Subagents** — `.claude/agents/<name>.md` (or `/agents`). Each runs in its **own context window** with its own tools/model — spin up several in **parallel** and keep the noise out of your main chat. Frontmatter: `name`, `description`, `tools`, `model`. *(A subagent can't spawn more subagents.)*

**Hooks** — shell commands that fire on Claude's actions, configured in `.claude/settings.json`. e.g. a `PostToolUse` hook with an `Edit|Write` matcher auto-formats every file Claude edits. Run `/hooks` to view them (read-only — edit the JSON, or just ask Claude to add one). *Deterministic, not "maybe the model remembers."*

**MCP** — connect external tools (docs, Jira, Postgres, the browser) in one command:
```
claude mcp add --transport http <name> <url>     # then:  claude mcp list  →  ✔ Connected
```
Commit a `.mcp.json` to share a server with your team. Scopes: local / project / user.

**Skills** — `.claude/skills/<name>/SKILL.md`. The frontmatter `description` tells Claude when to use it; the folder name is the command. Inject live data with `` !`git diff HEAD` `` — Claude Code runs it and pastes the output in before reading the skill.

**Headless / scripting** — `claude -p "..."` prints the answer and exits. Pipe stdin in, get text or `--output-format json` out. Perfect for CI and one-liners.

## Keyboard
`Esc` interrupt · `Esc Esc` rewind · `Shift+Tab` cycle permission modes · `@` mention a file · `/` commands · `↑` prompt history · `Ctrl+C` quit

## Three habits that pay off
1. **Write a real `CLAUDE.md`.** Specific beats vague — "use pnpm, not npm" > "follow best practices". Commit it so your whole team (and every agent) shares one memory.
2. **Plan before big changes.** `Shift+Tab` into plan mode, read the plan, *then* let it edit.
3. **Make the boring stuff deterministic.** A hook for formatting/tests beats hoping the model remembers.

---
*Made by Stig · **Run the Docs** · a project by Invotek. One Claude Code tip every weekday → [newsletter link]*

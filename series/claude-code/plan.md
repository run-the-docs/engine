# Run the Docs — Claude Code — Series Plan

The production rig is ready: the Mac Mini M4 (`user 'claude'`) has the full confirmed toolchain — tmux, ffmpeg 8.1, node v25.8.0, python3.14, Chrome, and the Kokoro ONNX model — which is exactly the 5-step pipeline this channel already runs for Kubernetes and React. The engine repo (`run-the-docs/engine`) already supports adding a new series with zero `checker.py` changes, because Claude Code docs publish an `llms.txt` index identical to the OpenClaw/Hono pattern the checker already consumes. The docs surface is fully mapped (the original WebFetch block was routed around: `docs.claude.com` 301-redirects to the canonical `code.claude.com/docs`, whose `llms.txt` enumerates all ~145 real pages). **Verdict: feasible and ready to scaffold — pending only Stig's approval per the HARD RULE "No Production Without an Approved Plan."** This document is the plan to be approved; no video is produced here.

## Source & Fidelity

**Tracking source for the registry checker:** `https://code.claude.com/docs/llms.txt`

- This `llms.txt` enumerates all ~145 Claude Code doc pages, each as a `code.claude.com/docs/en/<slug>.md` URL — the same pattern `registry/checker.py` already consumes for OpenClaw and Hono. **No `checker.py` code change is required.** On its next weekly run it will populate `contentHash` / `lastChecked` / `lastChanged` for the new `claude-code` entries automatically.
- **Migration note (locked):** the legacy roots `docs.anthropic.com/en/docs/claude-code/` and `docs.claude.com/en/docs/claude-code/` now 301-redirect to `code.claude.com/docs/en/`. All registry keys use the **canonical `code.claude.com` `.md` URLs** (matching the OpenClaw/Hono `.md`-suffixed style). Do **not** key entries to the old hosts (they will rot) and do **not** use `platform.claude.com/llms.txt` (that is the API/platform index, not the product docs).
- **meta.sources entry:** `name: "Claude Code"`, `baseUrl: "https://code.claude.com/docs/en/"`, `llmsTxt: "https://code.claude.com/docs/llms.txt"`.

**How the 1:1 rule is satisfied:** Every `Source doc URL` in the season table below is taken verbatim from that `llms.txt` index — no invented pages. Each episode is a faithful 1:1 mapping of its docs page(s): every heading, code example, and warning on the page is covered, nothing skipped, nothing invented. The convention used:

- **`full` / `short`** episodes map to exactly **one** docs page.
- **`two-part`** episodes pair two tightly-coupled small pages that the docs themselves cross-link as guide+reference or quickstart+deep-dive (e.g. setup + troubleshoot-install, interactive-mode + commands, security + permissions) and that are individually too small to anchor a full episode — OR, for `cli-reference` only, split one genuinely huge page (59.5KB) into two recorded parts within a single episode entry. The "huge page → up to two parts" allowance is used conservatively, for `cli-reference` alone.

**Verification applied:** the verification pass flagged one title mismatch (ep 18) and a large set of uncovered pages. Both are corrected below — ep 18 retitled to match the docs (`Extend Claude Code`), and the season extended from 40 to **54 episodes** so that previously-gapped pages (agent-teams/worktrees/workflows, the full Agent SDK surface, surfaces VS Code/Desktop/Web/Slack/Chrome, sandboxing, scheduled-tasks, output-styles/statusline, enterprise/admin, and the cloud-provider variants) are all mapped. Volatile pages (`whats-new/*`, `changelog`) and pure marketing kits (`champion-kit`, `communications-kit`) are **tracked in the registry but deliberately excluded from episode planning** to limit re-record churn; they can seed a future season.

## Branding

| Aspect | Decision |
|--------|----------|
| **Accent color** | `#da7756` (Anthropic clay/terracotta, RGB 218,119,86) |
| **Font** | JetBrains Mono (engine-locked; Apple-system / Menlo fallback) — unchanged |
| **Background** | `#0a0a0a` near-black (engine default; ideal terminal aesthetic) |
| **Code text** | `#90ee90` (engine green — unchanged) |
| **Schedule slot** | Saturday 09:00 Europe/Oslo, 1 episode/week |
| **Discord (approval)** | `#plan-review` (or the channel wired into `.github/workflows/request-review.yml`) |
| **Discord (series)** | `#claude-code` (new dedicated per-series channel) |

**Accent rationale:** Like `#326CE5` IS Kubernetes blue and `#61dafb` IS React cyan, the accent is brand-anchored, not invented. `#da7756` is the verified Anthropic brand hex (the PROJECT CONTEXT's `#D97757` is visually indistinguishable but off-spec — lock `#da7756`). Terminal-green was rejected as the accent because the engine already uses green (`#90ee90`) for code text in every series; promoting it would collide with code syntax color and fail to differentiate this series. Result: a clay-on-black terminal look that reads instantly as "Claude Code."

**Suggested `build.py` constant overrides (per episode):**
```
ACCENT='#da7756', HIGHLIGHT='#da7756', BG='#0a0a0a',
GRAD1='#1a1410', GRAD2='#2a1a12'   // warm-shifted dark gradient echoing the clay
CODE_TEXT='#90ee90', TEXT='#eee'
```
Document this as a new accent row in `STYLE_GUIDE.md`; episode label format: `claude code · <topic> · ep NN`.

**Recurring visual motifs (all respecting `verify-layout.js` zones — content must not draw below y=860; status line lives in the caption/footer zone):**
- **Simulated terminal pane** — framed monospace terminal, clay-tinted title bar showing the running command, animated streaming agent output. The signature recurring frame.
- **Tool-call cards** — rounded cards animating in as the agent invokes Read / Edit / Bash / Grep / Glob, tool name in clay + one-line arg summary.
- **Unified diff view** — red/green +/- hunks in JetBrains Mono (green stays `#90ee90`, deletions muted clay-red) for Edit / code-review / checkpointing episodes.
- **Permission / approval prompt** — clay-bordered y/n approve-deny box for permissions / permission-modes / sandboxing episodes.
- **Agent-loop ring** — circular think → act (tool) → observe diagram in clay for how-it-works / agent-loop / sub-agents episodes.
- **CLAUDE.md / file-tree card** — stylized `.claude/` tree + CLAUDE.md snippet for memory / settings / skills / hooks episodes.
- **Sub-agent fan-out** — lead node spawning parallel child agent nodes for subagents / agent-teams / worktrees / workflows episodes.
- **Slash-command chip** — a `/command` pill expanding into its action for slash-commands / skills episodes.
- **MCP plug/connector motif** — server-to-client connector animating data flow for the MCP episodes.
- **Status-line + spinner** — bottom-zone caption styled as a Claude Code status line (clay spinner glyph) reinforcing the in-terminal feel.

**Schedule note:** Mon/Wed/Fri (K8s) + Tue/Thu (React) consume all five weekdays, so Saturday is the only collision-free slot and gives the new series its own identity at a sustainable 1/week pace while the backlog builds. If a weekday is mandatory, the lowest-conflict fallback is sharing React's Tue/Thu by alternating weeks (1 React + 1 Claude Code) — but Saturday is cleaner. This is an open question for Stig (see below).

## Episode Season

**Run the Docs — Claude Code (Season 1) — 54 episodes, 6 arcs.** Every `Source doc URL` is a real page from `code.claude.com/docs/llms.txt`. Verification corrections applied: ep 18 retitled to match docs; 14 episodes added to close all reported coverage gaps. (`whats-new/*`, `changelog`, and marketing kits are registry-tracked but intentionally out of episode scope.)

### Arc 1 — Getting Started

| Ep | Title | Source doc URL | Format | ~Dur | Hook |
|----|-------|----------------|--------|------|------|
| 1 | What Claude Code Actually Is | https://code.claude.com/docs/en/overview | full | 8:00 | It reads your codebase, edits files, runs commands, and ships PRs — from terminal, IDE, desktop, and browser. The whole map in 8 minutes. |
| 2 | Your First Real Task | https://code.claude.com/docs/en/quickstart | full | 9:00 | From `claude` to a committed fix — the exact first session, step by step, nothing skipped. |
| 3 | How Claude Code Works Under the Hood | https://code.claude.com/docs/en/how-claude-code-works | full | 7:00 | The agent loop, the tools, the context window — the mental model that makes everything else click. |
| 4 | Advanced Setup & Install Troubleshooting | https://code.claude.com/docs/en/setup + https://code.claude.com/docs/en/troubleshoot-install | two-part | 9:00 | Native installer, Homebrew channels, Linux package managers, manual updates — plus fixes for when login won't cooperate. |
| 5 | Authentication & Logging In | https://code.claude.com/docs/en/authentication | full | 7:00 | Subscription, Console API key, or a third-party provider — every auth path and how to switch. |

### Arc 2 — Core Workflows

| Ep | Title | Source doc URL | Format | ~Dur | Hook |
|----|-------|----------------|--------|------|------|
| 6 | Common Workflows: The Prompt Recipes | https://code.claude.com/docs/en/common-workflows | full | 10:00 | Explore code, fix bugs, refactor, test, open PRs, write docs — the everyday recipe book, page-for-page. |
| 7 | Best Practices for Claude Code | https://code.claude.com/docs/en/best-practices | full | 9:00 | Prompting, context hygiene, plan-then-edit, scoping work — how power users actually drive the agent. |
| 8 | Interactive Mode & Slash Commands | https://code.claude.com/docs/en/interactive-mode + https://code.claude.com/docs/en/commands | two-part | 9:00 | Every keystroke, mode toggle, and built-in slash command inside a live session. |
| 9 | Managing Sessions | https://code.claude.com/docs/en/sessions | full | 7:00 | Resume, name, branch, and pick from history — your conversations are saved locally and addressable. |
| 10 | Plan Mode & Permission Modes | https://code.claude.com/docs/en/permission-modes | full | 7:00 | Plan, accept-edits, bypass, default — pick how much rope the agent gets before it touches disk. |
| 11 | Keep Working Toward a Goal | https://code.claude.com/docs/en/goal | short | 6:00 | Set a finish line and let Claude grind toward it — how goal-directed sessions stay on track. |

### Arc 3 — Configuration, Memory & Context

| Ep | Title | Source doc URL | Format | ~Dur | Hook |
|----|-------|----------------|--------|------|------|
| 12 | Claude Code Settings | https://code.claude.com/docs/en/settings | full | 10:00 | settings.json, top to bottom — every key, every scope, every precedence rule. |
| 13 | Environment Variables | https://code.claude.com/docs/en/env-vars | full | 7:00 | The full env-var table — model, auth, telemetry, network — every knob you can flip from the shell. |
| 14 | How Claude Remembers Your Project: CLAUDE.md & Auto Memory | https://code.claude.com/docs/en/memory | full | 9:00 | CLAUDE.md is read at the start of every session — and auto memory saves what Claude learns. The whole memory system. |
| 15 | Exploring the Context Window | https://code.claude.com/docs/en/context-window | full | 7:00 | What's in the window, what eats it, and how /context and /compact keep you from running out. |
| 16 | The .claude Directory | https://code.claude.com/docs/en/claude-directory | full | 7:00 | settings, commands, agents, skills, hooks — a guided tour of everything that lives in .claude/. |
| 17 | Checkpointing: Rewind Your Changes | https://code.claude.com/docs/en/checkpointing | short | 6:00 | Claude tracks file states so you can roll back a bad edit instantly — Esc-Esc and you're back. |
| 18 | Output Styles & the Status Line | https://code.claude.com/docs/en/output-styles + https://code.claude.com/docs/en/statusline | two-part | 7:00 | Reshape how Claude talks and what your status line shows — make the session feel like yours. |
| 19 | Customize Terminal, Keybindings & Fullscreen | https://code.claude.com/docs/en/terminal-config + https://code.claude.com/docs/en/keybindings | two-part | 7:00 | Tune your terminal, rebind every key, go fullscreen — the ergonomics layer the docs spell out in full. |

### Arc 4 — Extensibility: Skills, Hooks, MCP, Subagents, Plugins

| Ep | Title | Source doc URL | Format | ~Dur | Hook |
|----|-------|----------------|--------|------|------|
| 20 | Extend Claude Code | https://code.claude.com/docs/en/features-overview | full | 7:00 | Skills, hooks, MCP, subagents, plugins — five ways to extend the agent, and when to reach for each. |
| 21 | Extend Claude with Skills | https://code.claude.com/docs/en/skills | full | 9:00 | Package a repeatable workflow into a /command your whole team can run — that's a Skill. |
| 22 | Automate Actions with Hooks (Guide) | https://code.claude.com/docs/en/hooks-guide | full | 9:00 | Auto-format after every edit, block dangerous commands, ping yourself when Claude needs input — deterministic control via hooks. |
| 23 | Hooks Reference: Events, Schemas & I/O | https://code.claude.com/docs/en/hooks | full | 10:00 | Every hook event, the exact JSON in and out, exit codes, async hooks, MCP tool hooks — the full contract. |
| 24 | Connect Your First MCP Server | https://code.claude.com/docs/en/mcp-quickstart | full | 8:00 | Wire Claude into GitHub, Sentry, or Postgres in one command — your first MCP connection, end to end. |
| 25 | MCP Deep Dive: Transports, Scopes & Resources | https://code.claude.com/docs/en/mcp | full | 10:00 | stdio, SSE, HTTP; local vs project vs user scope; tools, resources, prompts — the complete MCP reference. |
| 26 | Create Custom Subagents | https://code.claude.com/docs/en/sub-agents | full | 9:00 | Give a task its own context window, its own tools, its own prompt — and keep your main thread clean. |
| 27 | Create Plugins | https://code.claude.com/docs/en/plugins | full | 9:00 | Bundle skills, hooks, MCP servers, and agents into one installable package — that's a plugin. |
| 28 | Plugins Reference & Dependencies | https://code.claude.com/docs/en/plugins-reference + https://code.claude.com/docs/en/plugin-dependencies | two-part | 8:00 | The full plugin manifest schema and how to pin dependency versions so installs stay reproducible. |
| 29 | Discover & Distribute Plugins via Marketplaces | https://code.claude.com/docs/en/discover-plugins + https://code.claude.com/docs/en/plugin-marketplaces | two-part | 9:00 | Install prebuilt plugins from a marketplace — then stand up your own to share across your team. |

### Arc 5 — Automation, SDK & CI/CD

| Ep | Title | Source doc URL | Format | ~Dur | Hook |
|----|-------|----------------|--------|------|------|
| 30 | Run Claude Code Programmatically (Headless) | https://code.claude.com/docs/en/headless | full | 8:00 | `claude -p` turns the agent into a Unix citizen: pipe in, get JSON out, fan out across files. |
| 31 | The Agent SDK: Build Your Own Agent | https://code.claude.com/docs/en/agent-sdk/overview | full | 8:00 | Everything Claude Code can do — its tools, its loop, its permissions — exposed as an SDK you build on. |
| 32 | Agent SDK Quickstart | https://code.claude.com/docs/en/agent-sdk/quickstart | full | 8:00 | Your first programmatic agent in under 20 lines — install, query, stream the result. |
| 33 | How the Agent Loop Works (SDK) | https://code.claude.com/docs/en/agent-sdk/agent-loop | full | 7:00 | Gather context, take action, verify, repeat — the loop that powers every Claude Code agent, in detail. |
| 34 | Custom Tools & MCP in the SDK | https://code.claude.com/docs/en/agent-sdk/custom-tools + https://code.claude.com/docs/en/agent-sdk/mcp | two-part | 9:00 | Hand your agent your own functions as tools — and plug it into external MCP servers from code. |
| 35 | SDK: Sessions, Streaming & Structured Output | https://code.claude.com/docs/en/agent-sdk/sessions + https://code.claude.com/docs/en/agent-sdk/streaming-output | two-part | 9:00 | Persist conversations, stream tokens in real time, and shape the result your code consumes. |
| 36 | SDK: Permissions, Subagents & System Prompts | https://code.claude.com/docs/en/agent-sdk/permissions + https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts | two-part | 9:00 | Gate every tool call, spawn subagents, and rewrite the system prompt — control the agent from code. |
| 37 | SDK: Cost Tracking & Observability | https://code.claude.com/docs/en/agent-sdk/cost-tracking + https://code.claude.com/docs/en/agent-sdk/observability | two-part | 8:00 | Watch tokens and latency with OpenTelemetry — production telemetry for your own agent. |
| 38 | SDK: Hosting & Secure Deployment | https://code.claude.com/docs/en/agent-sdk/hosting + https://code.claude.com/docs/en/agent-sdk/secure-deployment | two-part | 9:00 | Ship your agent to prod safely — hosting models and the deployment hardening checklist. |
| 39 | SDK Reference: Python & TypeScript | https://code.claude.com/docs/en/agent-sdk/python + https://code.claude.com/docs/en/agent-sdk/typescript | two-part | 10:00 | The full API surface — every option, type, and message — for both SDK languages. |
| 40 | Claude Code GitHub Actions | https://code.claude.com/docs/en/github-actions | full | 9:00 | @claude in a PR comment, automated review on every push, issue triage in CI — Claude living in your repo. |
| 41 | Claude Code GitLab CI/CD | https://code.claude.com/docs/en/gitlab-ci-cd | full | 8:00 | The same automated review and triage power, wired into GitLab pipelines instead of Actions. |
| 42 | Automate Work with Routines & Scheduled Tasks | https://code.claude.com/docs/en/routines + https://code.claude.com/docs/en/scheduled-tasks | two-part | 8:00 | Morning PR reviews, overnight CI analysis, weekly audits — prompts on a schedule, even when your laptop's off. |
| 43 | Agent Teams & Parallel Workflows | https://code.claude.com/docs/en/agent-teams + https://code.claude.com/docs/en/workflows | two-part | 9:00 | Orchestrate teams of Claude sessions and dynamic workflows — many agents, one goal. |
| 44 | Run Parallel Sessions with Worktrees | https://code.claude.com/docs/en/worktrees | full | 7:00 | One repo, many branches, many Claude sessions at once — parallelism without stepping on yourself. |

### Arc 6 — Surfaces, Reference, Security & Ops

| Ep | Title | Source doc URL | Format | ~Dur | Hook |
|----|-------|----------------|--------|------|------|
| 45 | Claude Code in VS Code | https://code.claude.com/docs/en/vs-code | full | 7:00 | The agent inside your editor — inline diffs, the sidebar, and everything the IDE integration unlocks. |
| 46 | Claude Code on Desktop | https://code.claude.com/docs/en/desktop + https://code.claude.com/docs/en/desktop-quickstart | two-part | 8:00 | The native desktop app from zero to first task — a GUI front end to the same engine. |
| 47 | Claude Code on the Web | https://code.claude.com/docs/en/claude-code-on-the-web + https://code.claude.com/docs/en/web-quickstart | two-part | 8:00 | Run Claude Code in the browser — no install, the same agent, end to end. |
| 48 | Claude Code in Slack & Chrome | https://code.claude.com/docs/en/slack + https://code.claude.com/docs/en/chrome | two-part | 8:00 | Drive the agent from a Slack thread or a Chrome tab — two more surfaces wired to one engine. |
| 49 | CLI Reference: Commands & Flags | https://code.claude.com/docs/en/cli-reference | two-part | 10:00 | Every command, every flag — the complete `claude --help` decoded, in two parts. |
| 50 | Tools Reference | https://code.claude.com/docs/en/tools-reference | full | 8:00 | Read, Edit, Bash, Grep, Glob, WebFetch and the rest — every built-in tool and what it's allowed to do. |
| 51 | Sandboxing & Sandbox Environments | https://code.claude.com/docs/en/sandboxing + https://code.claude.com/docs/en/sandbox-environments | two-part | 8:00 | Run the Bash tool in a sandbox and pick the right isolation level — safety rails for autonomous runs. |
| 52 | Manage Costs Effectively | https://code.claude.com/docs/en/costs | full | 7:00 | Where the tokens go, how to watch spend with /cost, and the settings that keep the bill sane. |
| 53 | Security: Writing Safe Code, the Model & Permissions | https://code.claude.com/docs/en/security-guidance + https://code.claude.com/docs/en/security + https://code.claude.com/docs/en/permissions | full (3-seg deep dive) | 10:00 | Flag secrets and injection as you build, understand the trust boundary, and master the allow/deny rules that gate every tool call. |
| 54 | Troubleshooting & Error Reference | https://code.claude.com/docs/en/troubleshooting + https://code.claude.com/docs/en/errors | two-part | 9:00 | When it breaks: the symptom-to-fix map, the error codes decoded, and `claude doctor` to the rescue. |

> **Coverage note:** Episode 53 follows the multi-segment deep-dive pattern (cf. kubernetes ep13) to cover three tightly-coupled security pages in one episode with per-segment `seg<N>.html` assets. Enterprise/admin pages (`admin-setup`, `third-party-integrations`, `network-config`, `server-managed-settings`, `managed-mcp`, `analytics`, `monitoring-usage`, `legal-and-compliance`, `data-usage`, `zero-data-retention`) and cloud-provider variants (`amazon-bedrock`, `google-vertex-ai`, `microsoft-foundry`, `claude-platform-on-aws`, `llm-gateway`) are **registered as `unplanned`** in the registry and held for a dedicated **Enterprise/Deployment mini-season** rather than forced into Season 1, to keep S1 focused on the developer adoption arc. They remain tracked so `checker.py` watches them for change.

**Summary**

| Arc | Episodes | Approx. Total Time |
|-----|----------|--------------------|
| Arc 1 — Getting Started | 5 | ~40 min |
| Arc 2 — Core Workflows | 6 | ~48 min |
| Arc 3 — Config, Memory & Context | 8 | ~60 min |
| Arc 4 — Extensibility | 10 | ~89 min |
| Arc 5 — Automation, SDK & CI/CD | 15 | ~127 min |
| Arc 6 — Surfaces, Reference, Security & Ops | 10 | ~83 min |
| **Total** | **54** | **~447 min (~7.5 hrs)** |

54 new episodes needed (none exist yet). At 1/week (Saturday): ~12.5 months. At 2/week: ~6 months.

## Engine Integration

**New example repo:** `run-the-docs/claude-code` — created **PUBLIC** (this is the public-by-design `run-the-docs` org for the channel; it is NOT under `Stig-Johnny`/`tablez-dev`, so the ALL-REPOS-PRIVATE rule does not apply). Mirrors the single-lowercase-tech-word convention of `run-the-docs/kubernetes` `/react` `/openclaw` `/hono`. Description: *"Code examples and episode guides for the Run the Docs — Claude Code series."* Internal layout mirrors the kubernetes repo: `README.md`, per-episode guide folders, and runnable `.claude/` examples (CLAUDE.md samples, skills, hooks, slash commands, MCP config snippets). **Examples must be first-party/illustrative only** (no third-party code without security review per CLAUDE.md) and must contain **no secrets and no internal infra paths** (e.g. `/Users/claude/...`, Kokoro model location).

**Real `registry/registry.json` entry example** (a planned episode — note the canonical `.md` key and migration note):
```json
"https://code.claude.com/docs/en/memory.md": {
  "url": "https://code.claude.com/docs/en/memory.md",
  "source": "claude-code",
  "slug": "claude-code/memory",
  "contentHash": null,
  "lastChecked": null,
  "lastChanged": null,
  "episode": {
    "series": "claude-code",
    "number": 14,
    "title": "How Claude Remembers Your Project: CLAUDE.md & Auto Memory",
    "plannedAt": "2026-06-08"
  },
  "episodeStatus": "planned",
  "notes": "Docs migrated from docs.anthropic.com/docs.claude.com -> code.claude.com/docs in 2026; track canonical .md URL"
}
```
Unplanned pages use the same shape with `episode: null`, `episodeStatus: "unplanned"`.

**Ordered engine-repo changes — PR #1 (`engine`, branch `docs/add-claude-code-series`):**
1. `registry/registry.json` → add `meta.sources[]`: `{ name: "Claude Code", baseUrl: "https://code.claude.com/docs/en/", llmsTxt: "https://code.claude.com/docs/llms.txt", notes: "Docs migrated from docs.anthropic.com/docs.claude.com to code.claude.com in 2026; llms.txt lists ~145 .md pages" }`.
2. `registry/registry.json` `docs` object → add ~145 `unplanned` entries (one per `code.claude.com/docs/en/*.md` page), each `{ source:"claude-code", slug:"claude-code/<path-slug>", contentHash:null, lastChecked:null, lastChanged:null, episode:null, episodeStatus:"unplanned", notes:null }`. Track `whats-new/*` and `changelog` but exclude them from episode planning.
3. Create `series/claude-code/plan.md` — the deliverable, in the exact kubernetes/openclaw format: H1 `# Claude Code Series — Full Coverage Plan`; "Based on:" line citing `https://code.claude.com/docs/en/` (llms.txt crawled 2026-06-06); Audience/Angle/Length preamble (Audience: developers adopting agentic coding; Angle: docs-faithful 1:1 page coverage; Length ~90/110/130s @ ~150 wpm, 30fps); Section-grouped tables (`# | Title | Docs Link | Key Concepts | Est. Length`); Summary table; Recommended Priority Order (next 10). **No "Existing Episodes" table** (new series).
4. Create `series/claude-code/README.md` mirroring `series/kubernetes/README.md` (audience, format, docs source = `code.claude.com/docs/en/`, code-examples repo = `github.com/run-the-docs/claude-code`).
5. Create `series/claude-code/episodes.md` mirroring the kubernetes tracker (`| Ep | Title | Topic | Duration | Status | YouTube Link | Transcript |`), all rows `Status=Planned`, YouTube/Transcript = TBD; add Release Strategy note (Saturday weekly) + playlist line.
6. `STYLE_GUIDE.md` → add the `claude-code` accent row: accent `#da7756` (clay) on BG `#0a0a0a`, code `#90ee90`, font JetBrains Mono, episode label `claude code · <topic> · ep NN`.
7. `pipeline/build_episode.sh` → update the hardcoded `Upload to Discord: #iclaw-e` print to `#claude-code` (or make it a variable). Minor, recommended.
8. **No `checker.py` change** — it already handles `llms.txt` sources; the new entries get `contentHash`/`lastChecked` on the next weekly run automatically.
9. `registry/docs-tracker.json` → **no entries yet** (flat publish-only tracker); add `{ep, series:"claude-code", title, docsUrl, videoDate, youtubeId}` rows only as episodes publish (post-approval).

**PR #2 (NEW repo `run-the-docs/claude-code`, PUBLIC):** scaffold `README.md` + per-episode guide folders + runnable `.claude/` examples; link it from `series/claude-code/README.md`.

**POST-APPROVAL ONLY (separate PR — do NOT include now):** create `series/claude-code/production/ep01/`, copy `pipeline/template_tts.py → tts.py`, `template_build.py → build.py` (override `ACCENT/HIGHLIGHT=#da7756`, `BG=#0a0a0a`), `template_render.py → render.py`, `build_episode.sh`; add `script.md` with Production Notes (accent `#da7756`, font JetBrains Mono, label `claude code · overview · ep 01`); run build; verify with `tools/verify-layout.js` (0 violations); then flip the registry entry `planned → published`.

## Demo Plan (Mac Mini, tmux)

A minimal, low-risk smoke test that proves the 5-step pipeline produces a Claude-Code-branded clip — **without** touching the engine production tree (so it does not violate the no-production rule; it writes to a throwaway scratch dir and is deleted after). It generates one narrated line over a single clay-on-black canvas card.

```bash
# 1. SSH to the production Mac Mini and open a dedicated tmux session
ssh claude@<mac-mini-host>
tmux new -s ccdemo

# 2. Scratch workspace (NOT under series/ — pure smoke test)
mkdir -p ~/runthedocs/scratch/cc-demo && cd ~/runthedocs/scratch/cc-demo

# 3. STEP 1 — TTS: one line through Kokoro (bm_george, the engine voice).
#    Trust the model's own SAMPLE_RATE constant; do NOT hardcode 24k/44.1k.
#    (copy the engine's pipeline/template_tts.py, set sentences=["Run the Docs. Claude Code. Every page, one to one."])
cp ~/runthedocs/engine/pipeline/template_tts.py ./tts.py
# edit `sentences` + model path /Users/claude/runthedocs/kokoro/onnx/model.onnx, then:
python3 tts.py            # -> voice.wav + timing.json

# 4. STEP 2 — minimal canvas card in the Claude Code accent.
#    Single scene: clay title "claude code · overview · ep 01" on #0a0a0a,
#    ACCENT='#da7756', code line in #90ee90, JetBrains Mono. 1920x1080, window.renderFrame(n).
#    (hand-write a tiny demo.html, or copy template_build.py with the overridden color constants)

# 5. STEP 3 — layout QA gate (must report 0 violations: content above y=860, caption below)
node ~/runthedocs/engine/tools/verify-layout.js ./demo.html

# 6. STEP 4 — render a few seconds of frames via canvas.toDataURL (NOT page.screenshot), batches of 30
cp ~/runthedocs/engine/pipeline/template_render.py ./render.py
python3 render.py         # -> frames/frame_%06d.png

# 7. STEP 5 — encode: libx264 crf20 + aac mux
ffmpeg -framerate 30 -i frames/frame_%06d.png -c:v libx264 -crf 20 -pix_fmt yuv420p video.mp4
ffmpeg -i video.mp4 -i voice.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 cc-demo.mp4

# 8. Inspect locally (do NOT post to a public channel / YouTube)
open cc-demo.mp4         # eyeball the clay-on-black look + audio sync

# 9. Clean up the scratch dir
cd ~ && rm -rf ~/runthedocs/scratch/cc-demo
```
**Success criteria:** `verify-layout.js` returns 0 violations; `cc-demo.mp4` plays with the narrated line in sync and the clay (`#da7756`) accent on near-black reads as "Claude Code." This validates Kokoro → canvas → QA gate → render → ffmpeg end-to-end for the new accent before any real ep01 is built. The clip is for internal eyeballing only — per the HARD RULE, nothing is published until the plan is approved.

## Open Questions for Stig

1. **Accent hex — confirm `#da7756`?** PROJECT CONTEXT proposed `#D97757`; the verified Anthropic brand hex is `#da7756`. They're visually near-identical, but one value must be locked in `STYLE_GUIDE.md` and reused in every `build.py` to avoid per-episode drift. **Recommend `#da7756`.**
2. **Schedule — Saturday 09:00 Europe/Oslo, or share React's Tue/Thu?** All five weekdays are taken (K8s Mon/Wed/Fri, React Tue/Thu). Saturday is collision-free and gives the series its own identity, but it's a new publishing day for the channel — confirm the audience tolerates a weekend slot, or accept alternating React's Tue/Thu (1 React + 1 Claude Code). **Recommend Saturday.**
3. **Season scope — 54 episodes (S1) with Enterprise/cloud-provider pages deferred to a mini-season?** The verification pass surfaced ~85 uncovered pages; I mapped the developer-adoption core into 54 episodes and held enterprise/admin + cloud-provider variants (Bedrock/Vertex/Foundry/AWS) for a later focused season. Confirm this split, or fold enterprise into S1.
4. **New repo name & visibility — `run-the-docs/claude-code`, PUBLIC?** Matches the four sibling example repos and lives in the public-by-design `run-the-docs` org (outside the private-repos rule). Confirm OK to create it public.
5. **First 3 episodes to ship (recommended priority order):** (1) **Ep 1 — What Claude Code Actually Is** (`overview`), the channel-anchor explainer; (2) **Ep 2 — Your First Real Task** (`quickstart`), the natural follow-on that converts viewers to users; (3) **Ep 6 — Common Workflows: The Prompt Recipes** (`common-workflows`), the highest-utility evergreen recipe book. Confirm this trio (or reorder) as the first three Saturdays after approval.
6. **Discord channels — create `#claude-code` for the series, and post `plan.md` to `#plan-review` for approval?** Per the HARD RULE the plan goes to the review channel first; published videos/build output go to `#claude-code` afterward. Confirm the exact approval channel name wired into `request-review.yml`.
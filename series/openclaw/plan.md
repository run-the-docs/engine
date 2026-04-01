# OpenClaw Series — Full Coverage Plan

Based on: https://docs.openclaw.ai/ (llms.txt crawled 2026-04-01, 375 pages)

**Audience:** Developers and power users setting up and extending OpenClaw as a personal AI assistant
**Angle:** "Your AI, on your infrastructure" — privacy-first, local-first, every tool explained

---

## Section 1: What is OpenClaw? (3 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 01 | What is OpenClaw? | [start/getting-started](https://docs.openclaw.ai/start/getting-started.md) + [start/lore](https://docs.openclaw.ai/start/lore.md) | Personal AI gateway, runs on your machine, connects to any chat platform, no vendor lock-in | ~90s |
| 02 | Installing OpenClaw | [start/wizard](https://docs.openclaw.ai/start/wizard.md) + [start/setup](https://docs.openclaw.ai/start/setup.md) | CLI wizard, config structure, first run, workspace concept | ~90s |
| 03 | Connecting Your First Channel | [channels/index](https://docs.openclaw.ai/channels/index.md) + [channels/discord](https://docs.openclaw.ai/channels/discord.md) | Channel concept, Discord setup, pairing, routing rules | ~95s |

---

## Section 2: Chat Channels (6 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 04 | Discord | [channels/discord](https://docs.openclaw.ai/channels/discord.md) | Bot setup, DM vs server, thread handling, reactions | ~90s |
| 05 | Telegram | [channels/telegram](https://docs.openclaw.ai/channels/telegram.md) | BotFather, webhook vs polling, groups, inline mode | ~90s |
| 06 | Signal & iMessage | [channels/signal](https://docs.openclaw.ai/channels/signal.md) + [channels/imessage](https://docs.openclaw.ai/channels/imessage.md) | Privacy-first channels, Apple integration, desktop linking | ~85s |
| 07 | Slack | [channels/slack](https://docs.openclaw.ai/channels/slack.md) | App manifest, socket mode, workspace scoping | ~85s |
| 08 | WhatsApp | [channels/whatsapp](https://docs.openclaw.ai/channels/whatsapp.md) | WhatsApp Business API, Meta app setup, media handling | ~85s |
| 09 | Channel Routing | [channels/channel-routing](https://docs.openclaw.ai/channels/channel-routing.md) + [channels/groups](https://docs.openclaw.ai/channels/groups.md) | Multi-channel routing, broadcast groups, per-channel config | ~90s |

---

## Section 3: Automation (6 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 10 | Cron Jobs | [automation/cron-jobs](https://docs.openclaw.ai/automation/cron-jobs.md) | Schedule types (at/every/cron), payload kinds, session targets, delivery modes | ~100s |
| 11 | Cron vs Heartbeat | [automation/cron-vs-heartbeat](https://docs.openclaw.ai/automation/cron-vs-heartbeat.md) | When to use each, batching checks, reducing API calls | ~85s |
| 12 | Webhooks | [automation/webhook](https://docs.openclaw.ai/automation/webhook.md) | Inbound webhooks, trigger format, routing to agent | ~85s |
| 13 | Hooks | [automation/hooks](https://docs.openclaw.ai/automation/hooks.md) | Pre/post message hooks, content filtering, transform | ~85s |
| 14 | Polls & Standing Orders | [automation/poll](https://docs.openclaw.ai/automation/poll.md) + [automation/standing-orders](https://docs.openclaw.ai/automation/standing-orders.md) | Periodic checks, persistent instructions, always-on behaviors | ~90s |
| 15 | Background Tasks | [automation/tasks](https://docs.openclaw.ai/automation/tasks.md) + [automation/clawflow](https://docs.openclaw.ai/automation/clawflow.md) | Long-running jobs, ClawFlow pipelines, task queues | ~90s |

---

## Section 4: AI Models & Agents (5 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 16 | Connecting AI Models | [models/index](https://docs.openclaw.ai/models/index.md) | Anthropic/OpenAI/Google/local, model config, per-session overrides | ~95s |
| 17 | Sub-Agents | [tools/subagents](https://docs.openclaw.ai/tools/subagents.md) | Spawning isolated agents, streaming to parent, use cases | ~95s |
| 18 | ACP Agents | [tools/acp-agents](https://docs.openclaw.ai/tools/acp-agents.md) | Codex/Claude Code in threads, runtime=acp, persistent sessions | ~90s |
| 19 | Skills | [tools/skills](https://docs.openclaw.ai/tools/skills.md) + [tools/creating-skills](https://docs.openclaw.ai/tools/creating-skills.md) | SKILL.md format, when to create, reusable workflows | ~90s |
| 20 | Thinking Levels | [tools/thinking](https://docs.openclaw.ai/tools/thinking.md) | Reasoning modes, when to use extended thinking, cost tradeoffs | ~80s |

---

## Section 5: Tools (7 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 21 | Code Execution | [tools/code-execution](https://docs.openclaw.ai/tools/code-execution.md) + [tools/exec](https://docs.openclaw.ai/tools/exec.md) | exec tool, approvals, PTY mode, background sessions | ~95s |
| 22 | Browser Control | [tools/browser](https://docs.openclaw.ai/tools/browser.md) | OpenClaw browser vs user browser, CDP, snapshot/act/screenshot | ~90s |
| 23 | Web Search | [tools/web](https://docs.openclaw.ai/tools/web.md) + [tools/web-fetch](https://docs.openclaw.ai/tools/web-fetch.md) | DuckDuckGo, fetch+extract, Brave/Exa/Perplexity options | ~80s |
| 24 | Memory & MEMORY.md | [tools/index](https://docs.openclaw.ai/tools/index.md) | Memory search, MEMORY.md pattern, session continuity | ~85s |
| 25 | Exec Approvals | [tools/exec-approvals](https://docs.openclaw.ai/tools/exec-approvals.md) + [tools/elevated](https://docs.openclaw.ai/tools/elevated.md) | Security model, allow-once vs allow-always, elevated mode | ~85s |
| 26 | Diffs & Canvas | [tools/diffs](https://docs.openclaw.ai/tools/diffs.md) | Diff viewer tool, canvas presentation, UI output | ~75s |
| 27 | TTS & Image | [tools/tts](https://docs.openclaw.ai/tools/tts.md) + [tools/image-generation](https://docs.openclaw.ai/tools/image-generation.md) | Voice replies, image gen, media tools | ~80s |

---

## Section 6: Configuration & Security (4 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 28 | Config Deep Dive | [cli/config](https://docs.openclaw.ai/cli/config.md) + [cli/configure](https://docs.openclaw.ai/cli/configure.md) | Config schema, patching vs applying, gateway restart | ~90s |
| 29 | Auth & Credentials | [auth-credential-semantics](https://docs.openclaw.ai/auth-credential-semantics.md) + [automation/auth-monitoring](https://docs.openclaw.ai/automation/auth-monitoring.md) | API keys, per-channel auth, credential storage | ~85s |
| 30 | Nodes & Pairing | [channels/pairing](https://docs.openclaw.ai/channels/pairing.md) | Pairing mobile/remote nodes, camera/screen/location tools | ~85s |
| 31 | Linux Server Deploy | [vps](https://docs.openclaw.ai/vps.md) + [ci](https://docs.openclaw.ai/ci.md) | Self-hosted on VPS, systemd, CI pipeline, updates | ~90s |

---

## Section 7: Web UI & Dashboard (2 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 32 | Dashboard & WebChat | [web/dashboard](https://docs.openclaw.ai/web/dashboard.md) + [web/webchat](https://docs.openclaw.ai/web/webchat.md) | Control UI, session history, WebChat interface | ~80s |
| 33 | Slash Commands & Plugins | [tools/slash-commands](https://docs.openclaw.ai/tools/slash-commands.md) + [tools/plugin](https://docs.openclaw.ai/tools/plugin.md) | Built-in commands, installing plugins, ClawHub | ~80s |

---

## Coverage Summary

| Section | Episodes |
|---------|----------|
| What is OpenClaw? | 3 |
| Chat Channels | 6 |
| Automation | 6 |
| AI Models & Agents | 5 |
| Tools | 7 |
| Configuration & Security | 4 |
| Web UI & Dashboard | 2 |
| **Total** | **33** |

**0 published. 33 episodes for full coverage (~48 min total)**
375 source docs pages — grouped to avoid one-page episodes on thin reference content.

---

## Sections Excluded

| Section | Reason |
|---------|--------|
| All individual channel pages (20+ channels) | Grouped by platform type; niche channels (Feishu, Zalo, IRC, Tlon) skip |
| CLI reference pages (30+ commands) | Reference content; mention in config deep dive episode |
| API reference (`openapi.json`) | Too technical for explainer format |
| ClawHub | Brief mention in skills episode |

---

## Recommended Priority Order (first 10)

1. **What is OpenClaw?** (#01) — awareness/discovery episode
2. **Installing OpenClaw** (#02) — onboarding
3. **Cron Jobs** (#10) — most powerful and unique feature
4. **Connecting Discord** (#04) — most popular channel
5. **Sub-Agents** (#17) — differentiating AI feature
6. **Code Execution** (#21) — exec tool is core to the dev use case
7. **Cron vs Heartbeat** (#11) — practical decision guide
8. **ACP Agents** (#18) — Codex/Claude Code integration
9. **Skills** (#19) — SKILL.md is key to extensibility
10. **Exec Approvals** (#25) — security model explainer

---

## Note on Conflict of Interest

OpenClaw is the platform this agent runs on. Episodes should be factual and accurate — do not over-hype. If a documented feature has known limitations, mention them. The audience trusts this channel for honest technical explainers.

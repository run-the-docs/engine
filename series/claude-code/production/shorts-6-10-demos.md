# Claude Code shorts 6–10 — recording playbook

Demo scenarios + artifact files for producing shorts 6–10 on the Mac Mini (real-terminal `claude` recordings, dir `cc-demo-repo`). Each short is a 1:1-faithful teaser of its `code.claude.com/docs` page; every claim was adversarially fact-checked against the live doc.

## EP 6 — EP 6 — UNDO ANYTHING CLAUDE DOES  ·  artifact: `slugify.py`

**Artifact file (stage in cc-demo-repo before recording):**

```
slugify.py
---
def slugify(text):
    # BUG: should lowercase, strip, and collapse whitespace to single hyphens
    return text.replace(" ", "-")
```

**Demo scenario:**

GOAL (≈25s on screen): show Claude editing a file, a SECOND edit going wrong, then /rewind restoring the file instantly while the conversation stays — proving "local undo" for Claude's edits.

ON-SCREEN COHERENCE NOTE (show as a one-line lower-third early): "Card = starting state. The demo first FIXES it, then introduces a NEW bad edit — that's what we rewind." The file-card shows the buggy `-` one-liner. Step 1 FIXES that bug; step 2 introduces a DIFFERENT regression (`_` replacement). 'Restore code' at the step-2 checkpoint reverts to the pre-step-2 = step-1 (correct) state per docs lines 13/19/35. Make step-2's result read as clearly-worse than the card (no lowercase, no strip, wrong separator, comment gone) so the restore payoff is obvious.

(a) STAGE BEFORE RECORDING (on Mac Mini, dir /tmp/rtd-demo/cc-demo-repo):
- Keep the two existing files exactly as-is: slugify.py (the buggy one-liner shown on the file-card) and test_slugify.py.
- Start a FRESH claude session in that dir (no prior checkpoints) so the rewind menu lists only this session's prompts: `cd /tmp/rtd-demo/cc-demo-repo && claude`. Clear the scrollback so the terminal is clean.
- IMPORTANT (docs limitation): the demo must rely ONLY on Claude's own file-editing tools — do NOT have Claude use bash `rm/mv/cp`, and do NOT hand-edit the file outside Claude or from another concurrent session, because checkpointing tracks NEITHER bash changes NOR external/manual edits (docs lines 70-78, 80-82). The edit we undo must be made by Claude's Edit tool, in this session.

(b) EXACT PROMPTS via tmux send-keys (one per checkpoint; each prompt creates a checkpoint):
  1. Send: `Rewrite slugify in slugify.py to lowercase, strip, and collapse whitespace into single hyphens. Edit the file directly.` — Enter. Let Claude apply the Edit (viewer sees the diff / "Updated slugify.py"). This is now the GOOD state.
  2. Send: `Actually, simplify it to just text.replace(" ", "_") and remove the comment.` — Enter. Let Claude apply this SECOND (deliberately wrong) Edit so the file is now regressed/broken. This is the "off the rails" moment.
  3. Confirm the prompt input is EMPTY first (if it has text, double-Esc only CLEARS the text per docs line 28 — it will NOT open the menu). Then open the rewind menu by sending Esc twice as TWO SEPARATE send-keys calls with a brief delay, NOT batched (the two keys can coalesce and the second Esc may not register):
       `tmux send-keys -t <pane> Escape` ; sleep 0.3 ; `tmux send-keys -t <pane> Escape`
     (Equivalent alternative: type `/rewind` then Enter.) Viewer sees the menu listing the prompts from steps 1 and 2.
  4. Navigate with DISCRETE key presses (small delay between each — the nested TUI is timing-sensitive; do NOT batch):
       - Down/Enter to highlight + select the STEP-2 prompt to open its action list.
       - The action list opens highlighted on the FIRST item ("Restore code and conversation"). "Restore code" is the THIRD item, so press Down TWICE, then Enter:
           `tmux send-keys -t <pane> Down` ; sleep 0.3 ; `tmux send-keys -t <pane> Down` ; sleep 0.3 ; `tmux send-keys -t <pane> Enter`
       (We restore CODE only, to demonstrate keeping the conversation while reverting files.)

(c) WHAT THE VIEWER MUST SEE (proof it works):
- The rewind menu visibly listing the session's prompts (step 1 + step 2) — proves "every prompt is a checkpoint."
- The action list, in the documented order: (1) Restore code and conversation, (2) Restore conversation, (3) Restore code, (4) Summarize from here, (5) Summarize up to here, (6) Never mind — with the selector landing on the 3rd item, "Restore code" — proves the granular options from the docs and matches the navigation in step (b)4.
- After choosing "Restore code", slugify.py reverts to its state before the bad step-2 edit (back to the correct step-1 version), while the conversation/history stays on screen — proves code reverted, conversation kept.
- Optional kicker if time allows: a final `cat slugify.py` (or Claude reads it) shows the regressed `_` replacement is gone and the lowercase/strip/hyphen version is back. Keep total runtime ~25s; if tight, end right after the file visibly snaps back in the menu/preview.

---

## EP 7 — EP 7 — CLAUDE RUNS A TEAM IN PARALLEL  ·  artifact: `.claude/agents/module-researcher.md`

**Artifact file (stage in cc-demo-repo before recording):**

```
.claude/agents/module-researcher.md
---
---
name: module-researcher
description: Read-only researcher for a single code module. Use proactively to investigate one module in its own context, then report a short summary back.
tools: Read, Grep, Glob
model: haiku
---

You research ONE module of the codebase in isolation.

When invoked:
1. Locate the module's entry points and key files
2. Map its responsibilities, dependencies, and public surface
3. Note any risks, TODOs, or rough edges

Return ONLY a tight summary to the main conversation:
- What the module does
- How it connects to the rest of the app
- Anything that looks off

Do not modify files. Keep the verbose exploration in your own context.
```

**Demo scenario:**

GOAL: On screen the viewer sees ONE `claude` session fan out into multiple subagents that run at the same time, each in its own context, then a synthesized summary lands in the main chat — proving parallel subagents with isolated context.

(a) STAGE BEFORE RECORDING (on Mac Mini, in cc-demo-repo):
  1. Ensure a small multi-module repo exists with three clearly separate dirs, e.g. `src/auth/`, `src/db/`, `src/api/`, each with 2-3 real source files (enough that exploring all three in the main chat would be noisy). A trivial Node/Express-style app is fine.
  2. Create the project subagent file `.claude/agents/module-researcher.md` with EXACTLY the artifact contents above (name: module-researcher, tools: Read, Grep, Glob, model: haiku, read-only body). This is a PROJECT subagent so it ships in the repo.
  3. Because subagent files added directly on disk load at session start, start Claude AFTER the file exists (do NOT add it mid-session) so it is picked up. Quick pre-check off-camera: run `/agents`, confirm `module-researcher` appears under the project scope, then exit.
  4. Clear the terminal; launch a fresh session: `claude`. Window sized for vertical crop.

(b) EXACT PROMPT(S) TO SEND (single prompt, drivable via tmux send-keys):
  Prompt 1 (the whole demo):
    "Use the module-researcher subagent to research the auth, database, and api modules in parallel — one subagent per module — then give me a one-line summary of each. Run them in the background so they go at once."

(c) WHAT THE VIEWER MUST SEE (the proof):
  - Claude announces it is delegating and SPAWNS THREE subagents (one per module). The transcript/task list shows multiple `module-researcher` tasks active concurrently (background tasks running side by side) — this is the "team in parallel" money shot.
  - Each subagent's own tool calls (Grep/Read/Glob over only its module) stay inside that subagent's panel/transcript — they do NOT flood the main conversation. Highlight that the main chat is short while the subagents are busy (isolated context windows).
  - When all three finish, three concise summaries return to the MAIN conversation — one line per module — that the main Claude synthesizes. The bulk of the exploration never appears in the main thread.
  - HONEST framing (matches docs limits): the subagents are read-only (tools: Read, Grep, Glob) and do not edit anything; they cannot spawn further subagents; the demo keeps each summary short on purpose because many detailed results would consume the main context.
  TIMING: ~20-30s. Drive with tmux: send the prompt, then capture the moment the three tasks light up at once, hold on the parallel task list (~5s), then cut to the three returned summaries in the main chat.

---

## EP 8 — EP 8 — AUTO-FORMAT EVERY FILE CLAUDE EDITS  ·  artifact: `.claude/settings.json`

**Artifact file (stage in cc-demo-repo before recording):**

```
.claude/settings.json
---
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

**Demo scenario:**

Goal: on camera, viewer sees Claude edit a messy file, then a PostToolUse hook auto-runs the formatter and the file snaps into clean style — with zero extra prompting. Drivable via tmux send-keys on the Mac Mini, ~25-30s.

(a) STAGE BEFORE RECORDING (off camera):
1. Use a dedicated JS scratch repo (NOT cc-demo-repo — that is a Python project: it has slugify.py / test_slugify.py, no package.json, no node_modules, no .claude/ — so dropping a lone greeting.js there is incongruous and Prettier wouldn't be the natural formatter). Create a throwaway dir, e.g. `mkdir -p /tmp/rtd-demo/js-scratch && cd /tmp/rtd-demo/js-scratch`.
2. Install the formatter once so it runs instantly on camera (Prettier is not cached — npx would otherwise fetch it mid-take): `npm init -y >/dev/null 2>&1 && npm i -D prettier >/dev/null 2>&1`. (jq is already present at /usr/bin/jq — VERIFIED. If staging on a fresh box, `brew install jq` first; the docs call jq out as a prerequisite.)
3. Create the hook config at /tmp/rtd-demo/js-scratch/.claude/settings.json with EXACTLY the artifact contents above (PostToolUse + "Edit|Write" matcher + `jq -r '.tool_input.file_path' | xargs npx prettier --write`).
4. Create a deliberately messy, Prettier-formattable throwaway demo file `greeting.js` so the reformat is visually obvious:
   `const   greet=(name)=>{return    'hi '+name}`   (extra spaces, no semicolons, single quotes, one line). This file exists only for this episode.
5. Open two stacked tmux panes: TOP pane runs `claude` (interactive, launched inside /tmp/rtd-demo/js-scratch so it loads .claude/settings.json); BOTTOM pane runs a portable live-view loop so the viewer sees the file change in real time:
   `while true; do clear; cat greeting.js; sleep 0.5; done`
   (Use this loop, NOT `watch` — VERIFIED that `watch`, `fswatch`, and `entr` are all ABSENT on the Mac Mini, so `watch -n0.5 ...` would fail with 'command not found' on camera. `clear` and bash are present at /usr/bin/clear. Alternative: `brew install watch` off camera during staging if you prefer the `watch` UI.)
6. Prove the hook is registered using a DETERMINISTIC, screenshot-friendly method: in the claude pane (or a third pane) run `cat .claude/settings.json` so the PostToolUse + Edit|Write + prettier command is visible on screen. OPTIONAL: you may instead open `/hooks` and select PostToolUse to show the same details, but the `/hooks` TUI is read-only and fragile to drive via tmux send-keys (it depends on cursor position / list order). If you do keep `/hooks`, send keystrokes with explicit sleeps between Down / Enter / Esc and budget a few extra seconds; `cat .claude/settings.json` is the safer default.

(b) PROMPT TO SEND (tmux send-keys into the claude pane, then Enter):
   "In greeting.js, change the greeting text from 'hi ' to 'Hello, '. Edit the file directly."
(Single Edit on greeting.js — this is what triggers the Edit|Write matcher.)

(c) WHAT THE VIEWER MUST SEE (the proof):
- Claude uses the Edit tool on greeting.js (tool call visible in the top pane).
- IMMEDIATELY after the edit succeeds, the PostToolUse hook fires (per docs, PostToolUse runs AFTER the tool call succeeds) and runs `npx prettier --write` on that exact path. With Prettier pre-installed off camera, the reformat is ~14ms (VERIFIED end-to-end: the messy one-liner becomes multi-line, double-quoted, semicolon-terminated output) — so the Edit round-trip + visible reflow fits comfortably in ~25-30s.
- The bottom live-view pane visibly reformats: the one-liner becomes multi-line, indented, double-quoted, semicolon-terminated Prettier output — AND it now says 'Hello, ' (Claude's edit) reflowed by the hook. The transformation happens with no second prompt.
- Optional end card text overlay: "PostToolUse hook → prettier --write — ran itself."
Honesty notes (respect the docs limits): (1) The hook runs AFTER the edit — it cannot undo it (docs: "PostToolUse hooks cannot undo actions"). (2) It only fires for the Edit/Write tools, so the demo deliberately tells Claude to "edit the file directly" rather than via a Bash command, which the Edit|Write matcher would not catch. (3) `npx prettier` only formats web/JS/CSS/JSON/MD files — for Python/Go/Rust you'd swap in black/ruff/gofmt (the copy already says "Prettier, Black, or your test suite"); this is why the demo uses a JS scratch repo so the on-screen Prettier choice fits the file.

---

## EP 9 — EP 9 — GIVE CLAUDE A NEW SUPERPOWER IN ONE COMMAND  ·  artifact: `.mcp.json`

**Artifact file (stage in cc-demo-repo before recording):**

```
.mcp.json
---
{
  "mcpServers": {
    "claude-code-docs": {
      "type": "http",
      "url": "https://code.claude.com/docs/mcp"
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

**Demo scenario:**

Goal: show a real Claude Code session gaining a new tool via MCP and visibly answering through it. Drivable via tmux send-keys on the Mac Mini, finishes in ~20-30s. Uses the docs' own first example (hosted claude-code-docs server) because it needs NO auth and connects with one command — the cleanest teaser.

(a) STAGE BEFORE RECORDING (in /tmp/rtd-demo/cc-demo-repo):
  - Ensure the server is NOT already added so the demo shows the real add->connect flow: run `claude mcp remove claude-code-docs 2>/dev/null || true` and `claude mcp remove claude-code-docs --scope local 2>/dev/null || true` in that directory.
  - Confirm a clean shell prompt in the repo dir; widen tmux pane for legible captions; clear scrollback.
  - Do NOT pre-create .mcp.json — the file-card shows the artifact; the live demo uses the CLI `claude mcp add` path (local scope) so nothing extra has to be approved on screen.
  - Network reachable (hosted HTTPS server). Optional sanity check off-camera: `curl -I https://code.claude.com/docs/mcp` (a 404/405 still means reachable, per the docs).

(b) EXACT COMMANDS / PROMPTS (each via tmux send-keys, ~2-4s apart):
  1. tmux send-keys -t demo 'claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp' Enter
     -> SEE the confirmation line: "Added HTTP MCP server claude-code-docs with URL: https://code.claude.com/docs/mcp to local config".
  2. tmux send-keys -t demo 'claude mcp list' Enter
     -> SEE "claude-code-docs" listed with the "✓ Connected" status indicator (green check).
  3. tmux send-keys -t demo 'claude' Enter   (start the interactive session)
  4. After the prompt appears, tmux send-keys -t demo 'Use the claude-code-docs server to look up what MCP_TIMEOUT does' Enter
     -> The first tool call triggers a permission prompt; tmux send-keys the approval (select "Yes"/allow once).
     -> SEE a tool call in Claude's output LABELED with the server name "claude-code-docs" (this is the proof the answer came through MCP, not built-in knowledge), followed by Claude's answer that MCP_TIMEOUT sets the server startup timeout in milliseconds.

(c) WHAT THE VIEWER MUST SEE (the proof): the one-line `claude mcp add` confirmation -> the "✓ Connected" row in `claude mcp list` -> a server-name-labeled tool call ("claude-code-docs") inside the session answering a question. That labeled tool call is the docs-accurate proof the feature works.

Respecting docs' limitations: the demo names the server in the prompt ON PURPOSE — the docs note Claude normally picks tools on its own, but naming it "guarantees the demonstration goes through the new server rather than another tool." We show the real permission prompt (don't skip it). We use the zero-auth hosted server, so no OAuth/browser step is implied. The closing caption reflects the docs' Note that each connected server consumes context window.

---

## EP 10 — EP 10 — TURN ANY WORKFLOW INTO A REUSABLE SKILL  ·  artifact: `.claude/skills/summarize-changes/SKILL.md`

**Artifact file (stage in cc-demo-repo before recording):**

```
.claude/skills/summarize-changes/SKILL.md
---
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullet points, then list any risks you notice such as missing error handling, hardcoded values, or tests that need updating. If the diff is empty, say there are no uncommitted changes.
```

**Demo scenario:**

REPO: cc-demo-repo on the Mac Mini (small Python project: slugify.py + test_slugify.py). The skill used is the docs' own getting-started example, verbatim — no invented behavior. (Docs put this skill at the PERSONAL path ~/.claude/skills/; we deliberately use the PROJECT path .claude/skills/ so the skill is visible IN the repo on camera — both are documented-valid and folder-name→command works identically. The consequence of project scope is a one-time workspace trust dialog, handled explicitly below.)

(a) STAGE BEFORE RECORDING:
1. cc-demo-repo is NOT yet a git repo (no .git, no commits), and the skill's `!`git diff HEAD`` REQUIRES an existing HEAD — in a repo with zero commits `git diff HEAD` fails fatally ("ambiguous argument 'HEAD': unknown revision"). So FIRST give it a baseline commit, on a feature branch, with a clean tree. From inside cc-demo-repo, run EXACTLY (verified working):
   - `rm -rf __pycache__`  (remove the stray pycache dir so it does not land in the baseline commit and pollute the diff card)
   - `git init -q`
   - `git add -A`
   - `git -c user.email=demo@demo.co -c user.name=demo commit -qm baseline`
   - `git checkout -b demo/skills`
   - `git status`  (confirm clean working tree)
   I verified this whole sequence: after baseline, an uncommitted edit shows correctly in `git diff HEAD` (exit 0) and __pycache__ stays out of the commit.
2. Create the skill file exactly as the docs show (this is the artifact card shown on screen):
   - `mkdir -p .claude/skills/summarize-changes`
   - Write `.claude/skills/summarize-changes/SKILL.md` with the artifact_contents above (frontmatter `description:` + `## Current changes` / `` !`git diff HEAD` `` + `## Instructions`). NOTE (soften wording): the project `.claude/skills/` directory must exist BEFORE `claude` starts, because creating the .claude/skills/ directory itself mid-session would need a restart to be watched (docs: a top-level skills dir created after session start requires a restart). Editing/adding a SKILL.md inside an already-watched .claude/skills/ takes effect live — but we create the dir + file before launch as the safe path that sidesteps this entirely.
3. Make one small, visible UNcommitted edit so `git diff HEAD` shows something real, e.g. add a `strip()`/lowercasing helper or a guard clause to `slugify.py`. Do NOT stage or commit it.
4. Launch claude fresh in the repo root: `claude`. Because this is PROJECT-scope, a workspace TRUST dialog appears — accept it as an explicit ordered beat BEFORE the first prompt; project skills (and the skill's tool grants) only load after trust (docs: project `.claude/skills/` `allowed-tools` and listing take effect after accepting the workspace trust dialog). If driving via tmux send-keys, script the Enter/confirm for the trust prompt first, then send the prompt.

(b) EXACT PROMPTS (drive via tmux send-keys, one Enter after each):
   HERO beat — proves auto-invocation via description:
     `What did I change?`
   (Claude should match the skill's description and load /summarize-changes on its own; the `` !`git diff HEAD` `` line is pre-rendered with the actual diff before Claude sees it.)
   FALLBACK (auto-invocation is a probabilistic model judgment, not deterministic — docs Troubleshooting "Skill not triggering"): if take 1 does not auto-load, either re-prompt closer to the description (`what did I change / review my diff`), or directly invoke the GUARANTEED fallback `/summarize-changes`. The recording must never dead-end on the probabilistic beat.

(c) WHAT THE VIEWER MUST SEE (proof the feature works):
   1. The trust dialog accepted (brief), then the file-card: `.claude/skills/summarize-changes/SKILL.md` with the `description:` frontmatter and the `` !`git diff HEAD` `` line highlighted (the dynamic-context-injection moment).
   2. In the terminal, Claude indicating it is USING / loading the `summarize-changes` skill WITHOUT being told to (no `/` typed) — auto-invocation from the description. (If the fallback was used, show the `/summarize-changes` invoke instead — same skill, still proves the point.)
   3. Claude's answer: 2–3 bullets summarizing the exact edit made to slugify.py, plus a short risks list — proving it summarized the LIVE diff, not guessed from memory.
   Optional tail beat if time allows (~3s) AND not already used as the fallback: type `/summarize-changes` to show the SAME skill is also directly invocable by name (folder name = command).

TIMING: trust + clean tree + one edit + single prompt fits ~20–30s. Stay within docs limits: the skill only summarizes/flags (read-only reasoning over `git diff HEAD`); it makes no commits and changes no files.

---


# Claude Code — next production batch (post-06-28)

The Shorts drip is banked through **2026-06-28 (ep23)**. Every produced episode is already
scheduled, so extending the drip needs **new** episodes recorded. This file makes a recording
session turn-key: 5 drafted scripts (`ep26/28/29/30/31.lines.json`), each verified 1:1 against
the live `code.claude.com/docs`, with the `recd.sh` case to add + the host-probe to run first.

> Scripts were drafted + adversarially verified by a 10-agent workflow (2026-06-24). Every one
> came back **revise** (not ship) — all fixes are folded into the `lines.json` here; the
> remaining work is host-side (the `recd.sh` case + a tmux panel-probe), which can't be done
> off-host. Caveats per episode below are load-bearing — read them before recording.

## Coverage map

**Covered (produced):** ep1 intro · ep2 fix-a-test · ep3 CLAUDE.md · ep4 plan-mode · ep5 custom
slash commands · ep6 rewind · ep7 subagents · ep8 hooks · ep9 MCP · ep10 skills · ep11 context ·
ep12 --continue · ep13 git-pipe · ep14 @-mention · ep15 /code-review · ep16 interview · ep17 /init ·
ep19 /goal · ep21 /sandbox · ep23 /statusline · ep24 ! shell · fable5 model · (ep18 auto-mode, ep25
/fast = authored but not produced).

**This batch (headless-recordable, drafted):**

| Ep | Topic | Docs page | Title (≤30) |
|----|-------|-----------|-------------|
| 26 | Install a plugin from a marketplace | `/en/discover-plugins` | EP 26 — INSTALL A PLUGIN |
| 28 | Output styles | `/en/output-styles` | EP 28 — OUTPUT STYLES |
| 29 | Extended thinking / effort | `/en/model-config` | EP 29 — THINK HARDER |
| 30 | Append to CLAUDE.md mid-chat | `/en/memory` | EP 30 — TELL IT TO REMEMBER |
| 31 | Background tasks | `/en/interactive-mode` | EP 31 — BACKGROUND TASKS |

**Produced 2026-06-26 (were "deferred"):** **ep22 worktrees** (`--worktree`; MODE=bash, recorded headless — the "two terminals" rationale was wrong, a first-class flag exists; `ss8e8MjPISw`, scheduled 07-09) · **ep27 a subagent in one command** (recorded as the headless `--agents` twin of the `/agents` wizard; MODE=prompt interactive so the `● slugify-explainer` delegation renders + a one-sentence answer — headless `-p` made COMPLETE=stable false-fire before the long subagent answered; `xOL1dVTQp_c`, scheduled 07-10).

**Produced 2026-06-26 (round 2, were "deferred"):** **ep18 permission modes** (Shift+Tab cycle default→acceptEdits→plan; NEW recd.sh `MODE=modecycle` + `COMPLETE=modecycle` BTab-keystroke handler [tmux drops `S-Tab`, use `BTab`] + per-episode `IDLE=6.0`; hero retargeted to the base cycle — auto/bypass are account-gated and narration-only; captions made state-agnostic since fix_term collapses the dwells so frame-perfect caption↔mode sync isn't achievable; `lBKOiEV3oGc`, scheduled 07-12) · **ep36 Stop hook** (redesigned to `MODE=bash`: `claude -p "…" && cat .claude/stop.log` — the hook fires on `-p` exit then cat shows it, killing the old in-session FOLLOWUP race; the nested settings shape is CORRECT — the workflow verifier's "flat" claim was wrong, empirically verified; `S3iaX_ur3YM`, scheduled 07-10).

**ep25 PRODUCED 2026-06-26 (round 3):** **ep25 fast mode** (`/fast on` → `↯ Fast mode ON · $10/$50 per Mtok`; MODE=slash toggle-only, COMPLETE=stable — the account's fast-mode usage credits got exhausted by a test query, and a query burns credits while the toggle does NOT, so the demo shows the toggle + the ↯ status-bar indicator only; `N4eCKNsGWQk`, scheduled 07-13 tail). GOTCHA: `/fast` is account-gated on **usage credits** — probe with a manual `/fast on` (clean = `↯ Fast mode ON`; gated = `Fast mode disabled · usage credits exhausted`), and DON'T add a follow-up query to the recipe (it drains credits mid-take).

**ep38 PRODUCED 2026-06-26 (NEW, beyond the original six — extends the drip):** **ep38 pick the right model** (`claude --model haiku -p "…"` runs a simple task on a cheaper/faster model; MODE=bash; the command visibly shows `--model haiku` + Haiku's answer — distinct from fable5's model showcase; `1h-48GITJuU`, scheduled 07-14). PICKED because it's leak-free: `/usage` & `/cost` render a panel that EXPOSES the operator's global setup (`/load-memory` skill + `discord` MCP server) → NOT recordable on the neutral channel; flag-based `claude -p` episodes stay clean.

**Still deferred (NOT headless):** ep20 /voice — real mic, hardware-blocked, off-pipeline only. **This is the LAST of the original "missing six" still unproduced** (ep18/22/25/27/36 all shipped; ep20 needs an operator mic recording).

## Post-06-28 slot plan (one/day, 13/16/19 UTC rotation continues)

| Date | Slot (UTC) | Ep |
|------|-----------|----|
| 2026-06-29 Mon | 13:00 | ep26 Install a plugin |
| 2026-06-30 Tue | 16:00 | ep29 Think harder |
| 2026-07-01 Wed | 19:00 | ep28 Output styles |
| 2026-07-02 Thu | 13:00 | ep31 Background tasks |
| 2026-07-03 Fri | 16:00 | ep30 Tell it to remember |

Order leads with the strongest hook (plugins) and spaces the two write-to-file demos (28/30).
Upload + `publishAt` needs the YouTube OAuth token (operator/Ops-E; ~weekly expiry — re-auth
before scheduling). The build/QA/upload steps are the standard `recd.sh → build-ep.sh → upload`.

## Per-episode recording recipe

Each draft `recd.sh` case below incorporates the verifier's fixes. They are NOT yet added to
`recd.sh` (host-tested step) — add the case during the recording session after the panel-probe.

### ep26 — Install a plugin  ⚠ use the CLI, not the slash/TUI path
The `/plugin` slash command opens an interactive 4-tab TUI (not headless). Record the **CLI**
path, which emits clean recordable output (verified live):
```
26) RESET=5411d3b; ARTIFACTS=""; MODE=bash; \
    PRECMD='claude plugin marketplace add anthropics/claude-code'; \
    TEXT='claude plugin install commit-commands@claude-code-plugins'; \
    COMPLETE=plugin_install ;;   # stop once both lines show:
    #   "Successfully added marketplace: claude-code-plugins"
    #   "Successfully installed plugin: commit-commands@claude-code-plugins (scope: user)"
```
- **Probe:** `claude --version` supports `claude plugin …`; `git ls-remote https://github.com/anthropics/claude-code HEAD` (the add/install hit github over the network — NOT WebFetch, so the disallow list doesn't block them, but an offline host fails).
- **Reset hygiene between takes:** `claude plugin uninstall commit-commands@claude-code-plugins` + `claude plugin marketplace remove claude-code-plugins` (verified to cleanly revert). Otherwise it shows "already installed".
- Captions/command already switched to the CLI form (no `/reload-plugins` — slash-only, can't show headless).

### ep28 — Output styles  (two-phase: style is read at session start)
`/output-style` was removed in v2.1.91 — the script uses the `outputStyle` **setting**, which a
fresh session reads at boot. Write it BEFORE the `claude -p` run:
```
28) RESET=5411d3b; ARTIFACTS=".claude/settings.local.json"; MODE=prompt; \
    PRECMD='mkdir -p .claude && printf "%s" "{\"outputStyle\":\"Explanatory\"}" > .claude/settings.local.json'; \
    CLAUDE='claude -p --strict-mcp-config --allowedTools Read Grep Glob --disallowedTools WebFetch WebSearch --effort low'; \
    TEXT='Explain what slugify.py does and why it lowercases before stripping characters.'; \
    COMPLETE=outputstyle ;;   # stop once the response is visibly reshaped: an educational
    #   "Insights"/"Insight:" aside OR clearly explanatory "why" prose, beyond a bare answer.
```
- **Probe:** PRECMD must run AFTER `recd.sh` resets the repo to RESET (the pipeline auto-resets first); then `cat .claude/settings.local.json` shows `{"outputStyle":"Explanatory"}` and `.claude/` + `slugify.py` exist at the sha. `claude --version` ≥ 2.1.91.
- **Caveat:** the Explanatory "Insights" block is a strong tendency, not a per-response contract — record 2-3 takes, keep the one where the aside renders.

### ep29 — Think harder  ✅ RECORDED + built 2026-06-24 (both formats, QA-clean)
**Shipped recipe (proven, now in `recd.sh`/`build-ep.sh`):** reused the `prompt → edit → testpass` path — `LAUNCH_FIRST=1` (clears the account toast), `--effort high`, `TEXT="ultrathink: fix slugify.py so the failing test passes, then run it."`, `COMPLETE=testpass`. The "with high effort" label renders in-terminal; 30.2s cut. The earlier concern below (gating on visible reasoning) was sidestepped by stopping on the test pass.
Plain `--verbose` is NOT documented to print reasoning in `-p` mode, so don't gate on it:
```
29) RESET=5411d3b; ARTIFACTS="slugify.py test_slugify.py"; MODE=prompt; \
    CLAUDE='claude --strict-mcp-config --allowedTools Read Edit "Bash(python3 *)" --disallowedTools WebFetch WebSearch --effort high'; \
    TEXT='ultrathink: slugify drops accents but leaves a stray double hyphen. Reason through the unicode normalization and separator-collapse, then fix slugify.py and run the tests.'; \
    COMPLETE=effort_testpass ;;   # stop once the "with high effort" label showed AND
    #   python3 -m pytest test_slugify.py reports passing.
```
- **Probe:** `claude --version` ≥ 2.1.154 (Opus 4.8 + effort); model must expose `high`. The "with high effort" label renders by the spinner — frame the spinner region.
- **Caveat:** line 2 names all five levels (low/med/high/x-high/max) — only fully correct on Opus 4.8/4.7/Fable 5 (4.6/Sonnet omit x-high). The demo only uses `high`, so it's fine; pick a 4.8 model on the host.
- If reasoning-on-camera is the whole point, switch to `--output-format stream-json --verbose --include-partial-messages | jq` (busier) — otherwise keep it simple.

### ep30 — Tell it to remember  ⚠ needs a new recd.sh clause + the CLAUDE.md sha
No `#` memory shortcut exists in current docs — the faithful path is the natural-language
"add this to CLAUDE.md". This edits a tracked file, so the permission prompt must be answered:
```
30) RESET=6a8d07c; ARTIFACTS="CLAUDE.md"; MODE=prompt; \
    CLAUDE='claude --strict-mcp-config --allowedTools Read Edit Write --disallowedTools WebFetch WebSearch --effort low'; \
    TEXT='Always run python3 -m pytest before committing. Add this to CLAUDE.md.'; \
    COMPLETE=memwrite ;;
```
Add the missing `memwrite)` clause to `recd.sh` (mirror `hookwrite`: grep the pane for
`Do you want to|1. Yes|allow Claude to edit` → `send-keys 1`, then succeed when the appended
line appears in `CLAUDE.md`):
```
memwrite) for i in $(seq 1 40); do sleep 3; p=$($TM capture-pane -pt cclive 2>/dev/null); \
  echo "$p" | grep -qiE "Do you want to|1\. Yes|allow Claude to edit" && $TM send-keys -t cclive "1"; \
  grep -qi "pytest" "$REPO/CLAUDE.md" 2>/dev/null && { echo "memwrite $i"; break; }; done; sleep 3 ;;
```
- **Probe:** use **RESET=6a8d07c** (the sha that ships a populated CLAUDE.md — same as ep3), not 5411d3b. Confirm `git -C cc-demo-repo cat-file -p 6a8d07c:CLAUDE.md` is non-empty with a heading the line can land under. The `*)` default does NOT press `1` → the edit hangs to timeout, so the `memwrite)` clause is mandatory.
- **Differentiation from ep3:** ep3 teaches *what* CLAUDE.md is; ep30's hero is the *mid-chat append* + the auto-memory-vs-CLAUDE.md distinction (line 5). Keep the hook on the append.

### ep31 — Background tasks  (keep the suite FAST in print mode)
`Ctrl+B` is interactive-only — it's narration line 5, never a scripted keystroke:
```
31) RESET=5411d3b; ARTIFACTS="test_slugify.py slugify.py"; MODE=prompt; \
    CLAUDE='claude -p --strict-mcp-config --allowedTools Bash Read --disallowedTools WebFetch WebSearch --effort low'; \
    TEXT='Run the test suite (pytest -q test_slugify.py) in the background so you do not block, tell me the background task ID, then read the output file and report pass/fail.'; \
    COMPLETE=bgtask ;;   # stop once a run_in_background task-ID line showed AND a populated
    #   Read of the output file reported pytest pass/fail.
```
- **Probe:** per `/en/headless`, the bg shell is killed ~5s after the final result — so **keep the suite fast** (do NOT pad with `sleep`; padding risks the Read landing on an empty file). A near-instant suite is fine — the money shot is the task-ID line + the populated Read, not wall-clock. Ensure `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` is unset.
- **Caveat:** print mode can't show live multi-turn responsiveness — line 3 was softened to "Clawd keeps working" (not "keeps responding to you").

## Production checklist (per episode)
1. Add the `recd.sh` case (above) + for ep30 the `memwrite)` clause; tmux panel-probe per the notes.
2. `recd.sh <N>` → record → `build-ep.sh <N>` (narrate + render 4:5 + 9:16) → frame QA (≤30-char header, 9:16 header not clipped).
3. Upload + set `publishAt` to the slot above (YouTube OAuth — operator/Ops-E).
4. `r2-sync.sh <N>` for the 9:16, add to website (or same-origin), update the D1 catalog.
5. Post to Discord #run-the-docs.

## Post-07-07 — ep37 (drafted + verified 2026-06-25)

### ep37 — Steer one run (`--append-system-prompt`)  ⚠ bash-PRINT pattern (like ep34's `-p`), NOT send-keys
Docs: `code.claude.com/docs/en/cli-reference` (System prompt flags). The flag **applies only to the
current invocation** — the docs explicitly contrast it with CLAUDE.md (`/en/memory`, persistent) and
output styles (`/en/output-styles`, persistent), which is the episode's hook. Distinct from ep34
(`-p | jq` plumbing); this shows `-p` *behavior steering*.

Record the headless **PRINT** form in **`MODE=bash`** (like ep34's `-p`): `CLAUDE=':'` skips the TUI
launch and the full `claude … -p "…"` command is typed into a plain `$ ` shell, so the printed answer
renders in the terminal. `COMPLETE=stable` (the default stability handler) catches it; no bespoke clause
needed. (The earlier `MODE=prompt; TEXT=""` draft was superseded by this bash-print form during
recording — this block matches the shipped `recd.sh` case.)

```
37) RESET=5411d3b; ARTIFACTS=""; MODE=bash; CLAUDE=':'; TEXT='claude --strict-mcp-config --append-system-prompt "Always answer in TypeScript and put a one-line ELI5 comment above every function." --allowedTools Read Grep Glob --disallowedTools WebFetch WebSearch --effort low -p "Write a function that slugifies a string."'; COMPLETE=stable ;;
```

Notes (from the verify pass):
- `--disallowedTools WebFetch WebSearch` is the **actual** restriction; `--allowedTools Read Grep Glob`
  only lets those run **without a permission prompt** (docs: "to restrict which tools are available, use
  `--tools`"). `--effort low` = fast single-turn answer (not "deterministic" — output isn't guaranteed).
- No tracked-file edit → no permission prompt to script around (unlike ep30's `memwrite`), and no
  RESET-state dependency beyond the standard slugify-present sha `5411d3b` (same as ep1/6/14).
- **Visible payoff:** the printed answer is TypeScript with an ELI5 comment above the function — a rule
  in neither CLAUDE.md nor an output style; a re-run without the flag answers normally.
- **Slot (shipped):** 2026-07-08 17:00 UTC — next open slot after ep33 (07-07 19:00). Recorded + built
  2026-06-26 (engine#81), YouTube `e9hzul46hHU`; scheduled after a pull-back from an accidental immediate
  public publish (cockpit card website#47).

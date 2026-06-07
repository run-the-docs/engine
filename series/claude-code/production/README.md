# Claude Code series — production pipeline

Real-terminal LinkedIn/TikTok/Shorts videos teaching Claude Code, mapped 1:1 to code.claude.com/docs. Runs on the Mac Mini under `~/runthedocs/series/claude-code/demo/`. These are the canonical scripts (kept in sync here so they don't live only on the host).

## Outputs per episode
- `claude-ep<N>-45.mp4` — **4:5** (1080×1350) for LinkedIn / X
- `claude-ep<N>-916.mp4` — **9:16** (1080×1920) for TikTok / YouTube Shorts / Reels

## Pipeline
1. **`recd.sh`** — unified recorder. `EP=<n> bash recd.sh`. Per-episode it: resets `cc-demo-repo` to the right commit (`RESET=`) so file cards + the live session see correct files; sets `tmux focus-events on` + `mouse on` so Claude's tmux hint chrome never renders; records a real `claude` session via tmux + asciinema; for slash episodes it reveals the `/` menu before running the command. Stops the recorder before closing claude (no exit-tail). Renders `.cast → .gif → claude-ep<N>-term.mp4`.
2. **`narrate_chatterbox.py <ep.lines.json>`** — Chatterbox TTS (own venv `~/chatterbox-venv`). Reads `[display, spoken]` line pairs → `narration.wav` + `narration.json` (segments/timing/title/sub/artifact). Perth watermark no-op'd. Pronunciation handled in the spoken column (Claude→Clawd, Invotek→Invo Tech, CLAUDE.md→"the Clawd dot M D file").
3. **`make_assets_45.py` / `make_assets_916.py`** — PIL header + captions + hook + file-card (`artifact.png`) for each format. Header divider sits **below** the subtitle. File-card content **word-wraps** to the card width (preserves code indentation; no right-edge clipping).
4. **`compose_45.py` / `compose_916.py`** — ffmpeg composite. Fits terminal to narration length; **`content_end()` trims the dead `[terminated]` tail** (keeps the last frame quickly followed by another). Suppresses the final outro caption (footer CTA carries it — no duplicate).

## Build — one path
**Always build via `build-ep.sh`.** Do not hand-run `compose_*.py` against a `rec/` left by another episode (see Guards).
- `bash build-ep.sh <N>` — narrate → assets → compose, **both** formats. Caches `narration-ep<N>.{wav,json}`. It also (a) **resets `cc-demo-repo` to the episode's commit before assets** so the file-card matches the episode, and (b) **asserts `rec/narration.json` title == `ep<N>.lines.json` title** (FATAL on mismatch).
- `RENDER_ONLY=1 bash build-ep.sh <N>` — re-render from cached narration with **no TTS re-roll** (also resets the repo + runs the guard). Preferred over `render45.sh`.
- `bash render45.sh <N>` — legacy render-only helper (no repo reset). Kept for compatibility; prefer `RENDER_ONLY=1 build-ep.sh`.
- `bash build_kit.py` — assembles the local posting kit (`~/Desktop/RunTheDocs-ClaudeCode/`): per-episode video + cover + `copy.md` (LinkedIn/TikTok/YouTube/X) + `POSTING-KIT.md` schedule.
- `bash push-to-nas.sh` — archives both formats + term cut + source to the Synology DS412+ (`<nas-tailscale-ip>`) once a DSM share is mounted (`/Volumes/video` by default).

## Guards — never ship the wrong episode (postmortem 2026-06-07)
`narrate` + `make_assets` write **shared, per-build-overwritten** files (`rec/narration.json`, `rec/narration.wav`, `rec/*.png`). Running `compose_*.py` **alone** — or any build that skips `narrate`+`make_assets` — bakes the **previous** episode's title / file-card / captions / audio onto **this** episode's terminal, silently. This shipped EP1 & EP2 titled **"EP 5 — SLASH COMMANDS"** with captions that didn't match the demo.

Now enforced:
- **COMPOSE GUARD** (`compose_{45,916}.py`): refuses to run when `rec/narration.json`'s episode ≠ `CC_OUT`'s episode.
- **Title assert** (`build-ep.sh`): `rec/narration.json` title must equal `ep<N>.lines.json` title.
- **Repo reset** (`build-ep.sh`): file-cards always reflect the episode's own files (buggy slugify for EP1, fixed for EP4, …).
- **Self-test:** `bash test-compose-guard.sh` → must print `GUARD_SELFTEST_OK` (case1 = the bug scenario is rejected; case2 = a matching build passes).
- **MANDATORY pre-publish check (per episode, both formats):** `ffmpeg -ss 5 -i rec/claude-ep<N>-45.mp4 -frames:v 1 /tmp/chk.png` and eyeball title + file-card + first caption. The pipeline can produce confident-looking **wrong** output — never upload unverified.

## cc-demo-repo reset commits (per episode)
EP1/EP2 → `5411d3b` (baseline, buggy slugify) · EP3 → `6a8d07c` (CLAUDE.md) · EP4 → `29299f9` (slugify fixed + titlecase) · EP5 → `0b6488a` (/test command).

## Notes
- Tooling installed via `uv` + managed CPython 3.12 (brew `python@3.12` has a broken pyexpat). ffmpeg/asciinema/agg via homebrew (see approved-tools).
- Posting copy: `../posting-kit/` (per-episode) + `../linkedin-posting-plan.md` (strategy).

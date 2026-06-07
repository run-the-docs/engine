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

## Build
- `bash build-ep.sh <N>` — narrate → assets → compose, **both** formats. Caches `narration-ep<N>.{wav,json}`.
- `bash render45.sh <N>` — render-only (no re-narrate), both formats, from cached narration. Use after a re-record or an asset/compose tweak.
- `bash build_kit.py` — assembles the local posting kit (`~/Desktop/RunTheDocs-ClaudeCode/`): per-episode video + cover + `copy.md` (LinkedIn/TikTok/YouTube/X) + `POSTING-KIT.md` schedule.
- `bash push-to-nas.sh` — archives both formats + term cut + source to the Synology DS412+ (`<nas-tailscale-ip>`) once a DSM share is mounted (`/Volumes/video` by default).

## cc-demo-repo reset commits (per episode)
EP1/EP2 → `5411d3b` (baseline, buggy slugify) · EP3 → `6a8d07c` (CLAUDE.md) · EP4 → `29299f9` (slugify fixed + titlecase) · EP5 → `0b6488a` (/test command).

## Notes
- Tooling installed via `uv` + managed CPython 3.12 (brew `python@3.12` has a broken pyexpat). ffmpeg/asciinema/agg via homebrew (see approved-tools).
- Posting copy: `../posting-kit/` (per-episode) + `../linkedin-posting-plan.md` (strategy).

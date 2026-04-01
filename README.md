# Run the Docs — Engine

The backbone of the Run the Docs channel: doc registry, change detection, and video build pipeline.

## Published Series

| Series | Episodes | Playlist | Example Code |
|--------|----------|----------|--------------|
| Kubernetes | 11 | [YouTube](https://www.youtube.com/playlist?list=PLdv4kqmXd-vVPLhuw8avEjDD7Tf5TrTES) | [GitHub](https://github.com/run-the-docs/kubernetes) |
| React | 10 | [YouTube](https://www.youtube.com/playlist?list=PLdv4kqmXd-vXCpWN_G3CDkmzGpjZIA4K8) | [GitHub](https://github.com/run-the-docs/react) |

**21 videos live** on [Run the Docs](https://www.youtube.com/@RuntheDocs) · [Website](https://run-the-docs.pages.dev/)

## Structure

```
registry/
  registry.json      ← tracked doc URLs with content hashes + episode status
  checker.py         ← weekly change detector, flags episodes that need updating
series/
  kubernetes/        ← episode plan, transcripts, production assets
  react/             ← episode plan, transcripts, production assets
pipeline/
  README.md          ← full pipeline docs (TTS → HTML → render → encode)
  template_tts.py
  template_build.py
  template_render.py
  template_mix.sh
  build_episode.sh
```

## Doc registry

Every tracked source doc has:
- `url` — the canonical source
- `contentHash` — SHA256 of last-fetched content
- `lastChecked` / `lastChanged` — timestamps
- `episodeStatus` — `unplanned` | `planned` | `recorded` | `published`
- `episode` — series, number, title, video file, Discord message ID, publish date

## Running the checker

```bash
python3 registry/checker.py
```

Fetches all tracked URLs, compares content hashes, reports:
1. Docs that changed since last check
2. Published episodes whose source doc changed (need updating)
3. New URLs in any source's `llms.txt`

## Sources tracked

| Source | Docs | llms.txt |
|--------|------|---------|
| OpenClaw | 370 | https://docs.openclaw.ai/llms.txt |
| Hono.js | — | https://hono.dev/llms.txt |
| Manifest | 9 | https://manifest.build/docs/llms.txt |
| Kubernetes | 14 (curated) | kubernetes.io/docs — no llms.txt |
| React | 10 (learn/) | https://react.dev/llms.txt |

## Pipeline

Each episode is built with a 4-step pipeline. See [pipeline/README.md](./pipeline/README.md) for full docs.

1. **TTS** — Kokoro `bm_george` voice → `voice.wav` + `timing.json`
2. **Build** — HTML canvas animation driven by `timing.json`
3. **Render** — Playwright renders frames via `canvas.toDataURL()`
4. **Encode** — ffmpeg mixes video + audio

## Style Guide

See [STYLE_GUIDE.md](./STYLE_GUIDE.md) for brand colors, fonts, animation conventions, and caption standards. All episodes must match.

## Schedule

Checker runs every Monday 09:00 Oslo time via OpenClaw cron.
Notifies #iclaw-e on Discord if anything changed.

# Run the Docs — Engine

The backbone of the Run the Docs channel: doc registry, change detection, and video build pipeline.

## Structure

```
registry/
  registry.json   ← 372+ tracked doc URLs with content hashes + episode status
  checker.py      ← weekly change detector, flags episodes that need updating
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
| Manifest | 1 README | GitHub raw |

## Schedule

Checker runs every Monday 09:00 Oslo time via OpenClaw cron.
Notifies #iclaw-e on Discord if anything changed.

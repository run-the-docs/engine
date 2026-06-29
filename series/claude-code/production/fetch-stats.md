# Routine — fetch video performance stats into the cockpit

Pulls per-video views / likes / comments (+ owner watch-time, retention) for the Run the
Docs channel and surfaces them on the cockpit `/videos` page. Mirrors the publish-status
split: a **token step the operator runs**, then an **orchestrator step that touches no secret**.

## Why it's split (Ops-E HC1 / never-expose-secrets)
`fetch-stats.py` needs the channel OAuth token (Data API + Analytics API). The token lives
only on the Mac Mini (`~/.config/youtube/env.sh`) and is Bearer-only — the operator runs the
fetch; the orchestrator only ingests the resulting JSON (which holds no secret) and writes it
to D1 via the Cloudflare MCP.

> **Token window:** the OAuth refresh token expires ~weekly (Testing-mode consent). Run while
> live, or re-auth first: `python3 ~/.config/youtube/oauth_reauth.py url`.

## 1. [OPERATOR] Fetch on the Mac Mini
```bash
cd <engine>/series/claude-code/production
source ~/.config/youtube/env.sh
python3 fetch-stats.py > /tmp/stats.json     # token is never printed; stats.json has no secret
```
`stats.json` is a flat array, one row per upload: `{youtube_id, as_of, source, views, likes,
comments, watch_time_minutes, avg_view_duration_seconds, avg_view_percentage, impressions,
ctr, subscribers_gained}`. `source` is `analytics-api` when owner metrics came back, else
`data-api`. Hand `/tmp/stats.json` to the orchestrator (paste / attach / commit to a scratch path).

## 2. [ORCHESTRATOR] Map youtube_id -> video_id and UPSERT to D1 (no secret)
The fetch is keyed by `youtube_id`; the D1 `stats` table is keyed by the catalog `video_id`
(`cc-epN`). Map via the `videos` table, then UPSERT each row via the Cloudflare MCP on
database `d298499d-abb8-4009-b184-9bd8145617c1`:

```sql
-- mapping
SELECT id, youtube_id FROM videos WHERE youtube_id IS NOT NULL;
-- one UPSERT per fetched row (INSERT OR REPLACE keyed by (video_id, as_of))
INSERT OR REPLACE INTO stats
  (video_id, youtube_id, as_of, source, views, likes, comments,
   watch_time_minutes, avg_view_duration_seconds, avg_view_percentage,
   impressions, ctr, subscribers_gained)
VALUES (...);
```
Re-uploads: if a fetched `youtube_id` isn't in `videos` (a flop was re-uploaded under a new id),
fix `videos.youtube_id` first so the row maps. Each fetch is a NEW `as_of` snapshot — never
overwrite an older one; the site renders `MAX(as_of)` per video, and history stays for trends.

## 3. [ORCHESTRATOR] Re-derive the site artifact + PR
```bash
# Cloudflare MCP: SELECT the latest snapshot per video (see videos/build-stats.py docstring),
# save the result JSON, then:
python3 videos/build-stats.py <export.json> > videos/stats.json   # in run-the-docs/website
```
Open a website PR with the regenerated `videos/stats.json`; Cloudflare Pages redeploys `/videos`.
run-the-docs/website `main` is unprotected, so squash-merge it directly
(`gh pr merge <n> --repo run-the-docs/website --squash --delete-branch`) — no `--admin` needed.

## Cadence
Best-effort weekly (the YT token is the gate; there is no always-on server-side stats job
because the OAuth token can't live in CI until the consent screen is published to Production —
claude-3 #781 / deadline #25). The public-views half can be refreshed anytime, token-free, from
the channel RSS feed (latest ~15 videos only), which is how the initial 2026-06-24 snapshot was seeded.

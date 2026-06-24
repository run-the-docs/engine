---
title: "Tee-up: grant the YouTube Analytics scope (the view funnel)"
description: "Operator/Ops-E runbook to add yt-analytics.readonly to the Run the Docs channel token so fetch-stats.py can capture impressions / CTR / retention / traffic / subscribers — the metrics that diagnose where views are lost. AI scaffolds; operator runs every token step."
type: runbook
audience: both
updated: 2026-06-24
---

# Grant the YouTube Analytics scope (instrument the view funnel)

## Why this is the #1 growth enabler
Today the channel token only has the **public Data API** (views / likes / comments). That makes the
view *funnel* invisible: we can't see **impressions** (is the algorithm even pushing the Short?),
**swipe-away / first-3s retention** (did viewers bail on the hook?), **average view %**, **traffic
source** (feed vs search vs browse), or **subscribers gained**. Those are exactly the metrics that tell
us *which lever moves views* — without them, every recommendation in `growth-strategy.md` is inference,
not measurement. The single biggest unlock is granting one read-only Analytics scope.

It also lets us settle the open question: is the flat 531–1093 view band an **impressions ceiling**
(algo isn't pushing → topic/seed problem) or a **conversion problem** (it pushes, viewers swipe → hook
problem)? Those need opposite fixes and are currently indistinguishable.

## Cardinal rule (Ops-E HC1 / never-expose-secrets)
The **operator/Ops-E** runs every step that touches the OAuth client secret or the refresh token. The
**AI scaffolds** (this runbook; `fetch-stats.py` is already extended to read the new metrics) and
**resumes** after (ingests the resulting JSON, UPSERTs to D1 via the Cloudflare MCP — no secret). The
token value is Bearer-only and never printed.

> **✅ Done for Run the Docs 2026-06-24** (steps 1, 2, 4, 5 — scope + API-enable + re-auth + verify; retention/watch-time now flow into D1). **Still pending: step 3 (Publish to Production)** — until then the token still expires ~weekly.

## Steps (operator/Ops-E, on the Mac Mini — config lives in `~/.config/youtube/`)

1. **Add the scope to the consent request.** In the re-auth helper's scope list, add
   `https://www.googleapis.com/auth/yt-analytics.readonly` alongside the existing
   `youtube.readonly` / `youtube` scopes (so uploads/scheduling keep working). The list lives in
   `~/.config/youtube/oauth_reauth.py` (the `SCOPES`/`scope` it requests).
2. **Enable the YouTube _Analytics_ API in the project** ⚠️ EASILY MISSED — it's a SEPARATE API from
   the Data API that uploads use, and the scope grant alone is NOT enough. Until it's on you get
   `403 "YouTube Analytics API has not been used in project <N> before or it is disabled"`. One click:
   open `https://console.developers.google.com/apis/api/youtubeanalytics.googleapis.com/overview?project=<PROJECT_ID>`
   (the project id is in the OAuth client; for Run the Docs it's **860780625550**) → **Enable** → wait ~2 min to propagate.
3. **Publish the consent screen to Production** (GCP console → the channel's OAuth client → OAuth
   consent screen → **Publish app**). This also kills the documented **7-day refresh-token expiry**
   (the "Testing"-mode cause) — folding in claude-3 #781 / deadline #25 in the same pass.
4. **Re-run the consent flow** to re-mint the refresh token with the new scope:
   `python3 ~/.config/youtube/oauth_reauth.py url` → open the printed link, approve in your own browser
   (the **"This site can't be reached" page at `localhost:8765` IS success**) → copy the `code=...` value
   from the address bar → `oauth_reauth.py exchange "<code>"` saves the new `YT_REFRESH_TOKEN` (never
   printed). Same flow as the weekly re-auth; codes expire in ~5 min.
5. **Verify (operator runs; output has no secret):**
   ```bash
   source ~/.config/youtube/env.sh
   python3 <engine>/series/claude-code/production/fetch-stats.py > /tmp/stats.json
   # stderr should say "analytics=yes"; rows now carry watch_time_minutes / avg_view_duration_seconds /
   # avg_view_percentage / subscribers_gained. NOTE: impressions + ctr stay null — the Analytics API
   # does NOT expose them for Shorts (the reach call returns empty; expected, not an error).
   ```
   Hand `/tmp/stats.json` to the orchestrator → it UPSERTs the metrics into the rtd-social D1 `stats`
   table (columns already exist, nullable) and refreshes the cockpit — no schema change, no secret.

## What unlocks once this lands
- `fetch-stats.py` populates the 6 funnel metrics per video (it already queries them; they're empty
  only because the scope is missing — it degrades to public-only today).
- The decisive **hook A/B** becomes measurable: re-cut one known-winner topic and read its
  `avg_view_percentage` (retention) directly instead of inferring from raw view counts. (Impressions
  aren't available for Shorts, but retention is the metric that answers the hook question.)
- The recurring weekly token-expiry outage ends (consent screen → Production).

## AI vs operator
- **AI scaffolds:** this runbook; the extended `fetch-stats.py`; the D1 UPSERT + cockpit refresh after.
- **Operator/Ops-E runs (HC1):** the scope edit, the consent-screen publish, the `oauth_reauth.py`
  re-grant, and the verify `fetch-stats.py` run. The AI never sees the token.

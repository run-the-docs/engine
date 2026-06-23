# reconcile-publish-status.py — keep the cockpit's scheduled→posted badges current

Part of the schedule-reconciler (run-the-docs/engine#40 Phase 5). As the Claude Code
drip publishes, this flips each video's rtd-social D1 posting from `scheduled` to
`posted` and stamps the real publish time, so the cockpit Videos badges
(run-the-docs.pages.dev/videos) don't show a live video as "Scheduled".

**Auth-free.** It uses only the channel's public RSS feed — no YouTube OAuth, no secrets.
(Contrast: `series/claude-code/production/backfill-publish-times.py` uses the YT Data API
with OAuth to set the *initial* `status.publishAt` of newly-scheduled videos — that half
is operator/Ops-E. This reconciler handles the public transition the other way.)

## The orchestrator routine (claude-3, via the Cloudflare MCP)

Run on a schedule (daily is plenty for a daily drip — see cadence below):

1. **Read** the D1's scheduled YouTube rows via `mcp__cloudflare__d1_query` on
   `d298499d-abb8-4009-b184-9bd8145617c1`:
   ```sql
   SELECT p.video_id, v.episode, p.url, p.publish_at
   FROM postings p JOIN videos v ON v.id = p.video_id
   WHERE p.platform = 'youtube' AND p.status = 'scheduled';
   ```
2. **Reconcile** — feed that result (raw MCP envelope or a flat list) to the tool:
   ```bash
   python3 tools/reconcile-publish-status.py scheduled.json   # or: ... < scheduled.json
   ```
   It returns `{transitions, still_scheduled, summary}`. Each transition is a video that
   has gone public (now in the RSS) with `new_publish_at` = the real `publishedAt`.
3. **Apply** each transition via the Cloudflare MCP (orchestrator-side; no creds in the tool):
   ```sql
   UPDATE postings SET status='posted', publish_at='<new_publish_at>'
     WHERE platform='youtube' AND video_id='<video_id>' AND status='scheduled';
   UPDATE videos SET youtube_privacy='public' WHERE id='<video_id>' AND youtube_privacy='private';
   ```
4. **Regenerate + PR** — re-run the `videos/build-posted.py` flow in run-the-docs/website
   (MCP query → build-posted.py → `videos/posted.json`) and open a website PR. Until
   infra#365 wires Review-E for run-the-docs, admin-merge it (dispatch-miss fallback).
5. **Alert** — post a one-line summary to Discord `#run-the-docs` (transitions applied, or
   "no changes"). A weekly green heartbeat doubles as a dead-man's-switch.

If `summary.to_post == 0`, stop after step 2 — nothing changed.

## Automated (GitHub Action) — the always-on path

`.github/workflows/reconcile-publish-status.yml` runs the whole routine server-side on a
daily cron (`7 6 * * *`) + `workflow_dispatch`, so it no longer depends on an
orchestrator session being live. It mirrors the steps above but does the D1 read/write
over the Cloudflare **D1 REST `/query` endpoint** (via `tools/reconcile-d1.sh`) instead of
the MCP, then regenerates `videos/posted.json` in run-the-docs/website via a squash-merged
PR (website `main` is unprotected → the merge lands and the existing Pages deploy
republishes it).

**Activation — one operator/Ops-E step.** The workflow is **inert** until its only net-new
secret exists; the guard step skips cleanly (a `::notice::`) until then:

- **`RTD_SOCIAL_D1_TOKEN`** — a Cloudflare API token, scope **Account · D1 · Edit** on the
  dashecorp account `59710bf016d417f860051f1f00b00258` (D1 can't be dashboard-scoped to one
  DB → account-wide D1 is the minimum; make it a **dedicated** token, store only in
  Bitwarden, rotate on a schedule). Provision it onto `run-the-docs/engine` **via OpenTofu**
  in `dashecorp/infra` (`TF_VAR_rtd_social_d1_token` → `github_actions_secret`), **not**
  `gh secret set`. (`REVIEW_E_BOT_PEM`, the org-level review-e-bot App key used for the
  website commit, is already inherited — no provisioning.)

After it lands, smoke-test via **Actions → Reconcile publish status → Run workflow**.

**Safety baked in:** the D1 token is read from the env only and never echoed (no `set -x`
in `reconcile-d1.sh`); UPDATEs are parameterized (`?` + jq-built params); the posted.json
change goes via a PR (never a direct push to main); `concurrency` serializes overlapping
runs; UPDATEs are idempotent (`WHERE status='scheduled'` is a no-op once posted).

## Cadence

The public RSS lists only the ~15 most recent uploads, so run at least once per ~15
publishes. For the current daily drip, a **daily** run is comfortable. A video that has
fallen off the RSS window stays `scheduled` until a YT Data API backfill
(`backfill-publish-times.py`, OAuth) refreshes it — so pair this with an occasional
backfill, or run it daily and you'll never hit the window.

## Why RSS-only (no oembed)

YouTube oembed returns HTTP 401 for many *public* Shorts (a known quirk), which would
mis-flag a live Short as still scheduled. The channel RSS reliably lists public Shorts, so
it is the only trustworthy auth-free "is it public" signal here.

## Scope

Handles `scheduled → posted` (the drip going live). It does **not**: set initial scheduled
times for new videos (needs the OAuth backfill), detect a reschedule of a still-private
video (RSS can't see private state), or touch non-YouTube platforms. Pure core
(`parse_rss` / `vid_of` / `reconcile`) is unit-tested in `test_reconcile_publish_status.py`.

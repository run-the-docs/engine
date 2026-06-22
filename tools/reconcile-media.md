# Media reconciler — `reconcile-media.py`

Keeps the rig-cockpit "Videos" surface (`run-the-docs.pages.dev/videos`, driven by
`run-the-docs/website` `videos/catalog.json`) in sync with what is actually on the
`runthedocs-videos` R2 bucket — so a produced video **auto-appears** and a gap is
**detected**, with no hand edit. Phase 4 of the media-to-cockpit automation
(epic #40).

## What it does

Diffs three sets and emits a report + a reconciled catalogue:

| Set | Source |
|-----|--------|
| **EXPECTED** | every `series/claude-code/production/ep*.lines.json` (skips `published:false`) → keys `claude-ep<ID>-{45,916}.mp4` |
| **ON-R2** | the authenticated `r2_list_objects` result (fed in as JSON) |
| **IN-CATALOG** | `videos/catalog.json` episodes' `v916` |

Drift classes:

- **wiring-drift** — 916 on R2 but catalog `v916` null → **self-heal** (set `v916`).
- **wired-but-404** — catalog `v916` set but 916 gone → **self-heal** (strip `v916`; never leave a broken download).
- **needs-upload** — an expected key is absent on R2 → **alert**. Split into *UPLOAD* (the episode has a catalog card ⇒ already rendered ⇒ just `r2-sync.sh`) vs *RENDER+UPLOAD* (no card ⇒ `build-ep.sh` first).
- **missing-card** — an expected/on-R2 episode has no catalog entry → flag (editorial).

The tool is **pure and secret-free** (no network, no credentials) so it is CI-testable.
`python3 tools/test_reconcile_media.py` covers all four classes.

## How the orchestrator runs it (the runbook)

The reconciler runs **orchestrator-side** (claude-3 has authenticated R2 read via the
Cloudflare MCP and can open `run-the-docs/website` PRs — it never handles the R2 token):

1. `mcp__cloudflare__r2_list_objects(bucket="runthedocs-videos")` (paginate by prefix) → write the listing to `r2.json`.
2. Fetch the live `run-the-docs/website` `videos/catalog.json`.
3. `python3 tools/reconcile-media.py --catalog catalog.json --r2-json r2.json --lines-dir series/claude-code/production --write catalog.healed.json --report report.json`.
4. If wiring changed (`catalog.healed.json` differs): open a `run-the-docs/website` PR `chore: reconcile R2 media catalog (Closes #N)` (file a tracking issue first to satisfy the `Closes #N` norm) → auto-merges via `request-review.yml` → deploys via `deploy.yml`.
5. If `needs-upload` is non-empty: alert Discord `#admin` with the exact `r2-sync.sh` line; after 3 consecutive ticks, raise urgency + a deadline-tracker entry.
6. A weekly **green heartbeat** to `#tasks` (and a deadline-tracker dead-man's-switch) so silence is verified-healthy, not assumed.

`testdata/r2-snapshot.json` is a point-in-time presence snapshot (ep1–16 × {45,916}) used by the demo/tests.

## Phase 5 / follow-ups (tracked in #40)

- Wire the schedule (a `/schedule` routine) + the **live-site** render check (cache-busted fetch of `/videos`, assert each catalog episode renders a visible card + 200 on its video src) — not just the committed catalog.
- ETag/size content-verification (detect partial/stale/wrong-bytes) — needs the catalog to carry `etag`; fold with the `published` flag as a small catalog-schema add.
- Generalise keys to `(series, ep, format)` via a per-series `media.config.json`, and a non-video `artifacts` contract for the Docs/Files surfaces.

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
| **ON-R2** | the authenticated `r2_list_objects` result, **or** the auth-free in-bucket `manifest.json` (`r2.dev/manifest.json`, emitted by `r2-sync.sh` — Phase 2) — both feed `--r2-json` as a `[{key,bytes,etag}]` list |
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

### In-bucket manifest + `published` flag (Phase 2)

`r2-sync.sh`, after a successful sync, (re)emits **`manifest.json`** to the bucket root — a
public listing of every cut actually live on R2 (`{key, bytes, etag}` per object), because
the public r2.dev domain cannot list objects. It always reflects the **full** bucket (probed
from all local cuts), even when only a subset is synced. Step 1 above can therefore be replaced
by an **auth-free** `curl -s r2.dev/manifest.json > r2.json` when the orchestrator can't reach
the authed MCP — the `objects` array is exactly the `--r2-json` shape (and its `etag`/`bytes`
are what the future content-verification will check).

The **`published`** flag on `ep*.lines.json` (default `true` when absent) marks an episode as
*not* expected on R2 — set `published:false` on the deliberate holes (`ep18` unrecorded, `ep25`
skipped) so the reconciler doesn't fire permanent `needs-upload` false-positives for them.

## Phase 5 / follow-ups (tracked in #40)

- Wire the schedule (a `/schedule` routine) + the **live-site** render check (cache-busted fetch of `/videos`, assert each catalog episode renders a visible card + 200 on its video src) — not just the committed catalog.
- ETag/size content-verification (detect partial/stale/wrong-bytes) — needs the catalog to carry `etag`; fold with the `published` flag as a small catalog-schema add.
- Generalise keys to `(series, ep, format)` via a per-series `media.config.json`, and a non-video `artifacts` contract for the Docs/Files surfaces.

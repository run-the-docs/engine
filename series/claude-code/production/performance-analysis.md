---
title: "Claude Code video performance — analysis"
description: "Performance analysis of the Run the Docs Claude Code Shorts catalogue (17 published) — view/like distribution, what works, the Ep15 anomaly, and recommendations. Snapshot 2026-06-24."
updated: 2026-06-24
---

# Claude Code video performance — analysis (2026-06-24)

## TL;DR

- **The CC series works; the format is validated.** 17 Claude Code videos pulled 12,949 views vs the 66-video legacy K8s/React back-catalogue's 1,645 — ~7.9x more total views from a quarter of the videos, and ~219x on per-video median (876 vs 4). Keep mining `code.claude.com/docs` 1:1; do not revive legacy.
- **Reach is healthy and consistent.** Excluding two outliers, the 14 mature episodes sit in a tight 531–1093 view band (mean ~862, median ~876) — unusually low variance for a small-channel Shorts run, and above the typical 50–500 first-48h band for sub-1k-subscriber channels.
- **Engagement is the weak spot.** Blended like-rate is 0.79% (102 likes / 12,938 views), roughly 4–7x below the 3–6% "healthy" Shorts band. Reach is solved; the deliberate-like payoff is not.
- **Single biggest action: fix Ep15.** `/code-review` has 11 views at 4 days old while every neighbour did 500–1100 — a delivery/visibility failure, not weak content. Recovering it to the ~820 median is a ~+800-view swing (~6% of the entire series total) on a proven topic class. Verify in Studio first, then fix-in-place or re-upload.

## The numbers

| Ep | Topic | Published | Views | Likes | Likes/View% |
|----|-------|-----------|------:|------:|------------:|
| Ep16 | Interview-first (AskUserQuestion) | 06-21 | 1093 | 10 | 0.91% |
| Ep17 | /init writes CLAUDE.md | 06-22 | 1057 | 3 | 0.28% |
| Ep3 | Give Claude a memory (CLAUDE.md) | 06-07 | 1018 | 15 | 1.47% |
| Ep2 | The agentic loop | 06-07 | 1006 | 5 | 0.50% |
| Ep13 | Headless mode, one line | 06-18 | 1000 | 4 | 0.40% |
| Ep6 | Undo anything (rewind) | 06-11 | 945 | 7 | 0.74% |
| Ep8 | Auto-format on edit (hooks) | 06-13 | 931 | 7 | 0.75% |
| Ep4 | Plan mode | 06-10 | 815 | 6 | 0.74% |
| Ep12 | Session resume | 06-17 | 820 | 6 | 0.73% |
| Ep11 | Don't lose a long session (context) | 06-16 | 754 | 12 | 1.59% |
| Ep7 | Subagents in parallel | 06-12 | 718 | 7 | 0.97% |
| Ep1 | Your first session (overview) | 06-07 | 711 | 4 | 0.56% |
| Ep10 | Reusable skills | 06-15 | 671 | 9 | 1.34% |
| Ep14 | @ file references | 06-19 | 531 | 3 | 0.56% |
| Ep5 | Slash commands (re-upload, ~1d old) | 06-23 | 509 | 1 | 0.20% |
| fable5 | Fable 5 model fixing a real bug | 06-09 | 359 | 3 | 0.84% |
| Ep15 | /code-review (anomaly, 4d old) | 06-20 | 11 | 2 | 18.18% |

CC totals: **12,949 views across 17, mean ~762, median ~815** (clean set excluding Ep5 re-upload + Ep15 anomaly: mean ~865, median ~876). **CC vs legacy: 17 CC videos = 12,949 views vs 66 legacy videos = 1,645 — ~7.9x total, ~219x per-video median (876 vs 4).** Legacy's single best video (477) is below the CC series' worst mature episode (531).

## What's working

- **CLAUDE.md is the strongest theme.** Both CLAUDE.md-anchored episodes over-perform: Ep3 "Give Claude a memory" (1018, and the series' top liker at 15) and Ep17 "/init writes CLAUDE.md" (1057) — each ~18–22% above the ~865 clean mean. The persistent-memory benefit is the recurring winning hook.
- **Outcome/benefit-led titles beat feature-name titles.** Four of the top five clear 1000 views and all promise a result or vivid capability: Ep16 "Interview-first" (1093), Ep17 "/init writes CLAUDE.md" (1057), Ep3 "Give Claude a memory" (1018), Ep2 "The agentic loop" (1006), Ep13 "Headless mode, one line" (1000). Where there's an API name (AskUserQuestion) it sits in parentheses; the human benefit leads.
- **Concrete/quantified promises out-pull abstractions.** "Headless mode, one line" (1000) sells a quantified payoff; "/init writes CLAUDE.md" (1057) names the exact command and the exact artifact. Generic category framings land 15–23% below the clean mean: "Your first session (overview)" (711), "Reusable skills" (671).
- **Coined terms work when paired with a familiar concept.** "The agentic loop" (1006) and "Interview-first" (1093) introduce a memorable named concept the title implicitly explains — both top-five, beating undifferentiated nouns like "Slash commands" / "Reusable skills."
- **Reach trend is flat-to-up, not decaying.** Chronological trend across the 15 core episodes is +9.5 views/video; first-half mean ~796 vs second-half ~857. The two most recent full-cycle episodes (Ep16 1093, Ep17 1057) are among the four best, so there's no daily-drip fatigue.

## What's not

**Ep15 `/code-review` — almost certainly a distribution/visibility failure, not content.** 11 views at 4 days old, while chronological neighbours did 500–1100 (Ep14 531 / Ep16 1093), is a step-function break in delivery, not a gradient. The tell: 2 likes on 11 views = 18.18% L/V vs the channel's ~0.79% norm — a ~23x ratio anomaly that is mathematically incompatible with public discovery. That shape (a few insider/creator likes, near-zero organic impressions) points to a video that was effectively never served: stuck Private/Unlisted, mis-flagged age-restricted / not-made-for-kids, region-restricted, Shorts-ineligible (parsed as long-form, copyright/music claim suppressing the Shorts shelf), or simply never surfaced in the feed. Its topic class is the channel's *strongest* (the other command video, Ep17 /init, pulled 1057), so there is no content reason for 11 views.

**How to confirm (ordered, in YouTube Studio):**
1. **Reach > Impressions** — if impressions are ~0–50, the video was never served (delivery problem), not rejected by viewers.
2. **Visibility = Public** and check the Restrictions column for copyright / blocked-regions / age-restriction flags.
3. Confirm it renders as a **Short** (vertical, ≤3min, `#Shorts`) and appears in the channel's Shorts shelf, not as a regular video.
4. **Traffic sources** — absence of a "Shorts feed" source confirms it never entered the feed.
5. Load the watch URL **logged-out/incognito** to verify public reachability.

**The genuine laggards (clean-set, below the ~820 median):**
- **fable5 "Fable 5 model fixing a real bug" (359)** — the lowest non-anomaly, ~58% below the clean mean. It breaks the 1:1 feature-to-docs format (a model announcement, not a docs feature) — a format problem, not a title problem.
- **Ep14 "@ file references" (531)** — second-lowest, ~39% below the clean mean. Pure-syntax title with no benefit verb; syntax-led titles under-perform outcome-led ones by roughly 2x here (531 vs the ~1050 CLAUDE.md/interview tier).
- **Ep1 "Your first session (overview)" (711)** and **Ep10 "Reusable skills" (671)** — generic category framings with no hook.
- Note: **Ep5 "Slash commands" (509)** is a ~1-day-old re-upload of a prior flop (still ramping), so its count is age/history-driven, not a clean topic signal. A bare command name ("Slash commands") is weaker than command+outcome ("/init writes CLAUDE.md").

## Engagement

- **Baseline like-rate is 0.79–0.81%** (102 likes / 12,938 views blended; clean-set per-episode median 0.74%, mean 0.83%, range 0.28%–1.59%). Every episode is under half the 3–6% healthy Shorts floor — this is the clearest growth lever, and it's a call-to-action/payoff problem, not a reach problem.
- **Engagement is decoupled from reach.** Views↔likes correlation across the 15-episode normal set is only **0.320 (weak)**. The four >1000-view episodes span a 5x engagement gap (Ep3 1.47% vs Ep17 0.28%) — impressions don't predict the tap.
- **Persistence/pain-relief topics convert best.** Top like-rates: Ep11 "Don't lose a long session" 1.59% (12/754), Ep3 CLAUDE.md 1.47% (15/1018), Ep10 "Reusable skills" 1.34% (9/671) — each ~2x the median, despite mid-pack views. Loss-aversion / problem-first framing ("Don't lose…", "Undo anything", "Give Claude a memory") punches above its view weight.
- **High-reach, low-resonance cluster:** Ep17 /init 0.28% (3/1057), Ep13 headless 0.40% (4/1000), Ep2 agentic loop 0.50% (5/1006) — all ~1000+ views, all bottom-tier likes. They win the algorithm but don't earn the deliberate like. Notably the *manual* "give Claude a memory" framing (Ep3, 1.47%) resonates far more than the *mechanical* "/init writes the file for you" framing (Ep17, 0.28%) of the same underlying feature.
- **Comments are effectively null:** 2 total across all 17 episodes (both on Ep2), 16 of 17 at zero. There is no conversational signal to mine — only the like tap.

## Recommendations

1. **Fix Ep15 first — highest-EV action available.** Verify in Studio (impressions → visibility → Shorts-eligibility → traffic source → incognito load). If any flag is found, fix-in-place. Only if it's clean-but-dead, delete and re-upload (the Ep5 precedent recovered to 509 in ~1 day) at a 13/16/19 UTC slot with a fresh thumbnail/first-frame, and delete the dead original to avoid a duplicate. Upside: ~+800 views (~6% of series total) on a proven topic class.
2. **Rewrite the laggard titles to verb + benefit:**
   - Ep14 "@ file references" → **"Stop pasting code — just @ the file"**
   - Ep10 "Reusable skills" → **"Teach Claude a skill once, reuse it forever"**
   - Ep7 "Subagents in parallel" → **"Run 3 Claudes at once (subagents)"**
   - Ep1 "Your first session (overview)" → **"Your first 30 seconds in Claude Code"**
   - Pattern to apply everywhere: imply an outcome/payoff or a concrete artifact, the way the four winners do ("writes CLAUDE.md", "one line", "a memory").
3. **Topic priorities for the scheduled batch.** Front-load the named-command Shorts that match the proven over-performers (Ep17 /init 1057, Ep16 AskUserQuestion 1093): **ep9 MCP** (high search intent), **ep19 /goal**, **ep21 /sandbox**, **ep24 ! shell**, **ep23 /statusline**. Hold the abstract/meta titles — **ep28 output-styles, ep29 think-harder, ep30 CLAUDE.md-mid-chat** — until they get a benefit-led title rewrite (they mirror the soft performers Ep14 531 / Ep10 671).
4. **Steer the editorial mix toward durable-workflow topics for engagement.** Context, memory, skills, resume convert viewers to likers ~4–5x better than the headless/init cluster. Lean future topics that way; ep9 MCP and ep30 "CLAUDE.md mid-chat" resemble the high-engagement cluster, so frame them around the felt pain, not the mechanism.
5. **Strengthen the like CTA / payoff.** The 0.79% like-rate is the headline weakness. Add an explicit payoff/ask in the final 3–5s (especially on high-view, low-like topics like headless/init) and frame even mechanical features around a recognizable pain. Test it on the next batch and watch L/V move.
6. **Keep the cadence; don't increase volume.** The daily-weekday 13/16/19 UTC drip is producing a tight, healthy band — the floor is content quality (the only sub-500 mature item is the off-format fable5), not frequency. Reserve the 3rd daily slot (19 UTC) for re-uploads/title-fixes of laggards rather than always-new abstract topics — recycling a fixed laggard is higher-EV than a brand-new abstract one given the band is stable.
7. **Keep mining docs; retire legacy.** 30+ command/feature docs pages remain unmade against the full `code.claude.com/docs` surface. The runway is in continuing the 1:1 docs-feature format, not resurrecting a series that medians 4 views.

## Caveats

- **Single snapshot (2026-06-24), age-confounded.** Views/likes are cumulative lifetime totals captured once, not a time series. Episodes range from ~1 day old (Ep5) and 4 days (Ep15) to 17+ days (Ep1–3), so cross-episode comparisons mix very different exposure windows. No views-per-day normalization was possible; newer high-view episodes (Ep16/Ep17) are arguably even stronger given less time.
- **Views-only data.** No impressions, CTR, average-view-duration, retention, swipe-away, shares, or saves. These are exactly the metrics that would *confirm* the Ep15 diagnosis and explain the low like-rate — all Ep15 root-cause statements are inferences from view/like shape, not verified in Studio. Likes/view is a resonance proxy, not measured attention.
- **Small-N, noisy engagement.** Likes are single-digit-to-15 per episode (102 total); a swing of 1–3 likes moves a ratio materially. Per-episode L/V differences under ~0.3pp are noise; treat rankings as directional, not significant. The 0.79% aggregate is the only reliable engagement number. Ep15's 18.18% is a tiny-denominator artifact used only as a directional non-organic signal.
- **Unknown subscriber count.** The "over-performing its tier" framing depends on sub count; if the channel has several thousand subs, these numbers are merely on-par rather than above-band.
- **Segregated entries.** fable5 (off-format model demo) and Ep5 (re-upload of a flop) were excluded from core stats; folding them back in shifts the means/medians. Means/medians depend on which exclusions apply — all percent-vs-mean claims use the ~865 clean figure.
- **Confounded causation.** Title, topic, format, time-slot (13/16/19 UTC), thumbnail, and any external promotion are fully entangled — no A/B, no CTR. Title-rewrite suggestions and scheduled-episode win/flop predictions are untested priors to test, not forecasts. Benchmarks are blended third-party industry figures, not dev-tooling-niche-specific. The CC-vs-legacy gap also conflates topic search-demand and channel/algorithm era, not solely format quality.
- **Comments null.** 2 total comments cannot distinguish "no engagement" from "comments disabled" or "audience doesn't comment on Shorts" without account-side settings. Scheduled episodes have zero views and cannot be assessed; the published list is non-contiguous (Ep9/18/20/22/25/27 are gaps).

---
title: "How to get more views — Claude Code Shorts growth playbook"
description: "Forward-looking growth strategy for the Run the Docs Claude Code Shorts: the view funnel + data gap, the first-3-seconds hook, discoverability, distribution, audience/cross-platform, and a 2-week test plan. 2026-06-24."
updated: 2026-06-24
---

# How to get more views — Claude Code Shorts growth playbook (2026-06-24)

## TL;DR — the 3 highest-leverage moves (ranked, with the single biggest first)

1. **Kill the 2-3s branded intro card. Open frame 1 on the payoff.** Every episode burns its single most valuable asset — the swipe-or-stay window where 50-60% of all drop-off happens — on a static "RUN THE DOCS / EP N" wordmark. The first frame is the de-facto thumbnail and the hook, and right now it's channel branding the viewer hasn't earned a reason to care about. Open cold on the terminal mid-command or on the result (the diff, the generated file, the green test), demote the wordmark to a persistent small corner bug present from frame 1, and put the title/command card at ~5-8s after the first payoff. This is the one change most likely to lift reach across the *entire* series, because the flat 531-1093 view band is the signature of a uniform per-video penalty, not topic variance.

2. **Put a sound-off-readable text hook + the named command on frame 1, and start captions at 0:00.** Reclaim the search-intent and curiosity value the channel already proves works (named commands /init 1057, CLAUDE.md 1018) but currently spends on the throwaway intro window. Big top-third caption in the very first frame, matching the first spoken TTS line, e.g. "/init writes your whole CLAUDE.md". Burned-in captions from frame 1 add a documented 15-25% retention for muted autoplay.

3. **Instrument the funnel — grant the YouTube Analytics scope.** Every claim in this playbook (including #1 and #2) is *inference* from view/like shape + format + Shorts best practice, because only the public Data API (views/likes/comments) is granted. The decisive missing metric is "Viewed vs Swiped Away" / first-3s retention. The scope is self-serve for your own channel (no Google verification project), the D1 plumbing is ~80% built (empty nullable stats columns + a read-only fetcher already degrading to public-only). Without it you optimise blind; with it you confirm the intro-card penalty in one A/B cycle.

Moves 1 and 2 are low-cost, reversible, and structural (bake into the render template). Move 3 unblocks measurement. Do all three this week.

## The funnel & the data gap (why we must instrument first; what to capture)

Views = Impressions × viewed-rate × watch-quality, then the algorithm re-injects winners. Today only the bottom of that chain is visible. The 531-1093 band could be an **impressions ceiling** (algo isn't pushing — a topic/distribution problem) OR a **conversion problem** (it IS pushing but viewers swipe — a hook/first-frame problem). Those need *opposite* fixes and are currently indistinguishable. That ambiguity is the binding constraint on iteration speed.

The scope is a one-time OAuth re-grant on the channel's existing client at `~/.config/youtube/`: add `yt-analytics.readonly`, re-run the consent flow to re-mint the refresh token, and — in the same pass — publish the consent screen from "Testing" to "Production" to kill the documented 7-day refresh-token expiry. **Operator/Ops-E owns the token; agents must not handle it.**

Six metrics to capture per video, and what each decides:

| Metric | Decides |
|---|---|
| Impressions / "shown in feed" | Is the algo even pushing? Low impressions + decent viewed-% = topic/seed problem, not hook. |
| Swipe-away % first ~3s (hook retention) | THE diagnostic for this format. Target hold >80% past 3s; >40% swipe = hook broken. |
| Avg view duration + avg % viewed | Master distribution signal. Target >70% viewed / >55% AVD for sub-30s. |
| Traffic source (feed/browse/search/channel) | Distinguishes algorithmic reach from search-intent. Decides titles-for-search vs hooks-for-feed. |
| Returning vs new viewers | Only metric predicting channel longevity vs one-hit Shorts. Proves compounding. |
| Likes/comments (already visible) | Engagement proxy; 0.79% like-rate + ~2 comments corroborates weak retention. |

Until the scope lands, run the intro-card recut as an A/B and read the delta off public view counts — a clear mean/median lift after a held-topic recut corroborates the hypothesis without the API.

## Lever 1: the first 3 seconds (hook/retention — likely the biggest reach lever)

The intro card is a hook problem AND a topic problem combined: the channel's proven winners (named commands, outcome-led phrasing) are visible *during the throwaway window* and then disappear right when content starts. Best-practice is blunt — slow builds are "death for Shorts," and creators report "doubling retention by cutting the first 5 seconds." A static logo card spends the entire swipe decision on branding.

Actions, in order of leverage:

- **Open frame 1 on the action/payoff** — terminal mid-command or the result. Brand becomes a persistent corner bug, never owning a frame. Net brand exposure stays equal; the dead 2-3s disappears.
- **Frame-1 text hook, sound-off readable**, using a proven winner: outcome/benefit + named command (e.g. "Claude Code remembers your project — CLAUDE.md").
- **Captions at 0:00.** First words on screen = the hook line, matching TTS.
- **Tighten to 15-22s** for single-feature tips (the 15-20s / 85-95% retention band). Lead with the result, then show the command. Re-cut, don't re-shoot — trim the front. Target completion >60% for sub-30s.
- **Engineer the loop.** End on a frame that conceptually rejoins the open (or end mid-action) so the brain seeks closure and replays. Avoid a hard branded end-card that breaks the seam — even a 10% replay rate materially boosts distribution, and none of the current episodes appear engineered to loop.

Like-rate and comments are *downstream* of this — viewers who bail in 2s never reach the like/comment decision. Fix the open first; engagement should partially self-correct.

## Lever 2: discoverability (titles, first-frame-as-thumbnail, search-intent topics, hashtags)

Named-command topics win via search intent, and it's visible in your own data: /init (1057) and CLAUDE.md (1018) are exact strings a dev types; laggards @-file-refs (531) and slash-commands (509) are descriptive, not queries. YouTube now has a dedicated Shorts filter in search, and coding Shorts over-index on **saves** (devs bookmark commands) — a strong amplification signal. Titles/descriptions/transcript/on-screen text are all indexed; hashtags matter less than NLP reads of the title.

- **Fixed title formula:** outcome + named command, ≤60 chars (survives search truncation), command verbatim and early. E.g. "/agents — run an AI team in one terminal", "Stop re-explaining your repo: CLAUDE.md", "Headless Claude Code in your CI: claude -p".
- **Pin a custom 9:16 cover frame** ("Select Cover"): two high-contrast colours (orange ink on dark terminal), command name + outcome in ≤4 words. This is the thumbnail in search results and the /videos gallery even when the in-feed first frame changes.
- **Say the command in the first spoken line** and show it as on-screen text in the first 2s — both audio and on-screen text are indexed. Open with the answer, not "Today we'll look at…".
- **Description + hashtag template:** line 1 = command + one-line benefit + link to the matching code.claude.com/docs page (reinforces the 1:1 mapping). Hashtags: `#Shorts` first, then exactly `#ClaudeCode #AIcoding #DevTools` + one topic tag (e.g. `#MCP`). Never exceed ~5 useful tags or 15 total (over 15 = all ignored). First 3 render as clickable links.
- **Mine the docs for high-demand named commands** you haven't covered, ranked by "would a dev literally type this into search": /agents, /hooks, /mcp, /resume, /context, /compact, /usage, headless (claude -p), plan mode, checkpointing/rewind, output styles, statusline, skills, GitHub Actions code review, worktrees, auto memory. Avoid descriptive non-query topics (the laggard class).
- **Double down on the CLAUDE.md/memory + outcome cluster** — it's your proven winner. Make it a mini-series, not one-offs.

Treat Ep15 /code-review (delivery-failed, re-uploaded) as a fresh test, not a comp. Off-format (fable5 359) and re-uploads (509) underperform — the algorithm rewards format consistency.

## Lever 3: distribution, cadence & packaging

The band is a **seed-test ceiling**, not a schedule problem: every Short gets a similar-sized seed audience and none graduate to the snowball tier. A flat band across 17 uploads means the seed test fails at roughly the same point every time — so volume or slot changes alone won't lift the ceiling; they buy more identical tests. The intro-card fix (Lever 1) is the prime ceiling cause.

- **Lock a single daily slot at 13:00-14:00 UTC for ~3 weeks**, then iterate. Stop rotating 13/16/19 — rotation fragments the audience-habit signal and makes the slot impossible to learn from the only metric you have (views). 13-14 UTC catches US-East morning + EU afternoon. *No-op if* traffic-source data later shows views come overwhelmingly from search/browse (evergreen) rather than feed.
- **Test 2/day for 2 weeks — but only after the cold-open recut is live, spaced 5-6h apart** (e.g. 13 + 19 UTC) so they don't share a seed-audience window and cannibalise. YouTube won't promote two of your Shorts simultaneously; doubling at-bats only compounds if each is an independent shot that can clear the seed test — which requires the hook fix first.
- **Build 4-5 themed Shorts playlists and pin the top 5** (Ep16/17/3/2/13): "Memory & Context (CLAUDE.md)", "Slash Commands", "Agentic Loop", "Headless & CI". Lead each playlist with a known winner so the strong video pulls viewers into the next. This converts single-Short sessions into multi-video sessions — the one distribution move that raises views-per-viewer without needing the algorithm to widen reach, and it has no downside. Do it regardless of data.
- **Cadence consistency is already healthy** ("no daily-drip fatigue," flat-to-slightly-up). The weekday drip is working; don't touch frequency before fixing the hook.

## Lever 4: audience growth & cross-platform (subs, LinkedIn/TikTok/Reels, CTAs)

Subs seed the initial-velocity pool every new Short is tested against — the one place audience work feeds back into more views. The outro is currently a passive brand bumper ("Follow for a fresh Claude Code tip every day") with no named SUBSCRIBE action and no reason-to-sub at the satisfaction peak.

- **Turn on the three dark platforms this week — TikTok, Reels, X — using assets you already render.** The 9:16 cut and per-episode posting-kit copy already exist; the only missing step is the upload. ~3× the surfaces for zero new production, each with its own cold-start independent of YouTube. Judge each platform on its OWN view/follow count (you can't attribute cross-post views to YouTube subs without traffic-source data).
- **Rewrite the outro into an explicit subscribe ask at the payoff:** "That's one. Subscribe — I ship one Claude Code command every weekday," + a visible SUBSCRIBE text element in the final ~3s. Both the spoken line AND the hardcoded footer string in `make_assets_45.py` / `make_assets_916.py` must change together — editing narration alone is invisible on-screen because compose suppresses the lines.json closing caption.
- **Re-edit the LinkedIn cut for LinkedIn, and switch it to 9:16.** Replace the brand-card open with a first-line business-outcome hook in the post body ("Code review used to eat my Friday. One Claude Code command now does the first pass:"); use the 9:16 cut (LinkedIn boosts vertical over 4:5 in 2026 — you may be posting the deprioritised ratio); keep the YouTube link in the first comment (already correct). This is the surface most aligned to a fractional-CTO dev audience and is currently mis-formatted.
- **Seed one pinned comment + question per episode, reply within 2h.** Pin a comment that links the next step/playlist and asks a concrete question ("What's your CLAUDE.md look like?"). Comments/shares now drive Shorts ranking; near-zero comments (2 total) means no comment-driven distribution. This is the cheapest *measurable* lever — comments and like-rate are in the public Data API.
- **Convert ~1 in 3 episodes to a cliffhanger funnel** on multi-part topics ("…the second gotcha is the one that bites everyone — it's in the pinned playlist"). Cliffhangers convert better than complete-answer Shorts and pull toward a "next."
- **Add a Subscribe/Follow CTA to the /videos gallery and set the channel-page trailer + "one command a day" tagline** — channel-page visitors are high-intent.

## A 2-week test plan (what to change, what to measure, how to attribute)

Native A/B does NOT work on Shorts — attribution must come from one-variable-at-a-time swaps + the re-upload-as-fresh-cohort tactic (already used on Ep5/Ep15). Hold topic-class constant so a lift isolates the variable. Log every episode: ep#, topic-class, title-style, hook-style, length-s, slot-UTC, then the funnel metrics at 24h/72h/7d.

- **Day 0 (operator/Ops-E):** Grant `yt-analytics.readonly`, re-mint token, publish consent screen to Production. Extend the existing `fetch-stats.py` to UPSERT the 6 metrics into the D1 `stats` table (no new schema). Verify with one `reports.query`.
- **Days 1-3 — the decisive test:** Re-upload one KNOWN-WINNER topic (CLAUDE.md/memory or a named command) as a NEW video, **hook-first**: frame 1 = terminal + outcome caption, wordmark demoted to a ≤0.5s corner bug or moved to the end, ~18s. Hold thumbnail/title/topic constant vs the original. **Decision rule:** if first-3s swipe-away drops >10 points or % viewed rises above ~70%, make hook-first the permanent format and bake it into the render template (4:5 + 9:16 dual-format, /videos + LinkedIn inherit it).
- **Days 1-14 — one variable per week on the daily drip:** Wk1 hook-first vs intro-card; Wk2 outcome-led vs feature-name title; Wk3 fixed slot attribution (13 vs prior rotation); Wk4 length (~22s vs ~33s). Compare cohorts on impressions-normalised % viewed, NOT raw views.
- **In parallel:** turn on TikTok/Reels/X; build the themed playlists + pins (no-regret, do immediately); rewrite the outro CTA; seed pinned comments.
- **Go/no-go thresholds:** first-3s swipe >40% → re-cut hook-first. Avg viewed <55% → pacing/length problem. Impressions flat but % viewed high → distribution/topic problem, lean into search-intent titles + cross-post, don't touch the hook. Returning-viewer % ~0 after 4 weeks → add subscribe/next-episode CTA + series hook.
- **Reconcile the two reach hypotheses in week 1:** pull traffic-source for the 5 winners (Ep16/17/3/2/13) vs 3 laggards. Winners over-indexing on SEARCH → invest in named-command/outcome titles (evergreen, compounding). Winners over-indexing on FEED → the intro-card test is decisive and hook is the lever.

## Caveats (the data gap; small-N; inference vs measured)

- **Everything here is inference, not measurement.** Only the public Data API (views/likes/comments) is granted — NO impressions, NO swipe-through/CTR, NO average-view-duration or retention curve, NO traffic sources, NO subscriber count. The intro-card-suppresses-reach call is a strong format-based inference (convergent 2026 Shorts best practice + the flat 531-1093 band that looks like a uniform per-video ceiling), but it is not proven. The single decisive missing metric is "Viewed vs Swiped Away" / first-3s retention.
- **Direction is medium-high confidence; magnitude is low.** If the held-topic A/B shows no lift, the limiter is elsewhere (thumbnail/title CTR or topic-market fit) and priorities shift to those levers. The recut is low-cost and reversible, so it's the right first bet even under the gap.
- **n=17 with confounds (video age, topic) means early swap cohorts will be noisy.** Treat week-1 results as directional; require a repeat before locking any format change.
- **Cross-post attribution is impossible without traffic-source data** — judge TikTok/Reels/X on their own native counts, not on YouTube sub lift.
- **The fastest confidence-raiser by far is granting the Analytics scope** (self-serve, ~15 min, no Google verification project). It turns this entire playbook from a best-practice bet into a measured result within one week.

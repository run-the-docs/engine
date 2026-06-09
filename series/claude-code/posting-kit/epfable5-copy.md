# Fable 5 — Claude Code's most powerful model, fixing a real bug

**Suggested slot:** Tuesday 09:00 CET (news-led — ride the launch window; free on Pro/Max/Team through June 22).

**Files:**
- `fable5-linkedin-4x5.mp4` (1080×1350 — LinkedIn + X native upload)
- `fable5-vertical-9x16.mp4` (1080×1920 — TikTok / YouTube Shorts / Reels)
- `fable5-cover.jpg` (thumbnail)

---

## LinkedIn (upload the 4:5 natively — NO link in body)

Claude Code just got its most powerful model, and I put it straight to work fixing a real bug in my terminal.

Anthropic launched **Claude Fable 5** today — they call it their most capable model, available in the Claude API and in Claude Code immediately. Their headline example is wild: Anthropic says Stripe "compressed months of engineering into days," including a 50-million-line Ruby migration in a single day. And they say the longer and more complex the task, the bigger Fable 5's lead over their other models.

I wanted something smaller and honest, so I gave it a genuinely sneaky bug: a `business_days()` counter with a one-line off-by-one. The docstring promises an *inclusive* date range, but the loop quietly stops a day early, so a full Mon–Fri week returns 4 instead of 5. The kind of bug that makes you blame the weekend logic for an hour.

I launched `claude --model claude-fable-5`, pointed it at the failing test, and asked for the root cause. It didn't guess at the weekday check — it traced the loop boundary, spotted that the inclusive end day was never counted, changed `<` to `<=`, and reran the test. Green.

My honest take: it's one bounded fix, not the 50M-line claim — but the *diagnosis* was the impressive part. It read intent from the docstring instead of pattern-matching the symptom. One more thing I appreciate: Anthropic says in high-risk domains (cyber, bio, chem) Fable 5 doesn't refuse — it falls back to Opus 4.8, with >95% of sessions involving no fallback at all. It's also free on Pro, Max, Team and Enterprise until June 22, then credit-metered ($10 / $50 per million in/out).

If a model can read your *intent* and not just your symptom — what's the first real bug you'd hand it?

**First comment:**
> Watch it: [YouTube link]
> I write up one Claude Code tip every weekday — [newsletter link]
> I am Stig; I build dev/AI tooling at Invotek.

#ClaudeCode #Fable5 #AICoding #DeveloperTools #Anthropic

---

## TikTok / Instagram Reels

claude code just shipped its most powerful model and i made it earn it.

anthropic calls **fable 5** their most capable model ever. so i handed it a nasty off-by-one — a business-days counter that drops the last day of an inclusive range. full work week returns 4 instead of 5.

`claude --model claude-fable-5`, point it at the failing test, ask for the root cause. it didn't blame the weekend logic — it traced the loop boundary, flipped `<` to `<=`, reran the test, green.

honest version: one small fix, not anthropic's 50-million-line migration claim. but it read the *intent* from the docstring. that's the part that got me.

follow for a Claude Code tip a day.

#claudecode #fable5 #aicoding #coding #developer #anthropic

---

## YouTube Shorts

**Title:** Anthropic's new Fable 5 fixed a real bug in my terminal

**Description:**
I gave Anthropic's brand-new Claude Fable 5 a subtle off-by-one in my terminal — an inclusive date range that quietly drops its last day. It traced the loop boundary, fixed it, and the test went green.
Honest framing: one small bug-fix, not Anthropic's 50M-line migration claim — but the diagnosis was sharp.

[newsletter link]

Run the Docs — Claude Code series. A project by Invotek.

#Shorts #ClaudeCode #Fable5 #AICoding

---

## X / Twitter

Claude Code just got its most powerful model — so I made it fix a real bug.

I handed Claude Fable 5 a sneaky off-by-one: a business-days counter that drops the last day of an inclusive range (full week = 4, not 5). It didn't blame the weekend logic — it traced the loop boundary, flipped `<` to `<=`, reran the test. Green.

Anthropic says it's their most capable model, and the longer the task the bigger its lead. Free on Pro till June 22.

Honest take + the run (link in reply).

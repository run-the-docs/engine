#!/usr/bin/env python3
import os, json, textwrap
KIT=os.path.expanduser("~/Desktop/RunTheDocs-ClaudeCode")
EPS=[
 dict(n=1, title="Your first Claude Code session", topic="From install to first answer — and a spotted bug",
   date="Mon 2026-06-08", time="09:00 CET",
   li_hook="Open your repo, ask a question, get an answer. No setup.",
   li_body="""Most "AI for devs" tools want config, indexing, an account dance.

Claude Code skips all of it.

In this 30s demo:
- Launch `claude` inside any repo
- Ask in plain English: "what does this service do?"
- It reads your actual code and answers
- It even flags a bug — read-only, nothing touched

No onboarding. No pasting files into a chat box. It just works where your code already lives.

Ep 1 of Run the Docs: your first session, start to answer.""",
   li_cta="Watch the 30s run, then tell me: what's the first question you'd ask about a repo you inherited?",
   li_first="Tip: that read-only first pass is the safest way to onboard onto unfamiliar code. Ask it to map the entry points and data flow before you change a single line — you get a mental model in minutes, with zero risk of edits.",
   li_tags="#ClaudeCode #DeveloperTools #AICoding #SoftwareEngineering #DevWorkflow",
   tiktok="It found a bug I never asked it to look for. I opened a normal repo, typed claude, and asked one plain-English question about slugify.py. The answer came back with a real edge case in the code. No config, no setup, fully read-only. This is the entry point most devs skip. Would you let a tool read your code before it ever touches it?",
   tiktok_tags="#claudecode #aicoding #devtok #coding #programming #softwareengineering",
   yt_title="Your First Claude Code Session: Ask in Plain English, It Spots a Real Bug",
   yt_desc="Open any repo, type claude, ask a question in plain English, get an answer. In this first session it reads slugify.py and flags a real bug. Read-only, zero setup.\n\nRun the Docs — Claude Code series.\nDocs: <docs-link>\n#Shorts #ClaudeCode #AICoding #DeveloperTools #Programming",
   x="Typed `claude` in a normal repo, asked one plain-English question about slugify.py, and it flagged a real bug I never pointed at. No config. Read-only. That's the entire first session.\n\n#claudecode #aicoding"),
 dict(n=2, title="The agentic loop", topic="Fix a failing test, hands-free",
   date="Tue 2026-06-09", time="09:00 CET",
   li_hook="A failing test, fixed before you finish your coffee.",
   li_body="""You describe the task: "fix the failing test."

Claude Code runs the loop:
- Reads the code to understand what broke
- Proposes the edit as a diff you approve
- Runs the tests to confirm green

No copy-paste. No context-switching. No black box.

Every change lands as a diff you sign off on, so you stay in control while the busywork disappears. That's the agentic loop: read, edit, verify, repeat.

30 seconds, in your own terminal.""",
   li_cta="Watch the loop run end to end in the clip. What's the first task you'd hand it: a flaky test, a refactor, or a stubborn bug?",
   li_first="One habit that makes this safer: keep changes small and let it run the tests after each edit. A tight read-edit-verify loop beats one giant diff every time. Ep 1 (why the terminal is the right home for an AI agent) is on our page if you missed it.",
   li_tags="#ClaudeCode #AItools #DeveloperProductivity #SoftwareEngineering #DevTools",
   tiktok="A failing test goes in. A green suite comes out. And you signed off on every line in between. Watch Claude Code read test_slugify.py, find the bug, propose a fix as a diff, then run the suite green. No hand-edits, no autopilot. Would you let it touch your tests?",
   tiktok_tags="#claudecode #aicoding #devtok #coding #pytest",
   yt_title="Claude Code fixes a failing test hands-free — you approve the diff first",
   yt_desc="A failing test_slugify.py, fixed in one loop: Claude Code reads the code, finds the bug, proposes the fix as a diff you approve, then runs the suite green. You stay in control start to finish.\nRun the Docs — Claude Code series.\nFull docs: <docs-link>\n#Shorts #ClaudeCode #AICoding #Pytest",
   x="Failing test in. Green suite out. You approved the diff in between.\n\nThe agentic loop: Claude Code reads test_slugify.py, finds the bug, proposes a fix as a diff you approve, then runs the tests green. Hands-free, never on autopilot.\n\n#claudecode #aicoding"),
 dict(n=3, title="Give Claude a memory with CLAUDE.md", topic="Stop re-explaining your project every session",
   date="Wed 2026-06-10", time="09:00 CET",
   li_hook="Stop re-explaining your project to your AI every session.",
   li_body="""One file fixes it: CLAUDE.md.

Drop your conventions, stack, and rules in it once. Claude Code reads it automatically — every session, unprompted.

No more pasting "we use X, never do Y" at the top of every chat.

Run /init and it generates a first draft from your actual codebase. Edit, commit, done.

30 seconds in the video. Real terminal, real file. The payoff: an AI that already knows how your repo works before you type a word.""",
   li_cta="Watch the 30s demo, then try /init on your repo tonight. What's the one rule you'd put in your CLAUDE.md first?",
   li_first='Tip: keep it short and specific. Vague rules get ignored — "use pnpm, not npm" beats "follow best practices." And commit it so your whole team (and every agent) shares the same memory.',
   li_tags="#ClaudeCode #AICoding #DeveloperTools #SoftwareEngineering #DevProductivity",
   tiktok='Claude forgets your project the second you close the tab, so you re-paste "we use X, never do Y" into every chat. One file kills that: CLAUDE.md. Put your stack, conventions, and rules in it once and Claude Code reads it automatically at the start of every session. Run /init and it drafts one from your actual repo, then you edit and commit. 30 seconds, real terminal, no setup. What\'s the first rule you\'d put in yours?',
   tiktok_tags="#claudecode #aicoding #devtok #coding #programming #devtools",
   yt_title="Stop re-pasting project rules: give Claude Code memory with CLAUDE.md",
   yt_desc="Claude forgets your project every session, so you keep re-pasting your stack and rules. Put them in CLAUDE.md once and Claude Code reads it automatically. Run /init to draft one from your repo, then edit and commit.\nRun the Docs — Claude Code series. Full series: <docs-link>\n#Shorts #ClaudeCode #AICoding #DevTools",
   x="Claude forgets your project every session, so you re-paste your stack and rules into every chat. Fix it with one file: CLAUDE.md. Put your conventions in once and Claude Code reads it automatically. Run /init to draft it from your repo. 30s demo. #ClaudeCode #AIcoding"),
 dict(n=4, title="Plan mode", topic="See the plan before Claude touches a single file",
   date="Thu 2026-06-11", time="09:00 CET",
   li_hook="Claude Code wanted to rewrite 6 files. I saw all of it first.",
   li_body="""Plan mode is the safety rail for big changes.

Before it touches a single file, Claude proposes a step-by-step plan — read-only. Nothing executes yet.

You:
- Read exactly what it intends to do
- Edit the plan inline (Ctrl+G)
- Approve when it's right
- Then it runs

No surprise edits. No "wait, why did it change that?" The diff matches the plan you signed off on.

This is how we let an agent loose on real codebases without flinching.

30s terminal demo below.""",
   li_cta="Watch the review-then-execute loop in the clip. Do you let your AI agent edit straight away, or gate the big changes? Curious how others draw that line.",
   li_first="Tip: use plan mode for anything touching more than 2-3 files or migrations. For a one-line typo fix it's overkill — let it run. The skill is knowing which changes deserve a plan. Full series (Run the Docs) is in my profile.",
   li_tags="#ClaudeCode #AIagents #DeveloperTools #SoftwareEngineering #DevWorkflow",
   tiktok="Claude Code mapped out a 6-file change and didn't touch one of them. Plan mode shows a numbered, read-only plan first. You edit it with Ctrl+G, approve it, and only then does it run exactly what you signed off. No surprise edits on big changes. Would you let it loose without reading the plan first?",
   tiktok_tags="#claudecode #aicoding #devtok #coding #programming #refactoring",
   yt_title="Claude Code Plan Mode: read the plan before it edits a single file",
   yt_desc="Plan mode makes Claude Code lay out a numbered, read-only plan before touching any file. Edit it with Ctrl+G, approve, and it runs exactly that. Demo file: slugify.py.\n\nRun the Docs — Claude Code series.\nDocs: <docs-link>\n#Shorts #ClaudeCode #AICoding #DevTools",
   x="Claude Code planned a 6-file change and edited zero of them — until I'd read the plan.\n\nPlan mode lays out a numbered, read-only plan first. Edit it (Ctrl+G), approve, and it runs exactly that. No surprise edits on big changes.\n\n#claudecode #aicoding"),
 dict(n=5, title="Slash commands", topic="Turn your best prompts into one-keystroke team shortcuts",
   date="Fri 2026-06-12", time="09:00 CET",
   li_hook="Your best prompts shouldn't live in one person's head.",
   li_body="""Most teams retype the same instructions every day.

Claude Code fixes that with slash commands.

Type / for built-ins:
- /review — review the current diff
- /resume — pick up where you left off
- /clear — reset the context

Then save your own. Drop a markdown file in .claude/commands/, add $ARGUMENTS for inputs, commit it.

Now your whole team runs the same prompt, the same way — straight from git. 30 seconds in the demo.""",
   li_cta="Watch the 30s terminal demo, then steal the pattern. What's the one prompt your team retypes every single day?",
   li_first='Tip: a command is just a .md file, so review it in a PR like any other code. We keep ours in the repo so onboarding a new dev means "git pull" — they inherit every team workflow on day one. Full episode link below.',
   li_tags="#ClaudeCode #DeveloperTools #AICoding #DevWorkflow #SoftwareEngineering",
   tiktok="Your team's sharpest prompt is rotting in one Slack thread. Save it as a markdown file in .claude/commands, drop in $ARGUMENTS for the input, and commit. Now it's a slash command everyone runs the same way, versioned in git. What prompt would you turn into a command first?",
   tiktok_tags="#claudecode #aicoding #devtools #devtok #coding #programming",
   yt_title="Turn a repeated prompt into a team slash command in Claude Code",
   yt_desc="A markdown file in .claude/commands becomes a slash command. Add $ARGUMENTS to pass input, commit it, and your whole team runs the same workflow from git.\nRun the Docs — Claude Code series.\nDocs: <docs-link>\n#Shorts #ClaudeCode #AICoding #DevTools",
   x="Stop re-pasting the same prompt across your team. Save it as a markdown file in .claude/commands, add $ARGUMENTS, commit. Now it's a slash command everyone runs the same way, versioned in git instead of stuck in one head. #ClaudeCode #AICoding"),
]

def copy_md(e):
    return f"""# Ep {e['n']} — {e['title']}
**Suggested slot:** {e['date']} · {e['time']}   |   **Topic:** {e['topic']}

**Files in this folder:**
- `ep{e['n']}-linkedin-4x5.mp4` — LinkedIn (and X)
- `ep{e['n']}-vertical-9x16.mp4` — TikTok / YouTube Shorts / Instagram Reels
- `ep{e['n']}-cover.jpg` — thumbnail / cover frame

---

## LinkedIn  (upload `ep{e['n']}-linkedin-4x5.mp4` natively — no link in the post body)

{e['li_hook']}

{e['li_body']}

{e['li_cta']}

▶ Full series + episode links in the first comment.

{e['li_tags']}

**First comment (post yourself within ~1 min):**
> {e['li_first']}

---

## TikTok / Instagram Reels  (upload `ep{e['n']}-vertical-9x16.mp4`)

{e['tiktok']}

{e['tiktok_tags']}

---

## YouTube Shorts  (upload `ep{e['n']}-vertical-9x16.mp4`)

**Title:** {e['yt_title']}

**Description:**
{e['yt_desc']}

---

## X / Twitter  (upload `ep{e['n']}-linkedin-4x5.mp4`)

{e['x']}
"""

os.makedirs(KIT, exist_ok=True)
for e in EPS:
    d=os.path.join(KIT, f"ep{e['n']}"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"ep{e['n']}-copy.md"), "w").write(copy_md(e))

rows="\n".join(
 f"| {e['date']} | {e['time']} | **Ep {e['n']}** — {e['title']} | [`ep{e['n']}/`](ep{e['n']}/) | [copy](ep{e['n']}/ep{e['n']}-copy.md) |"
 for e in EPS)
master=f"""# Run the Docs — Claude Code · Posting Kit

Everything to schedule Week 1. Each `ep<N>/` folder has the two video files, a cover image, and `ep<N>-copy.md` with ready-to-paste copy for **LinkedIn, TikTok, YouTube Shorts, and X**.

> **Publishing is gated on your Discord ✅ for Day 1.** Dates below are *suggested* (weekday mornings, the proven B2B slot) — adjust the start date to whenever you greenlight. Cadence: daily for the week-1 launch sprint; drop to 3–4×/week if Days 3–5 reach sags.

## Schedule
| Date | Time | Episode | Folder | Copy |
|------|------|---------|--------|------|
{rows}

## Formats (already rendered, in each folder)
- **`-linkedin-4x5.mp4`** — 1080×1350. Use for **LinkedIn** and **X**.
- **`-vertical-9x16.mp4`** — 1080×1920. Use for **TikTok**, **YouTube Shorts**, **Instagram Reels**.

## How to post (the rules that drive reach)
1. **Upload the video natively** to each platform — never post a YouTube/external link in a LinkedIn body (it suppresses reach).
2. **Hook is line 1.** The copy is written so the first line works alone in the feed (assume the rest is hidden behind "…more").
3. **First comment:** post it yourself within ~1 minute (it holds the one link + a teaser for tomorrow). Keep the post body link-free.
4. **Guard the first 60–90 min:** reply to every comment with a real follow-up question — early engagement velocity is what the algorithm rewards.
5. **3–5 hashtags**, at the very end, niche + broad.

## Per-platform notes
- **LinkedIn / TikTok** uploads are manual (LinkedIn personal-profile API is restricted; TikTok's posting API needs app approval). Use each platform's native scheduler.
- **YouTube Shorts** can be automated (Playwright flow in the run-the-docs skill) — links are allowed in the description.
- Full strategy (cadence, timing, first-comment template, A/B notes) lives in `run-the-docs/engine → series/claude-code/linkedin-posting-plan.md`.

_Generated from the rebuilt Phase-2 videos. EP5 currently has a longer end-hold (its narration runs ~30s vs ~12s of terminal action) — fine to ship, but a richer re-record or trimmed narration would tighten it._
"""
open(os.path.join(KIT, "POSTING-KIT.md"), "w").write(master)
print("KIT_DOCS_OK ->", KIT)
for root,_,files in os.walk(KIT):
    for f in sorted(files): print("  ", os.path.relpath(os.path.join(root,f), KIT))

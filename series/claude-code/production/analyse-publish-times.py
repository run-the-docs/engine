#!/usr/bin/env python3
"""Analyse the Claude Code series' produce->publish timing.

Correlates each episode's lines.json FIRST commit (a production/scripted-time proxy,
from local git) with its YouTube publish time (from the public channel RSS), mapped
episode<->video via series/claude-code/youtube-ids.json. Computes per-episode lead
time + the publish cadence, then writes series/claude-code/publishing-cadence.md.

Repeatable + auth-free at runtime: local git + public RSS + the committed id map.
Refresh youtube-ids.json from the rtd-social D1 (videos.youtube_id) when ids change.

Usage (from anywhere in the engine repo):
  python3 series/claude-code/production/analyse-publish-times.py            # write the doc
  python3 series/claude-code/production/analyse-publish-times.py --print    # stdout only
"""
import json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone
from statistics import mean

CHANNEL = "UCAA-EgO7FejXuto6tHxDzHg"
RSS = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"
HERE = os.path.dirname(os.path.abspath(__file__))
SERIES = os.path.dirname(HERE)                       # series/claude-code
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                      capture_output=True, text=True).stdout.strip() or os.path.dirname(SERIES)
IDS_PATH = os.path.join(SERIES, "youtube-ids.json")
DOC_PATH = os.path.join(SERIES, "publishing-cadence.md")
GLOB = "series/claude-code/production"


def iso(s):
    return datetime.fromisoformat(s.strip().replace("Z", "+00:00"))


def lines_path(ep):
    stem = "epfable5" if ep == "fable5" else f"ep{ep}"
    return f"{GLOB}/{stem}.lines.json"


def added_time(ep):
    """First (add) commit time of the episode's lines.json from GitHub, ISO; None if absent.
    Uses `gh api` (not local `git log`) because squash-merged history in a local clone
    collapses every file's add-time to the clone point; the GitHub commit history is the
    authoritative per-file timeline. Requires an authenticated `gh`."""
    out = subprocess.run(
        ["gh", "api", f"repos/run-the-docs/engine/commits?path={lines_path(ep)}&per_page=100",
         "--jq", ".[-1].commit.committer.date"],
        capture_output=True, text=True).stdout.strip()
    return out or None


def rss_publish_times():
    """videoId -> published datetime, from the public channel RSS (public videos only)."""
    xml = urllib.request.urlopen(RSS, timeout=25).read().decode("utf-8", "replace")
    out = {}
    for entry in xml.split("<entry>")[1:]:
        vid = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", entry)
        pub = re.search(r"<published>([^<]+)</published>", entry)
        if vid and pub:
            out[vid.group(1)] = iso(pub.group(1))
    return out


def youtube_status(ids):
    """videoId -> {privacy, publishAt} via the YouTube Data API, for SCHEDULED/private
    videos that the public RSS can't show. Uses the same OAuth creds as the rest of the
    YT pipeline (YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN from the env — e.g.
    `source ~/.config/youtube/env.sh` on the Mac Mini). The token is read from the env and
    sent only as a Bearer header — never printed or logged. Returns {} (graceful) when the
    creds aren't present or the API is unavailable, so the script still runs anywhere."""
    import urllib.parse
    cid, cs, rt = (os.environ.get("YT_CLIENT_ID"), os.environ.get("YT_CLIENT_SECRET"),
                   os.environ.get("YT_REFRESH_TOKEN"))
    ids = [i for i in ids if i]
    if not (cid and cs and rt and ids):
        return {}
    try:
        body = urllib.parse.urlencode({"client_id": cid, "client_secret": cs,
                                       "refresh_token": rt, "grant_type": "refresh_token"}).encode()
        tok = json.load(urllib.request.urlopen(
            "https://oauth2.googleapis.com/token", data=body, timeout=25))["access_token"]
        out = {}
        for i in range(0, len(ids), 50):
            url = "https://www.googleapis.com/youtube/v3/videos?part=status&id=" + ",".join(ids[i:i + 50])
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
            for it in json.load(urllib.request.urlopen(req, timeout=25)).get("items", []):
                st = it.get("status", {})
                out[it["id"]] = {"privacy": st.get("privacyStatus"), "publishAt": st.get("publishAt")}
        return out
    except Exception as e:                       # never surface the token in an error
        sys.stderr.write(f"  [YouTube Data API unavailable: {type(e).__name__}]\n")
        return {}


def main():
    ids = {k: v for k, v in json.load(open(IDS_PATH, encoding="utf-8")).items()
           if not k.startswith("_")}
    pub_by_id = rss_publish_times()

    rows, scheduled = [], []
    for ep, vid in ids.items():
        added = added_time(ep)
        pub = pub_by_id.get(vid)
        if pub and added:
            rows.append({"ep": ep, "added": iso(added), "pub": pub,
                         "lead": (pub - iso(added)).total_seconds() / 86400})
        elif added:
            scheduled.append({"ep": ep, "vid": vid, "added": iso(added)})  # produced, not yet public

    yt = youtube_status([s["vid"] for s in scheduled])   # status.publishAt (creds-gated)
    for s in scheduled:
        pa = yt.get(s["vid"], {}).get("publishAt")
        s["publishAt"] = iso(pa) if pa else None

    rows.sort(key=lambda r: r["pub"])
    leads = [r["lead"] for r in rows]
    pubs = [r["pub"] for r in rows]
    adds = [r["added"] for r in rows]
    slots = {}
    for r in rows:
        slots[r["pub"].strftime("%H:%M")] = slots.get(r["pub"].strftime("%H:%M"), 0) + 1
    gaps = [(pubs[i] - pubs[i - 1]).total_seconds() / 3600 for i in range(1, len(pubs))]
    big_gaps = sum(1 for g in gaps if g > 36)

    def epn(ep):
        return ep if ep == "fable5" else "Ep " + ep

    L = []
    L.append("# Claude Code — publishing cadence")
    L.append("")
    L.append("_Generated by `series/claude-code/production/analyse-publish-times.py` "
             "(re-run to refresh). Production time = each episode's `lines.json` first "
             "git commit (a scripted-time proxy); publish time = the public YouTube RSS, "
             "matched via `youtube-ids.json`._")
    L.append("")
    if rows:
        L.append(f"**Window:** produced {min(adds).strftime('%Y-%m-%d')} → "
                 f"{max(adds).strftime('%m-%d')}, published "
                 f"{min(pubs).strftime('%Y-%m-%d')} → {max(pubs).strftime('%m-%d')}.  "
                 f"**Lead time:** min {min(leads):.1f}d · mean {mean(leads):.1f}d · "
                 f"max {max(leads):.1f}d.")
        L.append("")
        L.append("| ep | scripted (commit, UTC) | published (UTC) | lead | slot |")
        L.append("|----|------------------------|-----------------|------|------|")
        for r in rows:
            L.append(f"| {epn(r['ep'])} | {r['added'].strftime('%m-%d %H:%M')} | "
                     f"{r['pub'].strftime('%m-%d %H:%M')} | {r['lead']:.2f}d | "
                     f"{r['pub'].strftime('%H:%M')} |")
        L.append("")
        L.append(f"**Publish slots (UTC):** " +
                 ", ".join(f"{k} ×{v}" for k, v in sorted(slots.items())) + ".")
        L.append(f"**Cadence:** {len(rows)} public videos over "
                 f"{(max(pubs) - min(pubs)).days} days; {big_gaps} gap(s) >36h "
                 f"(breaks in the daily drip — e.g. pulled/flopped episodes).")
        L.append("")
        L.append("**Read:** production is front-loaded into a short batch, then released "
                 "as a ~daily drip on rotating slots — so lead time grows as the drip pays "
                 "down the backlog (the gap between max-lead and 0 is roughly the runway "
                 "buffer in days).")
    if scheduled:
        L.append("")
        L.append("## Scheduled (not yet public)")
        L.append("")
        if any(s.get("publishAt") for s in scheduled):
            L.append("| ep | scripted (commit, UTC) | scheduled publish (UTC) | lead |")
            L.append("|----|------------------------|-------------------------|------|")
            far = datetime.max.replace(tzinfo=timezone.utc)
            for s in sorted(scheduled, key=lambda s: s["publishAt"] or far):
                if s["publishAt"]:
                    lead = (s["publishAt"] - s["added"]).total_seconds() / 86400
                    L.append(f"| {epn(s['ep'])} | {s['added'].strftime('%m-%d %H:%M')} | "
                             f"{s['publishAt'].strftime('%m-%d %H:%M')} | {lead:.2f}d |")
                else:
                    L.append(f"| {epn(s['ep'])} | {s['added'].strftime('%m-%d %H:%M')} | (unknown) | — |")
            L.append("")
            L.append("_Scheduled publish times via the YouTube Data API (`status.publishAt`)._")
        else:
            L.append(f"Produced + have a video id but absent from the public RSS: "
                     f"{', '.join(epn(s['ep']) for s in scheduled)}. **Scheduled publish times "
                     f"need the YouTube Data API** — re-run on the Mac Mini with "
                     f"`source ~/.config/youtube/env.sh` first (its OAuth creds fill `status.publishAt`).")
    doc = "\n".join(L) + "\n"

    if "--print" in sys.argv:
        sys.stdout.write(doc)
    else:
        open(DOC_PATH, "w", encoding="utf-8").write(doc)
        print(f"wrote {DOC_PATH}  ({len(rows)} public, {len(scheduled)} scheduled, "
              f"mean lead {mean(leads):.1f}d)" if rows else f"wrote {DOC_PATH} (no public rows)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reconcile the rtd-social D1 'scheduled' YouTube postings against the channel's
actual publish state, so the cockpit Videos badges flip scheduled -> posted as the
drip goes live — WITHOUT any YouTube OAuth (only public signals).

Phase 5 of run-the-docs/engine#40. Pipeline (orchestrator-side):
  1. Orchestrator MCP-reads the D1's scheduled youtube rows and feeds them as JSON:
       SELECT p.video_id, v.episode, p.url, p.publish_at
       FROM postings p JOIN videos v ON v.id = p.video_id
       WHERE p.platform = 'youtube' AND p.status = 'scheduled';
     (raw Cloudflare MCP response or a flat [rows] list — both accepted, on stdin or argv[1])
  2. This tool checks each row's video id against the channel's public RSS feed
     (authoritative for "is it public" + gives the real publishedAt) and emits a JSON
     plan of scheduled -> posted transitions to STDOUT.
  3. Orchestrator applies the plan to the D1 via the Cloudflare MCP
       UPDATE postings SET status='posted', publish_at=<new_publish_at> WHERE ...
       UPDATE videos   SET youtube_privacy='public' WHERE id=<video_id>
     regenerates videos/posted.json, and opens a run-the-docs/website PR.

Auth-free + secret-free: only the public RSS feed. The diff core (parse_rss / vid_of /
reconcile) is pure and unit-tested; network I/O lives at the edges.

WHY RSS-only (no oembed fallback): YouTube oembed returns HTTP 401 for many *public*
Shorts (a known quirk — see auto-memory), which would mis-flag a live video as still
scheduled. The channel RSS reliably lists public Shorts, so it is the trustworthy signal.
LIMITATION: the RSS shows only the ~15 most recent uploads, so run the reconciler at
least once per ~15 publishes (a daily run during a daily drip is comfortably enough). A
video that has fallen off the RSS window stays 'scheduled' until a YT Data API backfill
(series/claude-code/production/backfill-publish-times.py, OAuth) refreshes it.
"""
import json, re, sys, urllib.request

CHANNEL = "UCAA-EgO7FejXuto6tHxDzHg"
RSS = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"


def parse_rss(xml):
    """videoId -> publishedAt (ISO-8601) for the public videos in the channel RSS."""
    out = {}
    for entry in xml.split("<entry>")[1:]:
        vid = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", entry)
        pub = re.search(r"<published>([^<]+)</published>", entry)
        if vid and pub:
            out[vid.group(1)] = pub.group(1).strip()
    return out


def vid_of(row):
    """The YouTube id of a posting row: explicit youtube_id, else parsed from the watch url."""
    if row.get("youtube_id"):
        return row["youtube_id"]
    m = re.search(r"[?&]v=([A-Za-z0-9_-]+)", row.get("url") or "")
    return m.group(1) if m else None


def reconcile(scheduled, rss_pub):
    """Pure. Given scheduled rows + {videoId: publishedAt} from the RSS, return
    (transitions, still_scheduled). A scheduled row whose video now appears in the RSS
    has gone public -> transition to 'posted' with publish_at set to the REAL publishedAt
    (refining the earlier scheduled estimate). Everything else stays scheduled."""
    transitions, still = [], []
    for row in scheduled:
        vid = vid_of(row)
        if vid and vid in rss_pub:
            transitions.append({
                "video_id": row["video_id"],
                "youtube_id": vid,
                "new_status": "posted",
                "new_publish_at": rss_pub[vid],
                "old_publish_at": row.get("publish_at"),
                "source": "rss",
            })
        else:
            still.append({
                "video_id": row["video_id"],
                "youtube_id": vid,
                "publish_at": row.get("publish_at"),
            })
    return transitions, still


def rows_from(data):
    """Accept the raw Cloudflare MCP d1_query response or a flat list of row dicts."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        r = data.get("result", data)
        if isinstance(r, list) and r and isinstance(r[0], dict) and "results" in r[0]:
            return r[0]["results"]
        if isinstance(r, dict) and "results" in r:
            return r["results"]
        if isinstance(r, list):
            return r
    return []


def fetch_rss():
    return parse_rss(urllib.request.urlopen(RSS, timeout=25).read().decode("utf-8", "replace"))


def main():
    src = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else None
    raw = open(src, encoding="utf-8").read() if src else sys.stdin.read()
    scheduled = rows_from(json.loads(raw))
    transitions, still = reconcile(scheduled, fetch_rss())
    json.dump({
        "transitions": transitions,
        "still_scheduled": still,
        "summary": {"checked": len(scheduled), "to_post": len(transitions),
                    "still_scheduled": len(still)},
    }, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    sys.stderr.write(f"reconcile: {len(scheduled)} scheduled checked, "
                     f"{len(transitions)} -> posted, {len(still)} still scheduled\n")


if __name__ == "__main__":
    main()

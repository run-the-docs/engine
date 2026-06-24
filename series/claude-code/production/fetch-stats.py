#!/usr/bin/env python3
"""Fetch per-video performance for the Run the Docs channel and emit stats.json.

Run on the Mac Mini, where the channel OAuth creds live:

    source ~/.config/youtube/env.sh
    python3 series/claude-code/production/fetch-stats.py > /tmp/stats.json

Then hand /tmp/stats.json to the orchestrator, which maps youtube_id -> D1 video_id
and UPSERTs into the rtd-social `stats` table via the Cloudflare MCP (see fetch-stats.md).

Auth: refreshes an access token from YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN
in the environment. The token is Bearer-only and is NEVER printed or logged. No secret is
written to stats.json — only public-ish performance metrics.

Sources (one OAuth run covers both):
  - Data API  videos.list?part=statistics      -> views, likes, comments (every upload)
  - Analytics API reports.query (dim=video, lifetime)
                  -> estimatedMinutesWatched, averageViewDuration, averageViewPercentage
    Degrades gracefully: if the Analytics call fails (scope/permission), public stats are
    still emitted with source='data-api'. (impressions / ctr / subscribers_gained are left
    null in v1 — the D1 columns exist and this script can be extended to fill them.)

stats.json shape: a flat array of row dicts, one per video:
  {youtube_id, as_of, source, views, likes, comments,
   watch_time_minutes, avg_view_duration_seconds, avg_view_percentage,
   impressions, ctr, subscribers_gained}
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UPLOADS_PLAYLIST = "UUAA-EgO7FejXuto6tHxDzHg"  # Run the Docs channel uploads playlist
TOKEN_URL = "https://oauth2.googleapis.com/token"
DATA_API = "https://www.googleapis.com/youtube/v3"
ANALYTICS_API = "https://youtubeanalytics.googleapis.com/v2/reports"


def _post_form(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _get(url, token, params):
    q = urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(f"{url}?{q}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def access_token():
    for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"):
        if not os.environ.get(k):
            sys.exit(f"missing env {k} — run: source ~/.config/youtube/env.sh")
    tok = _post_form(
        TOKEN_URL,
        {
            "client_id": os.environ["YT_CLIENT_ID"],
            "client_secret": os.environ["YT_CLIENT_SECRET"],
            "refresh_token": os.environ["YT_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
    )
    if "access_token" not in tok:
        sys.exit(
            f"token refresh failed: {tok.get('error', '?')} "
            "(re-auth: python3 ~/.config/youtube/oauth_reauth.py url)"
        )
    return tok["access_token"]


def all_upload_ids(token):
    ids, page = [], None
    while True:
        params = {"part": "contentDetails", "playlistId": UPLOADS_PLAYLIST, "maxResults": 50}
        if page:
            params["pageToken"] = page
        data = _get(f"{DATA_API}/playlistItems", token, params)
        ids += [it["contentDetails"]["videoId"] for it in data.get("items", [])]
        page = data.get("nextPageToken")
        if not page:
            break
    return ids


def statistics(token, ids):
    out = {}
    for i in range(0, len(ids), 50):
        data = _get(f"{DATA_API}/videos", token, {"part": "statistics", "id": ",".join(ids[i:i + 50])})
        for it in data.get("items", []):
            s = it.get("statistics", {})
            out[it["id"]] = {
                "views": int(s["viewCount"]) if "viewCount" in s else None,
                "likes": int(s["likeCount"]) if "likeCount" in s else None,
                "comments": int(s["commentCount"]) if "commentCount" in s else None,
            }
    return out


def analytics(token, ids):
    """Lifetime per-video analytics. Returns {} on any failure (graceful degrade)."""
    if not ids:
        return {}
    try:
        data = _get(
            ANALYTICS_API,
            token,
            {
                "ids": "channel==MINE",
                "startDate": "2005-01-01",
                "endDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "metrics": "estimatedMinutesWatched,averageViewDuration,averageViewPercentage",
                "dimensions": "video",
                "filters": "video==" + ",".join(ids[:500]),
                "maxResults": 500,
            },
        )
        idx = {h["name"]: i for i, h in enumerate(data.get("columnHeaders", []))}
        res = {}
        for row in data.get("rows", []):
            res[row[idx["video"]]] = {
                "watch_time_minutes": row[idx["estimatedMinutesWatched"]],
                "avg_view_duration_seconds": row[idx["averageViewDuration"]],
                "avg_view_percentage": row[idx["averageViewPercentage"]],
            }
        return res
    except Exception as e:  # noqa: BLE001 — degrade to public-only on any analytics error
        print(f"# analytics unavailable ({e}); emitting public stats only", file=sys.stderr)
        return {}


def main():
    token = access_token()
    ids = all_upload_ids(token)
    stats = statistics(token, ids)
    ana = analytics(token, ids)
    as_of = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = []
    for vid in ids:
        s = stats.get(vid, {})
        a = ana.get(vid, {})
        rows.append(
            {
                "youtube_id": vid,
                "as_of": as_of,
                "source": "analytics-api" if a else "data-api",
                "views": s.get("views"),
                "likes": s.get("likes"),
                "comments": s.get("comments"),
                "watch_time_minutes": a.get("watch_time_minutes"),
                "avg_view_duration_seconds": a.get("avg_view_duration_seconds"),
                "avg_view_percentage": a.get("avg_view_percentage"),
                "impressions": None,
                "ctr": None,
                "subscribers_gained": None,
            }
        )
    json.dump(rows, sys.stdout, indent=2)
    sys.stdout.write("\n")
    print(f"# {len(rows)} videos, as_of {as_of}, analytics={'yes' if ana else 'no'}", file=sys.stderr)


if __name__ == "__main__":
    main()

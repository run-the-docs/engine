#!/usr/bin/env python3
"""Fetch YouTube publish times for the Claude Code series and emit JSON for the rtd-social D1.

For each CC episode video id it returns, via the YouTube Data API:
  - privacy      : public | unlisted | private
  - publishAt    : status.publishAt  — the SCHEDULED future publish time (set only while private+scheduled)
  - publishedAt  : snippet.publishedAt — the actual publish time (set once public)
  - publish_at   : publishAt if still scheduled, else publishedAt  (the value to store in postings.publish_at)

Output is a JSON object keyed by the rtd-social `postings.video_id` (cc-epN / cc-fable5),
printed to STDOUT only. All diagnostics go to STDERR, so you can redirect cleanly:

    source ~/.config/youtube/env.sh        # YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN
    python3 backfill-publish-times.py > /tmp/cc-publish.json

The OAuth token is read from the env and sent only as a Bearer header — never printed or logged.
The publish timestamps themselves are NOT secret. Self-contained: the id map below is a snapshot of
the rtd-social D1 (postings.url for platform='youtube'); regenerate it from the D1 if ids change.
"""
import json, os, sys, urllib.parse, urllib.request

# postings.video_id -> youtube id  (snapshot of rtd-social D1 d298499d, CC series, 2026-06-22)
CC = {
    "cc-ep1": "KWIj3BxGsqw", "cc-ep2": "ZZkYzzFCJXg", "cc-ep3": "k0p1V7T3D9E",
    "cc-ep4": "TCGGjyA95Pk", "cc-ep5": "Ys1Sq9Z_CNo", "cc-ep6": "3NAOynMjW7g",
    "cc-ep7": "fgNfzyllti8", "cc-ep8": "l8LjnU7ppiY", "cc-ep9": "lTsqbIBeupc",
    "cc-ep10": "GzFY-OFvh1Q", "cc-ep11": "UNwzgP3lswo", "cc-ep12": "ZSGZsCHGLYg",
    "cc-ep13": "VUJU176o3SI", "cc-ep14": "S8MTwUM56fM", "cc-ep15": "ATRBkdQhIlU",
    "cc-ep16": "ut-HJ5JgYTQ", "cc-ep17": "0zY7L-mL97Y", "cc-ep19": "EuTv512PFeg",
    "cc-ep21": "UUBbF4sj2lM", "cc-ep23": "92B5d5r9aFg", "cc-ep24": "0N91Z91x0kM",
    "cc-fable5": "8AoM8EP-wYY",
}


def access_token():
    cid, cs, rt = (os.environ.get("YT_CLIENT_ID"), os.environ.get("YT_CLIENT_SECRET"),
                   os.environ.get("YT_REFRESH_TOKEN"))
    if not (cid and cs and rt):
        sys.stderr.write("ERROR: YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN not set. "
                         "Run `source ~/.config/youtube/env.sh` first.\n")
        sys.exit(2)
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": cs,
                                   "refresh_token": rt, "grant_type": "refresh_token"}).encode()
    try:
        return json.load(urllib.request.urlopen(
            "https://oauth2.googleapis.com/token", data=body, timeout=25))["access_token"]
    except Exception as e:  # never surface the token/secret in an error
        sys.stderr.write(f"ERROR: token refresh failed ({type(e).__name__}). "
                         f"The refresh token may be expired (7-day 'Testing' OAuth limit) — re-auth via "
                         f"~/.config/youtube/oauth_reauth.py. No publish times fetched.\n")
        sys.exit(3)


def main():
    tok = access_token()
    by_yt = {v: k for k, v in CC.items()}
    ids = list(CC.values())
    status, snippet = {}, {}
    for i in range(0, len(ids), 50):
        chunk = ",".join(ids[i:i + 50])
        url = ("https://www.googleapis.com/youtube/v3/videos"
               "?part=status,snippet&maxResults=50&id=" + chunk)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
        for it in json.load(urllib.request.urlopen(req, timeout=25)).get("items", []):
            status[it["id"]] = it.get("status", {})
            snippet[it["id"]] = it.get("snippet", {})

    out = {}
    for vid in ids:
        st, sn = status.get(vid, {}), snippet.get(vid, {})
        publish_at = st.get("publishAt") or sn.get("publishedAt")
        out[by_yt[vid]] = {
            "youtube_id": vid,
            "privacy": st.get("privacyStatus"),
            "publishAt": st.get("publishAt"),
            "publishedAt": sn.get("publishedAt"),
            "publish_at": publish_at,
        }
    missing = [k for k, v in out.items() if not v["publish_at"]]
    sys.stderr.write(f"fetched {len(out)} episodes; "
                     f"{sum(1 for v in out.values() if v['publishAt'])} scheduled, "
                     f"{sum(1 for v in out.values() if v['privacy'] == 'public')} public"
                     + (f"; NO time for: {', '.join(missing)}" if missing else "") + "\n")
    sys.stdout.write(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()

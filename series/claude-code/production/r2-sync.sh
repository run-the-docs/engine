#!/bin/bash
# Gitops R2 sync for the Run the Docs "Claude Code" cuts.
#
# Uploads every rendered claude-ep*-{45,916}.mp4 to the `runthedocs-videos` R2
# bucket (idempotent — overwrites). This is the versioned, reviewable home for
# the upload logic (instead of an ad-hoc terminal command); run it on the host
# that holds the rendered cuts (the pipeline host).
#
# After a successful sync it (re)emits an in-bucket `manifest.json` — a public listing
# of every cut actually live on R2 (key + bytes + ETag), since the public r2.dev domain
# cannot list objects. That manifest is the steady-state "what's on R2" truth the
# reconciler/site consume (run-the-docs/engine#40 Phase 2). It always reflects the FULL
# bucket (re-probed from all local cuts), even when only a subset of episodes is synced.
#
# Auth: uses wrangler's own session — EITHER a stored `wrangler login` (OAuth)
# OR CLOUDFLARE_API_TOKEN in the env. We do NOT require the env token (the
# pipeline host is typically wrangler-logged-in). The token, if used, is
# OpenTofu-managed (dashecorp/infra) and surfaced out-of-band (Ops-E / SOPS) —
# NEVER committed here or printed. The bucket + its public r2.dev domain are
# OpenTofu-managed too (cloudflare/dashecorp.com/runthedocs-r2.tf, infra#262).
#
# Usage:
#   bash r2-sync.sh                 # sync all rendered cuts found in $REC
#   bash r2-sync.sh 17 19 21        # sync only these episode numbers
set -euo pipefail

BUCKET="runthedocs-videos"
PUBLIC_BASE="${RTD_R2_PUBLIC_BASE:-https://pub-8745206116f440c6b36f5e6bd0eb1905.r2.dev}"
REC="${REC:-$HOME/runthedocs/series/claude-code/demo/rec}"
MANIFEST_KEY="manifest.json"   # Phase 2: in-bucket listing — public r2.dev can't list objects

command -v wrangler >/dev/null 2>&1 || { echo "FATAL: wrangler not found on PATH"; exit 1; }
# Accept EITHER auth method: a stored `wrangler login` (OAuth) or a
# CLOUDFLARE_API_TOKEN in the env. whoami succeeds for both; never prints the token.
wrangler whoami >/dev/null 2>&1 || { echo "FATAL: wrangler is not authenticated — run 'wrangler login' or set CLOUDFLARE_API_TOKEN, then retry"; exit 1; }

# Build the file list: explicit episode numbers if given, else all rendered cuts.
files=()
if [ "$#" -gt 0 ]; then
  for n in "$@"; do
    for r in 45 916; do
      f="$REC/claude-ep${n}-${r}.mp4"
      [ -e "$f" ] && files+=("$f") || echo "WARN: missing $f (skipped)"
    done
  done
else
  shopt -s nullglob
  files=("$REC"/claude-ep*-45.mp4 "$REC"/claude-ep*-916.mp4)
fi

[ "${#files[@]}" -gt 0 ] || { echo "nothing to sync (no matching cuts in $REC)"; exit 0; }

# Upload one object with a 3-try backoff, then VERIFY it is publicly reachable at
# the right size before declaring success (tolerant of r2.dev edge propagation, so
# a fresh put isn't falsely flagged). wrangler reads CLOUDFLARE_API_TOKEN from the
# env; the token is never on the command line and never echoed.
put_and_verify() {
  local f="$1" key local_size hdr http_status remote_size try v
  key="$(basename "$f")"
  local_size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo 0)
  for try in 1 2 3; do
    if wrangler r2 object put "${BUCKET}/${key}" --file "$f" --remote; then
      for v in 1 2 3 4 5; do
        hdr=$(curl -sI -m 15 "${PUBLIC_BASE}/${key}" 2>/dev/null || true)
        http_status=$(printf '%s\n' "$hdr" | awk 'toupper($1) ~ /^HTTP/{print $2; exit}')
        remote_size=$(printf '%s\n' "$hdr" | awk 'tolower($1)=="content-length:"{gsub(/\r/,"",$2); print $2}')
        if [ "$http_status" = "200" ] && [ -n "$remote_size" ] && [ "$remote_size" = "$local_size" ]; then
          echo "R2: uploaded + verified ${key} (${remote_size} bytes)"
          return 0
        fi
        sleep $((v * 3))
      done
      echo "WARN: ${key} put but public readback not yet 200/${local_size} bytes; retrying put"
    fi
    sleep $((try * try * 2))
  done
  echo "FATAL: R2 upload/verify failed for ${key} after retries"
  return 1
}

# Re-emit the in-bucket manifest.json: probe the FULL set of local cuts against the public
# r2.dev domain (HEAD), record every one that is live (key + bytes + ETag), and upload the
# listing to the bucket root. Python builds the JSON (always present on the pipeline host;
# avoids a jq dependency + hand-rolled escaping). ETag/bytes let the reconciler verify bytes
# (r2.dev exposes ETag, serves no cache-control). Fail-loud: a manifest upload failure fails
# the run, consistent with the upload rail.
emit_manifest() {
  echo "R2: rebuilding ${MANIFEST_KEY} (in-bucket listing — r2.dev can't list)…"
  local out="$REC/$MANIFEST_KEY"
  python3 - "$REC" "$PUBLIC_BASE" "$BUCKET" "$out" <<'PY' || return 1
import glob, json, os, sys, urllib.request
rec, base, bucket, out = sys.argv[1], sys.argv[2].rstrip("/"), sys.argv[3], sys.argv[4]
UA = "rtd-reconcile/1.0 (run-the-docs media reconciler)"  # CF WAF 403s the default urllib UA
keys = sorted({os.path.basename(p) for p in
               glob.glob(os.path.join(rec, "claude-ep*-45.mp4")) +
               glob.glob(os.path.join(rec, "claude-ep*-916.mp4"))})
objs = []
for k in keys:
    try:
        with urllib.request.urlopen(urllib.request.Request(
                f"{base}/{k}", method="HEAD", headers={"User-Agent": UA}), timeout=15) as r:
            if r.status != 200:
                continue
            size = r.headers.get("Content-Length")
            objs.append({"key": k,
                         "bytes": int(size) if size and size.isdigit() else None,
                         "etag": (r.headers.get("ETag") or "").strip('"') or None})
    except Exception:
        continue  # not live on R2 (yet) -> omitted from the manifest
json.dump({"bucket": bucket, "public_base": base,
           "generated_by": "r2-sync.sh", "count": len(objs), "objects": objs},
          open(out, "w"), indent=2)
print(f"  {len(objs)} object(s) live on R2")
PY
  if wrangler r2 object put "${BUCKET}/${MANIFEST_KEY}" --file "$out" \
       --remote --content-type application/json; then
    echo "R2: ${MANIFEST_KEY} uploaded -> ${PUBLIC_BASE}/${MANIFEST_KEY}"
  else
    echo "FATAL: failed to upload ${MANIFEST_KEY}"; return 1
  fi
}

n=0; failed=()
for f in "${files[@]}"; do
  put_and_verify "$f" && n=$((n + 1)) || failed+=("$(basename "$f")")
done
if [ "${#failed[@]}" -gt 0 ]; then
  echo "FATAL: ${#failed[@]} object(s) failed upload/verify: ${failed[*]}"
  exit 1
fi
emit_manifest || { echo "FATAL: manifest emission failed"; exit 1; }
echo "R2 sync complete: $n object(s) -> $BUCKET (all verified; ${MANIFEST_KEY} refreshed)"

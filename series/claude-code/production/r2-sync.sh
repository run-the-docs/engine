#!/bin/bash
# Gitops R2 sync for the Run the Docs "Claude Code" cuts.
#
# Uploads every rendered claude-ep*-{45,916}.mp4 to the `runthedocs-videos` R2
# bucket (idempotent — overwrites). This is the versioned, reviewable home for
# the upload logic (instead of an ad-hoc terminal command); run it on the host
# that holds the rendered cuts (the pipeline host).
#
# Auth: wrangler reads CLOUDFLARE_API_TOKEN from the environment. That token is
# OpenTofu-managed (dashecorp/infra) and surfaced to this host out-of-band
# (Ops-E / SOPS) — it is NEVER committed here or printed. The bucket + its
# public r2.dev domain are OpenTofu-managed too (cloudflare/dashecorp.com/
# runthedocs-r2.tf, infra#262).
#
# Usage:
#   bash r2-sync.sh                 # sync all rendered cuts found in $REC
#   bash r2-sync.sh 17 19 21        # sync only these episode numbers
set -euo pipefail

BUCKET="runthedocs-videos"
REC="${REC:-$HOME/runthedocs/series/claude-code/demo/rec}"

: "${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN must be set in the env (OpenTofu-managed R2 token; never commit it) before syncing}"
command -v wrangler >/dev/null 2>&1 || { echo "FATAL: wrangler not found on PATH"; exit 1; }

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

n=0
for f in "${files[@]}"; do
  # wrangler reads CLOUDFLARE_API_TOKEN from the env; the token is never passed
  # on the command line, never echoed.
  wrangler r2 object put "${BUCKET}/$(basename "$f")" --file "$f" --remote
  echo "R2: uploaded $(basename "$f")"
  n=$((n + 1))
done
echo "R2 sync complete: $n object(s) -> $BUCKET"

#!/usr/bin/env bash
# Thin wrapper around the rtd-social Cloudflare D1 REST /query endpoint, for the
# server-side publish-status reconciler (.github/workflows/reconcile-publish-status.yml).
#
# The D1 API token is read from the environment ONLY and is never echoed, logged, or
# placed in argv — it goes straight into the Authorization header. NEVER add `set -x`
# here; it would expand the header and leak the bearer token into the run log.
#
# Usage:
#   RTD_SOCIAL_D1_TOKEN=...  reconcile-d1.sh query "SELECT ..." '["p1","p2"]'  # -> .result[0].results (JSON array)
#   RTD_SOCIAL_D1_TOKEN=...  reconcile-d1.sh exec  "UPDATE ..." '["p1"]'       # -> .result[0].meta.changes (int)
#
# SQL binds `?` positional placeholders to the params JSON array (injection-safe);
# pass params built with jq, never interpolated into the SQL string.
set -euo pipefail

ACCOUNT="59710bf016d417f860051f1f00b00258"          # dashecorp Cloudflare account
DB="d298499d-abb8-4009-b184-9bd8145617c1"           # rtd-social D1
: "${RTD_SOCIAL_D1_TOKEN:?RTD_SOCIAL_D1_TOKEN must be set in the environment}"

mode="${1:?usage: reconcile-d1.sh <query|exec> <sql> [paramsJSON]}"
sql="${2:?sql required}"
params="${3:-[]}"

body="$(jq -nc --arg sql "$sql" --argjson params "$params" '{sql:$sql, params:$params}')"
resp="$(curl -sS --fail-with-body -X POST \
  "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/d1/database/${DB}/query" \
  -H "Authorization: Bearer ${RTD_SOCIAL_D1_TOKEN}" \
  -H "Content-Type: application/json" \
  --data "$body")" || { echo "reconcile-d1: HTTP request to D1 failed" >&2; exit 1; }

if [ "$(printf '%s' "$resp" | jq -r '.success')" != "true" ]; then
  # surface ONLY the errors object — never the request body or headers
  printf 'reconcile-d1: D1 query failed: %s\n' "$(printf '%s' "$resp" | jq -c '.errors')" >&2
  exit 1
fi

case "$mode" in
  query) printf '%s\n' "$resp" | jq '.result[0].results' ;;
  exec)  printf '%s\n' "$resp" | jq '.result[0].meta.changes' ;;
  *) echo "reconcile-d1: unknown mode '$mode' (use query|exec)" >&2; exit 2 ;;
esac

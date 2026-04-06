#!/bin/bash
# Run the Docs — docs change checker wrapper
# Usage:
#   ./check-docs.sh              # check only, no Discord
#   ./check-docs.sh --discord    # check + post alert to Discord if changes found
#   DISCORD_WEBHOOK_URL=https://... ./check-docs.sh --discord

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE=/opt/homebrew/bin/node
RESULT_FILE="$SCRIPT_DIR/../docs-check-result.json"
DISCORD_CHANNEL_ID="1489920352594432051"

POST_DISCORD=0
if [[ "${1:-}" == "--discord" ]]; then
  POST_DISCORD=1
fi

# Run the checker
"$NODE" "$SCRIPT_DIR/check-docs-changes.js"

# Post to Discord if requested and changes were found
if [[ "$POST_DISCORD" -eq 1 ]]; then
  if [[ -z "${DISCORD_WEBHOOK_URL:-}" ]]; then
    echo "⚠  --discord flag set but DISCORD_WEBHOOK_URL is not set. Skipping Discord alert."
    exit 0
  fi

  CHANGED_COUNT=$("$NODE" -e "const r=require('$RESULT_FILE'); console.log(r.changed.length)")
  NEW_COUNT=$("$NODE" -e "const r=require('$RESULT_FILE'); console.log(r.new.length)")

  if [[ "$CHANGED_COUNT" -eq 0 && "$NEW_COUNT" -eq 0 ]]; then
    echo "No changes — skipping Discord alert."
    exit 0
  fi

  # Build message text
  MSG="**Run the Docs — Docs Change Alert** (channel <#${DISCORD_CHANNEL_ID}>)\n\n"

  if [[ "$CHANGED_COUNT" -gt 0 ]]; then
    MSG+="⚠ **${CHANGED_COUNT} docs page(s) changed** since the video was created:\n"
    CHANGED_LIST=$("$NODE" -e "
      const r=require('$RESULT_FILE');
      r.changed.forEach(ep => console.log(\`• [${ep.series.toUpperCase()} ep\${ep.ep}] \${ep.title} — <\${ep.url}>\`));
    ")
    MSG+="$CHANGED_LIST\n\n"
  fi

  if [[ "$NEW_COUNT" -gt 0 ]]; then
    MSG+="◆ **${NEW_COUNT} page(s) hashed for the first time** (baseline set):\n"
    NEW_LIST=$("$NODE" -e "
      const r=require('$RESULT_FILE');
      r.new.forEach(ep => console.log(\`• [${ep.series.toUpperCase()} ep\${ep.ep}] \${ep.title}\`));
    ")
    MSG+="$NEW_LIST\n\n"
  fi

  MSG+="_Stale episodes may need a re-check or video update._"

  # Post to Discord webhook
  curl -s -o /dev/null -w "Discord post: HTTP %{http_code}\n" \
    -X POST "$DISCORD_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    --data-binary "$(printf '{"content": "%s"}' "$(echo "$MSG" | sed 's/"/\\"/g')")"
fi

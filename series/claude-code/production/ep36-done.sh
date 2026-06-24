#!/usr/bin/env bash
printf "finished %s\n" "$(date +%H:%M:%S)" >> "$CLAUDE_PROJECT_DIR/.claude/stop.log"
exit 0

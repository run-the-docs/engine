#!/bin/bash
# Template ffmpeg mix command for Run the Docs episodes
# USAGE: bash template_mix.sh <series> <ep_number>
# Example: bash template_mix.sh react 02

SERIES=${1:-react}
EP=${2:-01}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # parent dir
VIDEOS_DIR="$SCRIPT_DIR/videos/$SERIES"

mkdir -p "$VIDEOS_DIR"

echo "Mixing audio + video for $SERIES ep$EP..."
echo "  Input: video.mp4 + voice.wav"
echo "  Output: $VIDEOS_DIR/ep${EP}.mp4"

ffmpeg -i video.mp4 -i voice.wav \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  "$VIDEOS_DIR/ep${EP}.mp4" 2>&1 | tail -3

# Verify result
DURATION=$(ffprobe -v error -show_format "$VIDEOS_DIR/ep${EP}.mp4" | grep duration | cut -d= -f2)
echo "✓ Done! Duration: ${DURATION}s"

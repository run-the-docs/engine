#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERIES_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VIDEOS_DIR="$(dirname "$(dirname "$(dirname "$SERIES_DIR")")")/videos/react"
EP="01"

echo "Building React ep${EP}..."
mkdir -p "$VIDEOS_DIR"
cd "$SCRIPT_DIR"

# 1. Generate TTS using Kokoro
echo "Generating voice audio with Kokoro TTS (bm_george)..."
python3 tts.py

# 2. Generate HTML animation with correct TOTAL_DURATION from TTS
echo "Building animation.html with exact timing from TTS..."
python3 build.py

# 3. Render frames
echo "Rendering animation frames..."
python3 render.py "$SCRIPT_DIR" animation.html

# 4. Encode
echo "Encoding video..."
ffmpeg -framerate 30 -i frames/frame_%06d.png \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  video.mp4 2>&1 | tail -3

# 5. Mix
echo "Mixing audio and video..."
ffmpeg -i video.mp4 -i voice.wav \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  "$VIDEOS_DIR/ep${EP}.mp4" 2>&1 | tail -3

# 6. Cleanup
rm -rf frames video.mp4 voice.wav

echo "✓ Done! Output: $VIDEOS_DIR/ep${EP}.mp4"

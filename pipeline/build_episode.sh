#!/bin/bash
"""
Master build script for Run the Docs episodes.

USAGE:
  cd series/<name>/production/ep<NN>
  bash build_episode.sh

This runs all 4 steps of the pipeline in sequence:
1. tts.py → voice.wav + timing.json
2. build.py → animation.html (with TOTAL_DURATION from TTS)
3. render.py → frames/ (exact frame count from timing.json)
4. ffmpeg mix → final .mp4 (audio + video synced)
"""

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERIES_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
SERIES_NAME="$(basename "$SERIES_DIR")"
PRODUCTION_DIR="$(dirname "$SCRIPT_DIR")"
EP=$(basename "$SCRIPT_DIR" | sed 's/ep//')
VIDEOS_DIR="$(dirname "$SERIES_DIR")/videos/$SERIES_NAME"

mkdir -p "$VIDEOS_DIR"

echo "=========================================="
echo "Run the Docs Pipeline"
echo "Series: $SERIES_NAME, Episode: $EP"
echo "=========================================="

cd "$SCRIPT_DIR"

# Step 1: TTS
echo ""
echo "STEP 1: Generate voice audio with Kokoro TTS..."
if [ ! -f "tts.py" ]; then
  echo "ERROR: tts.py not found in $SCRIPT_DIR"
  exit 1
fi
python3 tts.py

if [ ! -f "timing.json" ]; then
  echo "ERROR: timing.json not created by tts.py"
  exit 1
fi

echo "✓ Step 1 complete: voice.wav + timing.json"

# Step 2: Build HTML
echo ""
echo "STEP 2: Build animation.html with timing..."
if [ ! -f "build.py" ]; then
  echo "ERROR: build.py not found in $SCRIPT_DIR"
  exit 1
fi
python3 build.py

if [ ! -f "animation.html" ]; then
  echo "ERROR: animation.html not created by build.py"
  exit 1
fi

echo "✓ Step 2 complete: animation.html"

# Step 3: Render frames
echo ""
echo "STEP 3: Render animation frames..."
if [ ! -f "render.py" ]; then
  echo "ERROR: render.py not found in $SCRIPT_DIR"
  exit 1
fi
python3 render.py

if [ ! -d "frames" ] || [ -z "$(ls -A frames 2>/dev/null)" ]; then
  echo "ERROR: frames/ not created by render.py"
  exit 1
fi

FRAME_COUNT=$(ls frames/frame_*.png 2>/dev/null | wc -l)
echo "✓ Step 3 complete: $FRAME_COUNT frames rendered"

# Step 4: Encode and mix
echo ""
echo "STEP 4: Encode video and mix audio..."

echo "  Encoding frames to video.mp4..."
ffmpeg -framerate 30 -i frames/frame_%06d.png \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  video.mp4 2>&1 | tail -3

echo "  Mixing audio + video..."
ffmpeg -i video.mp4 -i voice.wav \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  "$VIDEOS_DIR/ep${EP}.mp4" 2>&1 | tail -3

echo "✓ Step 4 complete: final video mixed"

# Cleanup
echo ""
echo "Cleaning up temporary files..."
rm -rf frames video.mp4

# Verify
FINAL_VIDEO="$VIDEOS_DIR/ep${EP}.mp4"
if [ -f "$FINAL_VIDEO" ]; then
  DURATION=$(ffprobe -v error -show_format "$FINAL_VIDEO" | grep duration | cut -d= -f2 || echo "unknown")
  echo ""
  echo "=========================================="
  echo "✓ BUILD COMPLETE"
  echo "=========================================="
  echo "Output: $FINAL_VIDEO"
  echo "Duration: ${DURATION}s"
  echo ""
  echo "Next steps:"
  echo "1. Review the video"
  echo "2. Upload to Discord: #iclaw-e"
  echo "3. Get approval"
  echo "4. Commit to git: git add series/$SERIES_NAME/production/ep$EP/"
  echo "5. Update episodes.md (status = approved)"
  echo "6. Upload to YouTube with SRT captions"
  echo "=========================================="
else
  echo "ERROR: Final video not created at $FINAL_VIDEO"
  exit 1
fi

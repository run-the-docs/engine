#!/bin/bash
# Build script for React ep02: Importing and Exporting Components
# Usage: ./build.sh
# Output: ../../../videos/react/ep02.mp4

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERIES_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VIDEOS_DIR="$(dirname "$(dirname "$(dirname "$SERIES_DIR")")")/videos/react"
EP="02"

echo "Building React ep${EP}..."

# Ensure output directory exists
mkdir -p "$VIDEOS_DIR"

# 1. Generate TTS from script.md
echo "Generating voice audio..."
say -v "Samantha" -r 150 -f "$SCRIPT_DIR/script.md" -o "$SCRIPT_DIR/voice.aiff"

# Convert AIFF to WAV
ffmpeg -i "$SCRIPT_DIR/voice.aiff" -acodec pcm_s16le -ar 44100 \
  "$SCRIPT_DIR/voice.wav" 2>&1 | grep -E "(Duration|error)" || true

# Pad voice to 90 seconds
VOICE_DURATION=$(ffprobe -v quiet -show_format "$SCRIPT_DIR/voice.wav" | \
  grep duration | cut -d= -f2 | cut -d. -f1)
SILENCE_DURATION=$((90 - ${VOICE_DURATION:-50}))

ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t "$SILENCE_DURATION" \
  -q:a 9 -acodec pcm_s16le "$SCRIPT_DIR/silence.wav" 2>&1 | grep -E "(error|Duration)" || true

ffmpeg -i "$SCRIPT_DIR/voice.wav" -i "$SCRIPT_DIR/silence.wav" \
  -filter_complex "[0][1]concat=n=2:v=0:a=1" \
  "$SCRIPT_DIR/audio_final.wav" 2>&1 | grep -E "(error|muxing)" || true

# 2. Render HTML canvas to frames using Playwright
echo "Rendering animation frames..."
python3 - <<'PYTHON_EOF'
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64
import sys

script_dir = Path(__file__).parent.resolve()
html_file = script_dir / "animation.html"
frames_dir = script_dir / "frames"
frames_dir.mkdir(exist_ok=True)

total_frames = 90 * 30  # 90 seconds @ 30fps

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(f"file://{html_file}")
    page.wait_for_load_state("networkidle")
    
    for frame_num in range(total_frames):
        if frame_num % 300 == 0:
            print(f"  Frame {frame_num}/{total_frames}...")
        
        data_url = page.evaluate(f'''() => {{
            window.renderFrame({frame_num});
            return document.getElementById('c').toDataURL('image/png');
        }}''')
        
        png_data = base64.b64decode(data_url.split(',')[1])
        frame_path = frames_dir / f"frame_{frame_num:06d}.png"
        frame_path.write_bytes(png_data)
    
    browser.close()

print(f"✓ Rendered {total_frames} frames to {frames_dir}")
PYTHON_EOF

# 3. Encode frames to H.264 MP4
echo "Encoding video..."
ffmpeg -framerate 30 -i "$SCRIPT_DIR/frames/frame_%06d.png" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  "$SCRIPT_DIR/video.mp4" 2>&1 | tail -3

# 4. Mix audio + video
echo "Mixing audio and video..."
ffmpeg -i "$SCRIPT_DIR/video.mp4" -i "$SCRIPT_DIR/audio_final.wav" \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  "$VIDEOS_DIR/ep${EP}.mp4" 2>&1 | tail -3

# 5. Cleanup
echo "Cleaning up temporary files..."
rm -rf "$SCRIPT_DIR/frames" "$SCRIPT_DIR/video.mp4" \
  "$SCRIPT_DIR/voice.aiff" "$SCRIPT_DIR/voice.wav" \
  "$SCRIPT_DIR/silence.wav" "$SCRIPT_DIR/audio_final.wav"

echo "✓ Done! Output: $VIDEOS_DIR/ep${EP}.mp4"

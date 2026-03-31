#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERIES_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VIDEOS_DIR="$(dirname "$(dirname "$(dirname "$SERIES_DIR")")")/videos/react"
EP="01"

echo "Building React ep${EP}..."
mkdir -p "$VIDEOS_DIR"

# 1. Generate TTS using Kokoro
echo "Generating voice audio with Kokoro TTS (bm_george)..."
cd "$SCRIPT_DIR"
python3 tts.py

# voice.wav is now ready
VOICE_DURATION=$(ffprobe -v quiet -show_format voice.wav | grep duration | cut -d= -f2 | xargs printf "%.0f")
SILENCE_DURATION=$((90 - VOICE_DURATION))

echo "Voice duration: ${VOICE_DURATION}s, padding with ${SILENCE_DURATION}s silence"

ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t "$SILENCE_DURATION" \
  -q:a 9 -acodec pcm_s16le silence.wav 2>&1 | tail -1

ffmpeg -i voice.wav -i silence.wav \
  -filter_complex "[0][1]concat=n=2:v=0:a=1" \
  audio_final.wav 2>&1 | tail -1

# 2. Render frames
echo "Rendering animation frames..."
python3 render.py "$SCRIPT_DIR" animation_pro.html

# 3. Encode
echo "Encoding video..."
ffmpeg -framerate 30 -i frames/frame_%06d.png \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  video.mp4 2>&1 | tail -3

# 4. Mix
echo "Mixing audio and video..."
ffmpeg -i video.mp4 -i audio_final.wav \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  "$VIDEOS_DIR/ep${EP}.mp4" 2>&1 | tail -3

# 5. Cleanup
rm -rf frames video.mp4 voice.wav silence.wav audio_final.wav

echo "✓ Done! Output: $VIDEOS_DIR/ep${EP}.mp4"

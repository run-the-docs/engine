#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERIES_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VIDEOS_DIR="$(dirname "$(dirname "$(dirname "$SERIES_DIR")")")/videos/react"
EP="01"

echo "Building React ep${EP}..."
mkdir -p "$VIDEOS_DIR"

# 1. Generate TTS
echo "Generating voice audio..."
NARRATION=$(grep -v "^#" "$SCRIPT_DIR/script.md" | tr '\n' ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
edge-tts -t "$NARRATION" --voice en-US-ChristopherNeural \
  --write-media "$SCRIPT_DIR/voice.mp3" 2>&1 | grep -E "(error|Error)" || true

ffmpeg -i "$SCRIPT_DIR/voice.mp3" -acodec pcm_s16le -ar 44100 \
  "$SCRIPT_DIR/voice.wav" 2>&1 | tail -1

VOICE_DURATION=$(ffprobe -v quiet -show_format "$SCRIPT_DIR/voice.wav" | \
  grep duration | cut -d= -f2 | xargs printf "%.0f")
SILENCE_DURATION=$((90 - VOICE_DURATION))

ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t "$SILENCE_DURATION" \
  -q:a 9 -acodec pcm_s16le "$SCRIPT_DIR/silence.wav" 2>&1 | tail -1

ffmpeg -i "$SCRIPT_DIR/voice.wav" -i "$SCRIPT_DIR/silence.wav" \
  -filter_complex "[0][1]concat=n=2:v=0:a=1" \
  "$SCRIPT_DIR/audio_final.wav" 2>&1 | tail -1

# 2. Render frames
echo "Rendering animation frames..."
python3 "$SCRIPT_DIR/render.py" "$SCRIPT_DIR"

# 3. Encode
echo "Encoding video..."
ffmpeg -framerate 30 -i "$SCRIPT_DIR/frames/frame_%06d.png" \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  "$SCRIPT_DIR/video.mp4" 2>&1 | tail -3

# 4. Mix
echo "Mixing audio and video..."
ffmpeg -i "$SCRIPT_DIR/video.mp4" -i "$SCRIPT_DIR/audio_final.wav" \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  "$VIDEOS_DIR/ep${EP}.mp4" 2>&1 | tail -3

# 5. Cleanup
rm -rf "$SCRIPT_DIR/frames" "$SCRIPT_DIR/video.mp4" \
  "$SCRIPT_DIR/voice.mp3" "$SCRIPT_DIR/voice.wav" \
  "$SCRIPT_DIR/silence.wav" "$SCRIPT_DIR/audio_final.wav"

echo "✓ Done! Output: $VIDEOS_DIR/ep${EP}.mp4"

# Run the Docs — Style Guide

Visual and technical standards for all video series.

## Brand

### Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| Background | `#0a0a0a` | Canvas/page background |
| Gradient 1 | `#1a1a2e` | Background gradient start |
| Gradient 2 | `#16213e` | Background gradient end |
| Accent | `#0f3460` | Boxes, highlights |
| Highlight | `#e94560` | Call-to-action, emphasis (React pink) |
| Text | `#eee` | Body text |
| Code | `#90ee90` | Code syntax (light green) |
| Border | `#444` | Box borders, dividers |

### Typography

- **Body/Headlines:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Code:** `Menlo, Monaco, monospace`
- **Weights:** 400 (normal), 600 (bold)

## Video Specs

| Property | Value |
|----------|-------|
| Resolution | 1920×1080 (16:9) |
| Frame Rate | 30 fps |
| Codec | H.264 (`libx264`, crf=20) |
| Audio Codec | AAC |
| Duration Target | 60–90 seconds per episode |
| Bitrate | ~200 kbps (video) + ~128 kbps (audio) |

## Voice & Audio

### TTS Settings

- **Platform:** macOS `say` command (fallback: OpenClaw TTS / Microsoft Edge TTS)
- **Voice:** Samantha (macOS default, clear and neutral)
- **Rate:** 150 words per minute (`-r 150`)
- **Pitch:** Default
- **Output:** WAV (44100 Hz, mono, PCM s16)

### Background Music

- **Track:** `eco-technology.mp3` or `rewe-bg-music.mp3` (if needed)
- **Volume:** 2.5% of voice level (background only)
- **Mixing:** Voice is primary, music is optional ambient

### Intro/Outro

- **Intro silence:** 2.0 seconds before first word
- **Outro:** "Next episode: [topic]" as final hook
- **No fade-out:** End at natural silence from TTS

## Animation Style

### Canvas Setup

- **Libraries:** HTML5 Canvas + JavaScript (Playwright for rendering)
- **Background:** Linear gradient (135deg, `#1a1a2e` → `#16213e`)
- **Refresh:** Full redraw each frame (30fps)
- **No transitions:** Scenes change at timeline markers, not with fade effects

### Typography in Videos

- **Headline:** 56px, bold, `#eee`
- **Body:** 44–48px, normal, `#eee`
- **Code:** 24px monospace, `#90ee90`
- **Label/annotation:** 32px, `#e94560` (highlight color)

### Code Boxes

- **Background:** `rgba(20, 20, 35, 0.9)` (dark semi-transparent)
- **Border:** 2px `#444`
- **Padding:** 24px
- **Line height:** 32px between code lines
- **Text color:** `#90ee90` (code syntax green)

## Timeline Structure

Each episode follows this pattern:

| Time | Segment | Duration |
|------|---------|----------|
| 0:00–2:00 | Intro fade-in + title | 2s |
| 2:00–n | Body content (scenes, code examples) | ~60s |
| n–1:30 | Recap + next episode hook | ~30s |
| 1:30–end | Fade-out / silence | ~0s |

## Captions (SRT)

- **Language:** English (`en`)
- **Style:** One sentence per subtitle block
- **Timing:** Sync with voice narration ±0.5s
- **Position:** Standard centered bottom placement (auto-rendered by YouTube)
- **Font:** Default YouTube captions (no custom styling in SRT)

## File Naming

All episodes follow this pattern:

```
series/<series-name>/production/ep<NN>/
  script.md          # Narration (plain text, one sentence per line)
  animation.html     # HTML/Canvas source
  style.json         # Config (colors, fonts, timing)
  build.sh           # Bash script to render: `./build.sh` → ../../../ep<NN>.mp4
```

Example:
```
series/react/production/ep01/
  script.md
  animation.html
  style.json
  build.sh          # Outputs to: series/react/../../videos/react/ep01.mp4
```

## Build Process

Each `build.sh` must:

1. Read `script.md` and generate TTS WAV
2. Render HTML canvas to frames using Playwright
3. Encode frames to MP4
4. Mix audio + video
5. Output to `../../videos/<series>/ep<NN>.mp4`

Example:
```bash
#!/bin/bash
cd "$(dirname "$0")"
SERIES="react"
EP="01"

# Generate TTS
say -v Samantha -r 150 -f script.md -o voice.wav

# Render frames (Playwright)
python3 render.py animation.html 1920 1080 30 90 frames/

# Encode + mix
ffmpeg -framerate 30 -i frames/frame_%06d.png -c:v libx264 -crf 20 video.mp4
ffmpeg -i video.mp4 -i voice.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  ../../../videos/${SERIES}/ep${EP}.mp4

# Cleanup
rm -rf frames/ video.mp4 voice.wav
```

## Asset Checklist

Before committing a new episode:

- [ ] `script.md` contains final narration
- [ ] `animation.html` renders at 1920×1080
- [ ] `style.json` defines colors, fonts, timing
- [ ] `build.sh` is executable and tested locally
- [ ] Corresponding `.srt` file exists in `transcripts/`
- [ ] `episodes.md` lists episode with status "Production Assets Ready"

## Rationale

Storing source assets in git enables:
- **Reproducibility:** Re-render videos with the same style if docs change
- **Collaboration:** Multiple people can contribute updates to existing episodes
- **Maintenance:** Long-term archival of production choices
- **Automation:** CI/CD can auto-rebuild all videos when style changes

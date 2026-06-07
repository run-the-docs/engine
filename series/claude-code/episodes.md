# Claude Code — Episodes

## Week 1 (produced)
| Ep | Title | Source doc | Status |
|----|-------|-----------|--------|
| 1 | Your first session | code.claude.com/docs/en/quickstart | produced |
| 2 | The agentic loop | code.claude.com/docs/en/common-workflows | produced |
| 3 | CLAUDE.md memory | code.claude.com/docs/en/memory | produced |
| 4 | Plan mode | code.claude.com/docs/en/permission-modes | produced |
| 5 | Slash commands | code.claude.com/docs/en/slash-commands | produced |

Full 54-episode season in `plan.md`.

## Production
Reproducible on the Mac Mini: `production/build-ep.sh <N>` runs `narrate_chatterbox.py` (Chatterbox TTS) → `make_assets_45.py` (PIL header/captions) → `compose_45.py` (ffmpeg 4:5 composite). Each episode = `ep<N>.lines.json` (script) + `record-ep<N>.sh` (real claude session capture via asciinema/tmux).

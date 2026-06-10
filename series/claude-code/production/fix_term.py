#!/usr/bin/env python3
"""fix_term.py <gif> <out_term_mp4>

Rebuild the terminal video from a recorded asciinema gif, dropping the trailing
tmux-teardown frame(s) ("[terminated]" on a cleared screen) that otherwise become
the video's last frame. Robust: detects teardown frames by low content (not a fixed
index), so it works for short headless demos and long interactive ones alike, and is
a no-op-ish passthrough if the recording already ends on a content frame.
"""
import sys, subprocess, os, glob, tempfile
from PIL import Image

FF = '/opt/homebrew/bin/ffmpeg'
gif, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp(prefix='fixterm_')

subprocess.run([FF, '-y', '-i', gif, '-vsync', '0', os.path.join(tmp, 'f_%04d.png')],
               capture_output=True)
frames = sorted(glob.glob(os.path.join(tmp, 'f_*.png')))

if len(frames) <= 1:
    subprocess.run([FF, '-y', '-i', gif, '-vf',
                    'scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
                   capture_output=True)
    print('fix_term: <=1 frame, passthrough'); sys.exit(0)

# content score = count of non-near-black pixels on a downsampled grayscale frame
def score(p):
    im = Image.open(p).convert('L').resize((120, 160))
    return sum(1 for v in im.getdata() if v > 45)

scores = [score(f) for f in frames]
mx = max(scores) or 1
thresh = mx * 0.18                      # teardown frames ([terminated] on black) fall well below this
last_good = 0
for i in range(len(frames) - 1, -1, -1):
    if scores[i] >= thresh:
        last_good = i
        break
kept = frames[:last_good + 1]

# adaptive per-frame duration so the term lands near a typical narration length,
# instead of a fixed 0.4s that makes long demos overshoot (fast termSpeed) and
# short ones undershoot (slow termSpeed). Compose still fits term->narration.
HOLD = 2.5
TARGET = 17.0
per = (TARGET - HOLD) / max(len(kept), 1)
per = max(0.12, min(per, 0.9))
listf = os.path.join(tmp, 'list.txt')
with open(listf, 'w') as fh:
    for f in kept:
        fh.write("file '%s'\nduration %.3f\n" % (f, per))
    fh.write("file '%s'\nduration %.3f\n" % (kept[-1], HOLD))   # hold the final good frame
    fh.write("file '%s'\n" % kept[-1])

subprocess.run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', listf,
                '-vf', 'fps=12,scale=trunc(iw/2)*2:trunc(ih/2)*2',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
               capture_output=True)

print('fix_term: %d frames -> kept %d (dropped %d trailing teardown), last_good_score=%d max=%d'
      % (len(frames), len(kept), len(frames) - len(kept), scores[last_good], mx))

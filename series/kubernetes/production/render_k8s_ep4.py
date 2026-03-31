#!/usr/bin/env python3
"""Render K8s Ep4: Deployments frames using Playwright."""
import os, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_FILE = '/tmp/k8s_ep4.html'
OUT_DIR = '/tmp/k8s_ep4_frames'
TIMING_FILE = '/tmp/k8s_ep4_timing.json'
BATCH_SIZE = 300
W, H = 1920, 1080
CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

os.makedirs(OUT_DIR, exist_ok=True)

# Load total frames from timing
with open(TIMING_FILE) as f:
    timing = json.load(f)
TOTAL_FRAMES = timing['total_frames_30fps']
print(f"Total frames to render: {TOTAL_FRAMES}")

file_url = f"file://{HTML_FILE}"

def get_last_frame():
    existing = sorted(Path(OUT_DIR).glob('frame_*.png'))
    if existing:
        return int(existing[-1].stem.split('_')[1])
    return -1

total_start = time.time()
frame = get_last_frame() + 1
print(f"Starting from frame {frame}")

while frame < TOTAL_FRAMES:
    batch_end = min(frame + BATCH_SIZE, TOTAL_FRAMES)
    print(f"\nBatch: {frame}-{batch_end-1} ({batch_end-frame} frames)")
    batch_start_t = time.time()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=CHROME_PATH,
                args=['--no-sandbox','--disable-setuid-sandbox','--disable-gpu',
                      '--disable-dev-shm-usage','--disable-extensions',
                      '--no-default-browser-check','--no-first-run'],
                headless=True,
                timeout=30000,
            )
            context = browser.new_context(viewport={'width': W, 'height': H})
            page = context.new_page()
            page.goto(file_url, wait_until='networkidle', timeout=30000)
            time.sleep(2.0)  # wait for fonts/images
            page.wait_for_function("typeof window.renderFrame === 'function'", timeout=10000)
            canvas_el = page.locator('#c')

            for f in range(frame, batch_end):
                out_path = os.path.join(OUT_DIR, f'frame_{f:06d}.png')

                # 5 boundary checks
                for attempt in range(5):
                    try:
                        page.evaluate(f'window.renderFrame({f})')
                        data_url = page.evaluate('document.getElementById("c").toDataURL("image/png")')
                        if not data_url or not data_url.startswith('data:image/png'):
                            raise ValueError(f"Bad data URL at frame {f}")
                        import base64
                        b64 = data_url.split(',', 1)[1]
                        with open(out_path, 'wb') as fh:
                            fh.write(base64.b64decode(b64))
                        break
                    except Exception as e:
                        if attempt < 4:
                            print(f"  Retry {attempt+1} frame {f}: {e}")
                            time.sleep(0.5)
                        else:
                            raise

                if f % 90 == 0:
                    elapsed = time.time() - batch_start_t
                    done = f - frame + 1
                    fps_rate = done / elapsed if elapsed > 0 else 0
                    remaining = (TOTAL_FRAMES - f) / fps_rate if fps_rate > 0 else 0
                    print(f"  Frame {f}/{TOTAL_FRAMES} | {fps_rate:.1f} fps | ~{remaining/60:.1f}min left")

            browser.close()

    except Exception as e:
        print(f"Batch error: {e}")
        print("Retrying in 5s...")
        time.sleep(5)
        continue

    frame = get_last_frame() + 1
    batch_elapsed = time.time() - batch_start_t
    print(f"Batch done in {batch_elapsed:.1f}s")

total_elapsed = time.time() - total_start
print(f"\nAll {TOTAL_FRAMES} frames rendered in {total_elapsed/60:.1f}min")
print(f"Output: {OUT_DIR}")

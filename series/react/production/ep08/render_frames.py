import base64, json
from pathlib import Path
from playwright.sync_api import sync_playwright

with open('timing.json') as f:
    timing = json.load(f)
total_frames = timing['total_frames_30fps']

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(f"file://{Path('ep08.html').resolve()}")
    pg.wait_for_load_state("networkidle")
    Path('frames').mkdir(exist_ok=True)
    for fn in range(total_frames):
        if fn % 500 == 0: print(f"{fn}/{total_frames}...", flush=True)
        du = pg.evaluate(f"() => {{ window.renderFrame({fn}); return document.getElementById('c').toDataURL('image/png'); }}")
        Path(f'frames/frame_{fn:06d}.png').write_bytes(base64.b64decode(du.split(',')[1]))
    b.close()
print("Done")

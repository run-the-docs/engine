#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64

script_dir = Path(sys.argv[1]).resolve()
html_name = sys.argv[2] if len(sys.argv) > 2 else "animation.html"
html_file = script_dir / html_name
frames_dir = script_dir / "frames"
frames_dir.mkdir(exist_ok=True)

# Read timing.json to get correct frame count
timing_file = script_dir / "timing.json"
with open(timing_file, 'r') as f:
    timing = json.load(f)
total_frames = timing['total_frames_30fps']

print(f"Rendering {total_frames} frames to match audio duration...")

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
print(f"✓ Rendered {total_frames} frames")

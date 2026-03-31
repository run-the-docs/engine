#!/usr/bin/env python3
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64

script_dir = Path(sys.argv[1]).resolve()
html_file = script_dir / "animation.html"
frames_dir = script_dir / "frames"
frames_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(f"file://{html_file}")
    page.wait_for_load_state("networkidle")
    
    for frame_num in range(2700):
        if frame_num % 300 == 0:
            print(f"  Frame {frame_num}/2700...")
        
        data_url = page.evaluate(f'''() => {{
            window.renderFrame({frame_num});
            return document.getElementById('c').toDataURL('image/png');
        }}''')
        
        png_data = base64.b64decode(data_url.split(',')[1])
        frame_path = frames_dir / f"frame_{frame_num:06d}.png"
        frame_path.write_bytes(png_data)
    
    browser.close()
print(f"✓ Rendered 2700 frames")

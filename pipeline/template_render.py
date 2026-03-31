#!/usr/bin/env python3
"""
Template render script for Run the Docs episodes.

USAGE:
1. Copy this file to series/<name>/production/ep<NN>/render.py
2. Run after build.py: python3 render.py
3. Reads timing.json to determine exact frame count
4. Uses Playwright to render HTML canvas to PNG frames
5. Outputs: frames/ directory with frame_000000.png, frame_000001.png, etc.

CRITICAL: Uses canvas.toDataURL() inside page.evaluate(), NOT page.screenshot()
This ensures canvas paint completes before capture.
"""

import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64

# Read timing.json to get exact frame count
try:
    with open('timing.json', 'r') as f:
        timing = json.load(f)
except FileNotFoundError:
    print("ERROR: timing.json not found. Run tts.py first.")
    sys.exit(1)

total_frames = timing['total_frames_30fps']
print(f"Rendering {total_frames} frames from timing.json ({timing['total_duration']}s @ 30fps)...")

frames_dir = Path('frames')
frames_dir.mkdir(exist_ok=True)

html_file = Path('animation.html')
if not html_file.exists():
    print(f"ERROR: {html_file} not found. Run build.py first.")
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    # Load HTML
    page.goto(f"file://{html_file.resolve()}")
    page.wait_for_load_state("networkidle")
    
    # Wait for canvas + renderFrame function
    page.wait_for_function("() => typeof window.renderFrame === 'function'", timeout=15000)
    
    # Render frames
    for frame_num in range(total_frames):
        if frame_num % 300 == 0:
            print(f"  Frame {frame_num}/{total_frames}...")
        
        # CRITICAL: Use canvas.toDataURL() inside evaluate, NOT page.screenshot()
        data_url = page.evaluate(f'''() => {{
            window.renderFrame({frame_num});
            return document.getElementById('c').toDataURL('image/png');
        }}''')
        
        # Decode base64 and save
        png_data = base64.b64decode(data_url.split(',')[1])
        frame_path = frames_dir / f"frame_{frame_num:06d}.png"
        frame_path.write_bytes(png_data)
    
    browser.close()

print(f"✓ Rendered {total_frames} frames to {frames_dir}/")

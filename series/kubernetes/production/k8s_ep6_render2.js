#!/usr/bin/env node
/**
 * Render k8s_ep6.html - checkpoint render from frame 1290
 */
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const TIMING_FILE = '/tmp/k8s_ep6_timing.json';
const timing = JSON.parse(fs.readFileSync(TIMING_FILE, 'utf8'));
const TOTAL_FRAMES = timing.total_frames_30fps;
const OUT_DIR = '/tmp/k8s_ep6_frames';

const START_FRAME = parseInt(process.argv[2] || '1290');

fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  console.log(`Rendering frames ${START_FRAME}-${TOTAL_FRAMES} to ${OUT_DIR}...`);
  
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });

  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  const htmlPath = `file:///tmp/k8s_ep6.html`;
  await page.goto(htmlPath, { waitUntil: 'networkidle', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));
  await page.waitForFunction(() => typeof window.renderFrame === 'function', { timeout: 15000 });

  await page.evaluate(({ segs, totalDur }) => {
    window.setTiming(segs, totalDur);
  }, { segs: timing.segments, totalDur: timing.total_duration });

  console.log('Starting render...');
  const t0 = Date.now();
  const BATCH = 30;

  for (let f = START_FRAME; f < TOTAL_FRAMES; f += BATCH) {
    const batchEnd = Math.min(f + BATCH, TOTAL_FRAMES);
    
    const dataUrls = await page.evaluate(({ start, end }) => {
      const results = [];
      const canvas = document.getElementById('c');
      for (let i = start; i < end; i++) {
        window.renderFrame(i);
        results.push(canvas.toDataURL('image/png'));
      }
      return results;
    }, { start: f, end: batchEnd });

    for (let i = 0; i < dataUrls.length; i++) {
      const frameNum = f + i;
      const dataUrl = dataUrls[i];
      const base64Data = dataUrl.replace(/^data:image\/png;base64,/, '');
      const buffer = Buffer.from(base64Data, 'base64');
      const filename = path.join(OUT_DIR, `frame_${String(frameNum).padStart(6, '0')}.png`);
      fs.writeFileSync(filename, buffer);
    }

    if (f % 300 === 0) {
      const elapsed = (Date.now() - t0) / 1000;
      const pct = Math.round((f - START_FRAME) / (TOTAL_FRAMES - START_FRAME) * 100);
      console.log(`  ${pct}% (frame ${f}/${TOTAL_FRAMES}) elapsed=${elapsed.toFixed(1)}s`);
    }
  }

  const elapsed = (Date.now() - t0) / 1000;
  console.log(`\nRender complete in ${elapsed.toFixed(1)}s`);
  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });

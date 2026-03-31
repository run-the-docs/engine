#!/usr/bin/env node
/**
 * Render k8s_ep8.html using Playwright + canvas.toDataURL()
 * MANDATORY: canvas.toDataURL() ONLY — never page.screenshot()
 */
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const TIMING_FILE = '/tmp/k8s_ep8_timing.json';
const timing = JSON.parse(fs.readFileSync(TIMING_FILE, 'utf8'));
const TOTAL_FRAMES = timing.total_frames_30fps;
const OUT_DIR = '/tmp/k8s_ep8_frames';

fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  console.log(`Rendering ${TOTAL_FRAMES} frames to ${OUT_DIR}...`);

  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });

  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  const htmlPath = 'file:///tmp/k8s_ep8.html';
  await page.goto(htmlPath, { waitUntil: 'networkidle', timeout: 30000 });

  // Wait 2000ms after page load for font/image loading
  await new Promise(r => setTimeout(r, 2000));

  await page.waitForFunction(() => typeof window.renderFrame === 'function', { timeout: 15000 });

  // Inject timing data
  await page.evaluate(({ segs, totalDur }) => {
    window.setTiming(segs, totalDur);
  }, { segs: timing.segments, totalDur: timing.total_duration });

  // 5 boundary checks
  console.log('Verifying 5 scene boundaries...');
  const checks = [
    { frame: 0,    label: 't=0s  → hook scene (dark bg)' },
    { frame: 300,  label: 't=10s → problem scene' },
    { frame: 550,  label: 't=18s → PV+PVC binding' },
    { frame: 1180, label: 't=39s → access modes' },
    { frame: 1550, label: 't=51s → payoff' },
  ];

  for (const check of checks) {
    const result = await page.evaluate((frameNum) => {
      window.renderFrame(frameNum);
      const canvas = document.getElementById('c');
      const ctx = canvas.getContext('2d');
      const center = ctx.getImageData(960, 540, 1, 1).data;
      const top    = ctx.getImageData(100, 100, 1, 1).data;
      return {
        isBlack: center[0] < 5 && center[1] < 5 && center[2] < 5,
        r: center[0], g: center[1], b: center[2],
        tr: top[0], tg: top[1], tb: top[2],
      };
    }, check.frame);
    const status = result.isBlack ? '⚠️ BLACK' : '✓ OK';
    console.log(`  ${check.label}: center=rgb(${result.r},${result.g},${result.b}) ${status}`);
  }

  console.log('\nStarting full render...');
  const t0 = Date.now();
  const BATCH = 30;

  for (let f = 0; f < TOTAL_FRAMES; f += BATCH) {
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
      const base64Data = dataUrls[i].replace(/^data:image\/png;base64,/, '');
      const buffer = Buffer.from(base64Data, 'base64');
      const filename = path.join(OUT_DIR, `frame_${String(frameNum).padStart(6, '0')}.png`);
      fs.writeFileSync(filename, buffer);
    }

    if (f % 300 === 0) {
      const elapsed = (Date.now() - t0) / 1000;
      const pct = Math.round(f / TOTAL_FRAMES * 100);
      console.log(`  ${pct}% (frame ${f}/${TOTAL_FRAMES}) elapsed=${elapsed.toFixed(1)}s`);
    }
  }

  const elapsed = (Date.now() - t0) / 1000;
  console.log(`\nRender complete: ${TOTAL_FRAMES} frames in ${elapsed.toFixed(1)}s`);
  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });

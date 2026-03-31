#!/usr/bin/env node
/**
 * Render k8s_ep1.html using Playwright + canvas.toDataURL()
 * MANDATORY: canvas.toDataURL() ONLY — never page.screenshot()
 */
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const TIMING_FILE = '/tmp/k8s_ep1_timing.json';
const timing = JSON.parse(fs.readFileSync(TIMING_FILE, 'utf8'));
const TOTAL_FRAMES = timing.total_frames_30fps;
const OUT_DIR = '/tmp/k8s_ep1_frames';

fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  console.log(`Rendering ${TOTAL_FRAMES} frames to ${OUT_DIR}...`);
  
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });

  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  const htmlPath = `file:///tmp/k8s_ep1.html`;
  await page.goto(htmlPath, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForFunction(() => typeof window.renderFrame === 'function', { timeout: 15000 });

  // Inject timing data
  await page.evaluate(({ segs, totalDur }) => {
    window.setTiming(segs, totalDur);
  }, { segs: timing.segments, totalDur: timing.total_duration });

  // Verify 5 scene boundaries before full render
  console.log('Verifying scene boundaries...');
  const checks = [
    { frame: 0,   label: 't=0 → near-black' },
    { frame: 63,  label: 't=2.1 → hook scene non-black' },
    { frame: 360, label: 't=12 → three eras scene' },
    { frame: 720, label: 't=24 → K8s logo drawing' },
    { frame: 2133, label: 't=71.1 → desired state scene' },
  ];

  for (const check of checks) {
    const result = await page.evaluate((frameNum) => {
      window.renderFrame(frameNum);
      const canvas = document.getElementById('c');
      const dataUrl = canvas.toDataURL('image/png');
      // Check if non-black by sampling a pixel
      const ctx = canvas.getContext('2d');
      const pixel = ctx.getImageData(960, 540, 1, 1).data;
      return { 
        isBlack: pixel[0] < 5 && pixel[1] < 5 && pixel[2] < 5,
        r: pixel[0], g: pixel[1], b: pixel[2]
      };
    }, check.frame);
    console.log(`  ${check.label}: pixel(960,540)=rgb(${result.r},${result.g},${result.b}) ${result.isBlack ? '⚠️ BLACK' : '✓ OK'}`);
  }

  console.log('\nStarting full render...');
  const t0 = Date.now();
  const BATCH = 30; // Process 30 frames per batch

  for (let f = 0; f < TOTAL_FRAMES; f += BATCH) {
    const batchEnd = Math.min(f + BATCH, TOTAL_FRAMES);
    
    // Render batch and get all dataURLs
    const dataUrls = await page.evaluate(({ start, end }) => {
      const results = [];
      const canvas = document.getElementById('c');
      for (let i = start; i < end; i++) {
        window.renderFrame(i);
        results.push(canvas.toDataURL('image/png'));
      }
      return results;
    }, { start: f, end: batchEnd });

    // Save frames
    for (let i = 0; i < dataUrls.length; i++) {
      const frameNum = f + i;
      const base64 = dataUrls[i].replace('data:image/png;base64,', '');
      const buf = Buffer.from(base64, 'base64');
      const fname = path.join(OUT_DIR, `frame_${String(frameNum).padStart(6, '0')}.png`);
      fs.writeFileSync(fname, buf);
    }

    if (f % 300 === 0) {
      const elapsed = (Date.now() - t0) / 1000;
      const fps = f > 0 ? f / elapsed : 0;
      const eta = f > 0 ? (TOTAL_FRAMES - f) / fps : 0;
      console.log(`Frame ${f}/${TOTAL_FRAMES} (${(f/TOTAL_FRAMES*100).toFixed(1)}%) | ${fps.toFixed(1)} fps | ETA: ${eta.toFixed(0)}s`);
    }
  }

  await browser.close();
  const elapsed = (Date.now() - t0) / 1000;
  console.log(`\nDone! ${TOTAL_FRAMES} frames in ${elapsed.toFixed(1)}s (${(TOTAL_FRAMES/elapsed).toFixed(1)} fps)`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});

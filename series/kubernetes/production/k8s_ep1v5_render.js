#!/usr/bin/env node
/**
 * Render k8s_ep1v5.html using Playwright + canvas.toDataURL()
 * MANDATORY: canvas.toDataURL() ONLY — never page.screenshot()
 * Text-fix version: no ellipsis truncation in captions
 */
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const TIMING_FILE = '/tmp/k8s_ep1_timing.json';
const timing = JSON.parse(fs.readFileSync(TIMING_FILE, 'utf8'));
const TOTAL_FRAMES = timing.total_frames_30fps;
const OUT_DIR = '/tmp/k8s_ep1v5_frames';

fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  console.log(`Rendering ${TOTAL_FRAMES} frames to ${OUT_DIR}...`);
  
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });

  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  const htmlPath = `file:///tmp/k8s_ep1v5.html`;
  await page.goto(htmlPath, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForFunction(() => typeof window.renderFrame === 'function', { timeout: 15000 });

  // Wait for logo image to load (2s as required)
  console.log('Waiting for K8s logo to load...');
  await page.waitForTimeout(2000);
  
  const logoStatus = await page.evaluate(() => ({
    loaded: window.logoLoaded,
    naturalWidth: window.k8sLogo ? window.k8sLogo.naturalWidth : 0,
  }));
  console.log(`Logo loaded: ${logoStatus.loaded}, naturalWidth: ${logoStatus.naturalWidth}`);

  // Inject timing data
  await page.evaluate(({ segs, totalDur }) => {
    window.setTiming(segs, totalDur);
  }, { segs: timing.segments, totalDur: timing.total_duration });

  // Verify 5 scene boundaries before full render
  console.log('Verifying scene boundaries...');
  const checks = [
    { frame: 0,    label: 't=0 → dark intro' },
    { frame: 63,   label: 't=2.1 → hook scene active' },
    { frame: 360,  label: 't=12 → three eras scene' },
    { frame: 720,  label: 't=24 → K8s logo (real PNG)' },
    { frame: 2520, label: 't=84 → outro + URL pills' },
  ];

  for (const check of checks) {
    const result = await page.evaluate((frameNum) => {
      window.renderFrame(frameNum);
      const canvas = document.getElementById('c');
      const ctx = canvas.getContext('2d');
      const pixel = ctx.getImageData(960, 540, 1, 1).data;
      const topPx = ctx.getImageData(100, 100, 1, 1).data;
      return { 
        isBlack: pixel[0] < 5 && pixel[1] < 5 && pixel[2] < 5,
        r: pixel[0], g: pixel[1], b: pixel[2],
        tr: topPx[0], tg: topPx[1], tb: topPx[2]
      };
    }, check.frame);
    console.log(`  ${check.label}: center=rgb(${result.r},${result.g},${result.b}) top=rgb(${result.tr},${result.tg},${result.tb}) ${result.isBlack ? '⚠️ BLACK' : '✓ OK'}`);
  }

  // Check caption text rendering (verify no ellipsis)
  console.log('Checking caption text fix...');
  const captionCheck = await page.evaluate(() => {
    // Find a timing segment and test it
    window.renderFrame(30); // t=1s
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    // Check bottom area for caption
    const bottomPx = ctx.getImageData(960, 990, 1, 1).data;
    return { r: bottomPx[0], g: bottomPx[1], b: bottomPx[2] };
  });
  console.log(`  Caption area at t=1s: rgb(${captionCheck.r},${captionCheck.g},${captionCheck.b})`);

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

    // Save frames
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
      const pct = Math.round(f / TOTAL_FRAMES * 100);
      console.log(`  ${pct}% (frame ${f}/${TOTAL_FRAMES}) elapsed=${elapsed.toFixed(1)}s`);
    }
  }

  await browser.close();
  console.log(`\nDone! ${TOTAL_FRAMES} frames written to ${OUT_DIR}`);
}

main().catch(err => { console.error(err); process.exit(1); });

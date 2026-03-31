#!/usr/bin/env node
// Render k8s_ep3.html to PNG frames using puppeteer-core + local Chrome
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const FRAMES_DIR = '/tmp/k8s_ep3_frames';
const HTML_FILE = '/tmp/k8s_ep3.html';
const TOTAL_FRAMES = 2160; // 72s @ 30fps

// Chrome executable path
const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

fs.mkdirSync(FRAMES_DIR, { recursive: true });

// Check existing frames to resume
let startFrame = 0;
try {
  const existing = fs.readdirSync(FRAMES_DIR).filter(f => f.endsWith('.png')).sort();
  if (existing.length > 0) {
    startFrame = Math.max(0, parseInt(existing[existing.length-1].match(/(\d+)/)[0]) - 2);
  }
} catch(e) {}

console.log(`Rendering frames ${startFrame} to ${TOTAL_FRAMES-1}`);

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
      '--disable-web-security',
      '--allow-file-access-from-files',
      '--force-device-scale-factor=1',
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  await page.goto(`file://${HTML_FILE}`, { waitUntil: 'load' });
  await new Promise(r => setTimeout(r, 2000));

  // Check TOTAL_FRAMES matches
  const totalF = await page.evaluate(() => window.TOTAL_FRAMES);
  console.log(`HTML reports ${totalF} total frames`);

  let lastLog = Date.now();
  let batchStart = Date.now();

  for (let frame = startFrame; frame < TOTAL_FRAMES; frame++) {
    const dataUrl = await page.evaluate((f) => {
      return window.renderFrame(f);
    }, frame);

    const base64 = dataUrl.slice('data:image/png;base64,'.length);
    const buffer = Buffer.from(base64, 'base64');
    const fileName = `frame_${String(frame).padStart(6, '0')}.png`;
    fs.writeFileSync(path.join(FRAMES_DIR, fileName), buffer);

    if (Date.now() - lastLog > 5000) {
      const pct = ((frame / TOTAL_FRAMES) * 100).toFixed(1);
      const fps = Math.round((frame - startFrame + 1) / ((Date.now() - batchStart) / 1000));
      console.log(`Frame ${frame}/${TOTAL_FRAMES} (${pct}%) @ ${fps}fps`);
      lastLog = Date.now();
    }
  }

  await browser.close();
  console.log(`DONE: ${TOTAL_FRAMES} frames rendered to ${FRAMES_DIR}`);
})().catch(err => {
  console.error('FATAL:', err.message);
  console.error(err.stack);
  process.exit(1);
});

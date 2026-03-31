const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const FRAMES_DIR = '/tmp/k8s_ep9_frames';
const HTML_FILE = 'file:///tmp/k8s_ep9.html';
const TOTAL_DURATION = 75.588;
const FPS = 30;
const TOTAL_FRAMES = Math.ceil(TOTAL_DURATION * FPS);

if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });

(async () => {
  console.log(`Rendering ${TOTAL_FRAMES} frames at ${FPS}fps...`);
  
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security',
           '--allow-file-access-from-files', '--font-render-hinting=none'],
    defaultViewport: { width: 1920, height: 1080 },
  });

  const page = await browser.newPage();
  page.on('console', msg => { if (msg.type() === 'error') console.error('PAGE ERR:', msg.text()); });
  
  await page.goto(HTML_FILE, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 2000));

  // Verify boundary frames first
  const checkFrames = [0, 60, 675, 1125, 1800, 2050, TOTAL_FRAMES - 1];
  console.log('Verifying boundary frames...');
  for (const f of checkFrames) {
    const dataURL = await page.evaluate((frame) => {
      window.renderFrame(frame);
      return document.getElementById('c').toDataURL('image/png');
    }, f);
    const b64 = dataURL.replace('data:image/png;base64,', '');
    const buf = Buffer.from(b64, 'base64');
    const fpath = path.join(FRAMES_DIR, `verify_frame_${String(f).padStart(6,'0')}.png`);
    fs.writeFileSync(fpath, buf);
    console.log(`  Verified frame ${f}: ${buf.length} bytes`);
  }

  console.log('Rendering all frames...');
  const t0 = Date.now();
  
  for (let frame = 0; frame < TOTAL_FRAMES; frame++) {
    const dataURL = await page.evaluate((f) => {
      window.renderFrame(f);
      return document.getElementById('c').toDataURL('image/png');
    }, frame);
    
    const b64 = dataURL.replace('data:image/png;base64,', '');
    const buf = Buffer.from(b64, 'base64');
    const fname = `frame_${String(frame).padStart(6,'0')}.png`;
    fs.writeFileSync(path.join(FRAMES_DIR, fname), buf);
    
    if (frame % 150 === 0) {
      const elapsed = (Date.now() - t0) / 1000;
      const fps_actual = frame / elapsed;
      const remaining = (TOTAL_FRAMES - frame) / fps_actual;
      console.log(`  Frame ${frame}/${TOTAL_FRAMES} | ${fps_actual.toFixed(1)} fps | ~${remaining.toFixed(0)}s left`);
    }
  }

  await browser.close();
  const elapsed = (Date.now() - t0) / 1000;
  console.log(`Done! ${TOTAL_FRAMES} frames in ${elapsed.toFixed(1)}s`);
})();

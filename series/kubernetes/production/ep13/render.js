#!/usr/bin/env node
/**
 * Render ep13 Short animation — portrait 1080x1920
 * MANDATORY: canvas.toDataURL() only — never page.screenshot()
 */
const { chromium } = require('/Users/claude/.openclaw/workspace/node_modules/playwright');
const fs   = require('fs');
const path = require('path');

const TIMING_FILE = path.join(__dirname, 'timing.json');
const HTML_FILE   = path.join(__dirname, 'animation.html');
const OUT_DIR     = '/tmp/ep13_frames';

const timing      = JSON.parse(fs.readFileSync(TIMING_FILE, 'utf8'));
const TOTAL_FRAMES = timing.total_frames_30fps;

fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
    console.log(`Rendering ${TOTAL_FRAMES} frames → ${OUT_DIR}`);
    console.log(`Duration: ${timing.total_duration.toFixed(2)}s @ 30fps`);

    const browser = await chromium.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    });

    const page = await browser.newPage();
    await page.setViewportSize({ width: 1080, height: 1920 });

    await page.goto(`file://${HTML_FILE}`, { waitUntil: 'networkidle', timeout: 30000 });
    await new Promise(r => setTimeout(r, 2500)); // font load

    await page.waitForFunction(() => typeof window.renderFrame === 'function', { timeout: 15000 });

    // Inject timing
    await page.evaluate(({ segs, dur }) => {
        window.setTiming(segs, dur);
    }, { segs: timing.segments, dur: timing.total_duration });

    // Verify 5 boundary frames
    console.log('\nVerifying scene boundaries...');
    const checks = [
        { fn:    0, label: 't=0  hook' },
        { fn:   90, label: 't=3  labels' },
        { fn:  450, label: 't=15 examples' },
        { fn:  840, label: 't=28 eq-selectors' },
        { fn: 1200, label: 't=40 set-selectors' },
        { fn: 1400, label: 't=46 payoff' },
        { fn: 1700, label: 't=57 outro' },
    ];
    for (const c of checks) {
        const px = await page.evaluate((fn) => {
            window.renderFrame(fn);
            const ctx = document.getElementById('c').getContext('2d');
            const d = ctx.getImageData(540, 960, 1, 1).data;
            return { r: d[0], g: d[1], b: d[2] };
        }, c.fn);
        const isBlack = px.r < 5 && px.g < 5 && px.b < 5;
        console.log(`  f${String(c.fn).padStart(4)} ${c.label}: rgb(${px.r},${px.g},${px.b}) ${isBlack ? '⚠ BLACK' : '✓'}`);
    }

    // Full render in batches of 30
    console.log('\nStarting full render...');
    const t0 = Date.now();
    const BATCH = 30;

    for (let f = 0; f < TOTAL_FRAMES; f += BATCH) {
        const end = Math.min(f + BATCH, TOTAL_FRAMES);

        const dataUrls = await page.evaluate(({ start, end }) => {
            const results = [];
            const c = document.getElementById('c');
            for (let i = start; i < end; i++) {
                window.renderFrame(i);
                results.push(c.toDataURL('image/png'));
            }
            return results;
        }, { start: f, end });

        for (let i = 0; i < dataUrls.length; i++) {
            const fn  = f + i;
            const buf = Buffer.from(dataUrls[i].replace(/^data:image\/png;base64,/, ''), 'base64');
            fs.writeFileSync(path.join(OUT_DIR, `frame_${String(fn).padStart(6, '0')}.png`), buf);
        }

        if (f % 300 === 0) {
            const elapsed = (Date.now() - t0) / 1000;
            const fps = f > 0 ? f / elapsed : 0;
            const eta = fps > 0 ? (TOTAL_FRAMES - f) / fps : '?';
            process.stdout.write(`\r  Frame ${f}/${TOTAL_FRAMES} | ${fps.toFixed(1)} fps | ETA ${typeof eta === 'number' ? eta.toFixed(0) + 's' : eta}   `);
        }
    }

    const elapsed = (Date.now() - t0) / 1000;
    console.log(`\n\nDone! ${TOTAL_FRAMES} frames in ${elapsed.toFixed(1)}s (${(TOTAL_FRAMES/elapsed).toFixed(1)} fps avg)`);
    await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });

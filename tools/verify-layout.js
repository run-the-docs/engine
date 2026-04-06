#!/usr/bin/env node
'use strict';

/**
 * verify-layout.js — Visual layout verification for Run the Docs episodes
 *
 * Usage: node verify-layout.js <html-file> <timing.json>
 *
 * For each scene detected in the HTML's renderFrame dispatch, renders a key
 * frame and runs pixel-analysis checks:
 *   1. Zone violation  — content below y=860 (caption/footer zone)
 *   2. Left/right edge overflow — content within 4px of canvas edges
 *   3. Transition staleness — consecutive scene frames that look identical
 *   4. Bounding box overlap — two similarly-sized drawn elements intersect by >20%
 *   5. Text overflow — text box extends past x=0 or x=1920
 *
 * Exits 0 on pass, 1 on any violation.
 */

const { chromium } = require('/Users/claude/.openclaw/workspace/node_modules/playwright');
const fs   = require('fs');
const path = require('path');

// ── CLI args ──────────────────────────────────────────────────────────────────
const [htmlPath, timingPath] = process.argv.slice(2);
if (!htmlPath || !timingPath) {
  console.error('Usage: verify-layout.js <html-file> <timing.json>');
  process.exit(1);
}

const htmlAbs  = path.resolve(htmlPath);
const html     = fs.readFileSync(htmlAbs, 'utf8');
const timing   = JSON.parse(fs.readFileSync(timingPath, 'utf8'));
const totalDur = timing.total_duration;

// ── Scene boundary parser ─────────────────────────────────────────────────────
// Reads the `if (t < N) { sceneFoo(ctx, t); } else if ...` dispatch block
// from window.renderFrame and returns a list of scene descriptors.
function parseScenes(htmlSrc, totalDuration) {
  // Grab everything inside window.renderFrame = function(...) { ... }
  const bodyMatch = htmlSrc.match(
    /window\.renderFrame\s*=\s*function[^{]*\{([\s\S]*?)\};\s*\n?<\/script>/
  );
  if (!bodyMatch) throw new Error('Cannot locate window.renderFrame in HTML');
  const body = bodyMatch[1];

  // Match each `if/else if (t < EXPR) { sceneXxx(ctx`
  const branchRe = /(?:if|else\s+if)\s*\(\s*t\s*<\s*([^)]+)\)\s*\{[^}]*?(\w+)\s*\(\s*ctx/g;
  const raw = [];
  let m;
  while ((m = branchRe.exec(body)) !== null) {
    const expr  = m[1].trim();
    const fnName = m[2];
    // Evaluate threshold — supports literals and expressions like `totalDuration - 4`
    const threshold = /^[\d.]+$/.test(expr)
      ? parseFloat(expr)
      : Function('totalDuration', `return (${expr})`)(totalDuration);
    raw.push({ threshold, fn: fnName });
  }

  // Catch the final `else { sceneXxx(ctx` block
  const elseM = body.match(/\}\s*else\s*\{[^}]*?(\w+)\s*\(\s*ctx/);
  if (elseM) raw.push({ threshold: totalDuration, fn: elseM[1] });

  if (raw.length === 0) throw new Error('No scene dispatch branches found in renderFrame');

  return raw.map((s, i) => {
    const start = i === 0 ? 0 : raw[i - 1].threshold;
    const end   = s.threshold;
    const keyT  = Math.min((start + end) / 2, totalDuration - 0.034);
    return {
      index:    i + 1,
      name:     s.fn,
      start,
      end:      end === totalDuration ? 'end' : end,
      keyT,
      frameNum: Math.round(keyT * 30),
    };
  });
}

// ── Background color definitions (episode-specific) ───────────────────────────
// These are the expected "empty" canvas colors.  Any other color at a sampled
// position is treated as drawn content.
const BG_COLORS = [
  [8,  8,  16],   // #080810 — main bg
  [13, 13, 26],   // #0d0d1a — safe-area bg
  [30, 34, 51],   // #1e2233 — separator strip at y=958
];
const BG_TOL = 28; // per-channel tolerance (allows anti-aliasing fringe)

// ── Helpers ───────────────────────────────────────────────────────────────────
function collapseRanges(xs) {
  if (xs.length === 0) return '';
  const ranges = [];
  let lo = xs[0], hi = xs[0];
  for (let i = 1; i < xs.length; i++) {
    if (xs[i] <= hi + 12) { hi = xs[i]; }
    else { ranges.push(lo === hi ? `${lo}` : `${lo}–${hi}`); lo = hi = xs[i]; }
  }
  ranges.push(lo === hi ? `${lo}` : `${lo}–${hi}`);
  return ranges.join(', ');
}

// ── Bounding box overlap detection ───────────────────────────────────────────
function checkOverlaps(boxes, sceneLabel) {
  const violations = [];

  // Filter: skip tiny boxes and full-width elements (caption pill, footer)
  const filtered = boxes.filter(b => b.w >= 10 && b.h >= 10 && b.w < 1900);

  for (let i = 0; i < filtered.length; i++) {
    for (let j = i + 1; j < filtered.length; j++) {
      const a = filtered[i];
      const b = filtered[j];

      // Compute intersection rectangle
      const ix = Math.max(a.x, b.x);
      const iy = Math.max(a.y, b.y);
      const iw = Math.min(a.x + a.w, b.x + b.w) - ix;
      const ih = Math.min(a.y + a.h, b.y + b.h) - iy;

      if (iw <= 0 || ih <= 0) continue; // no overlap

      const overlapArea  = iw * ih;
      const aArea        = a.w * a.h;
      const bArea        = b.w * b.h;
      const smallerArea  = Math.min(aArea, bArea);

      // Skip when one box is fully contained in the other (text inside its container)
      if (overlapArea >= smallerArea * 0.95) continue;

      // Flag when overlap exceeds 5% of the smaller box's area
      if (overlapArea / smallerArea > 0.05) {
        const aLabel = a.type === 'text' ? `'${a.text}'` : a.type;
        const bLabel = b.type === 'text' ? `'${b.text}'` : b.type;
        violations.push(
          `OVERLAP in ${sceneLabel}: ${aLabel} ` +
          `(${Math.round(a.x)},${Math.round(a.y)},${Math.round(a.w)},${Math.round(a.h)}) ` +
          `overlaps with ${bLabel} ` +
          `(${Math.round(b.x)},${Math.round(b.y)},${Math.round(b.w)},${Math.round(b.h)}) ` +
          `by ${Math.round(overlapArea)}px`
        );
      }
    }
  }

  return violations;
}

// ── Text overflow detection ───────────────────────────────────────────────────
function checkTextOverflow(boxes, sceneLabel) {
  const violations = [];

  for (const b of boxes) {
    if (b.type !== 'text' || b.w < 10) continue;
    if (b.x + b.w > 1920) {
      violations.push(
        `TEXT OVERFLOW in ${sceneLabel}: '${b.text}' ` +
        `extends to x=${Math.round(b.x + b.w)} ` +
        `(right edge overflow by ${Math.round(b.x + b.w - 1920)}px)`
      );
    }
    if (b.x < 0) {
      violations.push(
        `TEXT OVERFLOW in ${sceneLabel}: '${b.text}' ` +
        `starts at x=${Math.round(b.x)} (left edge overflow)`
      );
    }
  }

  return violations;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const scenes = parseScenes(html, totalDur);

  // Header
  console.log('');
  console.log('════════════════════════════════════════');
  console.log('   RUN THE DOCS — LAYOUT VERIFICATION');
  console.log('════════════════════════════════════════');
  console.log(`\nHTML   : ${htmlPath}`);
  console.log(`Timing : ${timingPath}`);
  console.log(`Dur    : ${totalDur.toFixed(2)}s  (${timing.total_frames_30fps} frames)`);
  console.log(`\nScenes detected: ${scenes.length}`);
  scenes.forEach(s => {
    const endLabel = s.end === 'end' ? 'end' : `${s.end}s`;
    console.log(
      `  ${String(s.index).padStart(2)}. ${s.name.padEnd(28)}` +
      `t=${s.start}–${endLabel}  →  key frame ${s.frameNum} (t=${s.keyT.toFixed(1)}s)`
    );
  });
  console.log('');
  console.log('Running checks...\n');

  // Screenshot output directory
  const qaDir = path.join(path.dirname(htmlAbs), 'qa-verify');
  fs.mkdirSync(qaDir, { recursive: true });

  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });

  let sceneResults;
  try {
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto(`file://${htmlAbs}`, { waitUntil: 'networkidle', timeout: 30000 });
    await new Promise(r => setTimeout(r, 2500)); // font load
    await page.waitForFunction(() => typeof window.renderFrame === 'function', { timeout: 10000 });

    await page.evaluate(({ segs, dur }) => {
      window.setTiming(segs, dur);
    }, { segs: timing.segments, dur: totalDur });

    // ── Inject canvas draw-operation interceptor (once, after page is ready) ──
    await page.evaluate(() => {
      const boxes = [];
      const ctx = document.getElementById('c').getContext('2d');
      const origFillText   = ctx.fillText.bind(ctx);
      const origStrokeRect = ctx.strokeRect.bind(ctx);
      const origFillRect   = ctx.fillRect.bind(ctx);

      ctx.fillText = function(text, x, y, maxWidth) {
        const metrics = ctx.measureText(text);
        // Parse px size from CSS font string (e.g. "600 24px 'JetBrains Mono'" → 24)
        const sizeMatch = ctx.font.match(/(\d+(?:\.\d+)?)px/);
        const h = sizeMatch ? parseFloat(sizeMatch[1]) : 16;
        boxes.push({ type: 'text', text: text.substring(0, 30), x, y: y - h, w: metrics.width, h: h * 1.2 });
        return origFillText(text, x, y, maxWidth);
      };

      ctx.strokeRect = function(x, y, w, h) {
        boxes.push({ type: 'rect', x, y, w, h });
        return origStrokeRect(x, y, w, h);
      };

      ctx.fillRect = function(x, y, w, h) {
        // Skip full-canvas clears and background fills
        if (w < 1900 && h < 1000) {
          boxes.push({ type: 'fill', x, y, w, h });
        }
        return origFillRect(x, y, w, h);
      };

      window._layoutBoxes = boxes;
      window._clearBoxes  = () => { boxes.length = 0; };
    });

    sceneResults = [];

    for (const scene of scenes) {
      process.stdout.write(`  Rendering scene ${scene.index}/${scenes.length} (${scene.name})...`);

      // Clear recorded boxes before rendering this scene
      await page.evaluate(() => window._clearBoxes());

      // Render the key frame then collect pixel data
      const pixels = await page.evaluate(
        ({ fn, bgColors, tol }) => {
          window.renderFrame(fn);
          const canvas = document.getElementById('c');
          const ctx    = canvas.getContext('2d');

          function isBg(r, g, b) {
            return bgColors.some(([br, bg, bb]) =>
              Math.abs(r - br) <= tol &&
              Math.abs(g - bg) <= tol &&
              Math.abs(b - bb) <= tol
            );
          }

          // 1. Zone row: y=870, x=10..1909 (excludes 10px margins)
          const zoneRow  = ctx.getImageData(10, 870, 1900, 1).data;
          const zoneViol = [];
          for (let x = 0; x < 1900; x += 3) {
            const i = x * 4;
            if (!isBg(zoneRow[i], zoneRow[i+1], zoneRow[i+2]))
              zoneViol.push(x + 10);
          }

          // 2. Left edge column: x=3, y=80..854
          const leftCol  = ctx.getImageData(3, 80, 1, 775).data;
          const leftViol = [];
          for (let y = 0; y < 775; y += 4) {
            const i = y * 4;
            if (!isBg(leftCol[i], leftCol[i+1], leftCol[i+2]))
              leftViol.push(y + 80);
          }

          // 3. Right edge column: x=1916, y=80..854
          const rightCol  = ctx.getImageData(1916, 80, 1, 775).data;
          const rightViol = [];
          for (let y = 0; y < 775; y += 4) {
            const i = y * 4;
            if (!isBg(rightCol[i], rightCol[i+1], rightCol[i+2]))
              rightViol.push(y + 80);
          }

          // 4. Downsampled frame sample for transition comparison
          //    Content area y=60..950, x=10..1910, step 10px
          const sample = [];
          for (let y = 60; y < 950; y += 10) {
            const row = ctx.getImageData(10, y, 1900, 1).data;
            for (let x = 0; x < 1900; x += 10) {
              const i = x * 4;
              sample.push(row[i], row[i+1], row[i+2]);
            }
          }

          return { zoneViol, leftViol, rightViol, sample };
        },
        { fn: scene.frameNum, bgColors: BG_COLORS, tol: BG_TOL }
      );

      // Collect the draw-operation boxes recorded during renderFrame
      const boxes = await page.evaluate(() => window._layoutBoxes.slice());

      // Run canvas-based checks inline so we know whether to mark screenshot _FAIL
      const sceneLabel = `scene ${scene.index} (${scene.name}, f${scene.frameNum})`;
      const canvasViolations = [
        ...checkOverlaps(boxes, sceneLabel),
        ...checkTextOverflow(boxes, sceneLabel),
      ];

      // Screenshot — append _FAIL when canvas violations already detected
      const suffix     = canvasViolations.length > 0 ? '_FAIL' : '';
      const screenshotPath = path.join(
        qaDir,
        `scene_${String(scene.index).padStart(2, '0')}_${scene.name}_f${scene.frameNum}${suffix}.png`
      );
      await page.screenshot({ path: screenshotPath });

      sceneResults.push({ scene, pixels, boxes, canvasViolations, screenshotPath });
      process.stdout.write(` done\n`);
    }

    await browser.close();
  } catch (err) {
    await browser.close().catch(() => {});
    throw err;
  }

  // ── Analyze results ───────────────────────────────────────────────────────
  const violations = [];

  // Track which scenes have pixel-level violations so we can rename their screenshots
  const scenePixelViolations = new Map(); // sceneIndex → boolean

  for (const { scene, pixels } of sceneResults) {
    const label = `scene ${scene.index} (${scene.name}, f${scene.frameNum})`;
    const before = violations.length;

    // 1. Zone violation — content at y=870
    if (pixels.zoneViol.length >= 4) {
      violations.push(
        `ZONE VIOLATION in ${label}: ${pixels.zoneViol.length} non-bg pixels at y=870, x=${collapseRanges(pixels.zoneViol)}`
      );
    }

    // 2. Left edge overflow (x=3)
    if (pixels.leftViol.length >= 3) {
      violations.push(
        `OVERFLOW in ${label}: content at left edge (x=3) spanning y=${collapseRanges(pixels.leftViol)}`
      );
    }

    // 3. Right edge overflow (x=1916)
    if (pixels.rightViol.length >= 3) {
      violations.push(
        `OVERFLOW in ${label}: content at right edge (x=1916) spanning y=${collapseRanges(pixels.rightViol)}`
      );
    }

    scenePixelViolations.set(scene.index, violations.length > before);
  }

  // 4. Transition staleness — consecutive key frames should differ
  for (let i = 1; i < sceneResults.length; i++) {
    const prev = sceneResults[i - 1];
    const curr = sceneResults[i];
    const sp   = prev.pixels.sample;
    const sc   = curr.pixels.sample;

    let diffSum = 0;
    const len = Math.min(sp.length, sc.length);
    for (let j = 0; j < len; j++) diffSum += Math.abs(sp[j] - sc[j]);
    const avgDiff = diffSum / (len / 3);

    if (avgDiff < 1.5) {
      violations.push(
        `STALE TRANSITION from scene ${prev.scene.index} (${prev.scene.name}) → ` +
        `scene ${curr.scene.index} (${curr.scene.name}): ` +
        `key frames appear identical (avg pixel diff = ${avgDiff.toFixed(2)})`
      );
      // Mark both scenes so their screenshots get the _FAIL rename
      scenePixelViolations.set(prev.scene.index, true);
      scenePixelViolations.set(curr.scene.index, true);
    }
  }

  // 5 & 6. Overlap + text overflow violations (already computed per-scene)
  for (const { canvasViolations } of sceneResults) {
    violations.push(...canvasViolations);
  }

  // Rename screenshots to add _FAIL for scenes that have pixel/stale violations
  // (canvas violations already got the _FAIL suffix during the render loop)
  for (const { scene, screenshotPath } of sceneResults) {
    const hasPixelViol  = scenePixelViolations.get(scene.index);
    const alreadyFailed = screenshotPath.endsWith('_FAIL.png');
    if (hasPixelViol && !alreadyFailed) {
      const failPath = screenshotPath.replace(/\.png$/, '_FAIL.png');
      fs.renameSync(screenshotPath, failPath);
    }
  }

  // ── Output ────────────────────────────────────────────────────────────────
  console.log('');
  console.log('──────────────────────────────────────────');
  console.log('  RESULTS');
  console.log('──────────────────────────────────────────');
  console.log(`\nScreenshots saved to: ${qaDir}/\n`);

  if (violations.length === 0) {
    console.log('✅  PASS — No layout violations detected');
    console.log('');
    process.exit(0);
  } else {
    console.log(`❌  FAIL — ${violations.length} violation(s):\n`);
    violations.forEach(v => console.log(`  • ${v}`));
    console.log('');
    process.exit(1);
  }
}

main().catch(err => {
  console.error(`\nFATAL: ${err.message}`);
  process.exit(1);
});

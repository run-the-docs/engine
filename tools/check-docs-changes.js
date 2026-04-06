#!/usr/bin/env /opt/homebrew/bin/node
'use strict';

const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const TRACKER_PATH = path.join(__dirname, '..', 'docs-tracker.json');
const HASHES_PATH = path.join(__dirname, '..', 'docs-hashes.json');

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; RunTheDocsChecker/1.0)'
      }
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetchPage(res.headers.location).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
      }
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error(`Timeout fetching ${url}`)); });
  });
}

function extractArticleText(html) {
  // Strip script and style blocks first
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '');

  // Try to isolate the main article content
  // kubernetes.io uses <article> or <div class="td-content">
  const articleMatch =
    text.match(/<article[\s\S]*?<\/article>/i) ||
    text.match(/<div[^>]+class="[^"]*td-content[^"]*"[\s\S]*?<\/div>/i) ||
    text.match(/<main[\s\S]*?<\/main>/i);

  if (articleMatch) {
    text = articleMatch[0];
  }

  // Strip all remaining HTML tags
  text = text.replace(/<[^>]+>/g, ' ');
  // Collapse whitespace
  text = text.replace(/\s+/g, ' ').trim();
  return text;
}

function hashContent(text) {
  return crypto.createHash('sha256').update(text).digest('hex');
}

function loadHashes() {
  if (fs.existsSync(HASHES_PATH)) {
    return JSON.parse(fs.readFileSync(HASHES_PATH, 'utf8'));
  }
  return {};
}

function saveHashes(hashes) {
  fs.writeFileSync(HASHES_PATH, JSON.stringify(hashes, null, 2));
}

async function checkEpisode(ep, hashes) {
  const key = `k8s-ep${String(ep.ep).padStart(2, '0')}`;
  process.stdout.write(`  Fetching ep${ep.ep} — ${ep.title} ... `);

  let status, newHash, error;
  try {
    const html = await fetchPage(ep.docsUrl);
    const text = extractArticleText(html);
    newHash = hashContent(text);

    const stored = hashes[key];
    if (!stored) {
      status = 'NEW';
    } else if (stored.hash !== newHash) {
      status = 'CHANGED';
    } else {
      status = 'UNCHANGED';
    }

    hashes[key] = {
      hash: newHash,
      checkedAt: new Date().toISOString(),
      url: ep.docsUrl,
      firstSeenAt: stored ? stored.firstSeenAt : new Date().toISOString()
    };

    console.log(status);
  } catch (err) {
    status = 'ERROR';
    error = err.message;
    console.log(`ERROR — ${err.message}`);
  }

  return { ep: ep.ep, title: ep.title, series: ep.series, url: ep.docsUrl, status, error };
}

async function main() {
  const tracker = JSON.parse(fs.readFileSync(TRACKER_PATH, 'utf8'));
  const hashes = loadHashes();

  console.log(`\nRun the Docs — Docs Change Checker`);
  console.log(`Checking ${tracker.episodes.length} episodes...\n`);

  const results = [];
  for (const ep of tracker.episodes) {
    const result = await checkEpisode(ep, hashes);
    results.push(result);
    // Be polite — small delay between fetches
    await new Promise(r => setTimeout(r, 500));
  }

  saveHashes(hashes);

  // Build report
  const changed = results.filter(r => r.status === 'CHANGED');
  const newDocs = results.filter(r => r.status === 'NEW');
  const unchanged = results.filter(r => r.status === 'UNCHANGED');
  const errored = results.filter(r => r.status === 'ERROR');

  console.log('\n========================================');
  console.log('DOCS CHANGE REPORT');
  console.log('========================================\n');

  if (changed.length === 0 && newDocs.length === 0) {
    console.log('✓ All docs pages unchanged since last check.');
  }

  if (changed.length > 0) {
    console.log(`⚠  CHANGED (${changed.length}) — docs updated after video was created:`);
    for (const r of changed) {
      console.log(`   [${r.series.toUpperCase()} ep${r.ep}] ${r.title}`);
      console.log(`   ${r.url}`);
    }
    console.log();
  }

  if (newDocs.length > 0) {
    console.log(`◆  NEW (${newDocs.length}) — first time hashing these pages:`);
    for (const r of newDocs) {
      console.log(`   [${r.series.toUpperCase()} ep${r.ep}] ${r.title}`);
    }
    console.log();
  }

  if (unchanged.length > 0) {
    console.log(`✓  UNCHANGED (${unchanged.length}): ${unchanged.map(r => `ep${r.ep}`).join(', ')}`);
  }

  if (errored.length > 0) {
    console.log(`\n✗  ERRORS (${errored.length}):`);
    for (const r of errored) {
      console.log(`   ep${r.ep} — ${r.error}`);
    }
  }

  console.log(`\nHashes saved to: ${HASHES_PATH}`);
  console.log(`Checked at: ${new Date().toISOString()}\n`);

  // Emit JSON summary for wrapper script to parse
  const summary = { changed, new: newDocs, unchanged, errors: errored, checkedAt: new Date().toISOString() };
  fs.writeFileSync(path.join(__dirname, '..', 'docs-check-result.json'), JSON.stringify(summary, null, 2));
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});

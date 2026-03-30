#!/usr/bin/env python3
"""
Run the Docs — doc change checker
Fetches each doc URL, hashes content, flags changes vs stored registry.
Usage: python3 rtd-checker.py [--update] [--source openclaw|hono|manifest]
"""
import json, hashlib, urllib.request, sys, time
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path('/tmp/rtd-registry.json')
NOTIFY_CHANGED = True  # set False to just update hashes silently

def fetch(url: str, timeout=10) -> str | None:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'run-the-docs-checker/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  FETCH ERROR {url}: {e}")
        return None

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def main():
    update_mode = '--update' in sys.argv
    source_filter = None
    for arg in sys.argv[1:]:
        if arg.startswith('--source='):
            source_filter = arg.split('=')[1]

    registry = json.loads(REGISTRY_PATH.read_text())
    now = datetime.now(timezone.utc).isoformat()

    changed = []
    new_hashes = {}

    docs = registry['docs']
    total = len(docs)
    print(f"Checking {total} docs...")

    for i, (url, doc) in enumerate(docs.items()):
        if source_filter and doc.get('source') != source_filter:
            continue

        if i % 50 == 0:
            print(f"  {i}/{total}...")

        content = fetch(url)
        if content is None:
            continue

        h = content_hash(content)
        old_h = doc.get('contentHash')

        new_hashes[url] = h
        doc['lastChecked'] = now

        if old_h is None:
            # First check — just store hash
            doc['contentHash'] = h
            doc['lastChanged'] = now
        elif h != old_h:
            changed.append({
                'url': url,
                'slug': doc.get('slug'),
                'source': doc.get('source'),
                'oldHash': old_h,
                'newHash': h,
                'episodeStatus': doc.get('episodeStatus'),
                'episode': doc.get('episode')
            })
            doc['contentHash'] = h
            doc['lastChanged'] = now

        time.sleep(0.05)  # gentle rate limiting

    if update_mode or True:  # always update on run
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2))
        print(f"Registry updated.")

    print(f"\n=== Results ===")
    print(f"Changed docs: {len(changed)}")
    if changed:
        print("\nDocs that changed:")
        for c in changed:
            ep = c['episode']
            status = c['episodeStatus']
            ep_info = f" [Ep {ep['number']}: {ep['title']}]" if ep else ""
            print(f"  [{status}]{ep_info} {c['url']}")

        # Docs with published episodes that changed = need update
        published_changed = [c for c in changed if c['episodeStatus'] == 'published']
        if published_changed:
            print(f"\n⚠️  {len(published_changed)} published episode(s) need updating:")
            for c in published_changed:
                print(f"  → {c['episode']['title']} ({c['url']})")

    return changed

if __name__ == '__main__':
    main()

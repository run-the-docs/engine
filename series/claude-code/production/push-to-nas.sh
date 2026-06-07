#!/bin/bash
# Archive produced Run-the-Docs videos to the Synology DS412+ (Tailscale 100.95.36.122, ~9TB).
#
# Prereq: a shared folder on the NAS mounted on this Mac. One-time mount, e.g.:
#   SMB:  mount_smbfs //USER@100.95.36.122/video /Volumes/video
#   NFS:  sudo mount -t nfs -o resvport,nolocks 100.95.36.122:/volume1/video /Volumes/video
# (The DS412+ already exports NFS for k3s; add an export/share for this Mac in DSM.)
#
# Usage:  bash push-to-nas.sh            # push all episodes (both formats)
#         NAS_MOUNT=/Volumes/video bash push-to-nas.sh
set -euo pipefail
export PATH=/opt/homebrew/bin:$HOME/.local/bin:$PATH
DEMO=~/runthedocs/series/claude-code/demo; REC="$DEMO/rec"
NAS_MOUNT="${NAS_MOUNT:-/Volumes/video}"
DEST="$NAS_MOUNT/runthedocs/claude-code"

if [ ! -d "$NAS_MOUNT" ]; then
  echo "NAS not mounted at $NAS_MOUNT — mount the Synology share first, e.g.:"
  echo "  mount_smbfs //USER@100.95.36.122/video $NAS_MOUNT"
  echo "  (or NFS: sudo mount -t nfs -o resvport,nolocks 100.95.36.122:/volume1/video $NAS_MOUNT)"
  exit 1
fi

mkdir -p "$DEST"
pushed=0
for n in 1 2 3 4 5; do
  d="$DEST/ep${n}"; mkdir -p "$d"
  # finals (LinkedIn 4:5 + TikTok/Shorts 9:16), the raw terminal cut, source lines + cached narration
  for f in "claude-ep${n}-45.mp4" "claude-ep${n}-916.mp4" "claude-ep${n}-term.mp4"; do
    [ -f "$REC/$f" ] && { rsync -a "$REC/$f" "$d/"; pushed=$((pushed+1)); }
  done
  [ -f "$DEMO/ep${n}.lines.json" ]      && rsync -a "$DEMO/ep${n}.lines.json"      "$d/"
  [ -f "$REC/narration-ep${n}.json" ]   && rsync -a "$REC/narration-ep${n}.json"   "$d/"
done
echo "PUSH_TO_NAS_OK -> $DEST ($pushed media files synced)"
ls -R "$DEST" 2>/dev/null | head -50

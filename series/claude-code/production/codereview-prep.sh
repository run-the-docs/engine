#!/bin/bash
# ep15 prep: introduce an uncommitted change with a clear reviewable bug so
# /code-review has a real diff to flag (IndexError when text has < 2 words).
REPO="$HOME/runthedocs/series/claude-code/demo/cc-demo-repo"
cat >> "$REPO/slugify.py" <<'EOF'


def first_two_words(text):
    parts = text.split()
    return parts[0] + " " + parts[1]
EOF
echo "codereview-prep: appended first_two_words (IndexError on < 2 words)"

#!/bin/bash
# Concatenate the page parts in name order, expand the pinned source-link macros, and write ../index.html.
# Link expansion needs the repo file trees in src/trees/ (run ./fetch_trees.sh once).
set -e
cd "$(dirname "$0")"
cat $(ls parts/p[0-9]*.html | LC_ALL=C sort) | python3 expand.py > build.tmp && mv build.tmp ../index.html && echo "built ../index.html"

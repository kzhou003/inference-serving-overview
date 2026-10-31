#!/bin/bash
# Download the file list of every referenced repository at the commit pinned in pins.txt,
# so expand.py can check that each linked path exists. Requires an authenticated `gh`.
set -e
cd "$(dirname "$0")"
mkdir -p trees
while read -r alias full sha; do
  # alias = the owner/repo name used in the page macros (may be a pre-rename name); full = where it lives now
  f="trees/$(echo "$alias" | tr / _)"
  gh api "repos/$full/git/trees/$sha?recursive=1" --jq '.tree[].path' > "$f.txt"
  echo "$full $sha" > "$f.sha"
  echo "$full $(wc -l < "$f.txt") paths"
done < pins.txt

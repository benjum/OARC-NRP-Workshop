#!/usr/bin/env bash
# Replace the YOURNAME placeholder in every lab YAML with your own short name,
# so your Pods/PVCs don't collide with other participants in the shared namespace.
#
#   ./personalize.sh jsmith
#
# Names must be lowercase letters, digits, or '-', and start with a letter.
set -euo pipefail
cd "$(dirname "$0")"

NAME="${1:-}"
if [[ ! "$NAME" =~ ^[a-z][a-z0-9-]{0,19}$ ]]; then
  echo "Usage: ./personalize.sh <name>   e.g. ./personalize.sh jsmith"
  echo "  lowercase letters/digits/dashes, start with a letter, max 20 chars"
  exit 1
fi

count=0
for f in labs/*/*.yaml; do
  if grep -q YOURNAME "$f"; then
    # portable in-place edit (works with both GNU and macOS sed)
    sed "s/YOURNAME/$NAME/g" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
    count=$((count + 1))
  fi
done
echo "Updated $count YAML files for '$NAME'."
echo
echo "Now set this in your terminal (used by the commands in the lab READMEs):"
echo "  export ME=$NAME"

#!/bin/bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Usage: scripts/promote_page.sh <source-from-test-pages> <destination-dir> [destination-filename]" >&2
  echo "Example: scripts/promote_page.sh test-pages/my-draft.html events 2026-04-12-rally.html" >&2
  exit 1
fi

SRC="$1"
DEST_DIR="$2"
DEST_FILE="${3:-$(basename "$SRC")}" 

if [[ ! -f "$SRC" ]]; then
  echo "Source file not found: $SRC" >&2
  exit 1
fi

if [[ "$SRC" != test-pages/* ]]; then
  echo "Source should live under test-pages/ to keep draft-first flow." >&2
  exit 1
fi

if [[ ! -d "$DEST_DIR" ]]; then
  echo "Destination directory not found: $DEST_DIR" >&2
  exit 1
fi

DEST_PATH="$DEST_DIR/$DEST_FILE"
cp "$SRC" "$DEST_PATH"

echo "Copied $SRC -> $DEST_PATH"
read -r -p "Canonical URL for this page (e.g., https://www.local083.org/events/2026-01-01-example.html): " CANONICAL_URL

# Guidance echo-out (no mutation)
echo
echo "Next steps:" 
echo "1) Open $DEST_PATH and set canonical/og/twitter URLs and JSON-LD @id/url to: $CANONICAL_URL"
echo "2) Update title/description to match final content; remove placeholders." 

if [[ "$DEST_DIR" == events* || "$DEST_DIR" == */events* ]]; then
  echo "3) Update events/events.json for this event and add/update events/ical/*.ics if needed."
elif [[ "$DEST_DIR" == news* || "$DEST_DIR" == */news* ]]; then
  echo "3) Update news/news.json for this story."
else
  echo "3) Update any related navigation or index pages if needed."
fi

echo "4) Run: bash ./generate_sitemap.sh"
echo "5) Run: python3 scripts/site_quality_check.py --strict-placeholders"
echo "6) Verify union-first voice ("our union", "we") and working links before publishing."

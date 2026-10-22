#!/usr/bin/env bash
# Prints _build/guide/lead-magnet.html to guide/ai-guide.pdf.
# The published guide was originally produced by Headless Chrome (Skia/PDF).
# This folder starts with "_" so GitHub Pages does not publish the source.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HTML="$ROOT/_build/guide/lead-magnet.html"
OUT="${1:-$ROOT/guide/ai-guide.pdf}"
rm -rf /tmp/chrome-guide-pdf
# Headless Chrome writes the PDF, then often stays running. timeout stops it
# after the file is on disk; exit 124 is success when the PDF exists.
set +e
timeout 25 google-chrome \
  --headless=new \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --no-first-run \
  --user-data-dir=/tmp/chrome-guide-pdf \
  --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw \
  --print-to-pdf="$OUT" \
  "file://$HTML"
status=$?
set -e
if [[ ! -s "$OUT" ]]; then
  echo "Chrome did not write $OUT (exit $status)" >&2
  exit 1
fi
if [[ "$status" -ne 0 && "$status" -ne 124 ]]; then
  echo "Chrome exited $status" >&2
  exit "$status"
fi
echo "wrote $OUT"

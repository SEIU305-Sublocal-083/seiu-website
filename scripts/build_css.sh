#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE_DIR="${TMPDIR:-/tmp}/local083-tailwind"
TAILWIND_VERSION="3.4.19"

case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) ASSET="tailwindcss-macos-arm64"; EXPECTED_SHA256="7fdeb00818b6214a337383063282b2361ecb08bbc08f8c8a7ba97ee1e2eaa4fe" ;;
  Darwin-x86_64) ASSET="tailwindcss-macos-x64"; EXPECTED_SHA256="a597f407e0f1f03535731f5b42f1576a8152cb5fffc2f38e754722bc0c280045" ;;
  Linux-aarch64|Linux-arm64) ASSET="tailwindcss-linux-arm64"; EXPECTED_SHA256="e5b2d27694daa80cc52ec29553ba2c6bd43d86bd51a9d633ed24058b9c05a676" ;;
  Linux-x86_64) ASSET="tailwindcss-linux-x64"; EXPECTED_SHA256="4af3198c015616ea7d6617974ec3d70d987ecc00c1ca8463b0a30fd65cc7c06e" ;;
  *) echo "Unsupported Tailwind build platform: $(uname -s)-$(uname -m)" >&2; exit 1 ;;
esac

BINARY="$CACHE_DIR/$ASSET"

mkdir -p "$CACHE_DIR"

if [[ ! -x "$BINARY" ]] || [[ "$(shasum -a 256 "$BINARY" | awk '{print $1}')" != "$EXPECTED_SHA256" ]]; then
  curl --fail --location --silent --show-error \
    "https://github.com/tailwindlabs/tailwindcss/releases/download/v${TAILWIND_VERSION}/${ASSET}" \
    --output "$BINARY"
  echo "$EXPECTED_SHA256  $BINARY" | shasum -a 256 --check --status
  chmod +x "$BINARY"
fi

cd "$ROOT"
"$BINARY" \
  --config tailwind.config.cjs \
  --input styles/tailwind-input.css \
  --output styles/tailwind.css \
  --minify

printf 'Built %s\n' "$ROOT/styles/tailwind.css"

#!/usr/bin/env bash

# Fetches all available BAPI spec versions, determines the latest,
# and extracts tags from it. Output is used as skill context.

set -euo pipefail

API_URL="https://api.github.com/repos/clerk/openapi-specs/contents/bapi"
RAW_BASE="https://raw.githubusercontent.com/clerk/openapi-specs/main/bapi"
SPEC_CACHE_DIR="${TMPDIR:-/tmp}/clerk-openapi-specs"
mkdir -p "$SPEC_CACHE_DIR"

# Fetch version list, parse dates, sort, pick latest
VERSIONS_JSON="$SPEC_CACHE_DIR/versions.json"
curl -fsSL "$API_URL" -o "$VERSIONS_JSON"
versions=$(node - "$VERSIONS_JSON" <<'SCRIPT'
const fs = require("fs");
const items = JSON.parse(fs.readFileSync(process.argv[2], "utf8"))
  .map(i => i.name)
  .filter(n => /^\d{4}-\d{2}-\d{2}\.yml$/.test(n))
  .sort();
items.forEach(n => console.log(n));
SCRIPT
)

latest=$(echo "$versions" | tail -1)

echo "AVAILABLE VERSIONS: $(echo "$versions" | tr '\n' ' ')"
echo "LATEST VERSION: $latest"
echo ""
echo "TAGS:"
SPEC_FILE="$SPEC_CACHE_DIR/$latest"
[ -s "$SPEC_FILE" ] || curl -fsSL "${RAW_BASE}/${latest}" -o "$SPEC_FILE"
node "$(dirname "$0")/extract-tags.js" < "$SPEC_FILE"

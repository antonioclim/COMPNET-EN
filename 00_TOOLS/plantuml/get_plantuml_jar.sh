#!/usr/bin/env bash
# Download and validate the PlantUML JAR before atomically replacing the cache.
set -euo pipefail
PLANTUML_URL="https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
JAR_PATH="$TOOLS_DIR/plantuml.jar"
command -v java >/dev/null || { echo "[FAIL] Java is required to validate the JAR." >&2; exit 1; }
valid_jar() { [[ -s "$1" ]] && java -jar "$1" -version >/dev/null 2>&1; }
if valid_jar "$JAR_PATH"; then
  echo "[OK] Valid PlantUML JAR already present: $JAR_PATH"
  exit 0
fi
TEMP_JAR=$(mktemp "$TOOLS_DIR/.plantuml-download.XXXXXXXX.jar")
trap 'rm -f "$TEMP_JAR"' EXIT
echo "[INFO] Downloading PlantUML (latest release)..."
if command -v curl >/dev/null; then
  curl --connect-timeout 20 --max-time 300 -fSL -o "$TEMP_JAR" "$PLANTUML_URL"
elif command -v wget >/dev/null; then
  wget --timeout=30 --tries=2 -O "$TEMP_JAR" "$PLANTUML_URL"
else
  echo "[FAIL] Neither curl nor wget is available." >&2
  exit 1
fi
if ! valid_jar "$TEMP_JAR"; then
  echo "[FAIL] Download is not an executable PlantUML JAR; cache was not replaced." >&2
  exit 1
fi
mv -f "$TEMP_JAR" "$JAR_PATH"
echo "[OK] Validated PlantUML JAR saved to: $JAR_PATH"

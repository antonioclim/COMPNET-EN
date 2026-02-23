#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# get_plantuml_jar.sh — download the PlantUML JAR into 00_TOOLS/
#
# The JAR is intentionally kept out of Git history (.gitignore).
# Run this script once after cloning the repository.
# ──────────────────────────────────────────────────────────────
set -euo pipefail

PLANTUML_URL="https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar"

# Resolve paths relative to the script's own location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
JAR_PATH="$TOOLS_DIR/plantuml.jar"

if [[ -f "$JAR_PATH" ]]; then
    echo "[OK]   PlantUML JAR already present: $JAR_PATH"
    exit 0
fi

echo "[INFO] Downloading PlantUML (latest release)..."

if command -v curl &>/dev/null; then
    curl -fSL -o "$JAR_PATH" "$PLANTUML_URL"
elif command -v wget &>/dev/null; then
    wget -q --show-progress -O "$JAR_PATH" "$PLANTUML_URL"
else
    echo "[FAIL] Neither curl nor wget is available." >&2
    exit 1
fi

if [[ ! -s "$JAR_PATH" ]]; then
    echo "[FAIL] Download produced an empty file. Check your network." >&2
    rm -f "$JAR_PATH"
    exit 1
fi

echo "[OK]   PlantUML JAR saved to: $JAR_PATH"

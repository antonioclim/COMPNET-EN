#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# render_puml.sh — render all .puml files from an input directory
#
# Usage:
#   render_puml.sh <input_dir> <output_dir>
#
# Environment:
#   PLANTUML_JAR   Path to plantuml.jar.
#                  Default: 00_TOOLS/plantuml.jar (relative to this script).
# ──────────────────────────────────────────────────────────────
set -euo pipefail

# ── Resolve default jar path relative to the script itself ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLANTUML_JAR="${PLANTUML_JAR:-$TOOLS_DIR/plantuml.jar}"

# ── Argument handling ────────────────────────────────────────
if [[ $# -lt 2 ]]; then
    echo "Usage: $(basename "$0") <input_dir> <output_dir>" >&2
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# ── Pre-flight checks ───────────────────────────────────────
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "[FAIL] Input directory does not exist: $INPUT_DIR" >&2
    exit 1
fi

if [[ ! -f "$PLANTUML_JAR" ]]; then
    echo "[FAIL] PlantUML JAR not found: $PLANTUML_JAR" >&2
    echo "       Run:  bash 00_TOOLS/plantuml/get_plantuml_jar.sh" >&2
    exit 1
fi

if ! command -v java &>/dev/null; then
    echo "[FAIL] Java is required but not found on PATH." >&2
    exit 1
fi

# Count source files.
shopt -s nullglob
PUML_FILES=("$INPUT_DIR"/*.puml)
shopt -u nullglob

if [[ ${#PUML_FILES[@]} -eq 0 ]]; then
    echo "[WARN] No .puml files found in $INPUT_DIR"
    exit 0
fi

# ── Create output directory if absent ────────────────────────
mkdir -p "$OUTPUT_DIR"

# PlantUML resolves -o relative to each source file, so we
# convert to an absolute path to guarantee correct placement.
ABS_OUTPUT="$(cd "$OUTPUT_DIR" && pwd)"

# ── Render ───────────────────────────────────────────────────
echo "[INFO] Rendering ${#PUML_FILES[@]} diagram(s): $INPUT_DIR → $OUTPUT_DIR"

java -jar "$PLANTUML_JAR" -tpng -o "$ABS_OUTPUT" "${PUML_FILES[@]}"

echo "[OK]   ${#PUML_FILES[@]} diagram(s) rendered into $OUTPUT_DIR"

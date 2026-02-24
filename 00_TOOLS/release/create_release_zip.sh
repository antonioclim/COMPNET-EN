#!/usr/bin/env bash
# create_release_zip.sh — build a distributable ZIP from a repository checkout
# --------------------------------------------------------------------------
# Usage:
#   bash 00_TOOLS/release/create_release_zip.sh
#   bash 00_TOOLS/release/create_release_zip.sh <output.zip>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

OUT_NAME="${1:-compnet-course-kit_$(date +%Y-%m-%d).zip}"

echo "[INFO] Repository root: $REPO_ROOT"
echo "[INFO] Output archive:  $OUT_NAME"

echo "[INFO] Applying executable permission bits (Phase 4)"
bash 00_TOOLS/qa/apply_permissions.sh

if command -v node &>/dev/null; then
    echo "[INFO] Formatting check (Prettier offline)"
    node format-offline.js --check
else
    echo "[WARN] Node.js not found, skipping format check"
fi

echo "[INFO] Markdown link check"
python 00_TOOLS/qa/check_markdown_links.py

echo "[INFO] Language and lexical integrity check"
python 00_TOOLS/qa/check_integrity.py

echo "[INFO] Lecture figure target check"
python 00_TOOLS/qa/check_fig_targets.py --puml-only

if python -c "import pytest" &>/dev/null; then
    echo "[INFO] Pytest"
    python -m pytest -q
else
    echo "[WARN] pytest not installed, skipping test run"
fi

echo "[INFO] Creating ZIP archive"

rm -f "$OUT_NAME"

zip -r "$OUT_NAME" . \
    -x "./.git/*" \
    -x "./node_modules/*" \
    -x "*/__pycache__/*" \
    -x "*.pyc" \
    -x "*/.pytest_cache/*" \
    -x "*/.mypy_cache/*" \
    -x "*/.ruff_cache/*" \
    -x "./.DS_Store" \
    -x "./00_TOOLS/plantuml.jar"

echo "[OK] Archive created: $OUT_NAME"

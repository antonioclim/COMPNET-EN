#!/usr/bin/env bash
# apply_permissions.sh — Phase 4 executability enforcement
# ---------------------------------------------------------
# Reads executable_manifest.txt and ensures every listed path
# carries the executable bit in the working tree.
#
# Usage:  bash 00_TOOLS/qa/apply_permissions.sh          (from repo root)
#         bash 00_TOOLS/qa/apply_permissions.sh --dry-run (preview only)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/executable_manifest.txt"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

if [[ ! -f "$MANIFEST" ]]; then
    echo "ERROR: manifest not found at ${MANIFEST}" >&2
    exit 1
fi

applied=0
skipped=0
missing=0

while IFS= read -r line; do
    # Strip comments and blank lines
    line="${line%%#*}"
    line="$(echo "$line" | xargs)"          # trim whitespace
    [[ -z "$line" ]] && continue

    target="${REPO_ROOT}/${line}"

    if [[ ! -e "$target" ]]; then
        echo "  MISS  ${line}"
        (( missing++ )) || true
        continue
    fi

    if [[ -x "$target" ]]; then
        (( skipped++ )) || true
        continue
    fi

    if (( DRY_RUN )); then
        echo "  WOULD chmod +x  ${line}"
    else
        chmod +x "$target"
        echo "  +x    ${line}"
    fi
    (( applied++ )) || true

done < "$MANIFEST"

total=$(( applied + skipped + missing ))
echo ""
echo "── Summary ────────────────────────────────────"
echo "  Total manifest entries : ${total}"
echo "  Already executable     : ${skipped}"
echo "  Newly set +x           : ${applied}"
echo "  Missing from tree      : ${missing}"
if (( DRY_RUN )); then
    echo "  (dry-run — no changes written)"
fi
echo "────────────────────────────────────────────────"

exit 0

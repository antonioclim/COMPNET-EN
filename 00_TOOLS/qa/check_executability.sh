#!/usr/bin/env bash
# check_executability.sh — CI gate for Phase 4 permissions enforcement
# --------------------------------------------------------------------
# Exit 0  →  all manifest entries that exist in the tree are executable.
# Exit 1  →  at least one entry exists but is missing the executable bit.
#
# Usage:  bash 00_TOOLS/qa/check_executability.sh        (from repo root)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/executable_manifest.txt"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [[ ! -f "$MANIFEST" ]]; then
    echo "FATAL: manifest not found at ${MANIFEST}" >&2
    exit 1
fi

failures=0
checked=0

while IFS= read -r line; do
    line="${line%%#*}"
    line="$(echo "$line" | xargs)"
    [[ -z "$line" ]] && continue

    target="${REPO_ROOT}/${line}"

    # Only check paths that exist; missing paths are not a CI failure
    # (they may belong to optional / platform-specific components).
    [[ ! -e "$target" ]] && continue

    (( checked++ )) || true

    if [[ ! -x "$target" ]]; then
        echo "FAIL: not executable — ${line}" >&2
        (( failures++ )) || true
    fi
done < "$MANIFEST"

echo "Checked ${checked} manifest entries."

if (( failures > 0 )); then
    echo ""
    echo "${failures} file(s) missing executable bit."
    echo "Run:  bash 00_TOOLS/qa/apply_permissions.sh"
    exit 1
fi

echo "All entries OK."
exit 0

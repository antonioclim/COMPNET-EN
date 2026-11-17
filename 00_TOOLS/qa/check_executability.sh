#!/usr/bin/env bash
# check_executability.sh — CI gate for Phase 4 permissions enforcement
# --------------------------------------------------------------------
# Exit 0  →  every manifest entry exists and is executable; in a Git checkout,
#             its index mode is also 100755.
# Exit 1  →  a required path or executable mode is missing.
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

    if [[ ! -f "$target" ]]; then
        echo "FAIL: manifest path missing or not a file — ${line}" >&2
        (( failures++ )) || true
        continue
    fi

    (( checked++ )) || true

    if [[ ! -x "$target" ]]; then
        echo "FAIL: not executable — ${line}" >&2
        (( failures++ )) || true
    fi

    # A chmod applied only to the working tree must not conceal a wrong Git mode.
    # Archives have no Git index; there the extracted file mode is checked above.
    if [[ -e "${REPO_ROOT}/.git" ]]; then
        entry="$(git -C "$REPO_ROOT" ls-files --stage -- "$line")"
        mode="${entry%% *}"
        if [[ "$mode" != 100755 ]]; then
            echo "FAIL: Git index mode must be 100755 — ${line} (found ${mode:-untracked})" >&2
            (( failures++ )) || true
        fi
    fi
done < "$MANIFEST"

echo "Checked ${checked} manifest entries."

if (( failures > 0 )); then
    echo ""
    echo "${failures} executable-manifest check(s) failed."
    echo "Restore missing paths; apply and stage the intended executable modes."
    echo "Helper: bash 00_TOOLS/qa/apply_permissions.sh"
    exit 1
fi

echo "All entries OK."
exit 0

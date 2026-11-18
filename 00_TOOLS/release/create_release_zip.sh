#!/usr/bin/env bash
# Package a committed course checkout after the same source gates used by CI.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
cd -- "$REPO_ROOT"
PYTHON="${COMP_NET_PYTHON:-python3}"
OUT_NAME="${1:-$REPO_ROOT/../COMPNET-EN-$(git rev-parse --short HEAD).zip}"
if [[ -e "$OUT_NAME" ]]; then
    echo "Refusing to replace an existing archive: $OUT_NAME" >&2
    exit 1
fi
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Commit the intended source changes before packaging; the archive contains HEAD." >&2
    exit 1
fi
"$PYTHON" 00_TOOLS/qa/run_checks.py
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "A check changed tracked files. Review them before packaging." >&2
    exit 1
fi
# git archive includes only committed paths and their recorded modes.
# It never adds personal captures, credentials, test results or an earlier ZIP.
TEMP_ARCHIVE="$(mktemp "${OUT_NAME}.tmp.XXXXXX")"
trap 'rm -f -- "$TEMP_ARCHIVE"' EXIT
git archive --format=zip --prefix=COMPNET-EN/ --output="$TEMP_ARCHIVE" HEAD
"$PYTHON" - "$TEMP_ARCHIVE" "$OUT_NAME" <<'PY'
import os
from pathlib import Path
import sys
import zipfile
source, target = map(Path, sys.argv[1:])
with zipfile.ZipFile(source) as archive:
    bad = archive.testzip()
    if bad:
        raise SystemExit('ZIP CRC failure: ' + bad)
# Exclusive output creation prevents replacement even if a file appeared meanwhile.
with target.open('xb') as output, source.open('rb') as data:
    import shutil
    shutil.copyfileobj(data, output)
print('Archive created:', target.resolve())
PY

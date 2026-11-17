#!/usr/bin/env python3
"""Run the same non-mutating repository gates locally and in CI.

These gates cover source integrity and component regression tests. They do not
boot the OVA, start Docker/Mininet, import an LMS package or render a browser.
"""
from __future__ import annotations

import ast
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
EXCLUDED = {'.git', '.venv', '.venv-qa', 'venv', 'node_modules', '__pycache__', '.pytest_cache'}


def main() -> int:
    os.chdir(ROOT)
    missing = [name for name in ('pytest', 'yaml') if importlib.util.find_spec(name) is None]
    if missing:
        print('Missing QA dependencies: ' + ', '.join(missing), file=sys.stderr)
        print(f'{sys.executable} -m pip install -r 00_TOOLS/qa/requirements.txt', file=sys.stderr)
        return 2
    # Parse source without running demonstrations or creating bytecode files.
    paths = [p for p in ROOT.rglob('*.py') if not EXCLUDED.intersection(p.relative_to(ROOT).parts)]
    for path in paths:
        try:
            ast.parse(path.read_bytes(), filename=str(path.relative_to(ROOT)))
        except (SyntaxError, UnicodeError) as exc:
            print(exc, file=sys.stderr)
            return 1
    print(f'Python syntax: {len(paths)} source files parsed', flush=True)
    commands = [
        ['bash', '00_TOOLS/qa/check_executability.sh'],
        [sys.executable, '00_TOOLS/qa/check_markdown_links.py'],
        [sys.executable, '00_TOOLS/qa/check_integrity.py', '--exclude', 'CHANGELOG.md'],
        [sys.executable, '00_TOOLS/qa/check_fig_targets.py', '--puml-only'],
        [sys.executable, '-m', 'pytest', '-q'],
    ]
    environment = os.environ.copy()
    environment['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    for command in commands:
        print('Running: ' + ' '.join(command), flush=True)
        result = subprocess.run(command, env=environment, check=False)
        if result.returncode:
            return result.returncode
    print('Repository source gates passed; environment/browser acceptance remains separate.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

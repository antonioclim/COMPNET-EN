"""Small helper for S13 scripts: read optional `.env` port mappings.

Why this exists
---------------
Docker Compose uses `.env` for variable expansion, but Python scripts executed
directly from the host shell do not automatically inherit those values.

This helper keeps scripts robust when students:
- use the default ports (no `.env` present), OR
- generate a custom `.env` with different host port mappings

Design constraints
------------------
- standard library only (no python-dotenv dependency)
- very small parser: KEY=VALUE, ignores blanks/comments
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict


def load_env_file(env_path: Path) -> Dict[str, str]:
    if not env_path.exists():
        return {}

    data: Dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k:
            data[k] = v
    return data


def load_local_env() -> Dict[str, str]:
    """Loads `.env` from the S13 directory (if present)."""
    here = Path(__file__).resolve().parent
    return load_env_file(here / ".env")

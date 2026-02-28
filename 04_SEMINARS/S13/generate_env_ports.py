#!/usr/bin/env python3
"""S13 — generate a local `.env` with host port mappings.

Why this exists
---------------
When students run multiple Docker labs on the same machine, common ports such as
8080/8888/2121 may already be taken. Docker Compose supports variable expansion
inside the compose file, so we can keep the *same* lab topology but remap host
ports via a simple `.env`.

This generator is intentionally conservative:
- if `.env` already exists, it will NOT overwrite it (reproducibility)
- it picks the first free port in a small window near each default

Usage
-----
From this directory (04_SEMINARS/S13):

  python3 generate_env_ports.py

Then start the lab:

  docker compose -f S13_Part02_Config_Docker_Compose_Pentest.yml up -d

Notes
-----
- Docker Compose automatically reads `.env` from the *project directory*.
- If you run compose from another directory, pass `--project-directory` or `cd` here.
"""

from __future__ import annotations

import argparse
import errno
import socket
from pathlib import Path
from typing import Optional


DEFAULTS = {
    "DVWA_HOST_PORT": 8888,
    "WEBGOAT_HOST_PORT": 8080,
    "VSFTPD_HOST_PORT": 2121,
    "VSFTPD_BACKDOOR_HOST_PORT": 6200,
}


def _can_bind_ipv4(port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Binding to 0.0.0.0 approximates the default Docker behaviour (all interfaces).
        s.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False
    finally:
        try:
            s.close()
        except Exception:
            pass


def _can_bind_ipv6(port: int) -> Optional[bool]:
    """Best-effort IPv6 check.

    Returns:
      - True  : can bind to ::port
      - False : port is clearly in use on IPv6
      - None  : IPv6 not available / not meaningful on this host
    """
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    except OSError:
        return None

    try:
        s.bind(("::", port))
        return True
    except OSError as e:
        # If address family not supported or IPv6 disabled, treat as N/A.
        if e.errno in {errno.EAFNOSUPPORT, errno.EADDRNOTAVAIL}:
            return None
        # If port is already in use, treat as not free.
        if e.errno == errno.EADDRINUSE:
            return False
        # Unknown failure: do not block port selection (best effort).
        return None
    finally:
        try:
            s.close()
        except Exception:
            pass


def is_port_free(port: int) -> bool:
    if not _can_bind_ipv4(port):
        return False

    v6 = _can_bind_ipv6(port)
    if v6 is False:
        return False

    return True


def pick_port(hint: int, window: int = 50) -> int:
    for p in range(hint, hint + window + 1):
        if is_port_free(p):
            return p
    return hint


def write_env_file(path: Path, force: bool, window: int) -> None:
    if path.exists() and not force:
        print(f"[OK] {path.name} already exists — leaving it unchanged (reproducibility). ")
        return

    ports = {k: pick_port(v, window=window) for k, v in DEFAULTS.items()}

    lines = [
        "# S13 — Docker port mapping (host side)",
        "#",
        "# If a port is already in use on your machine:",
        "#   - delete `.env` and re-run this generator, OR",
        "#   - edit the values below manually",
        "#",
        "# This file is used by Docker Compose variable expansion in:",
        "#   S13_Part02_Config_Docker_Compose_Pentest.yml",
        "",
    ]

    for k in DEFAULTS.keys():
        lines.append(f"{k}={ports[k]}")
    lines.append("")  # final newline

    path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[OK] Wrote {path.name}:")
    for k in DEFAULTS.keys():
        print(f"  - {k}={ports[k]}")
    print("\nNext:")
    print("  docker compose -f S13_Part02_Config_Docker_Compose_Pentest.yml up -d")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate an optional `.env` for S13 port mappings.")
    ap.add_argument("--env-file", default=".env", help="Output file name (default: .env)")
    ap.add_argument("--force", action="store_true", help="Overwrite the env file if it already exists")
    ap.add_argument("--window", type=int, default=50, help="Search window size above each default port")
    args = ap.parse_args()

    env_path = Path(__file__).resolve().parent / args.env_file
    write_env_file(env_path, force=args.force, window=args.window)


if __name__ == "__main__":
    main()

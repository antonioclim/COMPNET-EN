#!/usr/bin/env python3
"""lab_runner.py — minimal Docker Compose runner for COMPNET-EN.

This script is intentionally conservative:
- standard library only
- does not modify repository content
- runs Compose in the lab's directory to keep relative paths correct

Usage examples (from repo root):
  python 00_TOOLS/lab_runner/lab_runner.py list
  python 00_TOOLS/lab_runner/lab_runner.py up c10-http-compose --build
  python 00_TOOLS/lab_runner/lab_runner.py up c13-iot-basic --variant tls --build
  python 00_TOOLS/lab_runner/lab_runner.py logs c10-http-compose --follow

"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


MANIFEST_REL = Path("00_TOOLS/lab_runner/labs.json")


@dataclass(frozen=True)
class Lab:
    lab_id: str
    title: str
    path: Path
    variants: Dict[str, List[str]]


def repo_root() -> Path:
    """Return repository root based on this file's location."""
    here = Path(__file__).resolve()
    # .../00_TOOLS/lab_runner/lab_runner.py -> repo root is parents[2]
    return here.parents[2]


def load_manifest(root: Path) -> List[Lab]:
    manifest_path = root / MANIFEST_REL
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported labs.json schema_version (expected 1)")

    labs: List[Lab] = []
    for item in data.get("labs", []):
        lab_id = str(item["id"]).strip()
        title = str(item.get("title", lab_id)).strip()
        path = Path(str(item["path"]).strip())
        variants = item.get("variants", {})
        if not isinstance(variants, dict) or not variants:
            raise ValueError(f"Lab '{lab_id}' must define a non-empty 'variants' mapping")

        norm_variants: Dict[str, List[str]] = {}
        for vname, files in variants.items():
            if isinstance(files, str):
                norm_variants[str(vname)] = [files]
            elif isinstance(files, list) and all(isinstance(x, str) for x in files):
                norm_variants[str(vname)] = [str(x) for x in files]
            else:
                raise ValueError(f"Lab '{lab_id}' variant '{vname}' must be a string or list of strings")

        labs.append(Lab(lab_id=lab_id, title=title, path=path, variants=norm_variants))

    return labs


def find_lab(labs: Sequence[Lab], lab_id: str) -> Lab:
    for lab in labs:
        if lab.lab_id == lab_id:
            return lab
    known = ", ".join(sorted(l.lab_id for l in labs))
    raise KeyError(f"Unknown lab id '{lab_id}'. Known labs: {known}")


def sanitise_project_name(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9_-]", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_-")
    return s or "compnet_lab"


def _can_run(cmd: List[str]) -> bool:
    try:
        proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
        return proc.returncode == 0
    except Exception:
        return False


def detect_compose_command() -> List[str]:
    """Return compose command as argv prefix.

    Preference order:
    1) $COMPNET_COMPOSE_CMD (split by spaces)
    2) `docker compose` if docker exists and `docker compose version` works
    3) `docker-compose` if present
    """

    override = os.environ.get("COMPNET_COMPOSE_CMD")
    if override:
        return override.split()

    docker = shutil.which("docker")
    if docker and _can_run([docker, "compose", "version"]):
        return [docker, "compose"]

    legacy = shutil.which("docker-compose")
    if legacy:
        return [legacy]

    raise FileNotFoundError(
        "No Docker Compose command found. Install Docker (preferred: 'docker compose') "
        "or legacy 'docker-compose'."
    )


def compose_args_for_variant(lab: Lab, variant: str) -> List[str]:
    if variant not in lab.variants:
        known = ", ".join(sorted(lab.variants.keys()))
        raise KeyError(f"Lab '{lab.lab_id}' has no variant '{variant}'. Known variants: {known}")

    args: List[str] = []
    for f in lab.variants[variant]:
        args.extend(["-f", f])
    return args


def run_compose(
    compose_cmd: List[str],
    cwd: Path,
    args: List[str],
    dry_run: bool = False,
) -> int:
    cmd = compose_cmd + args
    if dry_run:
        print("DRY-RUN:")
        print("  cwd:", str(cwd))
        print("  cmd:", " ".join(cmd))
        return 0

    try:
        proc = subprocess.run(cmd, cwd=str(cwd))
        return int(proc.returncode)
    except FileNotFoundError:
        print("ERROR: Docker Compose command not found.", file=sys.stderr)
        return 127


def cmd_list(labs: Sequence[Lab]) -> int:
    rows: List[Tuple[str, str, str]] = []
    for lab in sorted(labs, key=lambda x: x.lab_id):
        variants = ",".join(sorted(lab.variants.keys()))
        rows.append((lab.lab_id, lab.title, variants))

    w1 = max((len(r[0]) for r in rows), default=10)
    w2 = max((len(r[1]) for r in rows), default=10)

    print(f"{'LAB ID'.ljust(w1)}  {'TITLE'.ljust(w2)}  VARIANTS")
    print(f"{'-' * w1}  {'-' * w2}  {'-' * 20}")
    for lab_id, title, variants in rows:
        print(f"{lab_id.ljust(w1)}  {title.ljust(w2)}  {variants}")

    return 0


def cmd_info(labs: Sequence[Lab], root: Path, lab_id: str) -> int:
    lab = find_lab(labs, lab_id)
    payload: Dict[str, Any] = {
        "id": lab.lab_id,
        "title": lab.title,
        "path": str((root / lab.path).resolve()),
        "variants": lab.variants,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def cmd_up(
    labs: Sequence[Lab],
    root: Path,
    lab_id: str,
    variant: str,
    build: bool,
    pull: Optional[str],
    detach: bool,
    profiles: List[str],
    project_name: Optional[str],
    dry_run: bool,
) -> int:
    lab = find_lab(labs, lab_id)
    lab_dir = (root / lab.path).resolve()
    if not lab_dir.exists():
        raise FileNotFoundError(f"Lab folder not found: {lab_dir}")

    compose_cmd = detect_compose_command()
    args: List[str] = []

    args += compose_args_for_variant(lab, variant)

    pname = sanitise_project_name(project_name or lab.lab_id)
    args += ["-p", pname]

    for p in profiles:
        args += ["--profile", p]

    args += ["up"]
    if detach:
        args += ["-d"]
    if build:
        args += ["--build"]
    if pull:
        args += ["--pull", pull]

    return run_compose(compose_cmd, lab_dir, args, dry_run=dry_run)


def cmd_down(
    labs: Sequence[Lab],
    root: Path,
    lab_id: str,
    variant: str,
    volumes: bool,
    remove_orphans: bool,
    project_name: Optional[str],
    dry_run: bool,
) -> int:
    lab = find_lab(labs, lab_id)
    lab_dir = (root / lab.path).resolve()

    compose_cmd = detect_compose_command()

    args: List[str] = []
    args += compose_args_for_variant(lab, variant)

    pname = sanitise_project_name(project_name or lab.lab_id)
    args += ["-p", pname]

    args += ["down"]
    if volumes:
        args += ["-v"]
    if remove_orphans:
        args += ["--remove-orphans"]

    return run_compose(compose_cmd, lab_dir, args, dry_run=dry_run)


def cmd_ps(
    labs: Sequence[Lab],
    root: Path,
    lab_id: str,
    variant: str,
    project_name: Optional[str],
    dry_run: bool,
) -> int:
    lab = find_lab(labs, lab_id)
    lab_dir = (root / lab.path).resolve()

    compose_cmd = detect_compose_command()

    args: List[str] = []
    args += compose_args_for_variant(lab, variant)

    pname = sanitise_project_name(project_name or lab.lab_id)
    args += ["-p", pname]

    args += ["ps"]

    return run_compose(compose_cmd, lab_dir, args, dry_run=dry_run)


def cmd_logs(
    labs: Sequence[Lab],
    root: Path,
    lab_id: str,
    variant: str,
    follow: bool,
    tail: Optional[int],
    service: Optional[str],
    project_name: Optional[str],
    dry_run: bool,
) -> int:
    lab = find_lab(labs, lab_id)
    lab_dir = (root / lab.path).resolve()

    compose_cmd = detect_compose_command()

    args: List[str] = []
    args += compose_args_for_variant(lab, variant)

    pname = sanitise_project_name(project_name or lab.lab_id)
    args += ["-p", pname]

    args += ["logs"]
    if follow:
        args += ["-f"]
    if tail is not None:
        args += ["--tail", str(int(tail))]
    if service:
        args += [service]

    return run_compose(compose_cmd, lab_dir, args, dry_run=dry_run)


def main(argv: Optional[List[str]] = None) -> int:
    root = repo_root()
    labs = load_manifest(root)

    p = argparse.ArgumentParser(
        prog="lab_runner.py",
        description="Minimal Docker Compose lab runner for COMPNET-EN (Phase C pilot).",
    )
    p.add_argument("--dry-run", action="store_true", help="Print the docker compose command without running it")

    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List registered labs")

    sp_info = sub.add_parser("info", help="Show details for a lab")
    sp_info.add_argument("lab_id")

    def add_lab_args(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("lab_id")
        sp.add_argument(
            "--variant",
            default="default",
            help="Variant name (see 'list' output). Default: default",
        )
        sp.add_argument(
            "--project-name",
            default=None,
            help="Compose project name (default: derived from lab id)",
        )

    sp_up = sub.add_parser("up", help="Start a lab")
    add_lab_args(sp_up)
    sp_up.add_argument("--build", action="store_true", help="Build images before starting")
    sp_up.add_argument(
        "--pull",
        choices=["always", "missing", "never"],
        default=None,
        help="Pull policy (docker compose only): always/missing/never",
    )
    sp_up.add_argument(
        "--no-detach",
        action="store_true",
        help="Run in the foreground (default is detached)",
    )
    sp_up.add_argument(
        "--profile",
        action="append",
        default=[],
        dest="profiles",
        help="Enable a compose profile (repeatable)",
    )

    sp_down = sub.add_parser("down", help="Stop a lab")
    add_lab_args(sp_down)
    sp_down.add_argument("-v", "--volumes", action="store_true", help="Remove named volumes")
    sp_down.add_argument("--remove-orphans", action="store_true", help="Remove orphan containers")

    sp_ps = sub.add_parser("ps", help="Show container status for a lab")
    add_lab_args(sp_ps)

    sp_logs = sub.add_parser("logs", help="Show logs for a lab")
    add_lab_args(sp_logs)
    sp_logs.add_argument("-f", "--follow", action="store_true", help="Follow logs")
    sp_logs.add_argument("--tail", type=int, default=None, help="Number of lines to show")
    sp_logs.add_argument("service", nargs="?", default=None, help="Optional service name")

    args = p.parse_args(argv)

    if args.cmd == "list":
        return cmd_list(labs)

    if args.cmd == "info":
        return cmd_info(labs, root, args.lab_id)

    if args.cmd == "up":
        return cmd_up(
            labs,
            root,
            args.lab_id,
            args.variant,
            build=bool(args.build),
            pull=args.pull,
            detach=not bool(args.no_detach),
            profiles=list(args.profiles),
            project_name=args.project_name,
            dry_run=bool(args.dry_run),
        )

    if args.cmd == "down":
        return cmd_down(
            labs,
            root,
            args.lab_id,
            args.variant,
            volumes=bool(args.volumes),
            remove_orphans=bool(args.remove_orphans),
            project_name=args.project_name,
            dry_run=bool(args.dry_run),
        )

    if args.cmd == "ps":
        return cmd_ps(
            labs,
            root,
            args.lab_id,
            args.variant,
            project_name=args.project_name,
            dry_run=bool(args.dry_run),
        )

    if args.cmd == "logs":
        return cmd_logs(
            labs,
            root,
            args.lab_id,
            args.variant,
            follow=bool(args.follow),
            tail=args.tail,
            service=args.service,
            project_name=args.project_name,
            dry_run=bool(args.dry_run),
        )

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())

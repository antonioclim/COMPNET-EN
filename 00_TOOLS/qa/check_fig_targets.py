#!/usr/bin/env python3
"""check_fig_targets.py

Quality gate for lecture figure references.

Lectures use a lightweight figure marker syntax in Markdown:

    [FIG] assets/images/<name>.png

This script validates that each referenced PNG has a corresponding PlantUML
source at:

    assets/puml/<name>.puml

Two modes are provided:

- default (puml-only): require the PlantUML source but do not require the PNG
  to exist. This supports repositories where PNG renders are generated locally
  and kept out of version control.
- --require-png: require both the PlantUML source and the PNG render.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FIG_PATTERN = re.compile(r"^\s*\[FIG\]\s+(?P<path>\S+)\s*$")
PNG_REL_PATTERN = re.compile(r"^assets/images/(?P<name>[A-Za-z0-9._-]+)\.png$")


@dataclass(frozen=True)
class Finding:
    file: Path
    line_no: int
    message: str

    def format(self) -> str:
        return f"{self.file.as_posix()}:L{self.line_no}: {self.message}"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _iter_lecture_markdown_files(root: Path) -> list[Path]:
    lectures_dir = root / "03_LECTURES"
    if not lectures_dir.is_dir():
        return []

    md_files: list[Path] = []
    for lecture_dir in sorted(lectures_dir.iterdir()):
        if not lecture_dir.is_dir():
            continue
        if not re.fullmatch(r"C\d{2}", lecture_dir.name):
            continue

        md_files.extend(sorted(p for p in lecture_dir.glob("*.md") if p.is_file()))

    return md_files


def _check_file(md_path: Path, require_png: bool) -> list[Finding]:
    lecture_dir = md_path.parent

    findings: list[Finding] = []
    try:
        lines = md_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        findings.append(
            Finding(
                file=md_path,
                line_no=1,
                message=f"cannot be decoded as UTF-8: {exc}",
            )
        )
        return findings

    for idx, line in enumerate(lines, start=1):
        m = FIG_PATTERN.match(line)
        if not m:
            continue

        raw = m.group("path")
        m_png = PNG_REL_PATTERN.match(raw)
        if not m_png:
            findings.append(
                Finding(
                    file=md_path,
                    line_no=idx,
                    message=(
                        "invalid [FIG] target. Expected 'assets/images/<name>.png'"
                        f" but found '{raw}'"
                    ),
                )
            )
            continue

        name = m_png.group("name")
        expected_puml = lecture_dir / "assets" / "puml" / f"{name}.puml"
        if not expected_puml.is_file():
            findings.append(
                Finding(
                    file=md_path,
                    line_no=idx,
                    message=(
                        "missing PlantUML source for [FIG]. Expected "
                        f"'{expected_puml.as_posix()}'"
                    ),
                )
            )

        if require_png:
            expected_png = lecture_dir / "assets" / "images" / f"{name}.png"
            if not expected_png.is_file():
                findings.append(
                    Finding(
                        file=md_path,
                        line_no=idx,
                        message=(
                            "missing rendered PNG for [FIG]. Expected "
                            f"'{expected_png.as_posix()}'"
                        ),
                    )
                )

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate lecture [FIG] markers against assets/puml sources.",
    )
    parser.add_argument(
        "--require-png",
        action="store_true",
        help="Also require the referenced PNG to exist under assets/images/.",
    )
    parser.add_argument(
        "--puml-only",
        action="store_true",
        help="Require only the .puml source and ignore PNG existence (default).",
    )
    args = parser.parse_args(argv)

    # If both flags are provided, --require-png wins.
    require_png = bool(args.require_png)

    root = _repo_root()
    md_files = _iter_lecture_markdown_files(root)
    if not md_files:
        print("check_fig_targets  SKIPPED  (no lecture markdown files found)")
        return 0

    all_findings: list[Finding] = []
    for md in md_files:
        all_findings.extend(_check_file(md, require_png=require_png))

    if all_findings:
        for f in all_findings:
            print(f.format())
        print(f"check_fig_targets  FAILED  ({len(all_findings)} issue(s))")
        return 1

    mode = "require-png" if require_png else "puml-only"
    print(f"check_fig_targets  PASSED  ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

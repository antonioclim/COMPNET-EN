"""
report_generator.py — Markdown report helper for S13 (optional)

This small helper collects artefacts produced during the seminar and generates a
single Markdown report under:

  04_SEMINARS/S13/artifacts/report.md

Supported inputs (all optional)
-------------------------------
- Vulnerability checks:
    artifacts/vulncheck_*.json
  (produced by: S13_Part05_Script_Defensive_Vuln_Checker.py)

- A manual notes file:
    artifacts/notes.md  (or notes.txt)

The generator is **best-effort**: missing inputs are tolerated.

Usage
-----
  python3 report_generator.py
  python3 report_generator.py --out artifacts/my_report.md
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_vuln_reports(artifacts: Path) -> List[Path]:
    return sorted(artifacts.glob("vulncheck_*.json"))


def format_finding(f: Dict[str, Any]) -> str:
    kind = f.get("kind", "Finding")
    sev = f.get("severity", "info")
    evidence = f.get("evidence", "")
    rec = f.get("recommendation", "")
    return f"- **{kind}** *(severity={sev})*\n  - Evidence: {evidence}\n  - Recommendation: {rec}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate an S13 Markdown report from artefacts")
    ap.add_argument("--out", default=None, help="Output Markdown path (default: artifacts/report.md)")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    artifacts = here / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    out_path = Path(args.out) if args.out else (artifacts / "report.md")

    lines: List[str] = []
    lines.append("# S13 — Seminar report (auto-generated)")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")

    vuln_paths = find_vuln_reports(artifacts)
    if vuln_paths:
        lines.append("## Defensive vulnerability checks")
        lines.append("")
        for p in vuln_paths:
            data = load_json(p)
            service = data.get("service", "unknown")
            target = data.get("target", "unknown")
            port = data.get("port", "unknown")
            ts = data.get("timestamp_utc", "")
            lines.append(f"### {service} — {target}:{port}")
            if ts:
                lines.append(f"*Timestamp (UTC): {ts}*")
            lines.append("")
            findings = data.get("findings", [])
            if findings:
                for f in findings:
                    lines.append(format_finding(f))
            else:
                lines.append("- No findings recorded.")
            lines.append("")
    else:
        lines.append("## Defensive vulnerability checks")
        lines.append("")
        lines.append("_No `vulncheck_*.json` artefacts found yet._")
        lines.append("")

    # Optional notes
    notes_md = artifacts / "notes.md"
    notes_txt = artifacts / "notes.txt"
    if notes_md.exists() or notes_txt.exists():
        lines.append("## Notes")
        lines.append("")
        notes_path = notes_md if notes_md.exists() else notes_txt
        lines.append(notes_path.read_text(encoding="utf-8").rstrip())
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

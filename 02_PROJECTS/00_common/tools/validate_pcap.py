#!/usr/bin/env python3
"""
validate_pcap.py — deterministic validation (tshark) for PCAP/PCAPNG captures
Computer Networks Project Catalogue — RC2026

Typical use (in the student repository):
    python tools/validate_pcap.py --project S01 --pcap artifacts/pcap/traffic_e2.pcap

Notes:
- requires tshark to be installed (Wireshark CLI)
- rules are stored in tools/pcap_rules/<PROJECT>.json
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


_COND_RE = re.compile(r"^\s*(==|>=|<=|>|<)\s*(\d+)\s*$")


@dataclass
class RuleResult:
    rule_id: str
    passed: bool
    expected: str
    observed: int
    filt: str
    description: str


def _parse_condition(cond: str) -> Tuple[str, int]:
    m = _COND_RE.match(cond)
    if not m:
        raise ValueError(
            f"Invalid condition: {cond!r}. Use one of: '>= N', '<= N', '== N', '> N', '< N'."
        )
    op, n = m.group(1), int(m.group(2))
    return op, n


def _eval_condition(op: str, n: int, observed: int) -> bool:
    if op == "==":
        return observed == n
    if op == ">=":
        return observed >= n
    if op == "<=":
        return observed <= n
    if op == ">":
        return observed > n
    if op == "<":
        return observed < n
    raise ValueError(op)


def _run_tshark_count(pcap_path: Path, display_filter: str, decode_as: List[str]) -> int:
    tshark = shutil.which("tshark")
    if tshark is None:
        raise RuntimeError(
            "tshark is not installed or not on PATH. Install Wireshark (CLI) in the VM."
        )

    # Command: tshark -r file -Y "filter" -T fields -e frame.number
    # Count = number of lines.
    cmd = [tshark, "-r", str(pcap_path), "-Y", display_filter, "-T", "fields", "-e", "frame.number"]

    # decode-as (optional) for non-standard ports
    for d in decode_as:
        cmd.extend(["-d", d])

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    except FileNotFoundError:
        raise RuntimeError("tshark cannot be executed. Check the installation.")

    if proc.returncode != 0:
        # tshark returns non-zero for invalid filters as well
        raise RuntimeError(
            "tshark error.\n"
            f"Filter: {display_filter}\n"
            f"Decode-as: {decode_as}\n"
            f"STDERR:\n{proc.stderr.strip()}\n"
        )

    # Each line corresponds to a frame.number
    out = proc.stdout.strip()
    if not out:
        return 0
    return len(out.splitlines())


def load_rules(rules_dir: Path, project: str) -> Dict[str, Any]:
    rules_path = rules_dir / f"{project}.json"
    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")
    return json.loads(rules_path.read_text(encoding="utf-8"))


def validate(pcap_path: Path, rules: Dict[str, Any]) -> List[RuleResult]:
    decode_as: List[str] = rules.get("decode_as", []) or []
    results: List[RuleResult] = []
    for r in rules["rules"]:
        rule_id = r["id"]
        filt = r["filter"]
        expected = r["condition"]
        description = r.get("description", "")
        op, n = _parse_condition(expected)
        observed = _run_tshark_count(pcap_path, filt, decode_as)
        passed = _eval_condition(op, n, observed)
        results.append(RuleResult(rule_id, passed, expected, observed, filt, description))
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Project code (e.g. S01, A06)")
    ap.add_argument("--pcap", required=True, help="Path to the PCAP/PCAPNG file (e.g. artifacts/pcap/traffic_e2.pcap)")
    ap.add_argument("--rules-dir", default="tools/pcap_rules", help="Directory containing JSON rules (default: tools/pcap_rules)")
    args = ap.parse_args()

    project = args.project.strip().upper()
    pcap_path = Path(args.pcap).expanduser().resolve()
    rules_dir = Path(args.rules_dir).expanduser().resolve()

    if not pcap_path.exists():
        print(f"[FAIL] PCAP not found: {pcap_path}", file=sys.stderr)
        return 2

    try:
        rules = load_rules(rules_dir, project)
    except Exception as e:
        print(f"[FAIL] Unable to load rules: {e}", file=sys.stderr)
        return 2

    print(f"== PCAP validation for {project} ==")
    print(f"PCAP: {pcap_path}")
    if rules.get("decode_as"):
        print(f"Decode-as: {rules['decode_as']}")
    print()

    try:
        results = validate(pcap_path, rules)
    except Exception as e:
        print(f"[FAIL] Validation aborted: {e}", file=sys.stderr)
        return 2

    ok = True
    for rr in results:
        status = "OK" if rr.passed else "FAIL"
        if not rr.passed:
            ok = False
        print(f"[{status}] {rr.rule_id}: {rr.description}")
        print(f"       expected {rr.expected}, observed {rr.observed}")
        print(f"       filter: {rr.filt}")
    print()

    if ok:
        print("[OK] All rules passed.")
        return 0
    print("[FAIL] Some rules failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

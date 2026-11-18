#!/usr/bin/env python3
"""
validate_pcap.py — explicit capture checks (tshark) for PCAP/PCAPNG evidence
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
    measurement: str = "frames"


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


def _tshark_fields(pcap_path: Path, display_filter: str, decode_as: List[str],
                   fields: List[str], keylog: Path | None = None) -> List[List[str]]:
    tshark = shutil.which("tshark")
    if tshark is None:
        raise RuntimeError("tshark is not installed or not on PATH. Install Wireshark CLI in the VM.")
    cmd = [tshark, "-2", "-r", str(pcap_path), "-Y", display_filter,
           "-T", "fields", "-E", "occurrence=a", "-E", "aggregator=,",
           "-o", "tcp.desegment_tcp_streams:TRUE",
           "-o", "tcp.relative_sequence_numbers:TRUE"]
    for field in fields:
        cmd.extend(["-e", field])
    for decode in decode_as:
        cmd.extend(["-d", decode])
    if keylog is not None:
        cmd.extend(["-o", f"tls.keylog_file:{keylog}"])
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=90)
    if proc.returncode:
        raise RuntimeError(f"tshark failed for {display_filter!r}: {proc.stderr.strip()}")
    return [line.split("\t") for line in proc.stdout.splitlines() if line.strip()]


def _run_tshark_count(pcap_path: Path, display_filter: str, decode_as: List[str]) -> int:
    return len(_tshark_fields(pcap_path, display_filter, decode_as, ["frame.number"]))


def reassemble_segments(segments: List[Tuple[int, bytes]]) -> bytes:
    """Reassemble one direction; deduplicate retransmissions and reject gaps/conflicts.

    The course captures are bounded, short sessions. Sequence numbers are the
    relative tcp.seq values emitted by tshark. Incomplete captures must not be
    accepted as an application trace.
    """
    if not segments:
        return b""
    ordered = sorted(segments)
    start = ordered[0][0]
    if start != 1:
        raise ValueError("TCP application capture must start at relative sequence 1; capture the handshake.")
    result = bytearray()
    for seq, payload in ordered:
        offset = seq - start
        if offset > len(result):
            raise ValueError("Gap in captured TCP payload; cannot count complete commands.")
        overlap = min(len(result) - offset, len(payload))
        if result[offset:offset + overlap] != payload[:overlap]:
            raise ValueError("Conflicting TCP retransmission; application trace is ambiguous.")
        result.extend(payload[overlap:])
        if len(result) > 16 * 1024 * 1024:
            raise ValueError("TCP direction exceeds the 16 MiB teaching-capture limit.")
    return bytes(result)


def count_tcp_commands(rows: List[List[str]], commands: List[str]) -> int:
    """Count complete LF/CRLF-delimited commands, not substrings or packets."""
    streams: Dict[str, List[Tuple[int, bytes]]] = {}
    for row in rows:
        if len(row) != 3:
            raise ValueError("Unexpected tshark TCP field output.")
        stream, sequence, payload = row
        if payload:
            streams.setdefault(stream, []).append((int(sequence), bytes.fromhex(payload.replace(":", ""))))
    wanted = {command.encode("ascii") for command in commands}
    count = 0
    for segments in streams.values():
        payload = reassemble_segments(segments)
        if payload and not payload.endswith(b"\n"):
            raise ValueError("Incomplete command at end of TCP stream; expected LF/CRLF framing.")
        for line in payload.split(b"\n"):
            tokens = line.split(None, 1)
            if tokens and tokens[0] in wanted:
                count += 1
    return count


def validate_manifest(rules: Dict[str, Any], project: str | None = None) -> None:
    if not isinstance(rules, dict) or not isinstance(rules.get("project"), str) or not rules["project"].strip():
        raise ValueError("Rules must be an object with a project code.")
    if project is not None and rules["project"] != project:
        raise ValueError("Requested project and rule-manifest project do not agree.")
    items = rules.get("rules")
    if not isinstance(items, list) or not items:
        raise ValueError("The rules list must be non-empty; no validation can pass without checks.")
    decode_as = rules.get("decode_as", [])
    if not isinstance(decode_as, list) or any(not isinstance(v, str) or not v for v in decode_as):
        raise ValueError("decode_as must contain non-empty strings.")
    manual = rules.get("manual_checks", [])
    if not isinstance(manual, list) or any(not isinstance(v, str) or not v.strip() for v in manual):
        raise ValueError("manual_checks must contain non-empty strings.")
    ids = set()
    for rule in items:
        if not isinstance(rule, dict):
            raise ValueError("Each rule must be an object.")
        for field in ("id", "filter", "condition", "description"):
            if not isinstance(rule.get(field), str) or not rule[field].strip():
                raise ValueError(f"Rule field {field} must be a non-empty string.")
        if rule["id"] in ids:
            raise ValueError(f"Duplicate rule ID: {rule['id']}")
        ids.add(rule["id"])
        _parse_condition(rule["condition"])
        mode = rule.get("measurement", "frames")
        if mode not in {"frames", "tcp_commands", "field_occurrences", "distinct_values"}:
            raise ValueError(f"Unknown measurement: {mode}")
        if mode == "tcp_commands":
            commands = rule.get("commands")
            if not isinstance(commands, list) or not commands or any(
                not isinstance(c, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", c) for c in commands
            ):
                raise ValueError("tcp_commands needs a non-empty list of ASCII command tokens.")
        if mode in {"field_occurrences", "distinct_values"} and not re.fullmatch(
            r"[A-Za-z0-9_.]+", str(rule.get("field", ""))
        ):
            raise ValueError("Field measurement needs a valid tshark field name.")
        if rule.get("aggregation", "sum") not in {"sum", "max_per_stream"}:
            raise ValueError("Unknown field aggregation.")


def load_rules(rules_dir: Path, project: str) -> Dict[str, Any]:
    rules_path = rules_dir / f"{project}.json"
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    validate_manifest(rules, project)
    return rules


def validate(pcap_path: Path, rules: Dict[str, Any], keylog: Path | None = None) -> List[RuleResult]:
    validate_manifest(rules)
    decode_as = rules.get("decode_as", [])
    results = []
    for rule in rules["rules"]:
        mode = rule.get("measurement", "frames")
        filt = rule["filter"]
        if mode == "tcp_commands":
            rows = _tshark_fields(pcap_path, filt, decode_as,
                                  ["tcp.stream", "tcp.seq", "tcp.payload"], keylog)
            observed = count_tcp_commands(rows, rule["commands"])
        elif mode in {"field_occurrences", "distinct_values"}:
            rows = _tshark_fields(pcap_path, filt, decode_as, ["tcp.stream", rule["field"]], keylog)
            counts: Dict[str, int] = {}
            unique = set()
            for row in rows:
                stream, values = (row + [""])[:2]
                tokens = [value for value in values.split(",") if value]
                if "value" in rule:
                    tokens = [value for value in tokens if value == rule["value"]]
                counts[stream] = counts.get(stream, 0) + len(tokens)
                unique.update(tokens)
            observed = len(unique) if mode == "distinct_values" else (
                max(counts.values(), default=0) if rule.get("aggregation") == "max_per_stream"
                else sum(counts.values()))
        elif keylog is None:
            observed = _run_tshark_count(pcap_path, filt, decode_as)
        else:
            observed = len(_tshark_fields(pcap_path, filt, decode_as, ["frame.number"], keylog))
        op, n = _parse_condition(rule["condition"])
        results.append(RuleResult(rule["id"], _eval_condition(op, n, observed),
                                  rule["condition"], observed, filt, rule["description"], mode))
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Project code (e.g. S01, A06)")
    ap.add_argument("--pcap", required=True, help="Path to the PCAP/PCAPNG file (e.g. artifacts/pcap/traffic_e2.pcap)")
    ap.add_argument("--rules-dir", default="tools/pcap_rules", help="Directory containing JSON rules (default: tools/pcap_rules)")
    ap.add_argument("--tls-keylog", type=Path, help="Optional session secrets from this local test; keep outside Git")
    args = ap.parse_args()

    project = args.project.strip().upper()
    pcap_path = Path(args.pcap).expanduser().resolve()
    rules_dir = Path(args.rules_dir).expanduser().resolve()

    if args.tls_keylog is not None and not args.tls_keylog.is_file():
        print("[FAIL] TLS key-log file does not exist", file=sys.stderr)
        return 2

    if not pcap_path.is_file():
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
        results = validate(pcap_path, rules, args.tls_keylog)
    except Exception as e:
        print(f"[FAIL] Validation aborted: {e}", file=sys.stderr)
        return 2

    ok = True
    for rr in results:
        status = "OK" if rr.passed else "FAIL"
        if not rr.passed:
            ok = False
        print(f"[{status}] {rr.rule_id}: {rr.description}")
        print(f"       expected {rr.expected}, observed {rr.observed} ({rr.measurement})")
        print(f"       filter: {rr.filt}")
    print()

    if ok:
        print("[OK] All capture checks passed; this is not full project acceptance.")
        for check in rules.get("manual_checks", []):
            print(f"[REVIEW] {check}")
        return 0
    print("[FAIL] Some rules failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

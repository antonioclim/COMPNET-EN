#!/usr/bin/env python3
"""
pcap_tshark_summary.py — optional tshark-based summary (labs)

This helper is intentionally conservative:
- If `tshark` is not installed, it prints a short hint and exits with code 2.
- It does *not* attempt to parse PCAPs on its own; that is the role of `pcap_stats.py`.

Examples
--------
  python3 pcap_tshark_summary.py --pcap capture.pcap
  python3 pcap_tshark_summary.py --pcap capture.pcap --out artifacts/summary.txt
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser(description="Optional tshark summary for a PCAP")
    ap.add_argument("--pcap", required=True, help="PCAP file path")
    ap.add_argument("--out", default=None, help="Write summary to this file (optional)")
    args = ap.parse_args()

    if not os.path.exists(args.pcap):
        print(f"[ERROR] PCAP not found: {args.pcap}", file=sys.stderr)
        return 2

    if shutil.which("tshark") is None:
        print("[INFO] tshark not found. Install Wireshark/tshark or use pcap_stats.py only.")
        return 2

    pcap = args.pcap
    sections: list[tuple[str, list[str]]] = [
        ("Capture metadata (capinfos)", ["tshark", "-r", pcap, "-q", "-z", "io,stat,0"]),
        ("Endpoints (IP)", ["tshark", "-r", pcap, "-q", "-z", "endpoints,ip"]),
        ("Conversations (TCP)", ["tshark", "-r", pcap, "-q", "-z", "conv,tcp"]),
        ("Conversations (UDP)", ["tshark", "-r", pcap, "-q", "-z", "conv,udp"]),
        ("Protocol hierarchy", ["tshark", "-r", pcap, "-q", "-z", "io,phs"]),
    ]

    out_lines: list[str] = []
    out_lines.append("=" * 72)
    out_lines.append("tshark summary")
    out_lines.append("=" * 72)
    out_lines.append(f"File: {pcap}")
    out_lines.append("")

    for title, cmd in sections:
        out_lines.append("-" * 72)
        out_lines.append(title)
        out_lines.append("-" * 72)
        rc, stdout = run(cmd)
        if rc != 0:
            out_lines.append(f"[WARN] Command failed (rc={rc}): {' '.join(cmd)}")
        out_lines.append(stdout.rstrip())
        out_lines.append("")

    result = "\n".join(out_lines).rstrip() + "\n"

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"[OK] Wrote: {out_path}")
        return 0

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

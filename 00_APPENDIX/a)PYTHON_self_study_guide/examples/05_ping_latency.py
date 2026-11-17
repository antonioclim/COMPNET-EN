#!/usr/bin/env python3
"""Read Linux ping results using a dataclass; run inside the VM or WSL Linux.

Each observation runs one iputils ping with a bounded wait. The standard ping
program performs ICMP; Python orchestrates it and parses its textual output.
A result marked succeeded still needs an RTT match to contribute to statistics.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import ipaddress
import math
import os
import re
import shutil
import statistics
import subprocess
from typing import Optional


@dataclass
class PingResult:
    sequence: int
    rtt_ms: Optional[float]
    succeeded: bool
    message: str = ''


def parse_ping_rtt(output: str) -> Optional[float]:
    """Return iputils' millisecond RTT (an upper bound for a time< sample)."""
    match = re.search(r'\btime[=<]\s*(\d+(?:\.\d+)?)\s*ms\b', output)
    return float(match.group(1)) if match else None


def run_ping(host: str, count: int = 3, timeout: float = 1.0) -> list[PingResult]:
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', host):
            raise ValueError('Use an IP address or hostname without shell syntax')
    if not 1 <= count <= 100 or not 0 < timeout <= 60:
        raise ValueError('count must be 1–100 and timeout must be greater than 0 and at most 60 seconds')
    executable = shutil.which('ping')
    if executable is None:
        raise RuntimeError('Linux ping is missing; install the iputils-ping package in your lab environment')
    results = []
    for sequence in range(1, count + 1):
        try:
            process = subprocess.run(
                [executable, '-n', '-c', '1', '-W', str(math.ceil(timeout)), host],
                capture_output=True, text=True, timeout=timeout + 3,
                env={**os.environ, 'LC_ALL': 'C'}, check=False)
            rtt = parse_ping_rtt(process.stdout)
            results.append(PingResult(sequence, rtt, process.returncode == 0,
                                      process.stderr.strip() or ('RTT parser found no sample' if rtt is None else '')))
        except subprocess.TimeoutExpired:
            results.append(PingResult(sequence, None, False, 'ping process timed out'))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--count', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=1.0)
    args = parser.parse_args()
    try:
        results = run_ping(args.host, args.count, args.timeout)
    except (ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    for result in results:
        print(result)
    samples = [r.rtt_ms for r in results if r.succeeded and r.rtt_ms is not None]
    print(f'Replies: {sum(r.succeeded for r in results)}/{len(results)}')
    if samples:
        print(f'RTT ms: min={min(samples):.3f}, mean={statistics.mean(samples):.3f}, max={max(samples):.3f}')
    return 0 if len(samples) == len(results) else 1


if __name__ == '__main__':
    raise SystemExit(main())

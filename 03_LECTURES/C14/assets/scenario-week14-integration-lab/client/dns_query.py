#!/usr/bin/env python3
"""Minimal DNS A-record query tool (stdlib only).

This exists so the lab can demonstrate TTL/caching without requiring dig/drill.

Examples (inside the client container):
  python dns_query.py www.week14.local
  python dns_query.py www.week14.local --server 10.14.0.10   # query auth directly
  python dns_query.py www.week14.local --server 10.14.0.53   # query resolver
  python dns_query.py www.week14.local --repeat 2 --sleep 5

"""

from __future__ import annotations

import argparse
import os
import random
import socket
import struct
import time
from typing import List, Tuple


def _encode_qname(name: str) -> bytes:
    parts = [p for p in name.strip(".").split(".") if p]
    out = b""
    for p in parts:
        b = p.encode("ascii")
        if len(b) > 63:
            raise ValueError("DNS label too long")
        out += struct.pack("!B", len(b)) + b
    return out + b"\x00"


def _read_name(data: bytes, offset: int, depth: int = 0) -> Tuple[str, int]:
    # Handle compression pointers.
    if depth > 10:
        raise ValueError("DNS name compression loop")

    labels: List[str] = []
    i = offset
    jumped = False
    jump_to = 0

    while True:
        if i >= len(data):
            raise ValueError("DNS name out of bounds")
        length = data[i]
        # pointer: 11xxxxxx xxxxxxxx
        if (length & 0xC0) == 0xC0:
            if i + 1 >= len(data):
                raise ValueError("Truncated DNS pointer")
            ptr = ((length & 0x3F) << 8) | data[i + 1]
            if not jumped:
                jump_to = i + 2
                jumped = True
            name, _ = _read_name(data, ptr, depth + 1)
            labels.append(name)
            i += 2
            break
        if length == 0:
            i += 1
            break
        i += 1
        if i + length > len(data):
            raise ValueError("Truncated DNS label")
        label = data[i : i + length].decode("ascii", errors="replace")
        labels.append(label)
        i += length

    if jumped:
        return ".".join(labels).replace("..", "."), jump_to
    return ".".join(labels), i


def query_a(server: str, name: str, timeout: float = 2.0) -> List[Tuple[str, int, str]]:
    """Return list of (rrname, ttl, ipv4) for A answers."""
    tid = random.randint(0, 0xFFFF)
    flags = 0x0100  # recursion desired
    qdcount = 1
    header = struct.pack("!HHHHHH", tid, flags, qdcount, 0, 0, 0)
    qname = _encode_qname(name)
    qtype = 1  # A
    qclass = 1  # IN
    question = qname + struct.pack("!HH", qtype, qclass)
    packet = header + question

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(packet, (server, 53))
    data, _ = sock.recvfrom(4096)

    if len(data) < 12:
        raise ValueError("Truncated DNS response")

    rid, rflags, rqd, ranc, rns, rar = struct.unpack("!HHHHHH", data[:12])
    if rid != tid:
        raise ValueError("Transaction ID mismatch")

    rcode = rflags & 0x000F
    if rcode != 0:
        raise ValueError(f"DNS error rcode={rcode}")

    offset = 12

    # Skip questions
    for _ in range(rqd):
        _, offset = _read_name(data, offset)
        offset += 4  # qtype + qclass

    answers: List[Tuple[str, int, str]] = []

    # Parse answers
    for _ in range(ranc):
        rrname, offset = _read_name(data, offset)
        if offset + 10 > len(data):
            raise ValueError("Truncated RR")
        rtype, rclass, ttl, rdlen = struct.unpack("!HHIH", data[offset : offset + 10])
        offset += 10
        rdata = data[offset : offset + rdlen]
        offset += rdlen

        if rclass != 1:
            continue
        if rtype == 1 and rdlen == 4:
            ipv4 = ".".join(str(b) for b in rdata)
            answers.append((rrname, int(ttl), ipv4))

    return answers


def main() -> int:
    ap = argparse.ArgumentParser(description="Minimal DNS A-record query tool (Week 14 lab)")
    ap.add_argument("name", help="DNS name to query")
    ap.add_argument("--server", default=os.environ.get("DNS_SERVER", "10.14.0.53"), help="DNS server IP")
    ap.add_argument("--repeat", type=int, default=1, help="Repeat count")
    ap.add_argument("--sleep", type=float, default=0.0, help="Sleep between repeats (seconds)")

    args = ap.parse_args()

    for i in range(args.repeat):
        ans = query_a(args.server, args.name)
        ts = time.strftime("%H:%M:%S")
        if not ans:
            print(f"[{ts}] NO A ANSWERS")
        else:
            for rrname, ttl, ipv4 in ans:
                print(f"[{ts}] {rrname} A {ipv4} TTL={ttl} (server={args.server})")
        if i + 1 < args.repeat and args.sleep:
            time.sleep(args.sleep)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

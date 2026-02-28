#!/usr/bin/env python3
"""
pcap_stats.py — quick PCAP statistics (labs)

Design constraints
------------------
- Must work in a teaching environment where third-party Python packages may
  *not* be installed.
- Prefer Scapy or dpkt when available, but provide a robust fallback.

Backends
--------
- scapy  : supports many capture formats; most feature-rich.
- dpkt   : lightweight; supports classic pcap (pcapng support varies).
- pure   : classic PCAP only (not pcapng); Ethernet + Linux cooked capture.

Usage
-----
  python3 pcap_stats.py --pcap file.pcap
  python3 pcap_stats.py --pcap file.pcap --json
  python3 pcap_stats.py --pcap file.pcap --backend pure
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass
class Stats:
    packets: int = 0
    bytes: int = 0
    ipv4: int = 0
    icmp: int = 0
    tcp: int = 0
    udp: int = 0
    other_l3: int = 0
    truncated: int = 0
    linktype: Optional[int] = None
    backend: str = "auto"


def _env_backend_choice(choice: str) -> str:
    choice = (choice or "auto").strip().lower()
    if choice not in {"auto", "scapy", "dpkt", "pure"}:
        raise ValueError(f"Unknown backend: {choice!r}")
    return choice


def _is_pcapng_magic(magic: int) -> bool:
    # pcapng Section Header Block magic is 0x0A0D0D0A
    return magic == 0x0A0D0D0A


def _pcap_endianness_from_magic(magic: int) -> Optional[str]:
    # Classic PCAP magic numbers:
    #   0xA1B2C3D4 (big-endian) or 0xD4C3B2A1 (little-endian)
    # Variants for nanosecond resolution exist; not used in our fallback.
    if magic == 0xA1B2C3D4:
        return ">"
    if magic == 0xD4C3B2A1:
        return "<"
    # ns variants
    if magic == 0xA1B23C4D:
        return ">"
    if magic == 0x4D3CB2A1:
        return "<"
    return None


def _parse_ipv4_proto(frame: bytes, linktype: int) -> Optional[int]:
    """
    Extract IPv4 protocol field from a frame, for a limited set of linktypes.

    Returns:
        ip_proto int (e.g. 1=ICMP, 6=TCP, 17=UDP) or None if not IPv4/unknown.
    """
    # DLT_EN10MB = 1 (Ethernet)
    if linktype == 1:
        if len(frame) < 14:
            return None
        eth_type = struct.unpack("!H", frame[12:14])[0]
        offset = 14

        # 802.1Q VLAN tag
        if eth_type == 0x8100:
            if len(frame) < 18:
                return None
            eth_type = struct.unpack("!H", frame[16:18])[0]
            offset = 18

        if eth_type != 0x0800:
            return None

        if len(frame) < offset + 20:
            return None

        v_ihl = frame[offset]
        version = v_ihl >> 4
        ihl = (v_ihl & 0x0F) * 4
        if version != 4 or ihl < 20:
            return None
        if len(frame) < offset + ihl:
            return None
        return frame[offset + 9]

    # DLT_LINUX_SLL = 113 (Linux cooked capture)
    if linktype == 113:
        if len(frame) < 16:
            return None
        proto = struct.unpack("!H", frame[14:16])[0]
        offset = 16
        if proto != 0x0800:
            return None
        if len(frame) < offset + 20:
            return None
        v_ihl = frame[offset]
        version = v_ihl >> 4
        ihl = (v_ihl & 0x0F) * 4
        if version != 4 or ihl < 20:
            return None
        if len(frame) < offset + ihl:
            return None
        return frame[offset + 9]

    return None


def stats_pure_pcap(path: str) -> Stats:
    st = Stats(backend="pure")

    with open(path, "rb") as f:
        header = f.read(24)
        if len(header) != 24:
            raise ValueError("File too small to be a classic PCAP (missing global header).")

        magic = struct.unpack("<I", header[0:4])[0]
        if _is_pcapng_magic(magic):
            raise ValueError("PCAPNG detected. The pure backend supports classic PCAP only. "
                             "Install scapy, or convert the capture to PCAP.")

        endian = _pcap_endianness_from_magic(magic)
        if endian is None:
            raise ValueError(f"Unknown PCAP magic number: 0x{magic:08x}")

        # Global header fields:
        #   magic(4), version_major(2), version_minor(2), thiszone(4),
        #   sigfigs(4), snaplen(4), network(4)
        _version_major, _version_minor, _thiszone, _sigfigs, _snaplen, network = struct.unpack(
            endian + "HHiiii", header[4:24]
        )
        st.linktype = network

        rec_hdr_fmt = endian + "IIII"  # ts_sec, ts_usec, incl_len, orig_len
        rec_hdr_size = struct.calcsize(rec_hdr_fmt)

        while True:
            rh = f.read(rec_hdr_size)
            if not rh:
                break
            if len(rh) != rec_hdr_size:
                st.truncated += 1
                break

            _ts_sec, _ts_subsec, incl_len, _orig_len = struct.unpack(rec_hdr_fmt, rh)
            frame = f.read(incl_len)
            if len(frame) != incl_len:
                st.truncated += 1
                break

            st.packets += 1
            st.bytes += incl_len

            proto = _parse_ipv4_proto(frame, network)
            if proto is None:
                st.other_l3 += 1
                continue

            st.ipv4 += 1
            if proto == 1:
                st.icmp += 1
            elif proto == 6:
                st.tcp += 1
            elif proto == 17:
                st.udp += 1
            else:
                st.other_l3 += 1

    return st


def stats_dpkt(path: str) -> Stats:
    st = Stats(backend="dpkt")
    import dpkt  # type: ignore

    with open(path, "rb") as f:
        reader = dpkt.pcap.Reader(f)
        st.linktype = reader.datalink()
        for ts, buf in reader:
            st.packets += 1
            st.bytes += len(buf)

            proto = _parse_ipv4_proto(buf, st.linktype or 1)
            if proto is None:
                st.other_l3 += 1
                continue

            st.ipv4 += 1
            if proto == 1:
                st.icmp += 1
            elif proto == 6:
                st.tcp += 1
            elif proto == 17:
                st.udp += 1
            else:
                st.other_l3 += 1
    return st


def stats_scapy(path: str) -> Stats:
    st = Stats(backend="scapy")
    from scapy.utils import PcapReader  # type: ignore
    from scapy.layers.inet import IP, TCP, UDP, ICMP  # type: ignore

    with PcapReader(path) as pr:
        for pkt in pr:
            st.packets += 1
            st.bytes += len(bytes(pkt))
            if IP in pkt:
                st.ipv4 += 1
                if ICMP in pkt:
                    st.icmp += 1
                elif TCP in pkt:
                    st.tcp += 1
                elif UDP in pkt:
                    st.udp += 1
                else:
                    st.other_l3 += 1
            else:
                st.other_l3 += 1
    return st


def _select_backend(choice: str) -> str:
    choice = _env_backend_choice(choice)
    if choice != "auto":
        return choice

    # Auto-detect: prefer scapy > dpkt > pure.
    try:
        import scapy  # noqa: F401
        return "scapy"
    except Exception:
        pass

    try:
        import dpkt  # noqa: F401
        return "dpkt"
    except Exception:
        pass

    return "pure"


def _as_dict(st: Stats) -> Dict[str, object]:
    return {
        "backend": st.backend,
        "linktype": st.linktype,
        "packets": st.packets,
        "bytes": st.bytes,
        "ipv4": st.ipv4,
        "icmp": st.icmp,
        "tcp": st.tcp,
        "udp": st.udp,
        "other_l3": st.other_l3,
        "truncated": st.truncated,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Quick PCAP stats (labs)")
    ap.add_argument("--pcap", required=True, help="Path to a PCAP file")
    ap.add_argument("--backend", default="auto", help="auto|scapy|dpkt|pure")
    ap.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = ap.parse_args()

    pcap_path = args.pcap
    if not os.path.exists(pcap_path):
        print(f"[ERROR] PCAP not found: {pcap_path}", file=sys.stderr)
        return 2

    backend = _select_backend(args.backend)

    try:
        if backend == "scapy":
            st = stats_scapy(pcap_path)
        elif backend == "dpkt":
            st = stats_dpkt(pcap_path)
        else:
            st = stats_pure_pcap(pcap_path)
    except Exception as exc:
        print(f"[ERROR] Failed to analyse capture with backend={backend!r}: {exc}", file=sys.stderr)
        if backend == "auto":
            print("[HINT] Try --backend pure for classic PCAP, or install scapy for pcapng support.", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(_as_dict(st), indent=2, sort_keys=True))
        return 0

    # Human-readable output
    print("=" * 72)
    print("PCAP statistics")
    print("=" * 72)
    print(f"File:       {pcap_path}")
    print(f"Backend:    {st.backend}")
    print(f"Linktype:   {st.linktype}")
    print(f"Packets:    {st.packets}")
    print(f"Bytes:      {st.bytes}")
    if st.packets:
        print(f"Avg bytes:  {st.bytes / st.packets:.1f}")
    print("-" * 72)
    print(f"IPv4:       {st.ipv4}")
    print(f"  ICMP:     {st.icmp}")
    print(f"  TCP:      {st.tcp}")
    print(f"  UDP:      {st.udp}")
    print(f"  Other L3: {st.other_l3}")
    if st.truncated:
        print(f"Truncated records: {st.truncated}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

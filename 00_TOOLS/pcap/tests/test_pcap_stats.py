"""Small classic-PCAP fixtures cover both byte orders and time resolutions."""
import importlib.util
from pathlib import Path
import struct
import subprocess
import sys

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "pcap_stats.py"
SPEC = importlib.util.spec_from_file_location("course_pcap_stats", SOURCE)
stats = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = stats
SPEC.loader.exec_module(stats)


def capture(endian="<", nanoseconds=False, linktype=1):
    magic = 0xA1B23C4D if nanoseconds else 0xA1B2C3D4
    header = struct.pack(endian + "IHHiIII", magic, 2, 4, 0, 0, 65535, linktype)
    frames = []
    for proto in (1, 6, 17):
        ip = bytes([0x45, 0, 0, 20, 0, 0, 0, 0, 64, proto]) + b"\0" * 10
        link = b"\0" * (12 if linktype == 1 else 14) + b"\x08\x00"
        frames.append(link + ip)
    return header + b"".join(struct.pack(endian + "IIII", 1, 0, len(f), len(f)) + f for f in frames), frames


@pytest.mark.parametrize("endian", ["<", ">"])
@pytest.mark.parametrize("nanoseconds", [False, True])
@pytest.mark.parametrize("linktype", [1, 113])
def test_all_four_magic_sequences_have_identical_statistics(tmp_path, endian, nanoseconds, linktype):
    raw, frames = capture(endian, nanoseconds, linktype)
    p = tmp_path / "example.pcap"
    p.write_bytes(raw)
    result = stats.stats_pure_pcap(str(p))
    assert (result.packets, result.bytes, result.ipv4, result.icmp, result.tcp, result.udp, result.truncated) == (3, sum(map(len, frames)), 3, 1, 1, 1, 0)
    assert result.linktype == linktype


@pytest.mark.parametrize("tail", [b"x", struct.pack("<IIII", 1, 0, 100, 100) + b"x"])
def test_truncated_record_preserves_counts_and_cli_failure(tmp_path, tail):
    raw, _ = capture()
    p = tmp_path / "truncated.pcap"
    p.write_bytes(raw + tail)
    result = stats.stats_pure_pcap(str(p))
    assert result.packets == 3 and result.truncated == 1
    proc = subprocess.run([sys.executable, str(SOURCE), "--pcap", str(p), "--backend", "pure", "--json"], capture_output=True, text=True)
    assert proc.returncode == 1 and '"truncated": 1' in proc.stdout


@pytest.mark.parametrize("kind", ["unknown", "pcapng", "linktype", "length"])
def test_unsupported_or_invalid_input_is_explicit(tmp_path, kind):
    raw, _ = capture()
    if kind == "unknown":
        raw = b"BAD!" + raw[4:]
    elif kind == "pcapng":
        raw = b"\x0a\x0d\x0d\x0a" + raw[4:]
    elif kind == "linktype":
        raw = raw[:20] + struct.pack("<I", 999) + raw[24:]
    else:
        raw = raw[:24] + struct.pack("<IIII", 0, 0, 0xFFFFFFFF, 1)
    p = tmp_path / "invalid.pcap"
    p.write_bytes(raw)
    with pytest.raises(ValueError):
        stats.stats_pure_pcap(str(p))

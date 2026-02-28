# PCAP utilities (optional)

This folder contains small helper tools for labs that involve packet captures.

## `pcap_stats.py`

A *dependency-light* PCAP statistics script.

- Preferably uses **Scapy** or **dpkt** when installed.
- Falls back to a **pure-Python classic PCAP parser** (Ethernet and Linux SLL).
- Prints packet count, byte count, and a simple protocol breakdown (ICMP/TCP/UDP/other).

### Examples

```bash
python3 00_TOOLS/pcap/pcap_stats.py --pcap capture.pcap
python3 00_TOOLS/pcap/pcap_stats.py --pcap capture.pcap --json
python3 00_TOOLS/pcap/pcap_stats.py --pcap capture.pcap --backend pure
```

## `pcap_tshark_summary.py` (optional)

If `tshark` is installed, produce a quick textual summary (endpoints / conversations).

```bash
python3 00_TOOLS/pcap/pcap_tshark_summary.py --pcap capture.pcap
```

## `capture_demo.sh`

Generate a tiny demo capture using `tcpdump` (requires sudo) and local traffic.

```bash
bash 00_TOOLS/pcap/capture_demo.sh --mixed
```

Output is written under `00_TOOLS/pcap/artifacts/`.

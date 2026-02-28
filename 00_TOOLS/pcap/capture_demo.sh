#!/usr/bin/env bash
set -euo pipefail

# capture_demo.sh — generate a small demo PCAP using tcpdump
#
# This tool is optional and intended for teaching (quick PCAP generation).
#
# Usage:
#   bash capture_demo.sh --mixed
#   bash capture_demo.sh --tcp
#   bash capture_demo.sh --udp
#
# Output:
#   00_TOOLS/pcap/artifacts/example_<mode>.pcap

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${HERE}/artifacts"
mkdir -p "${OUT_DIR}"

MODE="${1:---mixed}"
OUT="${OUT_DIR}/example_${MODE#--}.pcap"

if ! command -v tcpdump >/dev/null 2>&1; then
  echo "[capture_demo] tcpdump not found" >&2
  exit 1
fi

# netcat is used to generate a small amount of TCP/UDP traffic.
if ! command -v nc >/dev/null 2>&1; then
  echo "[capture_demo] netcat (nc) not found; TCP/UDP probes will be skipped" >&2
fi

FILTER="icmp or tcp or udp"
case "${MODE}" in
  --tcp) FILTER="tcp" ;;
  --udp) FILTER="udp" ;;
  --mixed) FILTER="icmp or tcp or udp" ;;
  *) echo "[capture_demo] Unknown mode: ${MODE}" >&2; exit 2 ;;
esac

echo "[capture_demo] Writing: ${OUT}"
sudo tcpdump -i any -w "${OUT}" "${FILTER}" >/dev/null 2>&1 &
PID="$!"
sleep 1

# Generate local traffic (always available).
ping -c 1 127.0.0.1 >/dev/null 2>&1 || true

# TCP and UDP on discard port; may fail but still generates attempted traffic.
if command -v nc >/dev/null 2>&1; then
  (printf "hello\n" | nc 127.0.0.1 9 >/dev/null 2>&1 || true)
  (printf "hi\n" | nc -u 127.0.0.1 9 >/dev/null 2>&1 || true)
fi

sudo kill "${PID}" >/dev/null 2>&1 || true
sleep 1

echo "[capture_demo] Done"

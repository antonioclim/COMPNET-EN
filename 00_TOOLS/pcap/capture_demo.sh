#!/usr/bin/env bash
set -euo pipefail

# Generate a short local demonstration capture. No external host is contacted.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$HERE/artifacts"
MODE="${1:---mixed}"
case "$MODE" in
  --tcp) FILTER="tcp" ;;
  --udp) FILTER="udp" ;;
  --mixed) FILTER="icmp or tcp or udp" ;;
  *) echo "Usage: bash capture_demo.sh [--tcp|--udp|--mixed]" >&2; exit 2 ;;
esac
command -v tcpdump >/dev/null || { echo "tcpdump is required" >&2; exit 2; }
command -v timeout >/dev/null || { echo "timeout is required" >&2; exit 2; }
command -v nc >/dev/null || { echo "netcat (nc) is required" >&2; exit 2; }
SUDO=()
if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  command -v sudo >/dev/null || { echo "sudo is required for capture" >&2; exit 2; }
  sudo -v || { echo "Capture permission was not granted" >&2; exit 1; }
  SUDO=(sudo -n)
fi
mkdir -p "$OUT_DIR"
OUT="$OUT_DIR/example_${MODE#--}.pcap"
PID=""
CAPTURE_RC=0
stop_capture() {
  [[ -n "$PID" ]] || return 0
  "${SUDO[@]}" kill -INT "$PID" 2>/dev/null || true
  for _ in {1..30}; do
    kill -0 "$PID" 2>/dev/null || break
    sleep 0.1
  done
  "${SUDO[@]}" kill -TERM "$PID" 2>/dev/null || true
  for _ in {1..20}; do
    kill -0 "$PID" 2>/dev/null || break
    sleep 0.1
  done
  "${SUDO[@]}" kill -KILL "$PID" 2>/dev/null || true
  if wait "$PID"; then CAPTURE_RC=0; else CAPTURE_RC=$?; fi
  [[ $CAPTURE_RC -ne 130 ]] || CAPTURE_RC=0
  PID=""
  return 0
}
trap stop_capture EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
echo "[capture_demo] Writing: $OUT"
"${SUDO[@]}" tcpdump -U -i lo -w "$OUT" "$FILTER" &
PID=$!
sleep 1
if ! kill -0 "$PID" 2>/dev/null; then
  stop_capture
  echo "[capture_demo] Capture failed to start" >&2
  exit 1
fi
if [[ "$MODE" == --mixed ]]; then
  ping -c 1 -W 1 127.0.0.1 >/dev/null 2>&1 || true
fi
if [[ "$MODE" != --udp ]]; then
  printf 'hello\n' | timeout 3 nc -w 1 127.0.0.1 9 >/dev/null 2>&1 || true
fi
if [[ "$MODE" != --tcp ]]; then
  printf 'hi\n' | timeout 3 nc -u -w 1 127.0.0.1 9 >/dev/null 2>&1 || true
fi
sleep 1
stop_capture
if [[ $CAPTURE_RC -ne 0 || ! -s "$OUT" ]]; then
  echo "[capture_demo] Capture failed (status $CAPTURE_RC)" >&2
  exit 1
fi
if ! FIRST_PACKET=$("${SUDO[@]}" tcpdump -n -r "$OUT" -c 1 2>/dev/null) || [[ -z "$FIRST_PACKET" ]]; then
  echo "[capture_demo] The capture is unreadable or contains no packets" >&2
  exit 1
fi
echo "[capture_demo] Done: readable capture containing local traffic: $OUT"

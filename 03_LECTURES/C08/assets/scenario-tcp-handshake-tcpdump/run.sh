#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PORT=9090
PCAP="capture.pcap"
SERVER_PID=""
TCPDUMP_PID=""
cleanup() {
  if [[ -n "$TCPDUMP_PID" ]]; then sudo kill -INT "$TCPDUMP_PID" 2>/dev/null || true; wait "$TCPDUMP_PID" 2>/dev/null || true; fi
  if [[ -n "$SERVER_PID" ]]; then kill "$SERVER_PID" 2>/dev/null || true; wait "$SERVER_PID" 2>/dev/null || true; fi
  rm -f server.pid tcpdump.pid
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
sudo -v
rm -f "$PCAP"
python3 server.py > server.log 2>&1 &
SERVER_PID=$!
printf '%s\n' "$SERVER_PID" > server.pid
sleep 0.3
kill -0 "$SERVER_PID" 2>/dev/null || { cat server.log >&2; exit 1; }
sudo -n tcpdump -U -i lo -w "$PCAP" "tcp port $PORT" > tcpdump.log 2>&1 &
TCPDUMP_PID=$!
printf '%s\n' "$TCPDUMP_PID" > tcpdump.pid
ready=0
for _ in {1..30}; do
  if ! kill -0 "$TCPDUMP_PID" 2>/dev/null; then cat tcpdump.log >&2; exit 1; fi
  if grep -q 'listening on' tcpdump.log; then ready=1; break; fi
  sleep 0.1
done
[[ "$ready" == 1 ]] || { cat tcpdump.log >&2; exit 1; }
python3 client.py
sleep 0.5
sudo kill -INT "$TCPDUMP_PID"
wait "$TCPDUMP_PID"
TCPDUMP_PID=""
[[ -s "$PCAP" ]] && [[ $(wc -c < "$PCAP") -gt 24 ]] || { echo "No captured packets; inspect tcpdump.log" >&2; exit 1; }
echo "Capture completed: $PCAP; inspect server.log and tcpdump.log."

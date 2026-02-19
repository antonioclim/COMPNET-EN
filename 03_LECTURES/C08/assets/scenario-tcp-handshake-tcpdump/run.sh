#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

PORT=9090
PCAP="capture.pcap"

echo "[run] cleaning old capture"
rm -f "$PCAP" || true

echo "[run] starting server"
python3 server.py > server.log 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > server.pid

sleep 0.3

echo "[run] starting tcpdump (requires sudo)"
sudo tcpdump -i lo -w "$PCAP" "tcp port $PORT" > tcpdump.log 2>&1 &
TCPDUMP_PID=$!
echo "$TCPDUMP_PID" > tcpdump.pid

sleep 0.3

echo "[run] running client"
python3 client.py

sleep 0.5

echo "[run] stopping tcpdump and server"
sudo kill "$TCPDUMP_PID" 2>/dev/null || true
kill "$SERVER_PID" 2>/dev/null || true

echo "[run] done. output:"
echo "  - $PCAP"
echo "  - server.log"
echo "  - tcpdump.log"

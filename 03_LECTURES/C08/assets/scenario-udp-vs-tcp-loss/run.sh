#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

LOSS="${1:-20}"

echo "[run] starting mininet scenario with loss=${LOSS}% (requires sudo)"

sudo /usr/bin/python3 - "$LOSS" <<'PY'
import time
import sys
from topo import build
from mininet.log import setLogLevel

setLogLevel("warning")
loss = float(sys.argv[1])
if not 0 <= loss <= 100:
    raise SystemExit("Loss must be between 0 and 100")
net = build(loss=loss)
h1, h2 = net.get("h1", "h2")
try:
    print("[run] UDP test")
    h2.cmd("python3 udp_receiver.py > udp_receiver.out 2>&1 &")
    time.sleep(0.2)
    h1.cmd("python3 udp_sender.py > udp_sender.out 2>&1")
    time.sleep(6.0)
    print(h2.cmd("cat udp_receiver.out").strip())

    print("\\n[run] TCP test")
    h2.cmd("python3 tcp_receiver.py > tcp_receiver.out 2>&1 &")
    time.sleep(0.2)
    h1.cmd("python3 tcp_sender.py > tcp_sender.out 2>&1")
    time.sleep(0.5)
    print(h2.cmd("cat tcp_receiver.out").strip())

finally:
    net.stop()
PY

echo "[run] done"

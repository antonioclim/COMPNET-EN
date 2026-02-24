#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

LOSS="${1:-20}"

echo "[run] starting mininet scenario with loss=${LOSS}% (requires sudo)"

sudo python3 - <<PY
import time
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.log import setLogLevel

setLogLevel("warning")

loss = float("${LOSS}")

net = Mininet(controller=OVSController, link=TCLink, autoSetMacs=True)
net.addController("c0")
h1 = net.addHost("h1", ip="10.0.0.1/24")
h2 = net.addHost("h2", ip="10.0.0.2/24")
s1 = net.addSwitch("s1")

net.addLink(h1, s1, loss=loss)
net.addLink(s1, h2, loss=loss)

net.start()

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

net.stop()
PY

echo "[run] done"

#!/usr/bin/env bash
set -e

apt-get update
apt-get install -y iptables iproute2 tcpdump

# enable forwarding
sysctl -w net.ipv4.ip_forward=1

# NAT from net_client -> net_server
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Optional: simulate "no inbound to client" (already typical)
# (client doesn't accept inbound anyway)

echo "NAT/FW ready. Keeping container alive."
tail -f /dev/null

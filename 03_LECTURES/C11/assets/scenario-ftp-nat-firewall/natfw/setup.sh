#!/usr/bin/env bash
set -euo pipefail
# Address-based matching is independent of Docker's eth0/eth1 ordering.
iptables -P FORWARD DROP
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -s 172.29.112.0/24 -d 172.29.113.10 -p tcp --dport 2121 -j ACCEPT
iptables -A FORWARD -s 172.29.112.0/24 -d 172.29.113.10 -p tcp --dport 30000:30009 -j ACCEPT
iptables -t nat -A PREROUTING -d 172.29.112.2 -p tcp --dport 2121 -j DNAT --to-destination 172.29.113.10
iptables -t nat -A PREROUTING -d 172.29.112.2 -p tcp --dport 30000:30009 -j DNAT --to-destination 172.29.113.10
iptables -t nat -A POSTROUTING -s 172.29.112.0/24 -d 172.29.113.10 -j MASQUERADE
echo "NAT/FW ready: client -> natfw -> FTP; passive range 30000-30009."
exec tail -f /dev/null

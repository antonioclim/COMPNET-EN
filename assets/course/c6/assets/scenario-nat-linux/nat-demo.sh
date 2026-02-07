#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  ip netns del ns_lan 2>/dev/null || true
  ip netns del ns_rtr 2>/dev/null || true
  ip netns del ns_wan 2>/dev/null || true
}
cleanup

ip netns add ns_lan
ip netns add ns_rtr
ip netns add ns_wan

ip link add v_lan type veth peer name v_rtr_lan
ip link add v_wan type veth peer name v_rtr_wan

ip link set v_lan netns ns_lan
ip link set v_rtr_lan netns ns_rtr
ip link set v_wan netns ns_wan
ip link set v_rtr_wan netns ns_rtr

ip -n ns_lan addr add 192.168.10.2/24 dev v_lan
ip -n ns_rtr addr add 192.168.10.1/24 dev v_rtr_lan

ip -n ns_wan addr add 203.0.113.2/24 dev v_wan
ip -n ns_rtr addr add 203.0.113.1/24 dev v_rtr_wan

ip -n ns_lan link set v_lan up
ip -n ns_rtr link set v_rtr_lan up
ip -n ns_wan link set v_wan up
ip -n ns_rtr link set v_rtr_wan up

ip -n ns_lan route add default via 192.168.10.1
ip -n ns_wan route add default via 203.0.113.1

# enable forwarding
ip netns exec ns_rtr sysctl -w net.ipv4.ip_forward=1 >/dev/null

# NAT (masquerade) on router
ip netns exec ns_rtr iptables -t nat -A POSTROUTING -o v_rtr_wan -j MASQUERADE

echo "Starting tcpdump in ns_wan for ICMP..."
ip netns exec ns_wan timeout 4 tcpdump -n -i v_wan icmp &
sleep 1

echo "Pinging from LAN host (192.168.10.2) to WAN host (203.0.113.2)..."
ip netns exec ns_lan ping -c 2 203.0.113.2 || true

echo
echo "You should see packets arrive in ns_wan with source rewritten to 203.0.113.1"
echo "Cleaning up..."
cleanup

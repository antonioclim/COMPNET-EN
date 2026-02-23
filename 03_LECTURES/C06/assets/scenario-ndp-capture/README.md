### Scenario: NDP Capture (IPv6)

Wireshark filters:
- icmpv6
- ndp

tcpdump:
- sudo tcpdump -i any -n 'icmp6'

Generate traffic:
- ping an IPv6 neighbour on the LAN or the gateway (if one exists)
- bring the interface up/down to observe RS/RA

Observe:
- Neighbor Solicitation: multicast
- Neighbor Advertisement: reply
- Router Advertisement: announces prefix and gateway

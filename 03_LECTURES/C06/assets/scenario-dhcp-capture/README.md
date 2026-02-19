### Scenario: DHCP capture (DORA)

Wireshark filters:
- bootp
- dhcp

tcpdump:
- sudo tcpdump -i any -n 'udp port 67 or udp port 68'

Generate traffic:
- reconnect an interface (disable/enable) or connect a new device
- alternatively, use a VM in NAT/bridged mode and renew the lease

Observe:
- Discover: broadcast
- Offer: usually unicast (depends on implementation)
- Request: broadcast
- Ack: unicast

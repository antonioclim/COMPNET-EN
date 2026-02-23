### Scenario: ICMP ping + traceroute

IPv4:
- ping -c 4 1.1.1.1
- traceroute 1.1.1.1  (or tracert on Windows)

Capture:
- sudo tcpdump -i any -n icmp

Observe:
- TTL decreases along the path
- traceroute uses ICMP Time Exceeded replies for each hop

### Scenariu: ICMP ping + traceroute

IPv4:
- ping -c 4 1.1.1.1
- traceroute 1.1.1.1  (sau tracert pe Windows)

Captura:
- sudo tcpdump -i any -n icmp

Observa:
- TTL scade pe traseu
- traceroute foloseste raspunsuri ICMP (Time Exceeded) pentru hop-uri

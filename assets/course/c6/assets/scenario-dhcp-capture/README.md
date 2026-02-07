### Scenariu: DHCP capture (DORA)

Wireshark filters:
- bootp
- dhcp

tcpdump:
- sudo tcpdump -i any -n 'udp port 67 or udp port 68'

Genereaza trafic:
- reconecteaza o interfata (disable/enable) sau conecteaza un device nou
- sau foloseste un VM in NAT/bridged si reinnoieste lease-ul

Observa:
- Discover: broadcast
- Offer: de obicei unicast (depinde de implementare)
- Request: broadcast
- Ack: unicast

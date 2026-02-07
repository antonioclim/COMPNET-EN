### Scenariu: ARP capture

Wireshark filter:
- arp

tcpdump:
- sudo tcpdump -i any -n arp

Genereaza ARP:
- ping gateway-ul local (ex: 192.168.1.1)

Observa:
- request broadcast
- reply unicast

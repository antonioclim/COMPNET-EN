### Scenariu: NDP capture (IPv6)

Wireshark filters:
- icmpv6
- ndp

tcpdump:
- sudo tcpdump -i any -n 'icmp6'

Genereaza trafic:
- ping catre un vecin IPv6 din LAN sau catre gateway (dacă există)
- conecteaza/deconecteaza interfata pentru a vedea RS/RA

Observa:
- Neighbor Solicitation: multicast
- Neighbor Advertisement: raspuns
- Router Advertisement: anunta prefix si gateway

### Scenariu: observare IPv4 vs IPv6 (TTL vs Hop Limit)

#### Obiectiv
- vezi diferența în captură între IPv4 și IPv6
- identifici câmpul TTL (IPv4) și Hop Limit (IPv6)

#### Cerințe
- Wireshark sau tcpdump
- un host care răspunde pe IPv6 (dacă ai conectivitate)

#### Captură (tcpdump, Linux/macOS)
IPv4:
- sudo tcpdump -i any -n 'icmp'

IPv6:
- sudo tcpdump -i any -n 'icmp6'

#### Generare trafic
IPv4:
- ping -c 4 1.1.1.1

IPv6 (dacă merge în rețeaua ta):
- ping -c 4 2606:4700:4700::1111

#### În Wireshark
Filtre:
- icmp
- icmpv6

#### Ce cauți
- IPv4 header: TTL
- IPv6 header: Hop Limit
- la IPv6: Next Header în loc de “Protocol”

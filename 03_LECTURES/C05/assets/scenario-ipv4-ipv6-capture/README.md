### Scenario: observing IPv4 vs IPv6 (TTL vs Hop Limit)

#### Objective
- observe the difference in a capture between IPv4 and IPv6
- identify the TTL field (IPv4) and the Hop Limit field (IPv6)

#### Requirements
- Wireshark or tcpdump
- a host that responds on IPv6 (if you have connectivity)

#### Capture (tcpdump, Linux/macOS)
IPv4:
- sudo tcpdump -i any -n 'icmp'

IPv6:
- sudo tcpdump -i any -n 'icmp6'

#### Generating traffic
IPv4:
- ping -c 4 1.1.1.1

IPv6 (if supported on your network):
- ping -c 4 2606:4700:4700::1111

#### In Wireshark
Filters:
- icmp
- icmpv6

#### What to look for
- IPv4 header: TTL
- IPv6 header: Hop Limit
- in IPv6: Next Header instead of "Protocol"

## Cross-References

Parent lecture: [`C05/ — Network Layer Addressing`](../../)
  
Lecture slides: [`c5-network-layer-addressing.md`](../../c5-network-layer-addressing.md)
  
Quiz: [`W05`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C05/assets/scenario-ipv4-ipv6-capture
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C05/assets/scenario-ipv4-ipv6-capture`

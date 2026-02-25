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

## Cross-References

Parent lecture: [`C06/ — NAT, ARP, DHCP, NDP and ICMP`](../../)
  
Lecture slides: [`c6-nat-arp-dhcp-ndp-icmp.md`](../../c6-nat-arp-dhcp-ndp-icmp.md)
  
Quiz: [`W06`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C06/assets/scenario-ndp-capture
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C06/assets/scenario-ndp-capture`

### Scenario: ICMP ping + traceroute

IPv4:
- ping -c 4 1.1.1.1
- traceroute 1.1.1.1  (or tracert on Windows)

Capture:
- sudo tcpdump -i any -n icmp

Observe:
- TTL decreases along the path
- traceroute uses ICMP Time Exceeded replies for each hop

## Cross-References

Parent lecture: [`C06/ — NAT, ARP, DHCP, NDP and ICMP`](../../)
  
Lecture slides: [`c6-nat-arp-dhcp-ndp-icmp.md`](../../c6-nat-arp-dhcp-ndp-icmp.md)
  
Quiz: [`W06`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C06/assets/scenario-icmp-traceroute
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C06/assets/scenario-icmp-traceroute`

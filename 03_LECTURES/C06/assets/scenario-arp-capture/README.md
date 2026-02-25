### Scenario: ARP capture

Wireshark filter:
- arp

tcpdump:
- sudo tcpdump -i any -n arp

Generate ARP:
- ping the local gateway (e.g. 192.168.1.1)

Observe:
- request broadcast
- reply unicast

## Cross-References

Parent lecture: [`C06/ — NAT, ARP, DHCP, NDP and ICMP`](../../)
  
Lecture slides: [`c6-nat-arp-dhcp-ndp-icmp.md`](../../c6-nat-arp-dhcp-ndp-icmp.md)
  
Quiz: [`W06`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C06/assets/scenario-arp-capture
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C06/assets/scenario-arp-capture`

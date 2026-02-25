### Scenario: DHCP capture (DORA)

Wireshark filters:
- bootp
- dhcp

tcpdump:
- sudo tcpdump -i any -n 'udp port 67 or udp port 68'

Generate traffic:
- reconnect an interface (disable/enable) or connect a new device
- alternatively, use a VM in NAT/bridged mode and renew the lease

Observe:
- Discover: broadcast
- Offer: usually unicast (depends on implementation)
- Request: broadcast
- Ack: unicast

## Cross-References

Parent lecture: [`C06/ — NAT, ARP, DHCP, NDP and ICMP`](../../)
  
Lecture slides: [`c6-nat-arp-dhcp-ndp-icmp.md`](../../c6-nat-arp-dhcp-ndp-icmp.md)
  
Quiz: [`W06`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C06/assets/scenario-dhcp-capture
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C06/assets/scenario-dhcp-capture`

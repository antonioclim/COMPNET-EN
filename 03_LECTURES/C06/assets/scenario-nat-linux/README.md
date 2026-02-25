### Scenario: NAT (masquerade) on Linux with namespaces

#### Requirements
- Linux
- root privileges (sudo)
- iproute2 (ip), iptables or nftables
- external internet access is not required: the script demonstrates SNAT towards an isolated uplink namespace

#### Demonstrates
- private host -> router -> uplink
- SNAT (masquerade) on the router
- source address rewriting observed with tcpdump

#### Running
- sudo bash nat-demo.sh

#### Cleanup
The script removes namespaces and links on exit.

## Files

| Name | Lines |
|------|-------|
| `nat-demo.sh` | 53 |

## Cross-References

Parent lecture: [`C06/ — NAT, ARP, DHCP, NDP and ICMP`](../../)
  
Lecture slides: [`c6-nat-arp-dhcp-ndp-icmp.md`](../../c6-nat-arp-dhcp-ndp-icmp.md)
  
Quiz: [`W06`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C06/assets/scenario-nat-linux
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C06/assets/scenario-nat-linux`

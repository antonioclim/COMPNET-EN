### Scenario: Scapy – ICMP echo (requires root/admin)

#### Requirements
- Linux (recommended)
- Scapy installed: `pip install scapy`
- Run with elevated privileges (root/admin): `sudo`

#### Running
- sudo python3 icmp-ping.py 1.1.1.1

#### Observations
- You construct an IP/ICMP packet at the application layer
- You receive a reply (or a timeout)

## Files

| Name | Lines |
|------|-------|
| `icmp-ping.py` | 14 |

## Cross-References

Parent lecture: [`C03/ — Network Programming (Sockets)`](../../)
  
Lecture slides: [`c3-intro-network-programming.md`](../../c3-intro-network-programming.md)
  
Quiz: [`W03`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W03_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C03/assets/scenario-scapy-icmp
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C03/assets/scenario-scapy-icmp`

### Scenario: CIDR basics (IPv4 calculator)

#### Objective
Given an IPv4 address/prefix, compute:
- the network address
- the broadcast address
- the first and last usable host
- the number of usable hosts

#### Running
- python3 cidr-calc.py 192.168.23.233/24
- python3 cidr-calc.py 10.2.10.233/8

## Files

| Name | Lines |
|------|-------|
| `cidr-calc.py` | 24 |

## Cross-References

Parent lecture: [`C05/ — Network Layer Addressing`](../../)
  
Lecture slides: [`c5-network-layer-addressing.md`](../../c5-network-layer-addressing.md)
  
Quiz: [`W05`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C05/assets/scenario-cidr-basic
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C05/assets/scenario-cidr-basic`

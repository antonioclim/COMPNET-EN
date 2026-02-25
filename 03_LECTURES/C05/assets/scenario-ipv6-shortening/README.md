### Scenario: IPv6 shortening and normalisation

#### Objective
Convert an IPv6 address to its canonical form and apply the standard shortening rules.

#### Running
- python3 ipv6-norm.py 2001:0000:0ef2:0000:0000:0ad8:7232:0ab8
- python3 ipv6-norm.py 2001:0:ef2::ad8:7232:ab8

## Files

| Name | Lines |
|------|-------|
| `ipv6-norm.py` | 14 |

## Cross-References

Parent lecture: [`C05/ — Network Layer Addressing`](../../)
  
Lecture slides: [`c5-network-layer-addressing.md`](../../c5-network-layer-addressing.md)
  
Quiz: [`W05`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C05/assets/scenario-ipv6-shortening
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C05/assets/scenario-ipv6-shortening`

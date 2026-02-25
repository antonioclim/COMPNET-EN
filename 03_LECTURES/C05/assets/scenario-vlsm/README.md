### Scenario: VLSM (IPv4)

#### Objective
Allocate subnets of different sizes within a given IPv4 address block.

#### Running (classic example)
- python3 vlsm-alloc.py 193.226.3.0/24 50 24 8 2 2 2

#### Output
- list the allocated subnets in allocation order

## Files

| Name | Lines |
|------|-------|
| `vlsm-alloc.py` | 51 |

## Cross-References

Parent lecture: [`C05/ — Network Layer Addressing`](../../)
  
Lecture slides: [`c5-network-layer-addressing.md`](../../c5-network-layer-addressing.md)
  
Quiz: [`W05`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C05/assets/scenario-vlsm
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C05/assets/scenario-vlsm`

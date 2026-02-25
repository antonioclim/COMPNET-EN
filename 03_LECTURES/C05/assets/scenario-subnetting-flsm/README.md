### Scenario: subnetting with a fixed-length mask (FLSM)

#### Objective
Split a /p network into N equal-sized subnets and list:
- network address, broadcast address and host range for each subnet

#### Running
- python3 flsm-split.py 192.168.23.0/24 4

## Files

| Name | Lines |
|------|-------|
| `flsm-split.py` | 36 |

## Cross-References

Parent lecture: [`C05/ — Network Layer Addressing`](../../)
  
Lecture slides: [`c5-network-layer-addressing.md`](../../c5-network-layer-addressing.md)
  
Quiz: [`W05`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C05/assets/scenario-subnetting-flsm
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C05/assets/scenario-subnetting-flsm`

# Week 05 — Network Layer (IPv4, IPv6)

10 PlantUML diagram sources for the network layer — IPv4, IPv6, subnetting and CIDR. Each file mirrors its counterpart in [`03_LECTURES/C05/assets/puml/`](../../../03_LECTURES/C05/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-cidr-subnetting.puml` | Cidr Subnetting | 34 |
| `fig-ipv4-comm-types.puml` | Ipv4 Comm Types | 39 |
| `fig-ipv4-header.puml` | Ipv4 Header | 46 |
| `fig-ipv4-vs-ipv6.puml` | Ipv4 Vs Ipv6 | 39 |
| `fig-ipv6-address-structure.puml` | Ipv6 Address Structure | 34 |
| `fig-ipv6-header.puml` | Ipv6 Header | 43 |
| `fig-l3-role.puml` | L3 Role | 26 |
| `fig-mac-vs-ip.puml` | Mac Vs Ip | 33 |
| `fig-prefix-mask.puml` | Prefix Mask | 33 |
| `fig-vlsm-allocation.puml` | Vlsm Allocation | 43 |

## Usage

Render all diagrams in this directory with the local JAR:

```bash
java -jar ../../../00_TOOLS/plantuml.jar -tpng *.puml
```

Or via the HTTP server:

```bash
cd .. && python3 generate_png_simple.py
```

## Cross-References

| Aspect | Link |
|---|---|
| Lecture | [`03_LECTURES/C05/`](../../../03_LECTURES/C05/) |
| Seminar | [`04_SEMINARS/S05/`](../../../04_SEMINARS/S05/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W05_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week05"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week05
```

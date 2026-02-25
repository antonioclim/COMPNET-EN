# Week 06 — Network Support Protocols

11 PlantUML diagram sources for network-layer support mechanisms — ARP, DHCP, NAT, ICMP and NDP. Each file mirrors its counterpart in [`03_LECTURES/C06/assets/puml/`](../../../03_LECTURES/C06/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-arp.puml` | Arp | 32 |
| `fig-dhcp-dora.puml` | Dhcp Dora | 35 |
| `fig-dhcp-relay.puml` | Dhcp Relay | 34 |
| `fig-icmp-role.puml` | Icmp Role | 42 |
| `fig-l3-support-map.puml` | L3 Support Map | 45 |
| `fig-nat-basic.puml` | Nat Basic | 31 |
| `fig-nat-dynamic.puml` | Nat Dynamic | 39 |
| `fig-nat-static.puml` | Nat Static | 31 |
| `fig-ndp.puml` | Ndp | 39 |
| `fig-pat.puml` | Pat | 37 |
| `fig-proxy-arp.puml` | Proxy Arp | 30 |

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
| Lecture | [`03_LECTURES/C06/`](../../../03_LECTURES/C06/) |
| Seminar | [`04_SEMINARS/S06/`](../../../04_SEMINARS/S06/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W06_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week06"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week06
```

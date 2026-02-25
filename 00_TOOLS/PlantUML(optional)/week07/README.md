# Week 07 — Routing Protocols

9 PlantUML diagram sources for routing protocols — RIP, OSPF, BGP and the routing table. Each file mirrors its counterpart in [`03_LECTURES/C07/assets/puml/`](../../../03_LECTURES/C07/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-distance-vector.puml` | Distance Vector | 42 |
| `fig-igp-vs-egp.puml` | Igp Vs Egp | 43 |
| `fig-l2-l3-changes.puml` | L2 L3 Changes | 26 |
| `fig-link-state.puml` | Link State | 45 |
| `fig-mininet-triangle.puml` | Mininet Triangle | 42 |
| `fig-ospf-areas.puml` | Ospf Areas | 48 |
| `fig-rip-loop.puml` | Rip Loop | 40 |
| `fig-router-role.puml` | Router Role | 35 |
| `fig-routing-table.puml` | Routing Table | 44 |

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
| Lecture | [`03_LECTURES/C07/`](../../../03_LECTURES/C07/) |
| Seminar | [`04_SEMINARS/S07/`](../../../04_SEMINARS/S07/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W07_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W07_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week07"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week07
```

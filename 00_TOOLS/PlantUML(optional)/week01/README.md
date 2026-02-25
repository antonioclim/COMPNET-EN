# Week 01 — Network Fundamentals

9 PlantUML diagram sources for network fundamentals — topologies, devices and reference models. Each file mirrors its counterpart in [`03_LECTURES/C01/assets/puml/`](../../../03_LECTURES/C01/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-circuit-vs-packet.puml` | Circuit Vs Packet | 43 |
| `fig-client-server-p2p.puml` | Client Server P2P | 37 |
| `fig-devices.puml` | Devices | 35 |
| `fig-encapsulation.puml` | Encapsulation | 29 |
| `fig-hub-switch-router.puml` | Hub Switch Router | 45 |
| `fig-lan-wan-internet.puml` | Lan Wan Internet | 35 |
| `fig-media.puml` | Media | 41 |
| `fig-network-vs-system.puml` | Network Vs System | 39 |
| `fig-topologies.puml` | Topologies | 60 |

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
| Lecture | [`03_LECTURES/C01/`](../../../03_LECTURES/C01/) |
| Seminar | [`04_SEMINARS/S01/`](../../../04_SEMINARS/S01/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W01_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W01_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week01"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week01
```

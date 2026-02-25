# Week 02 — OSI and TCP/IP Reference Models

8 PlantUML diagram sources for the OSI and TCP/IP reference models. Each file mirrors its counterpart in [`03_LECTURES/C02/assets/puml/`](../../../03_LECTURES/C02/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-osi-communication.puml` | Osi Communication | 56 |
| `fig-osi-encapsulation.puml` | Osi Encapsulation | 45 |
| `fig-osi-implementation.puml` | Osi Implementation | 40 |
| `fig-osi-layers.puml` | Osi Layers | 32 |
| `fig-osi-protocol-mapping.puml` | Osi Protocol Mapping | 60 |
| `fig-osi-vs-tcpip.puml` | Osi Vs Tcpip | 53 |
| `fig-tcp-vs-udp-layers.puml` | Tcp Vs Udp Layers | 40 |
| `fig-tcpip-layers.puml` | Tcpip Layers | 29 |

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
| Lecture | [`03_LECTURES/C02/`](../../../03_LECTURES/C02/) |
| Seminar | [`04_SEMINARS/S02/`](../../../04_SEMINARS/S02/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W02_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W02_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week02"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week02
```

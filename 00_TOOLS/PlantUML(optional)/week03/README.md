# Week 03 — Socket Programming

7 PlantUML diagram sources for network application programming (TCP and UDP client-server). Each file mirrors its counterpart in [`03_LECTURES/C03/assets/puml/`](../../../03_LECTURES/C03/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-app-over-http.puml` | App Over Http | 38 |
| `fig-raw-layering.puml` | Raw Layering | 45 |
| `fig-tcp-concurrency.puml` | Tcp Concurrency | 55 |
| `fig-tcp-framing-strategies.puml` | Tcp Framing Strategies | 48 |
| `fig-tcp-server-flow.puml` | Tcp Server Flow | 45 |
| `fig-udp-server-flow.puml` | Udp Server Flow | 40 |
| `fig-udp-session-ack-flow.puml` | Udp Session Ack Flow | 50 |

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
| Lecture | [`03_LECTURES/C03/`](../../../03_LECTURES/C03/) |
| Seminar | [`04_SEMINARS/S03/`](../../../04_SEMINARS/S03/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W03_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W03_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week03"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week03
```

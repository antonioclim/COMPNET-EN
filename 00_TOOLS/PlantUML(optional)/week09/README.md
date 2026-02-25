# Week 09 — Session and Presentation Layers

6 PlantUML diagram sources for the session layer and the presentation layer — MIME, encoding and compression. Each file mirrors its counterpart in [`03_LECTURES/C09/assets/puml/`](../../../03_LECTURES/C09/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-connection-vs-session.puml` | Connection Vs Session | 40 |
| `fig-content-type-vs-encoding.puml` | Content Type Vs Encoding | 38 |
| `fig-mime-examples.puml` | Mime Examples | 41 |
| `fig-osi-l5-l6.puml` | Osi L5 L6 | 44 |
| `fig-presentation-pipeline.puml` | Presentation Pipeline | 41 |
| `fig-session-mechanisms-modern.puml` | Session Mechanisms Modern | 35 |

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
| Lecture | [`03_LECTURES/C09/`](../../../03_LECTURES/C09/) |
| Seminar | [`04_SEMINARS/S09/`](../../../04_SEMINARS/S09/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W09_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W09_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week09"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week09
```

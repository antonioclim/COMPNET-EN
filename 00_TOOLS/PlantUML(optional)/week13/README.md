# Week 13 — IoT and Network Security

6 PlantUML diagram sources for IoT and security in computer networks. Each file mirrors its counterpart in [`03_LECTURES/C13/assets/puml/`](../../../03_LECTURES/C13/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-hardening-before-after.puml` | Hardening Before After | 34 |
| `fig-iot-architecture.puml` | Iot Architecture | 33 |
| `fig-iot-scenario-runtime.puml` | Iot Scenario Runtime | 36 |
| `fig-mqtt-pub-sub.puml` | Mqtt Pub Sub | 44 |
| `fig-vuln-lab-architecture.puml` | Vuln Lab Architecture | 33 |
| `fig-vulnerability-lifecycle.puml` | Vulnerability Lifecycle | 29 |

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
| Lecture | [`03_LECTURES/C13/`](../../../03_LECTURES/C13/) |
| Seminar | [`04_SEMINARS/S13/`](../../../04_SEMINARS/S13/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W13_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W13_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week13"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week13
```

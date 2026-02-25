# Week 04 — Physical and Data Link Layers

13 PlantUML diagram sources for the physical layer and the data link layer (Ethernet, Wi-Fi, VLANs). Each file mirrors its counterpart in [`03_LECTURES/C04/assets/puml/`](../../../03_LECTURES/C04/assets/puml/).

## Diagram Index

| File | Subject | Lines |
|---|---|---|
| `fig-csma-ca.puml` | Csma Ca | 48 |
| `fig-csma-cd.puml` | Csma Cd | 46 |
| `fig-ethernet-frame.puml` | Ethernet Frame | 33 |
| `fig-l1-l2-context.puml` | L1 L2 Context | 29 |
| `fig-l2-encapsulation.puml` | L2 Encapsulation | 29 |
| `fig-line-coding-overview.puml` | Line Coding Overview | 28 |
| `fig-llc-mac.puml` | Llc Mac | 30 |
| `fig-modulation.puml` | Modulation | 34 |
| `fig-switch-cam-learning.puml` | Switch Cam Learning | 53 |
| `fig-transfer-media.puml` | Transfer Media | 34 |
| `fig-vlan.puml` | Vlan | 36 |
| `fig-wifi-channels-24ghz.puml` | Wifi Channels 24Ghz | 42 |
| `fig-wifi-frame-concept.puml` | Wifi Frame Concept | 37 |

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
| Lecture | [`03_LECTURES/C04/`](../../../03_LECTURES/C04/) |
| Seminar | [`04_SEMINARS/S04/`](../../../04_SEMINARS/S04/) |
| Quiz | [`00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W04_Questions.md`](../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W04_Questions.md) |
| Rendering helper | [`../../plantuml/render_puml.sh`](../../plantuml/render_puml.sh) |

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)/week04"
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)/week04
```

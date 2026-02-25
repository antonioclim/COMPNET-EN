# PlantUML Diagrams — Weeks 1–13

118 PlantUML diagram sources distributed across 13 weekly directories, covering every lecture from network fundamentals (week 1) through IoT and security (week 13). Each `.puml` file is identical to its counterpart in `03_LECTURES/C{NN}/assets/puml/` — this directory exists as a flat, week-indexed collection for batch generation and printing.

## Diagram Count per Week

| Week | Topic | Diagrams | Week | Topic | Diagrams |
|------|-------|----------|------|-------|----------|
| 01 | Network fundamentals | 9 | 08 | Transport layer (TCP, UDP, TLS) | 12 |
| 02 | OSI vs TCP/IP models | 8 | 09 | Session and presentation layers | 6 |
| 03 | Socket programming | 7 | 10 | HTTP(S), REST, WebSockets | 10 |
| 04 | Physical and data link layers | 13 | 11 | FTP, DNS and SSH | 7 |
| 05 | Network layer (IPv4, IPv6) | 10 | 12 | E-mail (SMTP, POP3, IMAP) | 10 |
| 06 | ARP, DHCP, NAT, ICMP | 11 | 13 | IoT and security | 6 |
| 07 | Routing protocols | 9 | | | |

Range: 6–13 diagrams per week. Week 14 is a revision session with no dedicated diagrams.

## File / Folder Index

| Name | Description | Metric |
|---|---|---|
| [`week01/`](week01/README.md)–[`week13/`](week13/README.md) | Per-week diagram directories | 6–13 `.puml` files each |
| `generate_png_simple.py` | Renders diagrams via the PlantUML HTTP server | 147 lines |
| `generate_diagrams.py` | Full-featured renderer with error handling and parallelism | 471 lines |
| `generate_a4.py` | Produces A4-sized PNGs for printing (requires Pillow) | 241 lines |
| `generate_all.sh` | Shell wrapper that calls the Python generators | 234 lines |

## Usage

### PlantUML HTTP server (online, no local JAR)

```bash
python3 generate_png_simple.py
```

### Local JAR (recommended for offline or bulk rendering)

```bash
# Download the JAR once
bash ../plantuml/get_plantuml_jar.sh

# Render all diagrams
java -jar ../plantuml.jar -tpng week*/*.puml
```

### A4 format for printing

```bash
pip install Pillow
python3 generate_a4.py --dpi 150 --output-dir ./png_a4
```

## Design Rationale

The flat week-indexed layout allows batch operations (rendering, linting, counting) without navigating the lecture hierarchy. All diagrams use validated PlantUML syntax, a Material Design colour palette, Arial font and include `title` and `legend` blocks for consistency.

## Resolved Issues

Previous revisions removed `note as` syntax (which can produce empty renders on certain servers), eliminated complex multi-line notes and switched to `legend` blocks for explanatory text.

## Cross-References and Contextual Connections

### Lecture Mirror Mapping

Every `.puml` file here has an identical counterpart inside its corresponding lecture folder:

| This folder | Lecture folder |
|---|---|
| `week01/*.puml` | [`03_LECTURES/C01/assets/puml/`](../../03_LECTURES/C01/assets/puml/) |
| `week02/*.puml` | [`03_LECTURES/C02/assets/puml/`](../../03_LECTURES/C02/assets/puml/) |
| `week03/*.puml` | [`03_LECTURES/C03/assets/puml/`](../../03_LECTURES/C03/assets/puml/) |
| `week04/*.puml` | [`03_LECTURES/C04/assets/puml/`](../../03_LECTURES/C04/assets/puml/) |
| `week05/*.puml` | [`03_LECTURES/C05/assets/puml/`](../../03_LECTURES/C05/assets/puml/) |
| `week06/*.puml` | [`03_LECTURES/C06/assets/puml/`](../../03_LECTURES/C06/assets/puml/) |
| `week07/*.puml` | [`03_LECTURES/C07/assets/puml/`](../../03_LECTURES/C07/assets/puml/) |
| `week08/*.puml` | [`03_LECTURES/C08/assets/puml/`](../../03_LECTURES/C08/assets/puml/) |
| `week09/*.puml` | [`03_LECTURES/C09/assets/puml/`](../../03_LECTURES/C09/assets/puml/) |
| `week10/*.puml` | [`03_LECTURES/C10/assets/puml/`](../../03_LECTURES/C10/assets/puml/) |
| `week11/*.puml` | [`03_LECTURES/C11/assets/puml/`](../../03_LECTURES/C11/assets/puml/) |
| `week12/*.puml` | [`03_LECTURES/C12/assets/puml/`](../../03_LECTURES/C12/assets/puml/) |
| `week13/*.puml` | [`03_LECTURES/C13/assets/puml/`](../../03_LECTURES/C13/assets/puml/) |

### Downstream Dependencies

The QA script `check_fig_targets.py` validates that every `[FIG]` marker in lecture Markdown points to an existing `.puml` source — those sources live in the lecture copies, not here. This directory is not referenced by CI directly but serves as the canonical batch-generation source.

### Prerequisite

| Prerequisite | Path | Why |
|---|---|---|
| PlantUML JAR | [`../plantuml/get_plantuml_jar.sh`](../plantuml/get_plantuml_jar.sh) | Local rendering requires the JAR; run once after cloning |

### Suggested Learning Sequence

**Suggested sequence:** `../plantuml/get_plantuml_jar.sh` (download JAR) → this folder (batch render) → `03_LECTURES/CNN/assets/` (per-lecture rendering)

## Troubleshooting

**The JAR does not download:**

```bash
curl -L -o plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar
```

**Java is missing:**

```bash
sudo apt install default-jre
```

**A diagram does not render:** check the syntax in the online editor at `https://www.plantuml.com/plantuml/uml/` and confirm the file begins with `@startuml` and ends with `@enduml`.

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)"
```

To also fetch the rendering helpers:

```bash
git sparse-checkout add 00_TOOLS/plantuml
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)
```

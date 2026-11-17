# PlantUML(optional) — Week Mirrors of Lecture Diagrams (Batch Export)

Optional diagram collection used when instructors or students want batch export of PlantUML figures without traversing each lecture’s `assets/puml/` directory. Each `weekNN/` folder mirrors the PlantUML sources used in `03_LECTURES/CNN/assets/puml/` (Weeks 01–13) and can be rendered into PNG (and optionally PDF/SVG) using the scripts in this directory.

## File and Folder Index

| Name | Type | Description |
|---|---|---|
| [`README.md`](README.md) | Markdown | Orientation for the week-mirror diagram bundle (this file) |
| [`generate_all.sh`](generate_all.sh) | Bash | Offline renderer that downloads `plantuml.jar` into this directory and generates PNG next to each `.puml` |
| [`generate_diagrams.py`](generate_diagrams.py) | Python | Offline batch renderer supporting PNG/SVG/EPS/PDF/TXT with an explicit output directory |
| [`generate_a4.py`](generate_a4.py) | Python | Post-processes rendered PNG into page-friendly images for handouts |
| [`generate_png_simple.py`](generate_png_simple.py) | Python | Local Java renderer; downloads its JAR when absent |
| [`week01/`](week01/) | Subdir | Week 01 mirror |
| [`week02/`](week02/) | Subdir | Week 02 mirror |
| [`week03/`](week03/) | Subdir | Week 03 mirror |
| [`week04/`](week04/) | Subdir | Week 04 mirror |
| [`week05/`](week05/) | Subdir | Week 05 mirror |
| [`week06/`](week06/) | Subdir | Week 06 mirror |
| [`week07/`](week07/) | Subdir | Week 07 mirror |
| [`week08/`](week08/) | Subdir | Week 08 mirror |
| [`week09/`](week09/) | Subdir | Week 09 mirror |
| [`week10/`](week10/) | Subdir | Week 10 mirror |
| [`week11/`](week11/) | Subdir | Week 11 mirror |
| [`week12/`](week12/) | Subdir | Week 12 mirror |
| [`week13/`](week13/) | Subdir | Week 13 mirror |

## Visual Overview

```mermaid
flowchart TD
    W["weekNN/*.puml"] -->|"offline"| J["plantuml.jar (Java)"]
    J --> GA["generate_all.sh\nPNG next to .puml"]
    J --> GD["generate_diagrams.py\nPNG/SVG/PDF → out/"]
    GA --> A4["generate_a4.py\npage-friendly PNG"]
    GD --> A4
    W -->|"online"| GS["generate_diagrams.py --method http\nPlantUML server"]

    MIR["Mirrors lecture sources"] -.-> L["03_LECTURES/CNN/assets/puml/"]
    W -.-> MIR

    style W fill:#e1f5fe,stroke:#0288d1
    style J fill:#fff3e0,stroke:#f57c00
    style GS fill:#fce4ec,stroke:#c62828
```

## Usage

### Option 1: Offline rendering (recommended)

From the repository root:

```bash
# Option 1A: use the canonical JAR location used by the whole repository
bash 00_TOOLS/plantuml/get_plantuml_jar.sh

# Render all week folders into PNG next to each .puml
bash "00_TOOLS/PlantUML(optional)/generate_all.sh"
```

### Option 2: Offline rendering into a separate output directory

```bash
cd "00_TOOLS/PlantUML(optional)"
python3 generate_diagrams.py --source-dir . --output-dir ./out --jar-path ../plantuml.jar --method jar --format png
python3 generate_diagrams.py --source-dir . --output-dir ./out --jar-path ../plantuml.jar --method jar --format svg
```

### Option 3: Online rendering (no local Java)

```bash
cd "00_TOOLS/PlantUML(optional)"
python3 generate_diagrams.py --source-dir . --output-dir ./out --method http --format png
```

The HTTP method uploads diagram source to the public PlantUML service. Use the local JAR for private diagrams or offline work. The separate output directory preserves each source subdirectory, so identical basenames in different weeks do not overwrite one another. Run one `--format` per invocation.

For A4 handouts, `generate_a4.py --dpi 150 --jar ../plantuml.jar` stores the requested DPI in PNG metadata. Pixel dimensions are rounded to whole pixels; choose actual size (100%) when printing to preserve approximately 210 × 297 mm.

## Design Rationale

Lecture folders keep diagrams near the teaching material, while this directory provides a single location for batch export and handout preparation. The week partition mirrors the course delivery structure so instructors can export only the diagrams used in a given week.

## Cross-References and Contextual Connections

### Prerequisites and Dependency Links

| Prerequisite | Path | Why |
|---|---|---|
| Canonical PlantUML renderer | [`../plantuml/`](../plantuml/) | Provides the JAR used across the repository |
| Java (offline modes) | — | Required for `generate_all.sh` and `generate_diagrams.py` when using a local JAR |
| Internet access (online mode) | — | Required by `generate_diagrams.py --method http` |

### Lecture, Seminar, Project and Quiz Mapping

| This folder component | Lecture foundation | Seminar | Project | Quiz |
|---|---|---|---|---|
| `week01/` … `week13/` | Mirrors `03_LECTURES/C01–C13/assets/puml/` | Same-week seminars `04_SEMINARS/S01–S13/` | Not required | Weeks 01–13 (`COMPnet_W01_Questions.md` … `COMPnet_W13_Questions.md`) |

For week-specific lecture, seminar and quiz links, open the README in the relevant `weekNN/` subdirectory.

### Downstream Dependencies

No CI jobs and no course runtime scripts depend on this directory. It exists as an optional mirror and batch-export convenience layer.

### Suggested Learning Sequence

**Suggested sequence:** render diagrams in-place for a lecture (`03_LECTURES/CNN/assets/render.sh`) → if batch export is needed, use this folder’s scripts → optionally post-process with `generate_a4.py` for handouts

## Selective Clone Instructions

**Method A — Git sparse-checkout (requires Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set "00_TOOLS/PlantUML(optional)"
```

To fetch the canonical renderer as well:

```bash
git sparse-checkout add 00_TOOLS/plantuml
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/PlantUML(optional)
```

## Version and Provenance

- The week mirrors are kept in sync with the lecture `assets/puml/` sources
- Rendering scripts are maintained to support both offline (local JAR) and online (server-based) export

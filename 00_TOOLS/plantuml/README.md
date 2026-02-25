# plantuml — Central JAR Provisioning and Rendering

Two shell scripts that form the canonical PlantUML infrastructure for the entire repository. Every `assets/render.sh` wrapper in lectures, seminars and projects delegates to `render_puml.sh` here. The JAR itself is downloaded on demand and kept out of version control via `.gitignore`.

## File Index

| File | Description | Lines |
|---|---|---|
| [`get_plantuml_jar.sh`](get_plantuml_jar.sh) | Downloads the latest PlantUML release JAR into `00_TOOLS/plantuml.jar`; skips if already present | 39 |
| [`render_puml.sh`](render_puml.sh) | Renders all `.puml` files from an input directory into an output directory; accepts `PLANTUML_JAR` as an environment variable | 67 |

## Usage

Run once after cloning the repository:

```bash
bash 00_TOOLS/plantuml/get_plantuml_jar.sh
```

The JAR lands at `00_TOOLS/plantuml.jar`. To render diagrams for a specific lecture:

```bash
bash 03_LECTURES/C05/assets/render.sh
```

That wrapper internally calls:

```bash
render_puml.sh <input_dir>/puml <input_dir>/images
```

To override the JAR location:

```bash
PLANTUML_JAR=/path/to/plantuml.jar bash 00_TOOLS/plantuml/render_puml.sh ./puml ./images
```

## Cross-References and Contextual Connections

### Downstream Dependencies

This directory is the single most widely referenced tooling folder in the repository. Every `assets/render.sh` across lectures, seminars and projects calls `render_puml.sh`:

| Consumer | Count | Example path |
|---|---|---|
| Lectures | 14 | `03_LECTURES/C01/assets/render.sh` … `03_LECTURES/C14/assets/render.sh` |
| Seminars | 12 | `04_SEMINARS/S01/assets/render.sh` … `04_SEMINARS/S14/assets/render.sh` |
| Projects | 3 | `02_PROJECTS/00_common/assets/render.sh`, `01_network_applications/…`, `02_administration_security/…` |

The `PlantUML(optional)/` sibling directory contains the batch-generation scripts that also rely on the downloaded JAR.

### Prerequisite

| Prerequisite | Path | Why |
|---|---|---|
| Java 8+ | System-level install | PlantUML requires a JRE |

### Suggested Learning Sequence

**Suggested sequence:** `get_plantuml_jar.sh` (download) → any `assets/render.sh` (per-module render) → [`PlantUML(optional)/`](<../PlantUML(optional)/README.md>) (batch render)

## Selective Clone Instructions

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/plantuml
```

**Method B — Direct download (no Git required)**

```
https://github.com/antonioclim/COMPNET-EN/tree/main/00_TOOLS/plantuml
```

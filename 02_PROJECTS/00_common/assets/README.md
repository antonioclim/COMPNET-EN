# 00_common/assets — Shared Diagram Sources

PlantUML source files and a rendering script that produce the architectural diagrams used in [`../README_STANDARD_RC2026.md`](../README_STANDARD_RC2026.md) and related assessment documentation.

## File/Folder Index

| Name | Description |
|---|---|
| [`puml/`](puml/) | Six PlantUML source files covering the CI pipeline, E2 pipeline, PCAP validation, assessment phases, student-repo structure and tester lifecycle |
| [`images/`](images/) | Output directory for rendered PNGs (`.gitkeep` placeholder; populated by `render.sh`) |
| [`render.sh`](render.sh) | Shell script that delegates to the central PlantUML renderer at `../../../00_TOOLS/plantuml/render_puml.sh` |

## Usage

```bash
bash render.sh
# Outputs PNG files to images/
```

Requires `plantuml.jar` — see [`../../../00_TOOLS/plantuml/`](../../../00_TOOLS/plantuml/).

## Cross-References

The rendered diagrams illustrate concepts defined in [`../README_STANDARD_RC2026.md`](../README_STANDARD_RC2026.md). The rendering script depends on the central PlantUML helper in [`../../../00_TOOLS/plantuml/`](../../../00_TOOLS/plantuml/).

## Selective Clone

**Method A — Git sparse-checkout (requires Git ≥ 2.25)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 02_PROJECTS/00_common/assets
```

**Method B — Direct download**

Browse: <https://github.com/antonioclim/COMPNET-EN/tree/main/02_PROJECTS/00_common/assets>

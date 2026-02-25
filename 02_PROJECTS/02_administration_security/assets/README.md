# 02_administration_security/assets — Diagrams for A-Projects

PlantUML source files and a rendering script for the A01–A10 project architecture, demo-scenario and message-flow diagrams.

## File/Folder Index

| Name | Description | Count |
|---|---|---|
| [`puml/`](puml/) | PlantUML sources: architecture, demo-scenario and message-flow diagrams per project | 30 `.puml` files (3 × 10 projects) |
| [`images/`](images/) | Rendered PNG output (`.gitkeep` placeholder; populated by `render.sh`) | — |
| [`render.sh`](render.sh) | Delegates rendering to `../../../00_TOOLS/plantuml/render_puml.sh` | 6 lines |

## Usage

```bash
bash render.sh
# Renders all 30 .puml files into images/
```

## Cross-References

| Related area | Path | Relationship |
|---|---|---|
| Project briefs | [`../`](../) | Each A{NN} brief references its diagram set |
| PlantUML renderer | [`../../../00_TOOLS/plantuml/`](../../../00_TOOLS/plantuml/) | Central rendering script |

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/02_administration_security/assets
```

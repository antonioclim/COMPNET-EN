# 01_network_applications/assets — Diagrams and Portainer Guides

Supporting material for the S01–S15 project briefs: PlantUML architecture diagrams (three per project) and per-project Portainer debugging guides.

## File/Folder Index

| Name | Description | Count |
|---|---|---|
| [`PORTAINER/`](PORTAINER/) | Per-project Portainer guides with container maps, published ports and debugging strategies | 15 Markdown files across 15 subdirectories |
| [`puml/`](puml/) | PlantUML sources: architecture, E2 message flow and state diagrams for each project | 45 `.puml` files (3 × 15 projects) |
| [`images/`](images/) | Rendered PNG output (`.gitkeep` placeholder; populated by `render.sh`) | — |
| [`render.sh`](render.sh) | Delegates rendering to `../../../00_TOOLS/plantuml/render_puml.sh` | 6 lines |

## Usage

```bash
bash render.sh
# Renders all 45 .puml files into images/
```

## Cross-References

| Related area | Path | Relationship |
|---|---|---|
| Project briefs | [`../`](../) | Each S{NN} brief references its architecture diagram in `puml/` |
| Portainer overview map | [`../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md`](../../../00_TOOLS/Portainer/PROJECTS/PROJECTS_PORTAINER_MAP.md) | Summarises all 15 Portainer guides with tier ratings |
| PlantUML renderer | [`../../../00_TOOLS/plantuml/`](../../../00_TOOLS/plantuml/) | Central rendering script |

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/01_network_applications/assets
```

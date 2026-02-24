#!/usr/bin/env bash
# Render PlantUML diagrams for this module.
# Delegates to the central helper; run get_plantuml_jar.sh first.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/../../../00_TOOLS/plantuml/render_puml.sh" \
    "$SCRIPT_DIR/puml" "$SCRIPT_DIR/images"

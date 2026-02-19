# PlantUML diagrams – Weeks 1–14

72 diagrams optimised for rendering via the PlantUML HTTP server.

## Resolved issues

- Removed `note as` syntax (it can cause empty renders on some servers)
- Removed complex multi-line notes
- Used `legend` for explanatory text
- Simplified syntax for HTTP API compatibility

## Generation

### Using the PlantUML server (online)

```bash
python3 generate_png_simple.py
```

### Using a local JAR (recommended)

```bash
# Download the JAR once
wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar

# Generate all PNG files
java -jar plantuml.jar -tpng week*/*.puml
```

### A4 format for printing

```bash
pip install Pillow
python3 generate_a4.py --dpi 150 --output-dir ./png_a4
```

## Structure

- `week01-14/`: 5–6 diagrams per week
- Each diagram uses only validated PlantUML syntax
- Colours: Material Design palette
- Font: Arial (cross-platform)

## Usage in the course

The diagrams are referenced in the lecture and seminar materials. To include them in presentations:

1. Generate the PNG files with one of the scripts above
2. Copy the `.png` files into your slides
3. For printing, use the A4 variant with DPI 150+

## Troubleshooting

**The JAR does not download:**

```bash
# Alternative using curl
curl -L -o plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar
```

**Java is missing:**

```bash
sudo apt install default-jre
```

**A diagram does not render:**

- Check the syntax in the online editor: https://www.plantuml.com/plantuml/uml/
- Ensure the file starts with `@startuml` and ends with `@enduml`

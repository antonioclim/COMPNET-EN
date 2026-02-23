# PlantUML diagrams — Weeks 1–13

118 diagrams distributed across 13 weekly directories, suitable for rendering
via the PlantUML HTTP server or a local JAR.

## Diagram count per week

| Week | Diagrams | Week | Diagrams |
|------|----------|------|----------|
| 01   | 9        | 08   | 12       |
| 02   | 8        | 09   | 6        |
| 03   | 7        | 10   | 10       |
| 04   | 13       | 11   | 7        |
| 05   | 10       | 12   | 10       |
| 06   | 11       | 13   | 6        |
| 07   | 9        |      |          |

Range: 6–13 diagrams per week. There is no week14 directory (Week 14 is a
revision session with no dedicated diagrams).

## Resolved issues

- Removed `note as` syntax (can produce empty renders on certain servers).
- Removed complex multi-line notes.
- Used `legend` blocks for explanatory text.
- Simplified syntax for HTTP API compatibility.

## Generation

### PlantUML server (online)

```bash
python3 generate_png_simple.py
```

### Local JAR (recommended)

```bash
# Download the JAR once
wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar

# Generate all PNGs
java -jar plantuml.jar -tpng week*/*.puml
```

### A4 format for printing

```bash
pip install Pillow
python3 generate_a4.py --dpi 150 --output-dir ./png_a4
```

## Structure

- `week01/`–`week13/`: 6–13 diagrams per week.
- Every diagram uses only validated PlantUML syntax.
- Colour palette: Material Design.
- Font: Arial (cross-platform).
- All diagrams include `title` and `legend` blocks.

## Relation to lecture diagrams

Every `.puml` file here is identical to its counterpart in
`03_LECTURES/C{NN}/assets/puml/`. This directory exists as a flat,
week-indexed collection for batch generation and printing.

## Troubleshooting

**The JAR does not download:**

```bash
curl -L -o plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar
```

**Java is missing:**

```bash
sudo apt install default-jre
```

**A diagram does not render:**

- Check the syntax in the online editor: https://www.plantuml.com/plantuml/uml/
- Confirm the file begins with `@startuml` and ends with `@enduml`.

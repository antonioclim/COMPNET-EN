#!/bin/bash
#
# generate_all.sh - Generate PNG images from all PlantUML diagrams
#
# Usage:
#   ./generate_all.sh              # Use auto-detection
#   ./generate_all.sh --http       # Use HTTP server (no Java needed)
#   ./generate_all.sh --docker     # Use Docker
#   ./generate_all.sh --help       # Show help
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLANTUML_JAR="$SCRIPT_DIR/plantuml.jar"
PLANTUML_VERSION="1.2024.8"
PLANTUML_URL="https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar"

# Colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_ok() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
PlantUML Diagram Generator
==========================

Usage: $0 [OPTIONS]

Options:
    --http      Use PlantUML HTTP server (no Java required)
    --docker    Use Docker (requires Docker installed)
    --jar       Use local PlantUML JAR (requires Java)
    --download  Download PlantUML JAR only
    --svg       Generate SVG instead of PNG
    --help      Show this help message

Examples:
    $0                  # Auto-detect best method
    $0 --http           # Use online server
    $0 --docker --svg   # Use Docker, generate SVG

EOF
}

download_plantuml() {
    if [[ -f "$PLANTUML_JAR" ]]; then
        log_ok "PlantUML JAR already exists: $PLANTUML_JAR"
        return 0
    fi
    
    log_info "Downloading PlantUML ${PLANTUML_VERSION}..."
    
    if command -v wget &> /dev/null; then
        wget -q --show-progress -O "$PLANTUML_JAR" "$PLANTUML_URL"
    elif command -v curl &> /dev/null; then
        curl -L -o "$PLANTUML_JAR" "$PLANTUML_URL"
    else
        log_error "Neither wget nor curl is available"
        return 1
    fi
    
    log_ok "Downloaded: $PLANTUML_JAR"
}

check_java() {
    if command -v java &> /dev/null; then
        return 0
    else
        return 1
    fi
}

check_docker() {
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        return 0
    else
        return 1
    fi
}

generate_with_jar() {
    local format="$1"
    
    if [[ ! -f "$PLANTUML_JAR" ]]; then
        download_plantuml || exit 1
    fi
    
    if ! check_java; then
        log_error "Java is required but not installed"
        exit 1
    fi
    
    log_info "Generating diagrams with local JAR..."
    
    find "$SCRIPT_DIR" -name "*.puml" -print0 | while IFS= read -r -d '' file; do
        echo "  Processing: $(basename "$file")"
        java -jar "$PLANTUML_JAR" -t"$format" "$file"
    done
}

generate_with_docker() {
    local format="$1"
    
    if ! check_docker; then
        log_error "Docker is required but not available"
        exit 1
    fi
    
    log_info "Generating diagrams with Docker..."
    
    # Pull image if needed
    docker pull plantuml/plantuml:latest
    
    find "$SCRIPT_DIR" -name "*.puml" -print0 | while IFS= read -r -d '' file; do
        dir=$(dirname "$file")
        filename=$(basename "$file")
        echo "  Processing: $filename"
        docker run --rm -v "$dir:/data" plantuml/plantuml:latest -t"$format" "/data/$filename"
    done
}

generate_with_http() {
    local format="$1"
    
    log_info "Generating diagrams with HTTP server..."
    log_warn "This method requires internet connection"
    
    # Use Python script for HTTP generation
    python3 "$SCRIPT_DIR/generate_diagrams.py" --method http --format "$format"
}

# Parse arguments
METHOD="auto"
FORMAT="png"

while [[ $# -gt 0 ]]; do
    case $1 in
        --http)
            METHOD="http"
            shift
            ;;
        --docker)
            METHOD="docker"
            shift
            ;;
        --jar)
            METHOD="jar"
            shift
            ;;
        --download)
            download_plantuml
            exit 0
            ;;
        --svg)
            FORMAT="svg"
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
echo "========================================"
echo "PlantUML Diagram Generator"
echo "========================================"
echo ""

# Count diagrams
DIAGRAM_COUNT=$(find "$SCRIPT_DIR" -name "*.puml" | wc -l)
log_info "Found $DIAGRAM_COUNT diagram(s)"

# Auto-detect method if needed
if [[ "$METHOD" == "auto" ]]; then
    if check_java && [[ -f "$PLANTUML_JAR" ]]; then
        METHOD="jar"
    elif check_java; then
        log_info "Downloading PlantUML JAR..."
        download_plantuml
        METHOD="jar"
    elif check_docker; then
        METHOD="docker"
    else
        METHOD="http"
    fi
    log_info "Auto-detected method: $METHOD"
fi

log_info "Output format: $FORMAT"
echo ""

# Generate
case $METHOD in
    jar)
        generate_with_jar "$FORMAT"
        ;;
    docker)
        generate_with_docker "$FORMAT"
        ;;
    http)
        generate_with_http "$FORMAT"
        ;;
esac

echo ""
log_ok "Generation complete!"
echo ""
echo "Generated files are located next to their source .puml files."

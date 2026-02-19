#!/usr/bin/env python3
"""
Simple PlantUML PNG Generator
=============================

A minimal script that generates PNG images from all .puml files.
Automatically downloads PlantUML JAR if not present.

Usage:
    python3 generate_png_simple.py

Requirements:
    - Python 3.7+
    - Java Runtime Environment (JRE) 8+
    - Internet connection (for first-time JAR download)
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

# Configuration
PLANTUML_VERSION = "1.2024.8"
PLANTUML_JAR_URL = f"https://github.com/plantuml/plantuml/releases/download/v{PLANTUML_VERSION}/plantuml-{PLANTUML_VERSION}.jar"
PLANTUML_JAR_NAME = "plantuml.jar"


def download_plantuml_jar(target_path: Path) -> bool:
    """Download PlantUML JAR file."""
    print(f"Downloading PlantUML {PLANTUML_VERSION}...")
    print(f"  From: {PLANTUML_JAR_URL}")
    print(f"  To:   {target_path}")
    
    try:
        urllib.request.urlretrieve(PLANTUML_JAR_URL, target_path)
        print("  Download complete!")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def check_java() -> bool:
    """Check if Java is available."""
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False


def generate_png(puml_file: Path, jar_path: Path) -> bool:
    """Generate PNG from a single .puml file."""
    try:
        result = subprocess.run(
            ['java', '-jar', str(jar_path), '-tpng', str(puml_file)],
            capture_output=True,
            timeout=60,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"    Error: {e}")
        return False


def main():
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    jar_path = script_dir / PLANTUML_JAR_NAME
    
    print("=" * 60)
    print("PlantUML PNG Generator")
    print("=" * 60)
    
    # Check Java
    if not check_java():
        print("\n[ERROR] Java is not installed or not in PATH.")
        print("\nPlease install Java JRE 8 or later:")
        print("  Ubuntu/Debian: sudo apt install default-jre")
        print("  Fedora/RHEL:   sudo dnf install java-latest-openjdk")
        print("  macOS:         brew install openjdk")
        print("  Windows:       Download from https://adoptium.net/")
        sys.exit(1)
    
    print("[OK] Java is available")
    
    # Check/download PlantUML JAR
    if not jar_path.exists():
        print(f"\n[INFO] PlantUML JAR not found at {jar_path}")
        if not download_plantuml_jar(jar_path):
            print("\n[ERROR] Failed to download PlantUML JAR")
            print("Please download manually from: https://plantuml.com/download")
            sys.exit(1)
    
    print(f"[OK] PlantUML JAR: {jar_path}")
    
    # Find all .puml files
    puml_files = sorted(script_dir.rglob("*.puml"))
    
    if not puml_files:
        print("\n[WARNING] No .puml files found!")
        sys.exit(0)
    
    print(f"\n[INFO] Found {len(puml_files)} diagram(s)")
    print("-" * 60)
    
    # Generate PNGs
    success = 0
    failed = 0
    
    for puml_file in puml_files:
        rel_path = puml_file.relative_to(script_dir)
        png_file = puml_file.with_suffix('.png')
        
        print(f"  Generating: {rel_path}")
        
        if generate_png(puml_file, jar_path):
            if png_file.exists():
                size_kb = png_file.stat().st_size / 1024
                print(f"    -> {png_file.name} ({size_kb:.1f} KB)")
                success += 1
            else:
                print(f"    [WARN] PNG not created")
                failed += 1
        else:
            print(f"    [FAIL] Generation failed")
            failed += 1
    
    # Summary
    print("-" * 60)
    print(f"\nComplete! Generated {success}/{len(puml_files)} images")
    
    if failed > 0:
        print(f"  ({failed} failed)")
        sys.exit(1)
    
    print("\nPNG files are located next to their source .puml files.")


if __name__ == "__main__":
    main()

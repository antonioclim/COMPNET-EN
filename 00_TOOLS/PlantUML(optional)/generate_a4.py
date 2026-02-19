#!/usr/bin/env python3
"""
PlantUML A4 Generator
Generates diagrams at exact A4 dimensions with auto portrait/landscape detection.

Requirements: Java 8+, Pillow (pip install Pillow)
Usage: python3 generate_a4.py [--dpi 150] [--output-dir ./png_a4]
"""

import os
import sys
import re
import subprocess
import tempfile
import argparse
from pathlib import Path

# A4 = 210mm x 297mm
A4_SIZES = {
    72:  {'portrait': (595, 842),   'landscape': (842, 595)},
    96:  {'portrait': (794, 1123),  'landscape': (1123, 794)},
    150: {'portrait': (1240, 1754), 'landscape': (1754, 1240)},
    300: {'portrait': (2480, 3508), 'landscape': (3508, 2480)},
}


def detect_orientation(content: str) -> str:
    """Detect best orientation based on diagram content."""
    portrait = landscape = 0
    
    # Sequence diagrams -> portrait
    if 'participant' in content or '->>' in content:
        portrait += 5
    
    # Activity with start -> portrait  
    if re.search(r'^\s*start\s*$', content, re.MULTILINE):
        portrait += 4
    
    # Swimlanes -> portrait
    if re.search(r'\|[^|]+\|', content):
        portrait += 3
    
    # Many steps -> portrait
    if content.count(':') > 5:
        portrait += 2
    
    # Nested rectangles -> landscape
    if content.count('{') > 3:
        landscape += 3
    
    # together blocks -> landscape
    if 'together' in content:
        landscape += 2
    
    # Check line structure
    lines = [l for l in content.split('\n') if l.strip()]
    if lines:
        avg_len = sum(len(l) for l in lines) / len(lines)
        if len(lines) > 30 and avg_len < 40:
            portrait += 2
        elif avg_len > 50:
            landscape += 2
    
    return 'portrait' if portrait >= landscape else 'landscape'


def resize_to_a4(src_path: Path, dst_path: Path, width: int, height: int):
    """Resize image to exact A4 with content centred on white background."""
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow required. Install with: pip install Pillow")
        sys.exit(1)
    
    with Image.open(src_path) as img:
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, 'white')
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        
        img_w, img_h = img.size
        
        # Calculate scale to fit with margins (5% each side = 90% usable)
        usable_w = int(width * 0.92)
        usable_h = int(height * 0.92)
        
        scale = min(usable_w / img_w, usable_h / img_h, 1.0)
        
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        
        if scale < 1.0:
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Create white A4 canvas and paste centred
        canvas = Image.new('RGB', (width, height), 'white')
        x = (width - new_w) // 2
        y = (height - new_h) // 2
        canvas.paste(img, (x, y))
        
        canvas.save(dst_path, 'PNG')


def generate_diagram(puml_path: Path, output_dir: Path, dpi: int, jar_path: Path) -> tuple:
    """Generate single diagram in A4 format. Returns (success, orientation, message)."""
    try:
        with open(puml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orientation = detect_orientation(content)
        width, height = A4_SIZES[dpi][orientation]
        
        # Create output week directory
        week_dir = output_dir / puml_path.parent.name
        week_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate to temp file first
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_puml = Path(tmp_dir) / puml_path.name
            tmp_puml.write_text(content, encoding='utf-8')
            
            # Run PlantUML
            cmd = ['java', '-jar', str(jar_path), '-tpng', '-charset', 'UTF-8',
                   f'-o{tmp_dir}', str(tmp_puml)]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return (False, orientation, result.stderr[:100])
            
            # Find generated PNG
            tmp_png = Path(tmp_dir) / (puml_path.stem + '.png')
            
            if not tmp_png.exists():
                return (False, orientation, "PNG not generated")
            
            # Resize to A4
            final_png = week_dir / (puml_path.stem + '.png')
            resize_to_a4(tmp_png, final_png, width, height)
            
            return (True, orientation, str(final_png))
            
    except Exception as e:
        return (False, 'unknown', str(e)[:100])


def download_jar(jar_path: Path) -> bool:
    """Download PlantUML JAR if needed."""
    if jar_path.exists():
        return True
    
    print("Downloading PlantUML JAR...")
    url = "https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar"
    
    try:
        import urllib.request
        urllib.request.urlretrieve(url, jar_path)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate PlantUML diagrams in A4')
    parser.add_argument('--dpi', type=int, default=150, choices=[72, 96, 150, 300])
    parser.add_argument('--output-dir', type=str, default='./png_a4')
    parser.add_argument('--jar', type=str, default='./plantuml.jar')
    parser.add_argument('--input-dir', type=str, default='.')
    args = parser.parse_args()
    
    # Check Java
    try:
        subprocess.run(['java', '-version'], capture_output=True, check=True)
    except:
        print("ERROR: Java not found")
        sys.exit(1)
    
    # Check Pillow
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow required. Install: pip install Pillow")
        sys.exit(1)
    
    jar_path = Path(args.jar)
    output_dir = Path(args.output_dir)
    input_dir = Path(args.input_dir)
    
    if not download_jar(jar_path):
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    puml_files = sorted(input_dir.glob('week*/*.puml'))
    if not puml_files:
        print(f"No .puml files in {input_dir}/week*/")
        sys.exit(1)
    
    pw, ph = A4_SIZES[args.dpi]['portrait']
    print(f"Generating {len(puml_files)} diagrams in A4 @ {args.dpi} DPI")
    print(f"Portrait: {pw}x{ph} | Landscape: {ph}x{pw}")
    print("-" * 50)
    
    ok = err = port = land = 0
    failed = []
    
    for pf in puml_files:
        success, orient, msg = generate_diagram(pf, output_dir, args.dpi, jar_path)
        
        if success:
            ok += 1
            if orient == 'portrait':
                port += 1
                sym = 'P'
            else:
                land += 1
                sym = 'L'
            print(f"  [OK] [{sym}] {pf.parent.name}/{pf.stem}")
        else:
            err += 1
            failed.append((pf.name, msg))
            print(f"  [ERR]    {pf.parent.name}/{pf.stem}: {msg[:40]}")
    
    print("-" * 50)
    print(f"Done: {ok} OK ({port} portrait, {land} landscape), {err} errors")
    
    if failed:
        print("Failed:")
        for n, m in failed[:5]:
            print(f"  - {n}: {m}")
    
    return 0 if err == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
PlantUML Diagram Generator
==========================

Generates PNG images from all PlantUML (.puml) files in the diagrams directory.

Requirements:
    Option A (Local JAR - recommended for offline use):
        - Java Runtime Environment (JRE) 8+
        - PlantUML JAR file (download from https://plantuml.com/download)
        - Graphviz (for certain diagram types)
    
    Option B (HTTP Server):
        - Internet connection
        - Uses PlantUML public server (no local installation needed)
    
    Option C (Docker):
        - Docker installed
        - Uses official PlantUML Docker image

Usage:
    python3 generate_diagrams.py [OPTIONS]

Options:
    --method jar|http|docker    Generation method (default: auto-detect)
    --jar-path PATH             Path to plantuml.jar (default: ./plantuml.jar)
    --output-dir DIR            Output directory (default: same as source)
    --format png|svg|eps        Output format (default: png)
    --verbose                   Show detailed progress
    --dry-run                   Show what would be done without generating
    --parallel N                Number of parallel workers (default: 4)

Examples:
    python3 generate_diagrams.py
    python3 generate_diagrams.py --method http --verbose
    python3 generate_diagrams.py --jar-path /opt/plantuml.jar --parallel 8
    python3 generate_diagrams.py --method docker --format svg

Author: ASE-CSIE Computer Networks Course
"""

import os
import sys
import argparse
import subprocess
import shutil
import hashlib
import zlib
import base64
import string
import concurrent.futures
from pathlib import Path
from typing import Optional, List, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Configuration
DEFAULT_PLANTUML_JAR = "plantuml.jar"
PLANTUML_SERVER = "http://www.plantuml.com/plantuml"
DOCKER_IMAGE = "plantuml/plantuml:latest"
SUPPORTED_FORMATS = ["png", "svg", "eps", "pdf", "txt"]

# PlantUML encoding alphabet
PLANTUML_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase + "-_"
BASE64_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def encode_plantuml(text: str) -> str:
    """Encode PlantUML text for HTTP server URL."""
    compressed = zlib.compress(text.encode('utf-8'), 9)[2:-4]
    encoded = base64.b64encode(compressed).decode('ascii')
    
    # Convert from base64 to PlantUML alphabet
    result = ""
    for char in encoded:
        if char in BASE64_ALPHABET:
            result += PLANTUML_ALPHABET[BASE64_ALPHABET.index(char)]
        else:
            result += char
    
    return result


def find_puml_files(base_dir: Path) -> List[Path]:
    """Find all .puml files recursively."""
    puml_files = []
    for root, dirs, files in os.walk(base_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.puml'):
                puml_files.append(Path(root) / file)
    return sorted(puml_files)


def check_java() -> bool:
    """Check if Java is available."""
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_docker() -> bool:
    """Check if Docker is available."""
    try:
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_plantuml_jar(jar_path: Path) -> bool:
    """Check if PlantUML JAR exists and is valid."""
    if not jar_path.exists():
        return False
    try:
        result = subprocess.run(
            ['java', '-jar', str(jar_path), '-version'],
            capture_output=True,
            timeout=30
        )
        return result.returncode == 0
    except subprocess.SubprocessError:
        return False


def generate_with_jar(
    puml_file: Path,
    output_dir: Path,
    jar_path: Path,
    fmt: str = "png",
    verbose: bool = False
) -> Tuple[bool, str]:
    """Generate diagram using local PlantUML JAR."""
    output_file = output_dir / puml_file.with_suffix(f'.{fmt}').name
    
    try:
        cmd = [
            'java', '-jar', str(jar_path),
            f'-t{fmt}',
            '-o', str(output_dir),
            str(puml_file)
        ]
        
        if verbose:
            print(f"  Command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=60,
            text=True
        )
        
        if result.returncode == 0 and output_file.exists():
            return True, str(output_file)
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Timeout expired"
    except Exception as e:
        return False, str(e)


def generate_with_http(
    puml_file: Path,
    output_dir: Path,
    fmt: str = "png",
    verbose: bool = False
) -> Tuple[bool, str]:
    """Generate diagram using PlantUML HTTP server."""
    output_file = output_dir / puml_file.with_suffix(f'.{fmt}').name
    
    try:
        # Read and encode the PlantUML content
        with open(puml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encoded = encode_plantuml(content)
        url = f"{PLANTUML_SERVER}/{fmt}/{encoded}"
        
        if verbose:
            print(f"  URL length: {len(url)} chars")
        
        # Download the image
        request = Request(url)
        request.add_header('User-Agent', 'PlantUML-Generator/1.0')
        
        with urlopen(request, timeout=30) as response:
            with open(output_file, 'wb') as f:
                f.write(response.read())
        
        if output_file.exists() and output_file.stat().st_size > 0:
            return True, str(output_file)
        else:
            return False, "Empty or missing output file"
            
    except HTTPError as e:
        return False, f"HTTP Error {e.code}: {e.reason}"
    except URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, str(e)


def generate_with_docker(
    puml_file: Path,
    output_dir: Path,
    fmt: str = "png",
    verbose: bool = False
) -> Tuple[bool, str]:
    """Generate diagram using Docker PlantUML image."""
    output_file = output_dir / puml_file.with_suffix(f'.{fmt}').name
    
    try:
        # Mount the directory containing the file
        mount_dir = puml_file.parent.absolute()
        filename = puml_file.name
        
        cmd = [
            'docker', 'run', '--rm',
            '-v', f'{mount_dir}:/data',
            '-v', f'{output_dir.absolute()}:/output',
            DOCKER_IMAGE,
            f'-t{fmt}',
            '-o', '/output',
            f'/data/{filename}'
        ]
        
        if verbose:
            print(f"  Command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120,
            text=True
        )
        
        if result.returncode == 0 and output_file.exists():
            return True, str(output_file)
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Timeout expired"
    except Exception as e:
        return False, str(e)


def detect_method(jar_path: Path) -> Optional[str]:
    """Auto-detect the best available generation method."""
    if check_plantuml_jar(jar_path):
        return "jar"
    if check_java() and jar_path.exists():
        return "jar"
    if check_docker():
        return "docker"
    # HTTP is always available as fallback
    return "http"


def process_file(args: Tuple) -> Tuple[Path, bool, str]:
    """Process a single file (for parallel execution)."""
    puml_file, output_dir, method, jar_path, fmt, verbose = args
    
    if method == "jar":
        success, result = generate_with_jar(puml_file, output_dir, jar_path, fmt, verbose)
    elif method == "docker":
        success, result = generate_with_docker(puml_file, output_dir, fmt, verbose)
    else:  # http
        success, result = generate_with_http(puml_file, output_dir, fmt, verbose)
    
    return puml_file, success, result


def main():
    parser = argparse.ArgumentParser(
        description="Generate PNG images from PlantUML diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--source-dir',
        type=Path,
        default=Path(__file__).parent,
        help="Directory containing .puml files (default: script directory)"
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help="Output directory for generated images (default: same as source)"
    )
    
    parser.add_argument(
        '--method',
        choices=['jar', 'http', 'docker', 'auto'],
        default='auto',
        help="Generation method (default: auto-detect)"
    )
    
    parser.add_argument(
        '--jar-path',
        type=Path,
        default=Path(DEFAULT_PLANTUML_JAR),
        help=f"Path to plantuml.jar (default: {DEFAULT_PLANTUML_JAR})"
    )
    
    parser.add_argument(
        '--format',
        choices=SUPPORTED_FORMATS,
        default='png',
        help="Output format (default: png)"
    )
    
    parser.add_argument(
        '--parallel',
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Show detailed progress"
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Show what would be done without generating"
    )
    
    args = parser.parse_args()
    
    # Validate source directory
    if not args.source_dir.exists():
        print(f"Error: Source directory not found: {args.source_dir}")
        sys.exit(1)
    
    # Find all .puml files
    puml_files = find_puml_files(args.source_dir)
    
    if not puml_files:
        print(f"No .puml files found in {args.source_dir}")
        sys.exit(0)
    
    print(f"Found {len(puml_files)} PlantUML diagram(s)")
    
    # Detect or validate method
    if args.method == 'auto':
        method = detect_method(args.jar_path)
        print(f"Auto-detected method: {method}")
    else:
        method = args.method
        
        # Validate method availability
        if method == 'jar' and not check_plantuml_jar(args.jar_path):
            if not args.jar_path.exists():
                print(f"Error: PlantUML JAR not found at {args.jar_path}")
                print("\nTo download PlantUML JAR:")
                print("  wget https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar -O plantuml.jar")
                print("\nOr use --method http for online generation")
            elif not check_java():
                print("Error: Java is not installed or not in PATH")
            sys.exit(1)
        
        if method == 'docker' and not check_docker():
            print("Error: Docker is not installed or not running")
            sys.exit(1)
    
    print(f"Using method: {method}")
    print(f"Output format: {args.format}")
    
    if args.dry_run:
        print("\n=== DRY RUN - No files will be generated ===\n")
        for puml_file in puml_files:
            output_dir = args.output_dir or puml_file.parent
            output_file = output_dir / puml_file.with_suffix(f'.{args.format}').name
            print(f"  {puml_file} -> {output_file}")
        sys.exit(0)
    
    # Process files
    success_count = 0
    error_count = 0
    errors = []
    
    # Prepare work items
    work_items = []
    for puml_file in puml_files:
        output_dir = args.output_dir or puml_file.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        work_items.append((
            puml_file, output_dir, method, args.jar_path, args.format, args.verbose
        ))
    
    print(f"\nGenerating {len(work_items)} diagram(s) with {args.parallel} worker(s)...\n")
    
    # Use parallel processing for http method, sequential for others
    if method == 'http' and args.parallel > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {executor.submit(process_file, item): item[0] for item in work_items}
            
            for future in concurrent.futures.as_completed(futures):
                puml_file, success, result = future.result()
                
                if success:
                    success_count += 1
                    status = "✓"
                else:
                    error_count += 1
                    status = "✗"
                    errors.append((puml_file, result))
                
                rel_path = puml_file.relative_to(args.source_dir) if args.source_dir in puml_file.parents else puml_file.name
                print(f"  [{status}] {rel_path}")
                
                if args.verbose and not success:
                    print(f"      Error: {result}")
    else:
        for item in work_items:
            puml_file, success, result = process_file(item)
            
            if success:
                success_count += 1
                status = "✓"
            else:
                error_count += 1
                status = "✗"
                errors.append((puml_file, result))
            
            rel_path = puml_file.relative_to(args.source_dir) if args.source_dir in puml_file.parents else puml_file.name
            print(f"  [{status}] {rel_path}")
            
            if args.verbose and not success:
                print(f"      Error: {result}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Generation complete!")
    print(f"  Success: {success_count}")
    print(f"  Errors:  {error_count}")
    
    if errors:
        print(f"\nFailed files:")
        for puml_file, error in errors:
            print(f"  - {puml_file.name}: {error}")
    
    sys.exit(0 if error_count == 0 else 1)


if __name__ == "__main__":
    main()

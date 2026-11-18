#!/usr/bin/env python3
"""
Smoke Tests for Python Examples
===============================
Verifies that all modules import and function minimally.

Course: Computer Networks - ASE Bucharest, CSIE
Author: ing. dr. Antonio Clim

Run:
    python test_smoke.py
    
Or with pytest:
    pytest test_smoke.py -v
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import os
import importlib.util
from pathlib import Path

# NOTE: Auto-detect the examples/ directory
SCRIPT_DIR = Path(__file__).parent
EXAMPLES_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "tests" else SCRIPT_DIR


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
SUBPROCESS_TIMEOUT: int = 10  # Timeout for import checks
SCRIPT_TIMEOUT: int = 30      # Timeout for full script execution
TEST_PORT: int = 8080         # Standard port for socket tests


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
def load_example(filename):
    path = EXAMPLES_DIR / filename
    assert path.is_file(), f"Required example is missing: {path}"
    name = 'compnet_smoke_' + path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    for exported in getattr(module, '__all__', []):
        assert hasattr(module, exported), f"{filename}: missing export {exported}"
    return module


def test_socket_tcp_imports() -> None:
    module = load_example('01_socket_tcp.py')
    assert callable(module.server) and callable(module.client)


def test_bytes_vs_str_imports() -> None:
    module = load_example('02_bytes_vs_str.py')
    assert module.ensure_bytes('hello') == b'hello'
    assert module.safe_decode(b'hello') == 'hello'


def test_struct_parsing_imports() -> None:
    module = load_example('03_struct_parsing.py')
    assert module.get_protocol_name(6) == 'TCP'


def test_error_handling_imports() -> None:
    module = load_example('04_error_handling.py')
    assert callable(module.connect_with_retry) and callable(module.recv_exactly)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
def test_bytes_demo_runs() -> None:
    """Run the bytes demonstration without errors."""
    script_path = EXAMPLES_DIR / "02_bytes_vs_str.py"
    assert script_path.is_file(), f"Required example is missing: {script_path}"
        
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Script failed: {result.stderr.decode()}"
    
    # Verify that output contains expected text
    output = result.stdout.decode().lower()
    assert "bytes" in output or "str" in output, "Output does not contain keywords"


def test_struct_parsing_runs() -> None:
    """Run the struct demonstration without errors."""
    script_path = EXAMPLES_DIR / "03_struct_parsing.py"
    assert script_path.is_file(), f"Required example is missing: {script_path}"
        
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Script failed: {result.stderr.decode()}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FUNCTIONALITY
# ═══════════════════════════════════════════════════════════════════════════════
def test_bytes_encoding() -> None:
    """Verify encoding/decoding bytes ↔ str."""
    text = "Hello, Networks!"
    encoded = text.encode('utf-8')
    decoded = encoded.decode('utf-8')
    
    assert isinstance(encoded, bytes), "encode() must return bytes"
    assert isinstance(decoded, str), "decode() must return str"
    assert text == decoded, "Roundtrip encoding must preserve text"


def test_struct_pack_unpack() -> None:
    """Verify struct pack/unpack for ports."""
    import struct
    
    # Pack
    port = 8080
    packed = struct.pack('!H', port)  # Network byte order, unsigned short
    
    assert len(packed) == 2, "Unsigned short must be 2 bytes"
    assert packed == b'\x1f\x90', f"8080 in big-endian = 0x1F90, got {packed.hex()}"
    
    # Unpack
    unpacked, = struct.unpack('!H', packed)
    assert unpacked == port, f"Unpack must return {port}, got {unpacked}"


def test_socket_creation() -> None:
    """Verify that we can create a TCP socket."""
    import socket
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.fileno() >= 0, "Socket must have valid file descriptor"
        
        # Verify options
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # If we reach here without exception, it's OK


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_all_tests() -> bool:
    """Run all tests and display results."""
    tests: list = [
        test_socket_tcp_imports,
        test_bytes_vs_str_imports,
        test_struct_parsing_imports,
        test_error_handling_imports,
        test_bytes_encoding,
        test_struct_pack_unpack,
        test_socket_creation,
        test_bytes_demo_runs,
        test_struct_parsing_runs,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("SMOKE TESTS - Python Networking Examples")
    print("=" * 60)
    
    for test in tests:
        try:
            test()
            print(f"✅ PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {test.__name__}")
            print(f"   Reason: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {test.__name__}")
            print(f"   Exception: {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULT: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

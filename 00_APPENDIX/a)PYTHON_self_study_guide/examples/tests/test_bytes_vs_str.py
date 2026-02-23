#!/usr/bin/env python3
"""
Unit Tests for 02_bytes_vs_str.py
=================================
Comprehensive tests for bytes and string conversion functions.

Course: Computer Networks — ASE Bucharest, CSIE
Version: 5.0 — January 2026

Run with:
    python -m pytest test_bytes_vs_str.py -v
    
Or standalone:
    python test_bytes_vs_str.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ═══════════════════════════════════════════════════════════════════════════════
# ENCODING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_encode_ascii() -> None:
    """Test encoding ASCII string to bytes."""
    text = "Hello"
    encoded = text.encode('utf-8')
    
    assert isinstance(encoded, bytes), "encode() must return bytes"
    assert encoded == b"Hello", "ASCII should encode identically"
    assert len(encoded) == 5, "ASCII characters are 1 byte each"


def test_encode_unicode() -> None:
    """Test encoding Unicode string to bytes."""
    text = "Café"
    encoded = text.encode('utf-8')
    
    assert isinstance(encoded, bytes), "encode() must return bytes"
    assert len(encoded) == 5, "é is 2 bytes in UTF-8"


def test_encode_emoji() -> None:
    """Test encoding emoji to bytes."""
    text = "🐍"
    encoded = text.encode('utf-8')
    
    assert isinstance(encoded, bytes), "encode() must return bytes"
    assert len(encoded) == 4, "Emoji is 4 bytes in UTF-8"


def test_encode_romanian() -> None:
    """Test encoding Romanian characters."""
    text = "București"
    encoded = text.encode('utf-8')
    
    assert isinstance(encoded, bytes), "encode() must return bytes"
    # ș is 2 bytes in UTF-8, others are 1 byte
    assert len(encoded) == 10, "București should be 10 bytes in UTF-8"


# ═══════════════════════════════════════════════════════════════════════════════
# DECODING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_decode_ascii() -> None:
    """Test decoding ASCII bytes to string."""
    data = b"Hello"
    decoded = data.decode('utf-8')
    
    assert isinstance(decoded, str), "decode() must return str"
    assert decoded == "Hello", "ASCII should decode identically"


def test_decode_unicode() -> None:
    """Test decoding Unicode bytes to string."""
    data = "Café".encode('utf-8')
    decoded = data.decode('utf-8')
    
    assert isinstance(decoded, str), "decode() must return str"
    assert decoded == "Café", "UTF-8 roundtrip must preserve text"


def test_decode_invalid_utf8_strict() -> None:
    """Test decoding invalid UTF-8 with strict error handling."""
    data = b"Hello \x80\x81 World"  # Invalid UTF-8 bytes
    
    try:
        data.decode('utf-8')
        assert False, "Should have raised UnicodeDecodeError"
    except UnicodeDecodeError:
        pass  # Expected behaviour


def test_decode_invalid_utf8_replace() -> None:
    """Test decoding invalid UTF-8 with replacement."""
    data = b"Hello \x80 World"
    decoded = data.decode('utf-8', errors='replace')
    
    assert isinstance(decoded, str), "decode() must return str"
    assert "Hello" in decoded, "Valid parts should be preserved"
    assert "World" in decoded, "Valid parts should be preserved"
    assert "�" in decoded, "Invalid bytes should become replacement character"


def test_decode_invalid_utf8_ignore() -> None:
    """Test decoding invalid UTF-8 with ignore."""
    data = b"Hello \x80 World"
    decoded = data.decode('utf-8', errors='ignore')
    
    assert isinstance(decoded, str), "decode() must return str"
    assert "Hello" in decoded, "Valid parts should be preserved"
    assert "World" in decoded, "Valid parts should be preserved"
    assert "\x80" not in decoded, "Invalid bytes should be removed"


# ═══════════════════════════════════════════════════════════════════════════════
# ROUNDTRIP TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_roundtrip_simple() -> None:
    """Test encoding then decoding preserves text."""
    original = "Hello, World!"
    
    encoded = original.encode('utf-8')
    decoded = encoded.decode('utf-8')
    
    assert decoded == original, "Roundtrip must preserve text"


def test_roundtrip_unicode() -> None:
    """Test roundtrip with Unicode characters."""
    original = "Привет мир 你好世界 مرحبا"
    
    encoded = original.encode('utf-8')
    decoded = encoded.decode('utf-8')
    
    assert decoded == original, "Unicode roundtrip must preserve text"


def test_roundtrip_all_bytes() -> None:
    """Test that latin-1 encoding handles all byte values."""
    # latin-1 is a 1-to-1 mapping for bytes 0-255
    original_bytes = bytes(range(256))
    
    text = original_bytes.decode('latin-1')
    recovered = text.encode('latin-1')
    
    assert recovered == original_bytes, "latin-1 roundtrip must preserve all bytes"


# ═══════════════════════════════════════════════════════════════════════════════
# BYTES LITERAL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_bytes_literal() -> None:
    """Test bytes literal syntax."""
    data = b"Hello"
    
    assert isinstance(data, bytes), "b'...' must create bytes"
    assert len(data) == 5, "Length should be 5"


def test_bytes_hex() -> None:
    """Test hex representation of bytes."""
    data = b"\x00\x01\x02\xff"
    
    assert data.hex() == "000102ff", "hex() should produce lowercase hex"
    assert bytes.fromhex("000102ff") == data, "fromhex() should reverse hex()"


def test_bytes_concatenation() -> None:
    """Test concatenating bytes."""
    part1 = b"Hello"
    part2 = b" "
    part3 = b"World"
    
    combined = part1 + part2 + part3
    
    assert combined == b"Hello World", "Bytes concatenation should work"


def test_bytes_immutable() -> None:
    """Test that bytes are immutable."""
    data = b"Hello"
    
    try:
        data[0] = 65  # Try to modify
        assert False, "Should have raised TypeError"
    except TypeError:
        pass  # Expected — bytes are immutable


# ═══════════════════════════════════════════════════════════════════════════════
# BYTEARRAY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_bytearray_mutable() -> None:
    """Test that bytearray is mutable."""
    data = bytearray(b"Hello")
    
    data[0] = ord('J')  # Change 'H' to 'J'
    
    assert data == bytearray(b"Jello"), "bytearray should be mutable"


def test_bytearray_from_int() -> None:
    """Test creating bytearray with size."""
    data = bytearray(10)
    
    assert len(data) == 10, "bytearray(n) should create n zero bytes"
    assert all(b == 0 for b in data), "All bytes should be zero"


# ═══════════════════════════════════════════════════════════════════════════════
# SOCKET-RELEVANT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_socket_send_requires_bytes() -> None:
    """Verify that str cannot be used where bytes are expected."""
    import socket
    
    # Create a socket (we will not actually send anything)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # This should work (bytes)
        # sock.sendall(b"Hello")  # Would need connection
        
        # Verify bytes are correct type
        data = b"Hello"
        assert isinstance(data, (bytes, bytearray)), "Must be bytes for socket"
        
        # Verify string is NOT correct type
        text = "Hello"
        assert not isinstance(text, (bytes, bytearray)), "str is not valid for socket"
        
    finally:
        sock.close()


def test_network_message_encoding() -> None:
    """Test encoding a typical network message."""
    # Typical HTTP-style message
    message = "GET / HTTP/1.0\r\n\r\n"
    
    encoded = message.encode('ascii')  # HTTP uses ASCII
    
    assert encoded == b"GET / HTTP/1.0\r\n\r\n"
    assert len(encoded) == len(message), "ASCII is 1 byte per character"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> bool:
    """Run all tests and display results."""
    tests = [
        # Encoding
        test_encode_ascii,
        test_encode_unicode,
        test_encode_emoji,
        test_encode_romanian,
        # Decoding
        test_decode_ascii,
        test_decode_unicode,
        test_decode_invalid_utf8_strict,
        test_decode_invalid_utf8_replace,
        test_decode_invalid_utf8_ignore,
        # Roundtrip
        test_roundtrip_simple,
        test_roundtrip_unicode,
        test_roundtrip_all_bytes,
        # Bytes literal
        test_bytes_literal,
        test_bytes_hex,
        test_bytes_concatenation,
        test_bytes_immutable,
        # Bytearray
        test_bytearray_mutable,
        test_bytearray_from_int,
        # Socket-relevant
        test_socket_send_requires_bytes,
        test_network_message_encoding,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("UNIT TESTS — Bytes vs Strings")
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
            print(f"   {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"RESULT: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

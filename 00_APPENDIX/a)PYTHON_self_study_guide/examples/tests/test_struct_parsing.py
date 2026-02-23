#!/usr/bin/env python3
"""
Unit Tests for 03_struct_parsing.py
===================================
Comprehensive tests for binary protocol parsing with struct.

Course: Computer Networks — ASE Bucharest, CSIE
Version: 5.0 — January 2026

Run with:
    python -m pytest test_struct_parsing.py -v
    
Or standalone:
    python test_struct_parsing.py
"""

import struct
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ═══════════════════════════════════════════════════════════════════════════════
# BASIC PACK/UNPACK TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_pack_unsigned_byte() -> None:
    """Test packing an unsigned byte."""
    packed = struct.pack('!B', 255)
    
    assert packed == b'\xff', "255 should pack to 0xFF"
    assert len(packed) == 1, "Unsigned byte is 1 byte"


def test_pack_unsigned_short() -> None:
    """Test packing an unsigned short (port number)."""
    port = 8080
    packed = struct.pack('!H', port)
    
    assert len(packed) == 2, "Unsigned short is 2 bytes"
    assert packed == b'\x1f\x90', "8080 in big-endian is 0x1F90"


def test_pack_unsigned_int() -> None:
    """Test packing an unsigned int (IPv4 address)."""
    # 192.168.1.1 as integer
    ip_int = (192 << 24) | (168 << 16) | (1 << 8) | 1
    packed = struct.pack('!I', ip_int)
    
    assert len(packed) == 4, "Unsigned int is 4 bytes"
    assert packed == b'\xc0\xa8\x01\x01', "192.168.1.1 packed correctly"


def test_pack_unsigned_long_long() -> None:
    """Test packing an unsigned long long."""
    value = 2**63
    packed = struct.pack('!Q', value)
    
    assert len(packed) == 8, "Unsigned long long is 8 bytes"


def test_unpack_returns_tuple() -> None:
    """Test that unpack always returns a tuple."""
    packed = struct.pack('!H', 8080)
    unpacked = struct.unpack('!H', packed)
    
    assert isinstance(unpacked, tuple), "unpack() returns tuple"
    assert len(unpacked) == 1, "Single value gives single-element tuple"
    assert unpacked[0] == 8080, "Value should be 8080"


def test_unpack_with_trailing_comma() -> None:
    """Test unpacking with trailing comma idiom."""
    packed = struct.pack('!H', 8080)
    value, = struct.unpack('!H', packed)  # Note the trailing comma
    
    assert isinstance(value, int), "With comma, get int directly"
    assert value == 8080, "Value should be 8080"


# ═══════════════════════════════════════════════════════════════════════════════
# BYTE ORDER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_network_byte_order() -> None:
    """Test that '!' gives network (big-endian) byte order."""
    value = 0x1234
    
    packed_network = struct.pack('!H', value)
    packed_big = struct.pack('>H', value)
    
    assert packed_network == packed_big, "! should equal > (big-endian)"
    assert packed_network == b'\x12\x34', "Big-endian: high byte first"


def test_little_endian() -> None:
    """Test little-endian byte order."""
    value = 0x1234
    
    packed_little = struct.pack('<H', value)
    
    assert packed_little == b'\x34\x12', "Little-endian: low byte first"


def test_native_byte_order() -> None:
    """Test native byte order (platform-dependent)."""
    value = 0x1234
    
    # Native order may be little or big depending on platform
    packed_native = struct.pack('=H', value)
    
    assert len(packed_native) == 2, "Should still be 2 bytes"


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT STRING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_calcsize() -> None:
    """Test calculating format size."""
    assert struct.calcsize('!B') == 1, "Byte is 1"
    assert struct.calcsize('!H') == 2, "Short is 2"
    assert struct.calcsize('!I') == 4, "Int is 4"
    assert struct.calcsize('!Q') == 8, "Long long is 8"
    assert struct.calcsize('!BHI') == 7, "B+H+I = 1+2+4 = 7"


def test_multiple_values() -> None:
    """Test packing multiple values."""
    version = 1
    flags = 3
    length = 100
    
    packed = struct.pack('!BBH', version, flags, length)
    
    assert len(packed) == 4, "BBH = 1+1+2 = 4 bytes"
    
    v, f, l = struct.unpack('!BBH', packed)
    
    assert v == version, "Version preserved"
    assert f == flags, "Flags preserved"
    assert l == length, "Length preserved"


def test_signed_vs_unsigned() -> None:
    """Test signed vs unsigned formats."""
    # Unsigned byte: 0-255
    # Signed byte: -128 to 127
    
    packed_unsigned = struct.pack('!B', 200)
    packed_signed = struct.pack('!b', -56)  # -56 has same bits as 200
    
    # Both should have same bytes
    assert packed_unsigned == packed_signed, "200 unsigned = -56 signed"
    
    # But unpack gives different values
    unsigned_val, = struct.unpack('!B', packed_unsigned)
    signed_val, = struct.unpack('!b', packed_signed)
    
    assert unsigned_val == 200, "Unsigned interpretation"
    assert signed_val == -56, "Signed interpretation"


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL HEADER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_simple_header() -> None:
    """Test parsing a simple protocol header."""
    # Header: version (1B), type (1B), length (2B)
    header_data = b'\x01\x02\x00\x64'  # v1, type2, length100
    
    version, msg_type, length = struct.unpack('!BBH', header_data)
    
    assert version == 1, "Version should be 1"
    assert msg_type == 2, "Type should be 2"
    assert length == 100, "Length should be 100"


def test_ip_header_fragment() -> None:
    """Test parsing part of an IP header."""
    # Simplified: version_ihl (1B), tos (1B), total_length (2B)
    ip_fragment = b'\x45\x00\x00\x3c'  # IPv4, IHL=5, TOS=0, Length=60
    
    version_ihl, tos, total_length = struct.unpack('!BBH', ip_fragment)
    
    version = version_ihl >> 4
    ihl = version_ihl & 0x0F
    
    assert version == 4, "IP version should be 4"
    assert ihl == 5, "IHL should be 5 (20 bytes)"
    assert tos == 0, "TOS should be 0"
    assert total_length == 60, "Total length should be 60"


def test_length_prefixed_message() -> None:
    """Test building and parsing length-prefixed message."""
    payload = b"Hello, World!"
    
    # Build: 4-byte length prefix + payload
    header = struct.pack('!I', len(payload))
    message = header + payload
    
    assert len(message) == 4 + len(payload), "Message = header + payload"
    
    # Parse
    length, = struct.unpack('!I', message[:4])
    recovered_payload = message[4:4 + length]
    
    assert length == len(payload), "Length should match"
    assert recovered_payload == payload, "Payload should match"


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_unpack_wrong_size() -> None:
    """Test unpacking with wrong buffer size."""
    try:
        struct.unpack('!I', b'\x00\x00\x00')  # 3 bytes, need 4
        assert False, "Should have raised struct.error"
    except struct.error:
        pass  # Expected


def test_pack_value_out_of_range() -> None:
    """Test packing value outside valid range."""
    try:
        struct.pack('!B', 256)  # Max for unsigned byte is 255
        assert False, "Should have raised struct.error"
    except struct.error:
        pass  # Expected


def test_pack_negative_unsigned() -> None:
    """Test packing negative value in unsigned format."""
    try:
        struct.pack('!B', -1)  # Unsigned cannot be negative
        assert False, "Should have raised struct.error"
    except struct.error:
        pass  # Expected


# ═══════════════════════════════════════════════════════════════════════════════
# PRACTICAL EXAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

def test_port_number() -> None:
    """Test common port number conversions."""
    ports = [80, 443, 8080, 22, 53]
    
    for port in ports:
        packed = struct.pack('!H', port)
        unpacked, = struct.unpack('!H', packed)
        assert unpacked == port, f"Port {port} roundtrip failed"


def test_ipv4_address() -> None:
    """Test IPv4 address as 4 bytes."""
    # 192.168.1.100
    octets = (192, 168, 1, 100)
    
    packed = struct.pack('!BBBB', *octets)
    
    assert packed == b'\xc0\xa8\x01\x64', "IPv4 packed correctly"
    
    # Also works as single 32-bit int
    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
    packed_int = struct.pack('!I', ip_int)
    
    assert packed == packed_int, "Both methods give same result"


def test_timestamp_64bit() -> None:
    """Test 64-bit timestamp (like in NTP)."""
    import time
    
    timestamp = int(time.time())
    
    packed = struct.pack('!Q', timestamp)
    unpacked, = struct.unpack('!Q', packed)
    
    assert unpacked == timestamp, "Timestamp preserved"
    assert len(packed) == 8, "64-bit timestamp is 8 bytes"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> bool:
    """Run all tests and display results."""
    tests = [
        # Basic
        test_pack_unsigned_byte,
        test_pack_unsigned_short,
        test_pack_unsigned_int,
        test_pack_unsigned_long_long,
        test_unpack_returns_tuple,
        test_unpack_with_trailing_comma,
        # Byte order
        test_network_byte_order,
        test_little_endian,
        test_native_byte_order,
        # Format string
        test_calcsize,
        test_multiple_values,
        test_signed_vs_unsigned,
        # Protocol headers
        test_simple_header,
        test_ip_header_fragment,
        test_length_prefixed_message,
        # Error handling
        test_unpack_wrong_size,
        test_pack_value_out_of_range,
        test_pack_negative_unsigned,
        # Practical
        test_port_number,
        test_ipv4_address,
        test_timestamp_64bit,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("UNIT TESTS — Struct Parsing")
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

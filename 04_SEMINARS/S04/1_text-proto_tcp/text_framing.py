"""Length framing for S04: ASCII TOTAL_BYTES, space, then UTF-8 payload.

TOTAL_BYTES includes the header and separator. Maximum complete frame: 65536 bytes.
The receiver reads exact lengths, so split and coalesced TCP writes are equivalent.
"""
MAX_FRAME = 65536


def encode_frame(payload: str) -> bytes:
    body = payload.encode("utf-8")
    size = len(body) + 2
    while True:
        actual = len(str(size)) + 1 + len(body)
        if actual == size:
            break
        size = actual
    if size > MAX_FRAME:
        raise ValueError("Frame exceeds 65536 bytes")
    return str(size).encode("ascii") + b" " + body


def read_frame(sock):
    header = bytearray()
    while True:
        part = sock.recv(1)
        if not part:
            if not header:
                return None
            raise EOFError("Incomplete length header")
        if part == b" ":
            break
        if part not in b"0123456789" or len(header) >= 5:
            raise ValueError("Invalid length header")
        header.extend(part)
    if not header or (len(header) > 1 and header[0] == ord("0")):
        raise ValueError("Invalid length header")
    size = int(header)
    remaining = size - len(header) - 1
    if remaining < 0 or size > MAX_FRAME:
        raise ValueError("Invalid frame length")
    data = bytearray(header + b" ")
    while remaining:
        part = sock.recv(min(remaining, 4096))
        if not part:
            raise EOFError("Incomplete frame payload")
        data.extend(part)
        remaining -= len(part)
    return bytes(data)

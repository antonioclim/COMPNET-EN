"""Read/write the S04 one-byte total-length frame (2..255 bytes)."""
def encode_frame(payload: bytes) -> bytes:
    if not 1 <= len(payload) <= 254:
        raise ValueError("Pickled payload must fit in 254 bytes; shorten it")
    return bytes([len(payload) + 1]) + payload


def read_frame(sock):
    header = sock.recv(1)
    if not header:
        return None
    if header[0] < 2:
        raise ValueError("Invalid total frame length")
    remaining = header[0] - 1
    data = bytearray(header)
    while remaining:
        part = sock.recv(min(remaining, 4096))
        if not part:
            raise EOFError("Incomplete binary frame")
        data.extend(part)
        remaining -= len(part)
    return bytes(data)

"""Explicit framing shared by the local pseudo-FTP demonstration."""
from pathlib import Path


def read_exact(sock, size):
    data = bytearray()
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            raise EOFError("Connection ended inside a frame")
        data.extend(part)
    return bytes(data)


def read_line(sock, limit=1024):
    data = bytearray()
    while len(data) <= limit:
        part = sock.recv(1)
        if not part:
            if not data:
                return None
            raise EOFError("Incomplete control line")
        if part == b"\n":
            return bytes(data)
        data.extend(part)
    raise ValueError("Control line too long")


def send_reply(sock, text):
    payload = text.encode("utf-8")
    if len(payload) > 65536:
        raise ValueError("Control reply too large")
    sock.sendall(str(len(payload)).encode("ascii") + b"\n" + payload)


def read_reply(sock):
    header = read_line(sock, 5)
    if header is None or not header.isdigit() or int(header) > 65536:
        raise ValueError("Invalid control reply length")
    return read_exact(sock, int(header)).decode("utf-8")


def send_file(sock, content):
    if len(content) > 255:
        raise ValueError("This demonstration limits file content to 255 bytes")
    sock.sendall(bytes([len(content)]) + content)


def read_file(sock):
    return read_exact(sock, read_exact(sock, 1)[0])


def local_path(root, filename):
    """This exercise accepts one filename, never a directory or traversal path."""
    if not filename or filename in {".", ".."} or "/" in filename or "\\" in filename:
        raise ValueError("Use a filename without directories")
    root_path = Path(root).resolve()
    target = (root_path / filename).resolve()
    if target.parent != root_path:
        raise ValueError("File is outside the exercise directory")
    return target

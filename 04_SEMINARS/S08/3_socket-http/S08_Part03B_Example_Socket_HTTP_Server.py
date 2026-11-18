#!/usr/bin/env python3
import socket
import sys
import os
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit

"""
Seminar 8 -- Minimal HTTP server implemented manually with sockets.

This server:
 - listens on a given port (e.g. 8000)
 - receives HTTP requests (GET)
 - parses the first line of the request
 - determines which file to serve from the "static/" directory
 - returns valid HTTP responses:
      - 200 OK with the requested file
      - 404 Not Found if the file does not exist

The student must complete the areas marked with:
    # >>> STUDENT TODO
"""

BUFFER_SIZE = 4096
STATIC_DIR = str(Path(__file__).resolve().parent / "static")
MAX_HEADERS = 16384


def build_http_response(status_code, content, content_type="text/plain"):
    """
    Build a complete HTTP response as bytes.
    """

    reasons = {200: "OK", 400: "Bad Request", 403: "Forbidden", 404: "Not Found",
               405: "Method Not Allowed", 408: "Request Timeout",
               431: "Request Header Fields Too Large", 500: "Internal Server Error"}
    status_line = f"HTTP/1.1 {status_code} {reasons[status_code]}"
    if isinstance(content, str):
        content = content.encode("utf-8")

    headers = [
        f"Content-Type: {content_type}",
        f"Content-Length: {len(content)}",
        "Connection: close"
    ]

    header_block = "\r\n".join(headers)
    response = f"{status_line}\r\n{header_block}\r\n\r\n".encode("utf-8") + content
    return response


def handle_client(conn):
    """One bounded GET request per connection; no request body or persistent HTTP."""
    try:
        conn.settimeout(5)
        data = bytearray()
        while b"\r\n\r\n" not in data:
            part = conn.recv(min(BUFFER_SIZE, MAX_HEADERS + 1 - len(data)))
            if not part:
                if data:
                    conn.sendall(build_http_response(400, b"Incomplete request headers"))
                return
            data.extend(part)
            if len(data) > MAX_HEADERS:
                conn.sendall(build_http_response(431, b"Headers too large"))
                return
        try:
            line = bytes(data).split(b"\r\n", 1)[0].decode("ascii")
            method, target, version = line.split(" ")
            if version not in {"HTTP/1.0", "HTTP/1.1"}:
                raise ValueError("Unsupported HTTP version")
            if not target.startswith("/") or target.startswith("//"):
                raise ValueError("Expected an origin-form request target")
            parsed = urlsplit(target)
            path = unquote(parsed.path, errors="strict")
            if parsed.fragment or "\x00" in path or "\\" in path:
                raise ValueError("Invalid request target")
        except (ValueError, UnicodeError):
            conn.sendall(build_http_response(400, b"Invalid request line"))
            return
        if method != "GET":
            response = build_http_response(405, b"This teaching server supports GET only")
            response = response.replace(b"Connection: close", b"Allow: GET\r\nConnection: close", 1)
            conn.sendall(response)
            return
        if path in {"/", "/index.html"}:
            path = "/S08_Part03_Page_Index.html"
        root = Path(STATIC_DIR).resolve()
        candidate = (root / path.lstrip("/")).resolve()
        if not candidate.is_relative_to(root):
            conn.sendall(build_http_response(403, b"Path is outside the static directory"))
            return
        if not candidate.is_file():
            # >>> STUDENT TODO: customise the 404 page, preserving its byte length.
            conn.sendall(build_http_response(404, b"<h1>404 Not Found</h1>", "text/html"))
            return
        content = candidate.read_bytes()
        mime_type = mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"
        # >>> STUDENT TODO: add a suitable extra response header and inspect it.
        conn.sendall(build_http_response(200, content, mime_type))
    except socket.timeout:
        try:
            conn.sendall(build_http_response(408, b"Request timed out"))
        except OSError:
            pass
    except (OSError, ValueError):
        try:
            conn.sendall(build_http_response(500, b"Internal server error"))
        except OSError:
            pass
    finally:
        conn.close()


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {os.path.basename(sys.argv[0])} <port>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", PORT))
        s.listen(5)

        print(f"Manual HTTP server started on port {PORT}")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                conn, addr = s.accept()
                handle_client(conn)
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()

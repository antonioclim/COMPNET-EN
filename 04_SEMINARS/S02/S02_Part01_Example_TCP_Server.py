"""S02 – Example TCP server

This script provides a minimal TCP server implemented with Python's `socketserver` module.

Key properties:
- It listens on 127.0.0.1:12345.
- It accepts multiple clients concurrently (thread per connection).
- It exchanges repeated UTF-8 lines (LF delimiter, at most 1024 bytes per line).
- It replies with the uppercase variant and an LF delimiter.

This file is intended as a reference implementation for the seminar tasks.
"""

import socketserver


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """A TCPServer that spawns a thread for each client."""
    daemon_threads = True
    allow_reuse_address = True


class TCPRequestHandler(socketserver.StreamRequestHandler):
    """Handles a single TCP client connection."""

    def handle(self):
        while True:
            data = self.rfile.readline(1025)
            if not data:
                return
            if len(data) > 1024 or not data.endswith(b"\n"):
                self.wfile.write(b"ERR line must end in LF and fit in 1024 bytes\n")
                return
            message = data[:-1].removesuffix(b"\r").decode("utf-8", errors="replace")
            print(f"[SERVER] Received from {self.client_address}: {message}")
            self.wfile.write(message.upper().encode("utf-8") + b"\n")


def main():
    host = "127.0.0.1"
    port = 12345

    with ThreadedTCPServer((host, port), TCPRequestHandler) as server:
        print(f"[INFO] TCP server listening on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    main()

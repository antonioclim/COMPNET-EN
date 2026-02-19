"""S02 – Example TCP server

This script provides a minimal TCP server implemented with Python's `socketserver` module.

Key properties:
- It listens on 127.0.0.1:12345.
- It accepts multiple clients concurrently (thread per connection).
- It receives a message, prints it and replies with the uppercase variant.

This file is intended as a reference implementation for the seminar tasks.
"""

import socketserver


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """A TCPServer that spawns a thread for each client."""
    daemon_threads = True
    allow_reuse_address = True


class TCPRequestHandler(socketserver.BaseRequestHandler):
    """Handles a single TCP client connection."""

    def handle(self):
        # Receive data from the client
        data = self.request.recv(1024)
        if not data:
            return

        # Decode for logging (the protocol itself is byte-based)
        message = data.decode(errors="replace").strip()

        print(f"[SERVER] Received from {self.client_address}: {message}")

        # Send a response
        response = message.upper().encode()
        self.request.sendall(response)


def main():
    host = "127.0.0.1"
    port = 12345

    with ThreadedTCPServer((host, port), TCPRequestHandler) as server:
        print(f"[INFO] TCP server listening on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    main()

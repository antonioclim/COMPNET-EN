#!/usr/bin/env python3
import http.server
import socketserver
import json
import time
import sys

"""
Seminar 8 -- Minimal HTTP server using the Python standard library.

This server:

 - serves files from the current directory
 - responds with plain text at /hello
 - responds with JSON at /api/time
 - supports GET (sufficient for the laboratory)

Test:
    python3 simple_http_builtin.py 8000

Then:
    curl -v http://localhost:8000/
    curl -v http://localhost:8000/hello
    curl -v http://localhost:8000/api/time
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that extends SimpleHTTPRequestHandler."""

    def do_GET(self):
        """
        Override the do_GET method to handle custom endpoints.
        If the endpoint is not recognised, we call the standard handler
        which serves files from the current directory.
        """
        if self.path == "/hello":
            # Plain text response
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Hello! You have reached /hello.\n")
            return

        elif self.path == "/api/time":
            # JSON response with timestamp
            content = {
                "timestamp": time.time(),
                "readable": time.ctime()
            }
            body = json.dumps(content).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # If it is not a custom endpoint, use the standard behaviour
        return super().do_GET()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 simple_http_builtin.py <port>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    handler = MyHandler
    socketserver.TCPServer.allow_reuse_address = True

    print(f"Starting server on port {PORT}...")

    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        try:
            print("Server started. Press Ctrl+C to stop.")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            httpd.server_close()


if __name__ == "__main__":
    main()

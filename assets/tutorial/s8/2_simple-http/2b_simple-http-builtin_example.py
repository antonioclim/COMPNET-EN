#!/usr/bin/env python3
import http.server
import socketserver
import json
import time
import sys

"""
Seminar 8 – Server HTTP minimal folosind biblioteca standard Python.

Acest server:

 - servește fișiere din directorul curent
 - răspunde cu text simplu la /hello
 - răspunde cu JSON la /api/time
 - suportă GET (suficient pentru laborator)

Test:
    python3 simple_http_builtin.py 8000

Apoi:
    curl -v http://localhost:8000/
    curl -v http://localhost:8000/hello
    curl -v http://localhost:8000/api/time
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizat care extinde SimpleHTTPRequestHandler."""

    def do_GET(self):
        """
        Suprascriem metoda do_GET pentru a trata endpoint-uri custom.
        Dacă endpoint-ul nu este recunoscut, apelăm handlerul standard
        care servește fișiere din directorul curent.
        """
        if self.path == "/hello":
            # Răspuns text simplu
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Salut! Ai ajuns la /hello.\n")
            return

        elif self.path == "/api/time":
            # Răspuns JSON cu timestamp
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

        # Dacă nu e endpoint custom, folosim comportamentul standard
        return super().do_GET()


def main():
    if len(sys.argv) < 2:
        print("Utilizare: python3 simple_http_builtin.py <port>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    handler = MyHandler
    socketserver.TCPServer.allow_reuse_address = True

    print(f"Pornim serverul pe portul {PORT}...")

    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        try:
            print("Server pornit. Ctrl+C pentru oprire.")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nOprire server...")
        finally:
            httpd.server_close()


if __name__ == "__main__":
    main()
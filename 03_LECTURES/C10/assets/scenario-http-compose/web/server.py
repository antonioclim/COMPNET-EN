from __future__ import annotations

import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("X-Debug-Web", "python-simplehttp")
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"web serving on :{PORT}")
    httpd.serve_forever()

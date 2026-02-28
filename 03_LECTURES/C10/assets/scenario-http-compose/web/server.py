from __future__ import annotations

import http.server
import os
import socketserver

PORT = 8000
WEB_INSTANCE = os.environ.get("WEB_INSTANCE", "web").strip() or "web"


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Debug headers help students see which component generated which response.
        self.send_header("X-Debug-Web", "python-simplehttp")
        self.send_header("X-Web-Instance", WEB_INSTANCE)
        super().end_headers()


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"web serving on :{PORT} (instance={WEB_INSTANCE})")
    httpd.serve_forever()

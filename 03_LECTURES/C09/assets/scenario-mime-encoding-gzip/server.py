import gzip
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8089

FILES = {
  "/": ("index.html", "text/html; charset=utf-8"),
  "/data.json": ("data.json", "application/json; charset=utf-8"),
}

class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path not in FILES:
      self.send_response(404)
      self.send_header("Content-Type", "text/plain; charset=utf-8")
      self.end_headers()
      self.wfile.write(b"404\n")
      return

    filename, content_type = FILES[self.path]
    with open(filename, "rb") as f:
      body = f.read()

    accept_encoding = self.headers.get("Accept-Encoding", "")
    use_gzip = "gzip" in accept_encoding.lower()

    self.send_response(200)
    self.send_header("Content-Type", content_type)

    if use_gzip:
      body = gzip.compress(body, compresslevel=6)
      self.send_header("Content-Encoding", "gzip")

    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def log_message(self, format, *args):
    return

def main():
  httpd = HTTPServer((HOST, PORT), Handler)
  print(f"[server] http://{HOST}:{PORT}")
  httpd.serve_forever()

if __name__ == "__main__":
  main()

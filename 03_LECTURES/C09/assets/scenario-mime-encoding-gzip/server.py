import gzip
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8089

FILES = {
  "/": ("index.html", "text/html; charset=utf-8"),
  "/data.json": ("data.json", "application/json; charset=utf-8"),
}

def encoding_quality(header, coding):
  values = {}
  for part in header.split(","):
    fields = [field.strip() for field in part.split(";")]
    if not fields[0]:
      continue
    quality = 1.0
    for parameter in fields[1:]:
      if parameter.lower().startswith("q="):
        try:
          quality = float(parameter[2:])
        except ValueError:
          quality = 0.0
    values[fields[0].lower()] = quality if 0 <= quality <= 1 else 0.0
  if coding in values:
    return values[coding]
  if coding == "identity":
    return 0.0 if values.get("*") == 0 else 1.0
  return values.get("*", 0.0)

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
    gzip_q = encoding_quality(accept_encoding, "gzip")
    identity_q = encoding_quality(accept_encoding, "identity")
    use_gzip = gzip_q > 0 and gzip_q >= identity_q
    if not use_gzip and identity_q == 0:
      self.send_error(406, "No acceptable representation coding")
      return

    self.send_response(200)
    self.send_header("Content-Type", content_type)
    self.send_header("Vary", "Accept-Encoding")

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

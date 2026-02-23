from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8090

TEXT = "Hello, world. Characters: café naïve über"
BODY_UTF8 = (TEXT + "\n").encode("utf-8")

class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/ok":
      self.send_response(200)
      self.send_header("Content-Type", "text/plain; charset=utf-8")
      self.send_header("Content-Length", str(len(BODY_UTF8)))
      self.end_headers()
      self.wfile.write(BODY_UTF8)
      return

    if self.path == "/bad":
      # Intentional: body is UTF-8, but the declared charset is wrong
      self.send_response(200)
      self.send_header("Content-Type", "text/plain; charset=iso-8859-1")
      self.send_header("Content-Length", str(len(BODY_UTF8)))
      self.end_headers()
      self.wfile.write(BODY_UTF8)
      return

    self.send_response(404)
    self.send_header("Content-Type", "text/plain; charset=utf-8")
    self.end_headers()
    self.wfile.write(b"404\n")

  def log_message(self, format, *args):
    return

def main():
  httpd = HTTPServer((HOST, PORT), Handler)
  print(f"[server] http://{HOST}:{PORT}")
  print("[server] endpoints: /ok and /bad")
  httpd.serve_forever()

if __name__ == "__main__":
  main()

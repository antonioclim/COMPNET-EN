from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler)
    print("HTTP server: http://127.0.0.1:8000 (CTRL+C to stop)")
    server.serve_forever()

if __name__ == "__main__":
    main()

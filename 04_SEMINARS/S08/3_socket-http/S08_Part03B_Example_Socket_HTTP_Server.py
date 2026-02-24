#!/usr/bin/env python3
import socket
import sys
import os
import mimetypes

"""
Seminar 8 -- Minimal HTTP server implemented manually with sockets.

This server:
 - listens on a given port (e.g. 8000)
 - receives HTTP requests (GET)
 - parses the first line of the request
 - determines which file to serve from the "static/" directory
 - returns valid HTTP responses:
      - 200 OK with the requested file
      - 404 Not Found if the file does not exist

The student must complete the areas marked with:
    # >>> STUDENT TODO
"""

BUFFER_SIZE = 4096
STATIC_DIR = "static"


def build_http_response(status_code, content, content_type="text/plain"):
    """
    Build a complete HTTP response as bytes.
    """

    if status_code == 200:
        status_line = "HTTP/1.1 200 OK"
    elif status_code == 404:
        status_line = "HTTP/1.1 404 Not Found"
    else:
        status_line = "HTTP/1.1 500 Internal Server Error"

    headers = [
        f"Content-Type: {content_type}",
        f"Content-Length: {len(content)}",
        "Connection: close"
    ]

    header_block = "\r\n".join(headers)
    response = f"{status_line}\r\n{header_block}\r\n\r\n".encode("utf-8") + content
    return response


def handle_client(conn):
    """
    Receive the request, parse the first line, determine the requested file
    and return the appropriate HTTP response.
    """
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            return

        request_text = data.decode("utf-8", errors="replace")

        # First request line (e.g. "GET /index.html HTTP/1.1")
        first_line = request_text.split("\r\n")[0]

        # >>> STUDENT TODO
        # Parse the first line and extract the method and path.
        # If something is invalid, return 400 Bad Request (optional).
        #
        # Example:
        #   method, path, _ = first_line.split(" ")
        #

        try:
            method, path, _ = first_line.split(" ")
        except ValueError:
            # invalid request
            response = build_http_response(500, b"Error parsing request")
            conn.sendall(response)
            return

        if method != "GET":
            response = build_http_response(500, b"Only GET is supported")
            conn.sendall(response)
            return

        # The path "/" must be mapped to the main page in the `static/` directory.
        if path == "/":
            path = "/S08_Part03_Page_Index.html"

        # Compatibility: if the browser explicitly requests /index.html, serve the same main page.
        if path == "/index.html":
            path = "/S08_Part03_Page_Index.html"
        # Build the real path to the static file
        # remove any ".." for safety
        safe_path = os.path.normpath(path).lstrip("/")
        file_path = os.path.join(STATIC_DIR, safe_path)

        if not os.path.isfile(file_path):
            # >>> STUDENT TODO
            # Return a 404 Not Found response with a simple HTML message
            not_found_body = b"<h1>404 Not Found</h1>"
            response = build_http_response(404, not_found_body, "text/html")
            conn.sendall(response)
            return

        # If the file exists, read it
        with open(file_path, "rb") as f:
            content = f.read()

        # Determine the MIME type (optional)
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        # >>> STUDENT TODO
        # Return a 200 response with the file contents
        response = build_http_response(200, content, mime_type)
        conn.sendall(response)

    except Exception as e:
        error_msg = f"Internal error: {e}".encode("utf-8")
        response = build_http_response(500, error_msg, "text/plain")
        conn.sendall(response)

    finally:
        conn.close()


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {os.path.basename(sys.argv[0])} <port>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", PORT))
        s.listen(5)

        print(f"Manual HTTP server started on port {PORT}")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                conn, addr = s.accept()
                handle_client(conn)
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()

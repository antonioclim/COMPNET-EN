#!/usr/bin/env python3
import socket
import sys
import os
import mimetypes

"""
Seminar 8 – Server HTTP minimal implementat manual cu socket-uri.

Acest server:
 - ascultă pe un port dat (ex: 8000)
 - primește request-uri HTTP (GET)
 - parsează prima linie a request-ului
 - determină ce fișier trebuie servit din directorul "static/"
 - întoarce răspunsuri HTTP valide:
      - 200 OK cu fișierul cerut
      - 404 Not Found dacă fișierul nu există

Studentul trebuie să completeze zonele marcate cu:
    # >>> STUDENT TODO
"""

BUFFER_SIZE = 4096
STATIC_DIR = "static"


def build_http_response(status_code, content, content_type="text/plain"):
    """
    Construieste un raspuns HTTP complet, ca bytes.
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
    Preia request-ul, parseaza prima linie, determina fisierul cerut,
    si intoarce raspunsul HTTP potrivit.
    """
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            return

        request_text = data.decode("utf-8", errors="replace")

        # Prima linie de request (ex: "GET /index.html HTTP/1.1")
        first_line = request_text.split("\r\n")[0]

        # >>> STUDENT TODO
        # Parsati prima linie si extrageti metoda si path-ul.
        # Daca ceva nu e valid, intoarceti 400 Bad Request (optional).
        #
        # Exemplu:
        #   method, path, _ = first_line.split(" ")
        #

        try:
            method, path, _ = first_line.split(" ")
        except ValueError:
            # request invalid
            response = build_http_response(500, b"Eroare parsing request")
            conn.sendall(response)
            return

        if method != "GET":
            response = build_http_response(500, b"Doar GET este suportat")
            conn.sendall(response)
            return

        # Path-ul "/" trebuie mapat la "/index.html"
        if path == "/":
            path = "/index.html"

        # Construim calea reala spre fisierul static
        # eliminam eventuale ".." pentru siguranta
        safe_path = os.path.normpath(path).lstrip("/")
        file_path = os.path.join(STATIC_DIR, safe_path)

        if not os.path.isfile(file_path):
            # >>> STUDENT TODO
            # Intoarceti un raspuns 404 Not Found cu un mesaj simplu HTML
            not_found_body = b"<h1>404 Not Found</h1>"
            response = build_http_response(404, not_found_body, "text/html")
            conn.sendall(response)
            return

        # Daca exista fisierul, il citim
        with open(file_path, "rb") as f:
            content = f.read()

        # Determinam MIME type-ul (optional)
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        # >>> STUDENT TODO
        # Intoarceti un raspuns 200 cu continutul fisierului
        response = build_http_response(200, content, mime_type)
        conn.sendall(response)

    except Exception as e:
        error_msg = f"Eroare interna: {e}".encode("utf-8")
        response = build_http_response(500, error_msg, "text/plain")
        conn.sendall(response)

    finally:
        conn.close()


def main():
    if len(sys.argv) < 2:
        print("Utilizare: python3 socket_http_server.py <port>")
        sys.exit(1)

    PORT = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", PORT))
        s.listen(5)

        print(f"Server HTTP manual pornit pe portul {PORT}")
        print("Ctrl+C pentru oprire.")

        try:
            while True:
                conn, addr = s.accept()
                handle_client(conn)
        except KeyboardInterrupt:
            print("\nServer oprit.")


if __name__ == "__main__":
    main()

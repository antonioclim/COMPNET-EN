"""One-connection echo target for the TCP half-close exercise."""
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("--listen", default="127.0.0.1:8080")
args = parser.parse_args()
host, port = args.listen.rsplit(":", 1)
with socket.create_server((host, int(port))) as server:
    conn, address = server.accept()
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            conn.sendall(data)

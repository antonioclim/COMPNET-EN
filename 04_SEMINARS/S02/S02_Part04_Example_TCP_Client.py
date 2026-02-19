"""S02 – Example TCP client

This script connects to the TCP server from `S02_Part01_Example_TCP_Server.py`,
sends a single message and prints the reply.

It is a minimal reference client for the seminar tasks.
"""

import socket


def main():
    host = "127.0.0.1"
    port = 12345
    message = "Hello, world"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(message.encode())

        data = sock.recv(1024)

    print(f"[CLIENT] Sent: {message}")
    print(f"[CLIENT] Received: {data.decode(errors='replace')}")


if __name__ == "__main__":
    main()

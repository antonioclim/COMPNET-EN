"""S02 – Example UDP server

A very simple UDP echo server that converts the received message to uppercase.

Key properties:
- Uses UDP (connectionless)
- Receives datagrams from any number of clients
- Replies to each client with the same message, but uppercased

Usage:
    python3 S02_Part07_Example_UDP_Server.py <PORT>
"""

import socket
import sys


def main():
    # Validate command-line arguments.
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    # sys.argv[1] is a string → convert it to int.
    port = int(sys.argv[1])

    # Create a UDP socket:
    # - AF_INET   → IPv4
    # - SOCK_DGRAM → UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # bind(('', port)) means:
        # - ''   → all interfaces (0.0.0.0)
        # - port → the port on which the server listens
        server_socket.bind(("", port))

        print(f"[INFO] UDP server listening on 0.0.0.0:{port}")

        # Infinite loop: wait for client datagrams.
        while True:
            # recvfrom(1024) returns:
            # - up to 1024 bytes from a single UDP datagram
            # - the sender address (ip, port)
            message, address = server_socket.recvfrom(1024)

            # Debug output in the server:
            client_ip, client_port = address
            print(f"[INFO] Received {len(message)} bytes from {client_ip}:{client_port}")
            print(f"       Raw message: {message!r}")

            # Prepare the reply: uppercase the message.
            response = message.upper()

            # sendto() sends the reply back to the sender address.
            server_socket.sendto(response, address)
            print(f"[INFO] Sent response back to {client_ip}:{client_port}\n")


if __name__ == "__main__":
    main()

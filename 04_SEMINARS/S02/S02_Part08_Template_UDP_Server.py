"""S02 – Template UDP server (student task)

This file provides a minimal UDP server.

Students can adapt this code to implement a simple application-layer protocol
over UDP (e.g., ping/PONG, upper:... and similar commands).
"""

import socket
import sys


def main():
    # Verify that a port was provided on the command line.
    # Example:
    #   python3 S02_Part08_Template_UDP_Server.py 12345
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])

    # Create a UDP socket:
    # - AF_INET    → IPv4
    # - SOCK_DGRAM → UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # bind(('', port)) means:
        # - ''   → all interfaces (0.0.0.0)
        # - port → the port on which the server listens
        server_socket.bind(("", port))

        print(f"[INFO] UDP server listening on 0.0.0.0:{port}")

        while True:
            # recvfrom(1024) receives:
            # - up to 1024 bytes from a single UDP datagram
            # - the sender address (ip, port)
            message, address = server_socket.recvfrom(1024)

            client_ip, client_port = address
            print(f"[INFO] Received {len(message)} bytes from {client_ip}:{client_port}")
            print(f"       Raw message: {message!r}")

            # TODO (student): implement your protocol here.
            # For now, we provide a simple uppercase echo.
            response = message.upper()

            server_socket.sendto(response, address)
            print(f"[INFO] Sent response back to {client_ip}:{client_port}\n")


if __name__ == "__main__":
    main()

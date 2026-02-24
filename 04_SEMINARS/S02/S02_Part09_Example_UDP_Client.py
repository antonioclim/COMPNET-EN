"""S02 – Example UDP client

This script sends a single UDP datagram to a server and waits for a reply.

Usage:
    python3 S02_Part09_Example_UDP_Client.py <HOST> <PORT> <MESSAGE>
"""

import socket
import sys


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT> <MESSAGE>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    message = sys.argv[3].encode("utf-8")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"[INFO] Sending {len(message)} bytes to {host}:{port} ...")
        client_socket.sendto(message, (host, port))

        # Optional: set a timeout to avoid blocking indefinitely.
        client_socket.settimeout(3.0)

        try:
            data, address = client_socket.recvfrom(1024)
            print(f"[INFO] Received {len(data)} bytes from {address}: {data!r}")
        except socket.timeout:
            print("[WARN] No response received (timeout).")


if __name__ == "__main__":
    main()

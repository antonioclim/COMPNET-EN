import socket
import sys

"""
Simple UDP server.

Usage in Mininet (on h3):
    h3 python3 S06_Part03_Script_UDP_Server.py 6000

The server:
 - listens on all interfaces, on the given port
 - displays received messages
 - sends an echo reply back to the client
"""

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", port))
        print(f"[UDP SERVER] Listening on 0.0.0.0:{port}")

        while True:
            data, addr = s.recvfrom(1024)
            if not data:
                continue
            print(f"[UDP SERVER] From {addr}: {data.decode().strip()}")
            s.sendto(data, addr)


if __name__ == "__main__":
    main()

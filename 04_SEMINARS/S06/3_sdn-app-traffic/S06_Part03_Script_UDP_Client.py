import socket
import sys

"""
Simple UDP client.

Usage in Mininet (on h1):
    h1 python3 S06_Part03_Script_UDP_Client.py 10.0.10.3 6000

The client:
 - sends UDP messages to the given address and port
 - displays the reply received (if any)
 - 'exit' closes the client
"""

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print(f"[UDP CLIENT] Sending to {host}:{port}")
        while True:
            msg = input("udp> ").strip()
            if not msg:
                continue
            if msg == "exit":
                break

            s.sendto(msg.encode(), (host, port))

            # Wait for a reply (a timeout could be set, but for now we block)
            try:
                data, addr = s.recvfrom(1024)
                print(f"[UDP CLIENT] Received from {addr}: {data.decode().strip()}")
            except Exception as e:
                print(f"[UDP CLIENT] Error receiving: {e}")


if __name__ == "__main__":
    main()

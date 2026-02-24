import socket
import sys

"""
Simple TCP server (echo).

Usage in Mininet (on h2):
    h2 python3 S06_Part03_Script_TCP_Server.py 5000

The server:
 - listens on all interfaces, on the given port
 - accepts one client at a time
 - reads data, displays it and sends it back (echo)
"""

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])

    # Create an IPv4 TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow address reuse in case of a rapid restart
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen(1)
        print(f"[TCP SERVER] Listening on 0.0.0.0:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"[TCP SERVER] Connection from {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("[TCP SERVER] Client disconnected")
                    break
                print(f"[TCP SERVER] Received: {data.decode().strip()}")
                conn.sendall(data)


if __name__ == "__main__":
    main()

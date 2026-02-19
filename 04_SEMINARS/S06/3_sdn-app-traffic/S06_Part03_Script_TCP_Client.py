import socket
import sys

"""
Simple TCP client (echo client).

Usage in Mininet (on h1):
    h1 python3 S06_Part03_Script_TCP_Client.py 10.0.10.2 5000

The client:
 - connects to the given IP address and port
 - reads lines from the keyboard
 - sends them to the server and displays the response
 - 'exit' closes the client
"""

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[TCP CLIENT] Connecting to {host}:{port} ...")
        try:
            s.connect((host, port))
        except Exception as e:
            print(f"[TCP CLIENT] Connection failed: {e}")
            sys.exit(1)

        print("[TCP CLIENT] Connected. Type messages, 'exit' to quit.")
        while True:
            msg = input("tcp> ").strip()
            if not msg:
                continue
            if msg == "exit":
                break
            s.sendall(msg.encode())
            data = s.recv(1024)
            if not data:
                print("[TCP CLIENT] Server closed connection")
                break
            print(f"[TCP CLIENT] Received: {data.decode().strip()}")


if __name__ == "__main__":
    main()

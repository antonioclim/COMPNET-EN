import socket
import os

HOST = "127.0.0.1"
PORT = 9200

def main():
    pid = os.getpid()
    msg = f"hello from client {pid}\n".encode("utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(msg)
        data = s.recv(1024)
        print("Received:", data.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()

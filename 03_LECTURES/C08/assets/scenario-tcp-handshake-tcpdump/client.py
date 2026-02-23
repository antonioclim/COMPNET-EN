import socket
import time

HOST = "127.0.0.1"
PORT = 9090

def main():
    msg = b"hello"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(msg)
    data = s.recv(4096)
    print(f"[client] received: {data!r}")

    # Short delay so the closure is more visible in the capture
    time.sleep(0.2)
    s.close()

if __name__ == "__main__":
    main()

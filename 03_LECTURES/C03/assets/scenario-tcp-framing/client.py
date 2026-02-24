import socket
import time

HOST = "127.0.0.1"
PORT = 9100

def main():
    messages = ["one", "two", "three", "four"]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for m in messages:
            payload = (m + "\n").encode("utf-8")
            s.sendall(payload)
            time.sleep(0.05)

        s.shutdown(socket.SHUT_WR)

        buf = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            buf += chunk
        print("Client received:\n", buf.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()

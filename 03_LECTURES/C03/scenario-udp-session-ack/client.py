import socket
import time

HOST = "127.0.0.1"
PORT = 9300

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2.0)

        s.sendto(b"HELLO\n", (HOST, PORT))
        token_msg, _ = s.recvfrom(2048)
        token_line = token_msg.decode("utf-8", errors="replace").strip()
        print("Server:", token_line)

        token = token_line.split(":", 1)[1]
        for i in range(1, 4):
            payload = f"MSG:{token}:message {i}\n".encode("utf-8")
            s.sendto(payload, (HOST, PORT))
            ack, _ = s.recvfrom(2048)
            print("Server:", ack.decode("utf-8", errors="replace").strip())
            time.sleep(0.2)

if __name__ == "__main__":
    main()

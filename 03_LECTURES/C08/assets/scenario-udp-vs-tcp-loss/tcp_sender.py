import socket
import time

HOST = "10.0.0.2"
PORT = 9092
COUNT = 200

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    for i in range(COUNT):
        s.sendall(f"MSG {i}\n".encode("utf-8"))
        time.sleep(0.005)

    s.close()
    print("[tcp_sender] done")

if __name__ == "__main__":
    main()

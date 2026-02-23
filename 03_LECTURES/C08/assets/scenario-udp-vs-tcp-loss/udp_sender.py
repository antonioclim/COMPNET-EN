import socket
import time

HOST = "10.0.0.2"
PORT = 9091
COUNT = 200

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(COUNT):
        s.sendto(f"MSG {i}\n".encode("utf-8"), (HOST, PORT))
        time.sleep(0.005)
    print("[udp_sender] done")

if __name__ == "__main__":
    main()

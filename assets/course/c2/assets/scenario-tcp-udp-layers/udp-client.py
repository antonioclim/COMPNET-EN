import socket

HOST = "127.0.0.1"
PORT = 9001

def main():
    msg = "Salut din UDP client\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(msg.encode("utf-8"), (HOST, PORT))
        data, _ = s.recvfrom(4096)
        print("UDP response:", data.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()

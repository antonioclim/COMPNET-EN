import socket

HOST = "127.0.0.1"
PORT = 9001

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP server listening on {HOST}:{PORT}")

        data, addr = s.recvfrom(4096)
        print("UDP received from", addr, ":", data.decode("utf-8", errors="replace"))
        s.sendto(b"ACK from UDP server\n", addr)

if __name__ == "__main__":
    main()

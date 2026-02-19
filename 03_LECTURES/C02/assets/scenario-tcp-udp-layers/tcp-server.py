import socket

HOST = "127.0.0.1"
PORT = 9000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"TCP server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print("TCP client connected:", addr)
            data = conn.recv(4096)
            print("TCP received:", data.decode("utf-8", errors="replace"))
            conn.sendall(b"ACK from TCP server\n")

if __name__ == "__main__":
    main()

import socket

HOST = "127.0.0.1"
PORT = 9100

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"TCP framing server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print("Client connected:", addr)
            buf = b""
            while True:
                chunk = conn.recv(16)
                if not chunk:
                    print("Client closed")
                    break
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    msg = line.decode("utf-8", errors="replace")
                    print("Message:", msg)
                    conn.sendall(f"OK:{msg}\n".encode("utf-8"))

if __name__ == "__main__":
    main()

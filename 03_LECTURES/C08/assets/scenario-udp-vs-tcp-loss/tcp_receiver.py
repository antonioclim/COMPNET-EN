import socket

HOST = "0.0.0.0"
PORT = 9092

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, _ = s.accept()

    buf = b""
    lines = 0
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        buf += chunk
        while b"\n" in buf:
            _, buf = buf.split(b"\n", 1)
            lines += 1

    conn.close()
    print(f"[tcp_receiver] received lines: {lines}")

if __name__ == "__main__":
    main()

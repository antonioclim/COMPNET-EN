import socket
import threading

HOST = "127.0.0.1"
PORT = 9090

def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        if data:
            conn.sendall(b"echo: " + data)
    finally:
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[server] listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"[server] accepted {addr}")
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()

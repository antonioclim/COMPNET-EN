import socket
import threading

HOST = "127.0.0.1"
PORT = 9200

def handle(conn, addr):
    with conn:
        print("Client:", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(b"ECHO:" + data)
    print("Client closed:", addr)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(50)
        print(f"TCP multiclient server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()

import socket

HOST = "127.0.0.1"
PORT = 9000

def main():
    msg = "Salut din TCP client\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(msg.encode("utf-8"))
        data = s.recv(4096)
        print("TCP response:", data.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()

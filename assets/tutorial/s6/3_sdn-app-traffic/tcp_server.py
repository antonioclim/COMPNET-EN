import socket
import sys

"""
Server TCP simplu (echo).

Utilizare in Mininet (pe h2):
    h2 python3 tcp_server.py 5000

Serverul:
 - asculta pe toate interfetele, pe portul dat
 - accepta un client o data
 - citeste date, le afiseaza si le trimite inapoi (echo)
"""

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])

    # Cream un socket TCP IPv4
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Permitem reutilizarea adresei in caz de restart rapid
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", port))
        s.listen(1)
        print(f"[TCP SERVER] Listening on 0.0.0.0:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"[TCP SERVER] Connection from {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("[TCP SERVER] Client disconnected")
                    break
                print(f"[TCP SERVER] Received: {data.decode().strip()}")
                conn.sendall(data)


if __name__ == "__main__":
    main()

import socket

# Adresă IP:
# - "" sau "0.0.0.0" înseamnă "toate interfețele locale".
LISTEN_ADDR = ""
LISTEN_PORT = 5007


def main():
    """
    Receiver UDP pentru mesaje de broadcast.

    Toate datagramele trimise către portul LISTEN_PORT (inclusiv broadcast)
    vor fi primite aici, dacă firewall-ul și OS-ul permit.
    """

    # Creăm un socket UDP (IPv4).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Legăm socket-ul la (LISTEN_ADDR, LISTEN_PORT).
    # "" -> ascultă pe toate interfețele locale.
    sock.bind((LISTEN_ADDR, LISTEN_PORT))

    print(f"[INFO] UDP broadcast receiver listening on 0.0.0.0:{LISTEN_PORT}")

    while True:
        # recvfrom(1024) blochează până când orice host trimite o datagramă
        # către LISTEN_PORT.
        data, addr = sock.recvfrom(1024)
        ip, port = addr
        print(f"[RECV] {len(data)} bytes from {ip}:{port} -> {data.decode('utf-8', errors='ignore')!r}")


if __name__ == "__main__":
    main()

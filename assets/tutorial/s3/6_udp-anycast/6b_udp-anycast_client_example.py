import socket

# Pentru laborator, simulăm "anycast" folosind o adresă IPv6 locală.
# În realitate, anycast presupune rutare specială în rețea.
ANYCAST_ADDR = "::1"  # loopback IPv6
PORT = 5007


def anycast_client():
    """
    Client UDP IPv6 pentru "anycast" (simulat).

    Trimite un mesaj la ANYCAST_ADDR și așteaptă un răspuns.
    """

    # AF_INET6 -> IPv6.
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    message = b"Hello, anycast server!"
    print(f"[INFO] Sending to [{ANYCAST_ADDR}]:{PORT}")
    sock.sendto(message, (ANYCAST_ADDR, PORT))

    data, addr = sock.recvfrom(1024)
    print(f"[INFO] Received response: {data.decode('utf-8', errors='ignore')!r} from {addr}")

    sock.close()


if __name__ == "__main__":
    anycast_client()

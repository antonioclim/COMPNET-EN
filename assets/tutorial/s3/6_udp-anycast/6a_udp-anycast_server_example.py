import socket

# "::" = orice adresă IPv6 locală.
# Într-o rețea reală, anycast ar implica mai multe servere configurate
# cu aceeași adresă anycast, dar rulate în locații diferite.
ANYCAST_ADDR = "::"
PORT = 5007


def anycast_server():
    """
    Server UDP IPv6 "anycast" (simulat).

    Ascultă pe toate adresele IPv6 locale, pe portul PORT,
    și răspunde la orice mesaj cu un text fix.
    """

    # AF_INET6 -> IPv6, SOCK_DGRAM -> UDP.
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((ANYCAST_ADDR, PORT))

    print(f"[INFO] Anycast-like UDP server listening on [{ANYCAST_ADDR}]:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[RECV] From {addr} -> {data.decode('utf-8', errors='ignore')!r}")
        sock.sendto(b"Reply from anycast server", addr)
        print(f"[SEND] Reply to {addr}")


if __name__ == "__main__":
    anycast_server()

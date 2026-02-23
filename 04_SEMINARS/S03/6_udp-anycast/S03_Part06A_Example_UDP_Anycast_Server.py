import socket

# "::" = any local IPv6 address.
# In a real network, anycast would involve multiple servers configured
# with the same anycast address but running in different locations.
ANYCAST_ADDR = "::"
PORT = 5007


def anycast_server():
    """
    UDP IPv6 "anycast" server (simulated).

    Listens on all local IPv6 addresses on port PORT
    and replies to every message with a fixed text.
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

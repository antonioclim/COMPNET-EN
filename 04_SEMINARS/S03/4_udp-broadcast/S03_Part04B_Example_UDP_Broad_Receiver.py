import socket

# IP address:
# - "" or "0.0.0.0" means "all local interfaces".
LISTEN_ADDR = ""
LISTEN_PORT = 5007


def main():
    """
    UDP receiver for broadcast messages.

    All datagrams sent to LISTEN_PORT (including broadcast)
    will be received here, provided the firewall and OS permit it.
    """

    # Create a UDP (IPv4) socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to (LISTEN_ADDR, LISTEN_PORT).
    # "" -> listen on all local interfaces.
    sock.bind((LISTEN_ADDR, LISTEN_PORT))

    print(f"[INFO] UDP broadcast receiver listening on 0.0.0.0:{LISTEN_PORT}")

    while True:
        # recvfrom(1024) blocks until any host sends a datagram
        # to LISTEN_PORT.
        data, addr = sock.recvfrom(1024)
        ip, port = addr
        print(f"[RECV] {len(data)} bytes from {ip}:{port} -> {data.decode('utf-8', errors='ignore')!r}")


if __name__ == "__main__":
    main()

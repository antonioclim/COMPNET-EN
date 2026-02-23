import socket

# For the laboratory we simulate "anycast" using a local IPv6 address.
# In reality, anycast requires special routing in the network.
ANYCAST_ADDR = "::1"  # IPv6 loopback
PORT = 5007


def anycast_client():
    """
    Simulated UDP IPv6 "anycast" client.

    Sends a message to ANYCAST_ADDR and waits for a reply.
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

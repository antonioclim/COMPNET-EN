import socket
import struct

# The multicast group and port we listen on.
MCAST_GRP = "224.0.0.1"
MCAST_PORT = 5001


def main():
    """
    UDP multicast receiver.

    - subscribes to the multicast group MCAST_GRP
    - receives datagrams sent to the group
    """

    # Create a UDP (IPv4) socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind on all local interfaces, on MCAST_PORT.
    # "" or "0.0.0.0" = all interfaces.
    sock.bind(("", MCAST_PORT))

    # Tell the kernel to "join" the multicast group.
    group_bytes = socket.inet_aton(MCAST_GRP)
    # INADDR_ANY = any local interface.
    mreq = struct.pack("4sL", group_bytes, socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[INFO] UDP multicast receiver joined group {MCAST_GRP} on port {MCAST_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        ip, port = addr
        print(f"[RECV] {len(data)} bytes from {ip}:{port} -> {data.decode('utf-8', errors='ignore')!r}")


if __name__ == "__main__":
    main()

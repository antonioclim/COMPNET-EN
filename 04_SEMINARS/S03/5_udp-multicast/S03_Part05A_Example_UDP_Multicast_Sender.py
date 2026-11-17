import socket
import os
import sys

# IPv4 multicast group (class D address: 224.0.0.0 – 239.255.255.255).
MCAST_GRP = "239.255.0.1"
MCAST_PORT = 5001
MCAST_INTERFACE_IP = os.environ.get("MCAST_INTERFACE_IP", "0.0.0.0")


def main():
    """
    UDP multicast sender.

    Sends a message to the multicast group MCAST_GRP.
    All receivers that have subscribed to this group on MCAST_PORT
    will receive the datagram.
    """

    if len(sys.argv) >= 2:
        message = sys.argv[1]
    else:
        message = "Hello, multicast!"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # IP_MULTICAST_TTL controls how far the packet can travel
    # (how many router "hops"). 1 = local network only.
    # Limit this laboratory traffic to the selected local interface/subnet.
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MCAST_INTERFACE_IP))

    data = message.encode("utf-8")

    print(f"[INFO] Sending multicast to {MCAST_GRP}:{MCAST_PORT}")
    sock.sendto(data, (MCAST_GRP, MCAST_PORT))
    print(f"[SEND] {len(data)} bytes -> {MCAST_GRP}:{MCAST_PORT} :: {message!r}")

    sock.close()


if __name__ == "__main__":
    main()

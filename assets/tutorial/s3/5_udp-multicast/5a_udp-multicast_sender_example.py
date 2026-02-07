import socket
import sys

# Grup multicast IPv4 (adresă de clasă D: 224.0.0.0 - 239.255.255.255).
MCAST_GRP = "224.0.0.1"
MCAST_PORT = 5001


def main():
    """
    Sender UDP pentru multicast.

    Trimite un mesaj către grupul multicast MCAST_GRP.
    Toți receiver-ii care s-au abonat la acest grup pe MCAST_PORT
    vor primi datagrama.
    """

    if len(sys.argv) >= 2:
        message = sys.argv[1]
    else:
        message = "Hello, multicast!"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # IP_MULTICAST_TTL controlează cât de departe poate merge pachetul
    # (câte "hop-uri" routere). 1 = doar în rețeaua locală.
    # 32 e un exemplu; pentru laborator nu contează foarte mult dacă sunteți pe loopback.
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    data = message.encode("utf-8")

    print(f"[INFO] Sending multicast to {MCAST_GRP}:{MCAST_PORT}")
    sock.sendto(data, (MCAST_GRP, MCAST_PORT))
    print(f"[SEND] {len(data)} bytes -> {MCAST_GRP}:{MCAST_PORT} :: {message!r}")

    sock.close()


if __name__ == "__main__":
    main()

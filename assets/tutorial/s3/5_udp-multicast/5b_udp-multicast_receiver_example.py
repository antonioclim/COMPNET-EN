import socket
import struct

# Grupul multicast și portul pe care ascultăm.
MCAST_GRP = "224.0.0.1"
MCAST_PORT = 5001


def main():
    """
    Receiver UDP pentru multicast.

    - se abonează la grupul multicast MCAST_GRP
    - primește datagrame trimise către grup
    """

    # Creăm un socket UDP (IPv4).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind pe toate interfețele locale, pe portul MCAST_PORT.
    # Adresa "" sau "0.0.0.0" = toate interfețele.
    sock.bind(("", MCAST_PORT))

    # Trebuie să spunem kernel-ului să se "înscrie" în grupul multicast.
    group_bytes = socket.inet_aton(MCAST_GRP)
    # INADDR_ANY = orice interfață locală.
    mreq = struct.pack("4sL", group_bytes, socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[INFO] UDP multicast receiver joined group {MCAST_GRP} on port {MCAST_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        ip, port = addr
        print(f"[RECV] {len(data)} bytes from {ip}:{port} -> {data.decode('utf-8', errors='ignore')!r}")


if __name__ == "__main__":
    main()

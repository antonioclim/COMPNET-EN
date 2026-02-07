import socket
import sys
import time

# Adresa de broadcast IPv4 clasică.
# În practică se poate folosi și broadcast de rețea (ex: 192.168.1.255),
# dar pentru laborator lăsăm 255.255.255.255.
BCAST_ADDR = "255.255.255.255"

# Portul UDP pe care vor asculta receiverele.
BCAST_PORT = 5007


def main():
    """
    Sender UDP de broadcast.

    Trimite periodic mesaje către adresa de broadcast, astfel încât
    toate host-urile care ascultă pe portul BCAST_PORT să le poată primi.
    """

    # Mesajul poate fi dat în linia de comandă sau folosim un default.
    # Exemplu:
    #   python3 index_udp-broadcast_sender_example.py "Hello, broadcast!"
    if len(sys.argv) >= 2:
        base_message = sys.argv[1]
    else:
        base_message = "Hello, broadcast!"

    # Creăm un socket UDP (IPv4).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Activăm dreptul de a trimite broadcast.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(f"[INFO] Sending UDP broadcast to {BCAST_ADDR}:{BCAST_PORT}")
    print("[INFO] Press Ctrl+C to stop.\n")

    counter = 0
    try:
        while True:
            # Construim un mesaj care conține și un număr de secvență.
            message_str = f"{base_message} #{counter}"
            data = message_str.encode("utf-8")

            # sendto() trimite datagrama către adresa de broadcast.
            sock.sendto(data, (BCAST_ADDR, BCAST_PORT))
            print(f"[SEND] {len(data)} bytes -> {BCAST_ADDR}:{BCAST_PORT} :: {message_str!r}")

            counter += 1
            time.sleep(1.0)  # 1 mesaj pe secundă
    except KeyboardInterrupt:
        print("\n[INFO] Stopping broadcast sender.")
    finally:
        sock.close()
        print("[INFO] Socket closed.")


if __name__ == "__main__":
    main()

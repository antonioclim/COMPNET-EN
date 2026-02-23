import socket
import sys
import time

# Classic IPv4 broadcast address.
# In practice one may also use a network broadcast (e.g. 192.168.1.255),
# but for the laboratory we keep 255.255.255.255.
BCAST_ADDR = "255.255.255.255"

# UDP port on which receivers will listen.
BCAST_PORT = 5007


def main():
    """
    UDP broadcast sender.

    Sends periodic messages to the broadcast address so that
    all hosts listening on BCAST_PORT can receive them.
    """

    # The message can be given on the command line or a default is used.
    # Example:
    #   python3 index_udp-broadcast_sender_example.py "Hello, broadcast!"
    if len(sys.argv) >= 2:
        base_message = sys.argv[1]
    else:
        base_message = "Hello, broadcast!"

    # Create a UDP (IPv4) socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcast sending permission.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(f"[INFO] Sending UDP broadcast to {BCAST_ADDR}:{BCAST_PORT}")
    print("[INFO] Press Ctrl+C to stop.\n")

    counter = 0
    try:
        while True:
            # Build a message that includes a sequence number.
            message_str = f"{base_message} #{counter}"
            data = message_str.encode("utf-8")

            # sendto() sends the datagram to the broadcast address.
            sock.sendto(data, (BCAST_ADDR, BCAST_PORT))
            print(f"[SEND] {len(data)} bytes -> {BCAST_ADDR}:{BCAST_PORT} :: {message_str!r}")

            counter += 1
            time.sleep(1.0)  # 1 message per second
    except KeyboardInterrupt:
        print("\n[INFO] Stopping broadcast sender.")
    finally:
        sock.close()
        print("[INFO] Socket closed.")


if __name__ == "__main__":
    main()

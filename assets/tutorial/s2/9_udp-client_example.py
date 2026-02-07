import socket
import sys


def main():
    """
    Client UDP foarte simplu.

    Trimite un singur mesaj unui server UDP și afișează răspunsul.
    """

    # Usage: python3 index_udp-client_example.py <HOST> <PORT> <MESSAGE>
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT> <MESSAGE>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    MESSAGE = sys.argv[3]

    # Creăm un socket UDP (IPv4).
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Codificăm mesajul din string în bytes.
        data = MESSAGE.encode('utf-8')

        print(f"[INFO] Sending {len(data)} bytes to {HOST}:{PORT} ...")
        # sendto() trimite datagrama către (HOST, PORT).
        client_socket.sendto(data, (HOST, PORT))

        # recvfrom(1024) așteaptă un răspuns (max 1024 bytes) și
        # întoarce (mesaj, address).
        response, server_address = client_socket.recvfrom(1024)

        print(f"[INFO] Received {len(response)} bytes from {server_address}: {response!r}")


if __name__ == '__main__':
    main()

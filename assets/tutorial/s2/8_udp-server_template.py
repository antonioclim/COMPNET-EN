import socket
import sys


def main():
    """
    Server UDP foarte simplu (echo cu litere mari).

    Caracteristici:
    - folosește UDP (connectionless)
    - primește datagrame de la oricâți clienți
    - răspunde fiecărui client cu același mesaj, dar transformat în litere mari
    """

    # Verificăm dacă s-a dat portul în linia de comandă.
    # Exemplu de rulare:
    #   python3 index_udp-server_example.py 12345
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    # sys.argv[1] este un string -> îl convertim la int.
    PORT = int(sys.argv[1])

    # Creăm un socket UDP:
    # - AF_INET  -> IPv4
    # - SOCK_DGRAM -> UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # bind(('', PORT)) înseamnă:
        # - ''  -> toate interfețele de rețea (0.0.0.0)
        # - PORT -> portul pe care ascultă serverul
        server_socket.bind(('', PORT))

        print(f"[INFO] UDP server listening on 0.0.0.0:{PORT}")

        # Buclă infinită: serverul așteaptă mesaje de la clienți.
        while True:
            # recvfrom(1024) primește:
            # - maxim 1024 bytes dintr-o singură datagramă UDP
            # - adresa (ip, port) a expeditorului
            message, address = server_socket.recvfrom(1024)

            # Afișăm date de debugging în server:
            client_ip, client_port = address
            print(f"[INFO] Received {len(message)} bytes from {client_ip}:{client_port}")
            print(f"       Raw message: {message!r}")

            # Pregătim răspunsul: transformăm mesajul în litere mari.
            response = message.upper()

            # sendto() trimite răspunsul înapoi exact la adresa expeditorului.
            server_socket.sendto(response, address)
            print(f"[INFO] Sent response back to {client_ip}:{client_port}\n")


if __name__ == '__main__':
    main()

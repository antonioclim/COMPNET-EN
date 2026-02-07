import socket
import sys

"""
Client UDP simplu.

Utilizare in Mininet (pe h1):
    h1 python3 udp_client.py 10.0.10.3 6000

Clientul:
 - trimite mesaje UDP catre adresa si portul date
 - afiseaza raspunsul primit (daca primeste)
 - 'exit' inchide clientul
"""

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print(f"[UDP CLIENT] Sending to {host}:{port}")
        while True:
            msg = input("udp> ").strip()
            if not msg:
                continue
            if msg == "exit":
                break

            s.sendto(msg.encode(), (host, port))

            # asteptam un raspuns (putem seta un timeout, dar deocamdata asteptam)
            try:
                data, addr = s.recvfrom(1024)
                print(f"[UDP CLIENT] Received from {addr}: {data.decode().strip()}")
            except Exception as e:
                print(f"[UDP CLIENT] Error receiving: {e}")


if __name__ == "__main__":
    main()

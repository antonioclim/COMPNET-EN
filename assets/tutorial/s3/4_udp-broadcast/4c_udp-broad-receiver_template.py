import socket

LISTEN_ADDR = ""
LISTEN_PORT = 5007


def main():
    """
    Receiver UDP de broadcast care va fi extins de student.

    Obiectiv:
    - numără câte mesaje a primit
    - filtrează mesajele după un prefix
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_ADDR, LISTEN_PORT))

    print(f"[INFO] UDP broadcast receiver listening on 0.0.0.0:{LISTEN_PORT}")

    # >>> STUDENT CODE STARTS HERE
    """
    TODO (student):

    1. Inițializați o variabilă counter = 0 (înainte de bucla while).
    2. În bucla infinită:
       - primiți datele cu recvfrom(1024).
       - decodificați mesajul în text UTF-8.
       - incrementați counter cu 1.

       - Dacă mesajul NU începe cu prefixul "Hello",
         afișați un log:
           [SKIP] From <ip>:<port> -> "<text>"
         și continuați la următorul mesaj (continue).

       - Dacă mesajul începe cu "Hello":
         afișați:
           [OK] (#<counter>) From <ip>:<port> -> "<text>"

    Indicii:
    - folosiți text.startswith("Hello")
    - nu uitați să afișați și numărul curent de mesaje (counter)
    """

    # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()

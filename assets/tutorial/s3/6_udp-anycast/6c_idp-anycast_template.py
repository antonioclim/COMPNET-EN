import socket

ANYCAST_ADDR = "::"
PORT = 5007


def anycast_server():
    """
    Server UDP IPv6 "anycast" (simulat).

    Obiectiv student:
    - adăugați un "id" al serverului în răspuns (pentru a vedea cine răspunde)
    """

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.bind((ANYCAST_ADDR, PORT))

    # >>> STUDENT CODE STARTS HERE
    """
    TODO (student):

    1. Cereți utilizatorului să introducă un "server_id"
       (de ex. "S1", "S2", etc.) folosind input().

    2. În bucla while:
       - primiți un mesaj cu recvfrom(1024).
       - decodificați textul mesajului.
       - afișați un log:
         [RECV-<server_id>] From <addr> -> "<text>"

       - construiți un răspuns de forma:
         f"[{server_id}] Reply from anycast server"
         și trimiteți-l înapoi către client (encodat UTF-8).

       - afișați un log:
         [SEND-<server_id>] To <addr> -> "<reply>"
    """

    # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    anycast_server()

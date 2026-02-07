import socket
import struct
import time

MCAST_GRP = "224.0.0.1"
MCAST_PORT = 5001


def main():
    """
    Receiver UDP multicast extins de student.

    Obiectiv:
    - afișează timestamp pentru fiecare mesaj
    - numără câte mesaje a primit
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("", MCAST_PORT))

    group_bytes = socket.inet_aton(MCAST_GRP)
    mreq = struct.pack("4sL", group_bytes, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[INFO] UDP multicast receiver joined group {MCAST_GRP} on port {MCAST_PORT}")

    # >>> STUDENT CODE STARTS HERE
    """
    TODO (student):

    1. Inițializați un counter = 0.

    2. În bucla while:
       - primiți un mesaj cu recvfrom(1024)
       - incrementați counter
       - obțineți timpul curent (time.time()) și transformați-l
         într-un string lizibil (folosind time.strftime, time.localtime).

       - decodificați mesajul în text UTF-8.

       - afișați un log de forma:
         [#<counter> at <timestamp>] From <ip>:<port> -> "<text>"

    3. Observați în rulare că mai mulți receiver-i care rulează pe
       mașini diferite, dar în același grup multicast, primesc același mesaj.
       (Această observație va fi descrisă în fișierul de output.)
    """

    # <<< STUDENT CODE ENDS HERE


if __name__ == "__main__":
    main()

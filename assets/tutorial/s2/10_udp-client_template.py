import socket
import sys
import time


def main():
    """
    Client UDP interactiv.

    Obiectiv:
    - trimite mesaje repetate către server
    - măsoară timpul de răspuns (pseudo-RTT pentru UDP)
    - afișează statistici simple
    """

    # Usage: python3 index_udp-client_template.py <HOST> <PORT>
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <HOST> <PORT>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        print(f"[INFO] UDP client ready, sending to {HOST}:{PORT}")
        sent_count = 0
        received_count = 0

        # >>> STUDENT CODE STARTS HERE
        """
        TODO (student):

        1. Implementați o buclă interactivă:
           - Folosiți while True:
               - citiți un mesaj de la tastatură (input()).
               - dacă mesajul este "exit", ieșiți din buclă.

        2. Pentru fiecare mesaj:
           - incrementați contorul 'sent_count'.
           - salvați timpul curent înainte de sendto() (time.time()).
           - trimiteți mesajul către server (HOST, PORT), encodat în UTF-8.
           - setați un timeout pe socket (ex: 2 secunde) folosind:
                 client_socket.settimeout(2.0)
           - încercați să primiți răspunsul cu recvfrom(1024).
             * dacă răspunsul vine la timp:
                 - incrementați 'received_count'
                 - calculați "RTT" aproximativ: t_after - t_before
                 - afișați mesajul primit și RTT-ul în milisecunde.
             * dacă NU vine răspuns (timeout):
                 - afișați un mesaj de tip "[WARN] No response (timeout)".

        3. După ieșirea din buclă (când utilizatorul scrie "exit"):
           - afișați un mic rezumat:
             * numărul de mesaje trimise
             * numărul de răspunsuri primite
             * procentul de "pierderi" (dacă există)
        """

        # <<< STUDENT CODE ENDS HERE

        print("[INFO] UDP client terminated.")


if __name__ == '__main__':
    main()

import socket
import time

HOST = "127.0.0.1"
PORT = 12345


def main():
    # Creăm un socket TCP (IPv4).
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[INFO] Connecting to {HOST}:{PORT} ...")
        s.connect((HOST, PORT))
        print("[INFO] Connected.")

        # >>> STUDENT CODE STARTS HERE
        """
        TODO (student):

        1. Cereți utilizatorului să introducă mesaje de la tastatură
           într-o buclă (folosind input()).

        2. Pentru fiecare mesaj:
           - Dacă utilizatorul introduce 'exit', ieșiți din buclă.
           - Măsurați timpul înainte și după trimiterea și primirea
             răspunsului de la server (folosiți time.time()).
           - Trimiteți mesajul ca bytes (folosind .encode('utf-8')).
           - Citiți răspunsul serverului cu recv(1024).

        3. Afișați pentru fiecare rundă:
           - mesajul trimis
           - răspunsul primit
           - timpul total "round-trip" (RTT) în milisecunde.

        Indicii:
        - Folosiți o buclă while True:
              while True:
                  data = input("Mesaj (sau 'exit' pentru a ieși): ")
        - Conversie la bytes: data.encode('utf-8')
        - RTT (ms): (t_after - t_before) * 1000
        """

        # <<< STUDENT CODE ENDS HERE

    print("[INFO] Connection closed.")


if __name__ == "__main__":
    main()

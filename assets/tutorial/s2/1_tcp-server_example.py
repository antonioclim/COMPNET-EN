import socketserver

# Definim o clasă de handler pentru fiecare conexiune TCP nouă.
# socketserver.BaseRequestHandler este o clasă de bază care cere
# să suprascriem metoda handle() pentru a defini logica de procesare.
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Request handler pentru serverul nostru TCP.

    Pentru FIECARE conexiune nouă la server:
    - se creează o instanță MyTCPHandler
    - Wireshark va vedea un nou "TCP stream" (conversație)
    """

    def handle(self):
        """
        Metoda handle() este punctul de intrare pentru logica de server
        la nivel de aplicație.

        self.request  -> socket-ul TCP conectat la client
        self.client_address -> tuplu (ip, port) al clientului
        """
        # Primim maxim 1024 de bytes de la client.
        # .recv(1024) blochează execuția până când:
        # - vin date de la client, sau
        # - conexiunea este închisă / e o eroare.
        # .strip() elimină spațiile / newline-urile de la început/sfârșit.
        self.data = self.request.recv(1024).strip()

        # Afișăm adresa IP a clientului pentru log.
        print(f"{self.client_address[0]} wrote:")

        # Afișăm conținutul brut al mesajului (bytes).
        print(self.data)

        # Trimitem înapoi același mesaj, dar cu litere mari.
        # sendall() asigură trimiterea tuturor datelor.
        self.request.sendall(self.data.upper())


# Definim o clasă de server TCP care permite refolosirea adresei.
# allow_reuse_address = True -> putem reporni serverul rapid pe același port
# fără să așteptăm TIME_WAIT (util la laborator).
class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    # Adresa și portul pe care va asculta serverul.
    HOST, PORT = "localhost", 12345

    # Ne asigurăm că opțiunea este activă pe clasa de bază.
    socketserver.TCPServer.allow_reuse_address = True

    # Creăm serverul, legat de (HOST, PORT) și folosind MyTCPHandler
    # pentru a procesa fiecare conexiune.
    #
    # "with ... as server" garantează că, la ieșirea din bloc,
    # socket-ul este închis corect (chiar și dacă apare o excepție).
    with MyTCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"[INFO] TCP server listening on {HOST}:{PORT}")

        # server.serve_forever() intră într-o buclă infinită:
        # - acceptă conexiuni noi
        # - creează câte un handler pentru fiecare conexiune
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            # Când apăsăm Ctrl+C, ajungem aici și oprim serverul curat.
            print("\n[INFO] Shutting down server...")
            server.shutdown()

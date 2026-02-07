import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Request handler pentru serverul nostru TCP.

    Această clasă este instanțiată O DATĂ pentru fiecare conexiune nouă.
    """

    def handle(self):
        """
        TODO (student): adaptați logica astfel încât:
        - să afișați și portul clientului, nu doar IP-ul
        - să afișați lungimea mesajului primit (în bytes)
        - să trimiteți înapoi un răspuns de forma:
          b"OK: " + <mesajul original transform at în litere mari>

        Indiciu:
        - self.client_address este un tuplu (ip, port)
        - len(self.data) dă lungimea mesajului (în bytes)
        """
        # Citim datele de la client (maxim 1024 bytes).
        self.data = self.request.recv(1024).strip()

        # >>> STUDENT CODE STARTS HERE

        # 1. Afișați IP-ul și portul clientului în format:
        #    [CLIENT] <ip>:<port> connected
        #    Folosiți self.client_address.

        # 2. Afișați conținutul mesajului și lungimea sa:
        #    [CLIENT] Sent <len> bytes: <mesaj>

        # 3. Construiți un răspuns care începe cu b"OK: "
        #    urmat de mesajul original, transformat în litere mari.

        #    Exemplu: pentru "hello", răspunsul ar trebui să fie:
        #    b"OK: HELLO"

        # 4. Trimiteți răspunsul înapoi la client cu sendall().

        # <<< STUDENT CODE ENDS HERE


class MyTCPServer(socketserver.TCPServer):
    # Ne asigurăm că putem reporni serverul imediat pe același port.
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 12345
    socketserver.TCPServer.allow_reuse_address = True

    with MyTCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"[INFO] TCP server listening on {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down server...")
            server.shutdown()

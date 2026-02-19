import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Request handler for our TCP server.

    This class is instantiated ONCE for every new connection.
    """

    def handle(self):
        """
        TODO (student): adapt the logic so that:
        - you also display the client's port, not just its IP
        - you display the length of the received message (in bytes)
        - you send back a response of the form:
          b"OK: " + <the original message converted to upper case>

        Hint:
        - self.client_address is a tuple (ip, port)
        - len(self.data) gives the message length (in bytes)
        """
        # Read data from the client (at most 1024 bytes).
        self.data = self.request.recv(1024).strip()

        # >>> STUDENT CODE STARTS HERE

        # 1. Display the client's IP and port in the format:
        #    [CLIENT] <ip>:<port> connected
        #    Use self.client_address.

        # 2. Display the message content and its length:
        #    [CLIENT] Sent <len> bytes: <message>

        # 3. Build a response that starts with b"OK: "
        #    followed by the original message converted to upper case.

        #    Example: for "hello", the response should be:
        #    b"OK: HELLO"

        # 4. Send the response back to the client with sendall().

        print('[CLIENT] ', self.client_address[0], ':', self.client_address[1], ' connected')
        print('[CLIENT] Sent ', len(self.data), ' bytes: ', self.data.decode())

        response = b"OK: " + self.data.upper()
        self.request.sendall(response)

        # <<< STUDENT CODE ENDS HERE


class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ensure we can restart the server immediately on the same port.
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

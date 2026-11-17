"""S02 – Template TCP server (student task)

This file contains a minimal TCP server based on Python's `socketserver` module.

Students are expected to complete the TODO section inside `MyTCPHandler.handle()`.
"""

import socketserver


class MyTCPHandler(socketserver.StreamRequestHandler):
    """Request handler for our TCP server.

    This class is instantiated once for each new connection.
    """

    def handle(self):
        """Student TODO:

        Adapt the logic so that:

        - you print the client's port as well as its IP address
        - you print the length of the received message (in bytes)
        - you send back a response of the form:
          b"OK: " + <original message converted to uppercase>

        Hint:
        - self.client_address is a tuple (ip, port)
        - len(self.data) gives the message length (in bytes)
        """
        # TCP is a stream: read one bounded LF-terminated message at a time.
        while True:
            line = self.rfile.readline(1025)
            if not line:
                break
            if len(line) > 1024 or not line.endswith(b"\n"):
                self.request.sendall(b"ERR invalid line\n")
                break
            self.data = line[:-1].removesuffix(b"\r")

            # >>> STUDENT CODE STARTS HERE

            # 1. Print the client's IP and port in the format:
            #    [CLIENT] <ip>:<port> connected
            #    Use self.client_address.

            # 2. Print the message content and its length:
            #    [CLIENT] Sent <len> bytes: <message>

            # 3. Build a response that starts with b"OK: "
            #    followed by the original message converted to uppercase.
            #
            #    Example: for "hello", the response should be:
            #    b"OK: HELLO"

            # 4. Send the response back to the client with sendall(), including the terminating LF.

            # <<< STUDENT CODE ENDS HERE


class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ensure we can restart the server immediately on the same port.
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 12345

    with MyTCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"[INFO] TCP server listening on {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down server...")
            server.shutdown()

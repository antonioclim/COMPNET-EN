#!/usr/bin/env python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

"""
Seminar 9 – Server FTP pyftpdlib pentru Docker.

Directorul /app/test este montat din ./server-data
Directorul /app/nobody este montat din ./server-anon
"""

def main():
    authorizer = DummyAuthorizer()

    # user "test" cu parola "12345", radacina /app/test
    authorizer.add_user(
        "test",
        "12345",
        "./test",
        perm="elradfmwMT"
    )

    # anonymous user, read-only, radacina /app/nobody
    authorizer.add_anonymous("./nobody")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", 2121), handler)

    print("Server FTP pyftpdlib pornit pe portul 2121 (in container)...")
    print("Utilizator: test / 12345, root=./test")

    server.serve_forever()


if __name__ == "__main__":
    main()

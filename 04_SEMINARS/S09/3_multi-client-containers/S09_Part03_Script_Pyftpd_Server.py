#!/usr/bin/env python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

"""
Seminar 9 -- FTP server (pyftpdlib) for Docker.

The /app/test directory is mounted from ./server-data
The /app/nobody directory is mounted from ./server-anon
"""

def main():
    authorizer = DummyAuthorizer()

    # user "test" with password "12345", root /app/test
    authorizer.add_user(
        "test",
        "12345",
        "./test",
        perm="elradfmwMT"
    )

    # anonymous user, read-only, root /app/nobody
    authorizer.add_anonymous("./nobody")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", 2121), handler)

    print("FTP server (pyftpdlib) started on port 2121 (in container)...")
    print("User: test / 12345, root=./test")

    server.serve_forever()


if __name__ == "__main__":
    main()

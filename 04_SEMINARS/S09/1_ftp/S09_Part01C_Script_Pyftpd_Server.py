#!/usr/bin/env python3
"""
Seminar 9 -- Minimal FTP server using pyftpdlib.

This server:
 - defines two users (test and anonymous)
 - allows listing, reading and writing files
 - listens on port 2121 (FTP control port)
 - uses dynamic ports for data connections
"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def main():
    # Create the object that manages users.
    authorizer = DummyAuthorizer()

    # Add a user with password and dedicated directory.
    # Permissions: elradfmwMT = almost everything (list, read, write, mkdir etc.)
    authorizer.add_user(
        'test',           # username
        '12345',          # password
        './test',         # root directory for the user
        perm='elradfmwMT'
    )

    # Enable an anonymous user as well, with read-only access.
    authorizer.add_anonymous('./nobody')

    # Handler that will manage FTP connections
    handler = FTPHandler
    handler.authorizer = authorizer

    # FTP server listens locally on port 2121
    server = FTPServer(('0.0.0.0', 2121), handler)

    print("FTP server (pyftpdlib) started on port 2121...")
    print("User: test / 12345")

    # Run the server (blocking)
    server.serve_forever()


if __name__ == '__main__':
    main()

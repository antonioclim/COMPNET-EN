#!/usr/bin/env python3
"""
Seminar 9 – Server FTP minimal folosind pyftpdlib.

Acest server:
 - definește doi utilizatori (test și anonymous)
 - permite listarea, citirea și scrierea fișierelor
 - ascultă pe portul 2121 (FTP control port)
 - folosește porturi dinamice pentru conexiunile de date
"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def main():
    # Creează obiectul care gestionează utilizatorii.
    authorizer = DummyAuthorizer()

    # Adaugă un utilizator cu parolă și director propriu.
    # Permisiuni: elradfmwMT = aproape tot (list, read, write, mkdir etc.)
    authorizer.add_user(
        'test',           # username
        '12345',          # password
        './test',         # directory root pentru utilizator
        perm='elradfmwMT'
    )

    # Activăm și un utilizator anonim, doar cu read.
    authorizer.add_anonymous('./nobody')

    # Handlerul care va gestiona conexiunile FTP
    handler = FTPHandler
    handler.authorizer = authorizer

    # Server FTP ascultă local pe portul 2121
    server = FTPServer(('0.0.0.0', 2121), handler)

    print("Server FTP pyftpdlib pornit pe portul 2121...")
    print("Utilizator: test / 12345")

    # Rulează serverul (blochează)
    server.serve_forever()


if __name__ == '__main__':
    main()

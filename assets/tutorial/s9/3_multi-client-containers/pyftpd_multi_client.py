#!/usr/bin/env python3
"""
Seminar 9 – Client FTP pentru scenariul multi-client in Docker.

Acest script:
 - se conecteaza la serverul FTP (host: ftp-server, port: 2121)
 - se logheaza cu userul "test"/"12345"
 - poate face operatie de upload (STOR) sau download (RETR)
 - foloseste directorul local /app/client-data din container

Mod de utilizare in container:

    # upload:
    python3 pyftpd_multi_client.py upload from_client1.txt

    # download:
    python3 pyftpd_multi_client.py download from_client1.txt

"""

import sys
import os
from ftplib import FTP

SERVER_HOST = "ftp-server"
SERVER_PORT = 2121
USERNAME = "test"
PASSWORD = "12345"

LOCAL_DIR = "./client-data"


def upload_file(filename: str):
    os.makedirs(LOCAL_DIR, exist_ok=True)
    filepath = os.path.join(LOCAL_DIR, filename)

    if not os.path.isfile(filepath):
        print(f"[CLIENT] Fișier local {filepath} nu există, nu pot face upload.")
        return

    ftp = FTP()
    print(f"[CLIENT] Conectare la FTP {SERVER_HOST}:{SERVER_PORT} ...")
    ftp.connect(SERVER_HOST, SERVER_PORT)
    ftp.login(USERNAME, PASSWORD)
    print("[CLIENT] Login reușit.")

    with open(filepath, "rb") as f:
        print(f"[CLIENT] Urc fișierul {filename} pe server...")
        ftp.storbinary(f"STOR {filename}", f)

    print("[CLIENT] Upload complet.")
    print("[CLIENT] Lista fișiere pe server după upload:")
    ftp.retrlines("LIST")

    ftp.quit()


def download_file(filename: str):
    os.makedirs(LOCAL_DIR, exist_ok=True)
    filepath = os.path.join(LOCAL_DIR, filename)

    ftp = FTP()
    print(f"[CLIENT] Conectare la FTP {SERVER_HOST}:{SERVER_PORT} ...")
    ftp.connect(SERVER_HOST, SERVER_PORT)
    ftp.login(USERNAME, PASSWORD)
    print("[CLIENT] Login reușit.")

    with open(filepath, "wb") as f:
        print(f"[CLIENT] Descarc fișierul {filename} de pe server...")
        try:
            ftp.retrbinary(f"RETR {filename}", f.write)
            print("[CLIENT] Download complet.")
        except Exception as e:
            print(f"[CLIENT] Eroare la download: {e}")
            os.remove(filepath)

    print("[CLIENT] Lista fișiere pe server:")
    ftp.retrlines("LIST")

    ftp.quit()


def main():
    if len(sys.argv) < 3:
        print("Utilizare:")
        print("  python3 pyftpd_multi_client.py upload <filename>")
        print("  python3 pyftpd_multi_client.py download <filename>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    if mode == "upload":
        upload_file(filename)
    elif mode == "download":
        download_file(filename)
    else:
        print("Mod necunoscut. Folosiți 'upload' sau 'download'.")


if __name__ == "__main__":
    main()

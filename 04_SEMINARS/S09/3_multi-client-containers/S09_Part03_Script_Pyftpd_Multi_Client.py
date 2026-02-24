#!/usr/bin/env python3
"""
Seminar 9 -- FTP client for the multi-client Docker scenario.

This script:
 - connects to the FTP server (host: ftp-server, port: 2121)
 - logs in with user "test"/"12345"
 - can perform an upload (STOR) or download (RETR) operation
 - uses the local directory /app/client-data inside the container

Usage inside a container:

    # upload:
    python3 S09_Part03_Script_Pyftpd_Multi_Client.py upload from_client1.txt

    # download:
    python3 S09_Part03_Script_Pyftpd_Multi_Client.py download from_client1.txt

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
        print(f"[CLIENT] Local file {filepath} does not exist, cannot upload.")
        return

    ftp = FTP()
    print(f"[CLIENT] Connecting to FTP {SERVER_HOST}:{SERVER_PORT} ...")
    ftp.connect(SERVER_HOST, SERVER_PORT)
    ftp.login(USERNAME, PASSWORD)
    print("[CLIENT] Login successful.")

    with open(filepath, "rb") as f:
        print(f"[CLIENT] Uploading file {filename} to server...")
        ftp.storbinary(f"STOR {filename}", f)

    print("[CLIENT] Upload complete.")
    print("[CLIENT] File list on server after upload:")
    ftp.retrlines("LIST")

    ftp.quit()


def download_file(filename: str):
    os.makedirs(LOCAL_DIR, exist_ok=True)
    filepath = os.path.join(LOCAL_DIR, filename)

    ftp = FTP()
    print(f"[CLIENT] Connecting to FTP {SERVER_HOST}:{SERVER_PORT} ...")
    ftp.connect(SERVER_HOST, SERVER_PORT)
    ftp.login(USERNAME, PASSWORD)
    print("[CLIENT] Login successful.")

    with open(filepath, "wb") as f:
        print(f"[CLIENT] Downloading file {filename} from server...")
        try:
            ftp.retrbinary(f"RETR {filename}", f.write)
            print("[CLIENT] Download complete.")
        except Exception as e:
            print(f"[CLIENT] Download error: {e}")
            os.remove(filepath)

    print("[CLIENT] File list on server:")
    ftp.retrlines("LIST")

    ftp.quit()


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 S09_Part03_Script_Pyftpd_Multi_Client.py upload <filename>")
        print("  python3 S09_Part03_Script_Pyftpd_Multi_Client.py download <filename>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    if mode == "upload":
        upload_file(filename)
    elif mode == "download":
        download_file(filename)
    else:
        print("Unknown mode. Use 'upload' or 'download'.")


if __name__ == "__main__":
    main()

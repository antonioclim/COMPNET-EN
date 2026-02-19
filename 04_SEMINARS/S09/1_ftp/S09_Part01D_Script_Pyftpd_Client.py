#!/usr/bin/env python3
"""
Seminar 9 -- Minimal FTP client with ftplib.

Purpose:
 - connect to an FTP server
 - login (default: anonymous)
 - download a file with retrbinary()

The student must modify the code so that:
 - it performs LIST
 - it performs STOR for a local file (upload)
"""

from ftplib import FTP


def main():
    ftp = FTP()

    print("Connecting to FTP server...")
    ftp.connect('127.0.0.1', 2121)

    print("Logging in as anonymous...")
    ftp.login()   # TODO: allow login('test','12345') as well

    print("Server responds with:")
    print(ftp.getwelcome())

    # >>> STUDENT TODO
    # Add display of the file list from the server:
    # ftp.retrlines('LIST')

    # >>> STUDENT TODO
    # Download a file from the server (if it exists)
    # e.g.:
    # with open('downloaded.txt','wb') as fp:
    #     ftp.retrbinary('RETR a.txt', fp.write)

    # >>> STUDENT TODO
    # Upload a file to the server
    # e.g.:
    # with open('localfile.txt','rb') as fp:
    #     ftp.storbinary("STOR uploaded.txt", fp)

    ftp.quit()
    print("Connection closed.")


if __name__ == '__main__':
    main()

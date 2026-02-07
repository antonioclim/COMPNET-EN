
#!/usr/bin/env python3
"""
Seminar 9 – Client FTP minimal cu ftplib.

Scop:
 - conectare la server ftp
 - login (implicit: anonymous)
 - descărcarea unui fișier cu retrbinary()

Studentul trebuie să modifice codul astfel încât:
 - să facă LIST
 - să facă STOR pentru un fișier local (upload)
"""

from ftplib import FTP


def main():
    ftp = FTP()

    print("Conectare la server FTP...")
    ftp.connect('127.0.0.1', 2121)

    print("Logare ca anonymous...")
    ftp.login()   # TODO: permiteți și login('test','12345')

    print("Serverul răspunde cu:")
    print(ftp.getwelcome())

    # >>> STUDENT TODO
    # Adăugați afișarea listei de fișiere din server:
    # ftp.retrlines('LIST')

    # >>> STUDENT TODO
    # Descărcați un fișier de pe server (dacă există)
    # ex:
    # with open('downloaded.txt','wb') as fp:
    #     ftp.retrbinary('RETR a.txt', fp.write)

    # >>> STUDENT TODO
    # Urcați un fișier în server
    # ex:
    # with open('localfile.txt','rb') as fp:
    #     ftp.storbinary("STOR uploaded.txt", fp)

    ftp.quit()
    print("Conexiune închisă.")


if __name__ == '__main__':
    main()


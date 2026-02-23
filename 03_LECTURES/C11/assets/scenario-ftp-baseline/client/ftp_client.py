from ftplib import FTP
import os

HOST = os.environ.get("FTP_HOST", "ftp")
PORT = int(os.environ.get("FTP_PORT", "2121"))

def run(passive=True):
    ftp = FTP()
    ftp.connect(HOST, PORT, timeout=10)
    ftp.login("student", "student")
    ftp.set_pasv(passive)

    print("PASSIVE =", passive)
    print("PWD =", ftp.pwd())
    print("LIST:")
    ftp.retrlines("LIST")

    # upload + download
    data = b"hello ftp\n"
    with open("hello.txt", "wb") as f:
        f.write(data)

    with open("hello.txt", "rb") as f:
        ftp.storbinary("STOR hello.txt", f)

    with open("hello-down.txt", "wb") as f:
        ftp.retrbinary("RETR hello.txt", f.write)

    ftp.quit()
    print("done")

if __name__ == "__main__":
    run(passive=True)
    run(passive=False)

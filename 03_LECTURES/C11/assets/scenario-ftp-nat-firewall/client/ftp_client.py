from ftplib import FTP
import os

# Client sees FTP via NAT box as default gateway route; but docker DNS name works
HOST = os.environ.get("FTP_HOST", "ftp")
PORT = int(os.environ.get("FTP_PORT", "2121"))

def run(passive):
    ftp = FTP()
    ftp.connect(HOST, PORT, timeout=10)
    ftp.login("student", "student")
    ftp.set_pasv(passive)
    print("PASSIVE =", passive)
    ftp.retrlines("LIST")
    ftp.quit()

if __name__ == "__main__":
    # Run once with passive=True (should work)
    # then with passive=False (active) and discuss why it may fail in real topologies
    run(passive=True)
    run(passive=False)

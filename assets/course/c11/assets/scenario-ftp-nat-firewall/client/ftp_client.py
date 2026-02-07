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
    # Ruleaza o data cu passive=True (ar trebui sa mearga)
    # apoi cu passive=False (active) si discuta de ce poate pica in topologii reale
    run(passive=True)
    run(passive=False)

from ftplib import FTP, all_errors
import os

HOST = os.environ.get("FTP_HOST", "natfw")
PORT = int(os.environ.get("FTP_PORT", "2121"))

def run(passive):
    with FTP() as ftp:
        ftp.connect(HOST, PORT, timeout=10)
        ftp.login("student", "student")
        ftp.set_pasv(passive)
        print("PASSIVE =", passive)
        ftp.retrlines("LIST")
        ftp.quit()

if __name__ == "__main__":
    run(passive=True)  # Failure here is a genuine baseline connectivity failure.
    try:
        run(passive=False)
    except all_errors as exc:
        print("Expected active-mode limitation through this DNAT path:", exc)
        print("Inspect PORT/EPRT and the control reply; do not infer a data transfer.")
    else:
        raise SystemExit("Active mode unexpectedly succeeded: inspect the actual packet path.")

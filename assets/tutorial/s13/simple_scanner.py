# simple_scanner.py
#
# Scanner TCP minimal
# --------------------
# Obiectiv:
#   - scanează o adresă IP
#   - încearcă să se conecteze la fiecare port dintr-un interval
#   - raportează porturile deschise
#
# În acest stage, studenții trebuie să completeze secțiunile marcate
# cu "STUDENT CODE".

import socket
import sys

TARGET = "172.20.0.10"   # poate fi modificat de student
PORT_START = 1
PORT_END = 1024
TIMEOUT = 0.2

def scan_port(ip, port):
    """
    Încearcă o conexiune TCP către (ip, port).
    Folosește connect_ex pentru a evita excepțiile.
    Returnează True dacă portul este deschis.
    """

    # STUDENT CODE STARTS HERE
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    result = s.connect_ex((ip, port))
    s.close()

    return result == 0
    # STUDENT CODE ENDS HERE


def main():
    print(f"Scanning {TARGET} ports {PORT_START}-{PORT_END}")

    for port in range(PORT_START, PORT_END + 1):
        # STUDENT CODE STARTS HERE
        try:
            if scan_port(TARGET, port):
                print(f"[OPEN] {port}")
        except KeyboardInterrupt:
            print("\nScan interrupted.")
            sys.exit(0)
        # STUDENT CODE ENDS HERE

    print("Scan complete.")

if __name__ == "__main__":
    main()

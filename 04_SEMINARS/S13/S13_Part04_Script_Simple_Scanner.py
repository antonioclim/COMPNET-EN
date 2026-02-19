# S13_Part04_Script_Simple_Scanner.py
#
# Minimal TCP Scanner
# --------------------
# Objective:
#   - scan an IP address
#   - attempt to connect to each port in a given range
#   - report open ports
#
# In this stage, students must complete the sections marked
# with "STUDENT CODE".

import socket
import sys

TARGET = "172.20.0.10"   # can be changed by the student
PORT_START = 1
PORT_END = 1024
TIMEOUT = 0.2

def scan_port(ip, port):
    """
    Attempts a TCP connection to (ip, port).
    Uses connect_ex to avoid exceptions.
    Returns True if the port is open.
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

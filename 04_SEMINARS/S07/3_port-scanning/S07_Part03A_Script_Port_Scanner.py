#!/usr/bin/env python3
import socket
import sys
from typing import List

"""
Seminar 7 -- Mini TCP Port Scanner (connect scan)

This script scans a list of ports on a given host using
TCP connections (connect()) with a timeout.

The student must:
 - iterate through the list of ports
 - attempt to connect to each port
 - handle exceptions (closed port, timeout)
 - display for each port whether it is:
      OPEN    (connection succeeded)
      CLOSED  (connection refused)
      FILTERED (timeout, no response)

Sections marked with
    # >>> STUDENT TODO
must be completed.

Execution:

    python3 port_scanner.py <HOST> <START_PORT> <END_PORT>

Examples:

    python3 port_scanner.py 127.0.0.1 1 1024
    python3 port_scanner.py 10.0.10.2 20 100
"""


def scan_port(host: str, port: int, timeout: float = 0.5) -> str:
    """
    Scan a single TCP port on the given host.

    Returns a string:
      - "OPEN"
      - "CLOSED"
      - "FILTERED"

    Protocol:
      - use socket.AF_INET, socket.SOCK_STREAM (TCP)
      - set the timeout
      - attempt connect()
      - if it succeeds -> OPEN
      - if ConnectionRefusedError -> CLOSED
      - if timeout (socket.timeout) -> FILTERED
      - for other exceptions, print a message and treat as CLOSED/FILTERED (your choice)
    """

    # >>> STUDENT TODO: implement the logic below

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((host, port))
        s.close()
        return "OPEN"
    except ConnectionRefusedError:
        s.close()
        return "CLOSED"
    except socket.timeout:
        s.close()
        return "FILTERED"
    except Exception as e:
        # You may log the exception for debugging
        # print(f"[DEBUG] Port {port}: exception {e}")
        s.close()
        return "CLOSED"


def scan_range(host: str, start_port: int, end_port: int) -> List[str]:
    """
    Scan ports in the range [start_port, end_port] inclusive.

    Returns a list of strings of the form:
        "PORT <port> <STATE>"

    Example:
        "PORT 22 OPEN"
        "PORT 80 CLOSED"
    """

    results = []

    # >>> STUDENT TODO:
    # 1. Iterate through all ports from start_port to end_port (inclusive).
    # 2. For each port, call scan_port(host, port).
    # 3. Create a string of the form "PORT <port> <STATE>" and add it to results.
    # 4. Optionally: display progress on screen while scanning.

    for port in range(start_port, end_port + 1):
        state = scan_port(host, port)
        line = f"PORT {port} {state}"
        print(line)
        results.append(line)

    return results


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <HOST> <START_PORT> <END_PORT>")
        print("Example: python3 port_scanner.py 127.0.0.1 1 1024")
        sys.exit(1)

    host = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Invalid port range.")
        sys.exit(1)

    print(f"[INFO] Scanning host {host} on ports {start_port}-{end_port} ...")

    results = scan_range(host, start_port, end_port)

    # Save the results to a text file
    output_file = "S07_Part03_Output_Scan_Results.txt"
    with open(output_file, "w") as f:
        for line in results:
            f.write(line + "\n")

    print(f"[INFO] Scan complete. Results saved to {output_file}.")


if __name__ == "__main__":
    main()

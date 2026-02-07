#!/usr/bin/env python3
import socket
import sys
from typing import List

"""
Seminar 7 – Mini port-scanner TCP (connect scan)

Acest script scaneaza o lista de porturi pe un host dat, folosind
conexiuni TCP (connect()) cu timeout.

Studentul trebuie sa:
 - parcurga lista de porturi
 - incerce sa se conecteze la fiecare port
 - trateze exceptiile (port inchis, timeout)
 - afiseze pentru fiecare port daca este:
      OPEN    (conexiune reusita)
      CLOSED  (connection refused)
      FILTERED (timeout, nici un raspuns)

Zonele marcate cu
    # >>> STUDENT TODO
trebuie completate.

Rulare:

    python3 port_scanner.py <HOST> <START_PORT> <END_PORT>

Exemple:

    python3 port_scanner.py 127.0.0.1 1 1024
    python3 port_scanner.py 10.0.10.2 20 100
"""


def scan_port(host: str, port: int, timeout: float = 0.5) -> str:
    """
    Scaneaza un singur port TCP pe host-ul dat.

    Intoarce un string:
      - "OPEN"
      - "CLOSED"
      - "FILTERED"

    Protocol:
      - folosim socket.AF_INET, socket.SOCK_STREAM (TCP)
      - setam timeout
      - incercam connect()
      - daca reuseste -> OPEN
      - daca primim ConnectionRefusedError -> CLOSED
      - daca primim timeout (socket.timeout) -> FILTERED
      - pentru alte exceptii, afisam un mesaj si consideram CLOSED/FILTERED (la alegere)
    """

    # >>> STUDENT TODO: implementati logica de mai jos

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
        # Puteti loga exceptia pentru debugging
        # print(f"[DEBUG] Port {port}: exceptie {e}")
        s.close()
        return "CLOSED"


def scan_range(host: str, start_port: int, end_port: int) -> List[str]:
    """
    Scaneaza porturile din intervalul [start_port, end_port] inclusiv.

    Intoarce o lista de string-uri de forma:
        "PORT <port> <STATE>"

    Exemplu:
        "PORT 22 OPEN"
        "PORT 80 CLOSED"
    """

    results = []

    # >>> STUDENT TODO:
    # 1. Parcurgeti toate porturile de la start_port la end_port (inclusiv).
    # 2. Pentru fiecare port, apelati scan_port(host, port).
    # 3. Creati un string de forma "PORT <port> <STATE>" si adaugati-l in results.
    # 4. Optional: afisati progresul pe ecran in timp ce scanati.

    for port in range(start_port, end_port + 1):
        state = scan_port(host, port)
        line = f"PORT {port} {state}"
        print(line)
        results.append(line)

    return results


def main():
    if len(sys.argv) < 4:
        print(f"Utilizare: {sys.argv[0]} <HOST> <START_PORT> <END_PORT>")
        print("Exemplu: python3 port_scanner.py 127.0.0.1 1 1024")
        sys.exit(1)

    host = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Interval de porturi invalid.")
        sys.exit(1)

    print(f"[INFO] Scanez host-ul {host} pe porturile {start_port}-{end_port} ...")

    results = scan_range(host, start_port, end_port)

    # Salvam rezultatele intr-un fisier text
    output_file = "scan_results.txt"
    with open(output_file, "w") as f:
        for line in results:
            f.write(line + "\n")

    print(f"[INFO] Scanare terminata. Rezultatele au fost salvate in {output_file}.")


if __name__ == "__main__":
    main()

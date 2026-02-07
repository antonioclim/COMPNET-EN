#!/usr/bin/env python3
import socket
import struct
import sys
import time

"""
Seminar 7 – Detectarea unui port scan simplu (TCP SYN scan / connect scan)

Acest script:
 - asculta pachete la nivel Ethernet (AF_PACKET)
 - filtreaza pachetele IPv4 cu protocol TCP
 - verifica flag-urile TCP pentru a detecta SYN-uri
 - numara, pentru fiecare adresa sursa, cate porturi diferite sondeaza
   intr-o fereastra de timp scurta (ex: 5 secunde)
 - daca numarul de porturi atinge un prag (ex: 10), afiseaza un mesaj
   de alerta: "probabil port scan"

Zonele marcate cu
    # >>> STUDENT TODO
trebuie completate / ajustate de voi.

Rulare (NECESITA sudo):

    sudo python3 detect_scan.py <INTERFATA>

Exemple:

    sudo python3 detect_scan.py eth0
    h2 sudo python3 detect_scan.py h2-eth0   (in Mininet)
"""

# Configuratie pentru detectie
WINDOW_SECONDS = 5       # fereastra de timp (secunde)
PORT_THRESHOLD = 10      # numar de porturi distincte in fereastra => alerta


def ipv4_addr(raw_ip: bytes) -> str:
    return ".".join(str(b) for b in raw_ip)


def parse_ethernet_header(data: bytes):
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    return dest_mac, src_mac, proto, data[14:]


def parse_ipv4_header(data: bytes):
    version_ihl = data[0]
    ihl = (version_ihl & 0x0F) * 4
    ttl, proto, src, dst = struct.unpack("! 8x B B 2x 4s 4s", data[:20])
    src_ip_str = ipv4_addr(src)
    dst_ip_str = ipv4_addr(dst)
    return src_ip_str, dst_ip_str, proto, ihl


def parse_tcp_header(data: bytes):
    """
    Parseaza header-ul TCP pentru a obtine:
      - port sursa
      - port destinatie
      - flag-uri

    structura minimala:
      - source port (2 octeti)
      - dest port (2 octeti)
      - seq (4 octeti)
      - ack (4 octeti)
      - offset+reserved+flags (2 octeti)
      - rest...
    """
    if len(data) < 20:
        return None, None, None

    src_port, dst_port, seq, ack, offset_reserved_flags = struct.unpack(
        "! H H L L H", data[:14]
    )
    # offset (4 biti superiori)
    offset = (offset_reserved_flags >> 12) * 4
    # flag-urile sunt in ultimii 9 biti, dar pentru noi e suficient:
    # bitii de mai jos (TCP flags standard):
    #  CWR | ECE | URG | ACK | PSH | RST | SYN | FIN
    # Vom extrage doar SYN, ACK, FIN pentru exemplu.
    flags = offset_reserved_flags & 0x01FF

    # SYN este bitul 1 (daca numerotam FIN=1, SYN=2 etc.) – dar implementarea
    # poate varia, asa ca vom folosi o masca pentru SYN:
    # Valori tipice: FIN=0x001, SYN=0x002, RST=0x004, PSH=0x008,
    #                ACK=0x010, URG=0x020, ECE=0x040, CWR=0x080
    syn_flag = bool(flags & 0x002)
    ack_flag = bool(flags & 0x010)
    fin_flag = bool(flags & 0x001)

    return src_port, dst_port, {"SYN": syn_flag, "ACK": ack_flag, "FIN": fin_flag}


def main():
    if len(sys.argv) < 2:
        print(f"Utilizare: sudo {sys.argv[0]} <INTERFATA>")
        print("Exemplu: sudo python3 detect_scan.py eth0")
        sys.exit(1)

    interface = sys.argv[1]

    try:
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    except PermissionError:
        print("Eroare: trebuie sa rulati cu privilegii de root (sudo).")
        sys.exit(1)

    try:
        sniffer.bind((interface, 0))
    except OSError as e:
        print(f"Eroare la bind pe interfata {interface}: {e}")
        sys.exit(1)

    print(f"[INFO] Pornim detect_scan pe interfata {interface}")
    print(f"[INFO] Fereastra={WINDOW_SECONDS}s, prag porturi={PORT_THRESHOLD}")
    print("[INFO] Oprire cu Ctrl-C.\n")

    # Structura pentru contorizare:
    # scan_state = {
    #   "SRC_IP": {
    #       "ports": { port1: timestamp1, port2: timestamp2, ... },
    #   },
    #   ...
    # }
    scan_state = {}

    try:
        while True:
            raw_data, addr = sniffer.recvfrom(65535)
            now = time.time()

            dest_mac, src_mac, eth_proto, payload = parse_ethernet_header(raw_data)

            # Ne intereseaza doar IPv4
            if eth_proto != 0x0800:
                continue

            src_ip, dst_ip, proto, ip_header_len = parse_ipv4_header(payload)

            # Ne intereseaza doar TCP
            if proto != 6:
                continue

            ip_payload = payload[ip_header_len:]
            src_port, dst_port, flags = parse_tcp_header(ip_payload)
            if src_port is None:
                continue

            # Ne intereseaza în special pachetele cu SYN (inceput de conexiune)
            # si, optional, fara ACK (SYN "initial")
            is_syn = flags and flags.get("SYN", False)
            is_ack = flags and flags.get("ACK", False)

            # >>> STUDENT TODO:
            # Puteti decide ce considerati ca fiind "probabil scan":
            # - contorizam doar pachetele SYN fara ACK (probabil inceput de conexiune)
            # - sau contorizam si altele
            #
            # Pentru inceput, vom contoriza doar SYN fara ACK.

            if not (is_syn and not is_ack):
                continue

            # Initializam structuri pentru sursa curenta daca nu exista
            if src_ip not in scan_state:
                scan_state[src_ip] = {"ports": {}}

            # Scoatem porturile vechi (in afara ferestrei de timp) din dictionar
            ports_dict = scan_state[src_ip]["ports"]
            to_delete = []
            for p, ts in ports_dict.items():
                if now - ts > WINDOW_SECONDS:
                    to_delete.append(p)
            for p in to_delete:
                del ports_dict[p]

            # Inregistram portul curent cu timestamp
            ports_dict[dst_port] = now

            # Numar de porturi distincte in fereastra
            port_count = len(ports_dict)

            # Afisam ceva debug (optional)
            # print(f"[DEBUG] {src_ip} -> port {dst_port}, {port_count} porturi in {WINDOW_SECONDS}s")

            # Daca depasim pragul -> ALERTA
            if port_count >= PORT_THRESHOLD:
                print(f"[ALERT] Posibil port scan de la {src_ip}: "
                      f"{port_count} porturi diferite in ultimele {WINDOW_SECONDS} secunde")
                # Putem sa "resetam" starea pentru acest IP sau nu, la alegere:
                # ports_dict.clear()

    except KeyboardInterrupt:
        print("\n[INFO] Oprit de utilizator (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] detect_scan oprit.")


if __name__ == "__main__":
    main()

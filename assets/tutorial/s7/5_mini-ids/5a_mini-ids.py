#!/usr/bin/env python3
import socket
import struct
import sys
import time

"""
Seminar 7 – mini IDS (Intrusion Detection System) simplu

Acest script combina ideile din etapele anterioare:

 - sniffer de pachete IPv4 (AF_PACKET)
 - analiza TCP si UDP (porturi, flag-uri)
 - detectarea unui port scan TCP (multi-port)
 - detectarea unui "spray" UDP (multi-port)
 - detectarea unui posibil flood catre un anumit port

Studentul trebuie sa completeze logica de detectie si functia de log.

Zonele marcate cu:
    # >>> STUDENT TODO
trebuie completate.

Rulare (NECESITA sudo):

    sudo python3 mini_ids.py <INTERFATA>

Exemple:

    sudo python3 mini_ids.py eth0
    h2 sudo python3 mini_ids.py h2-eth0   (in Mininet)
"""

# ------------------ CONFIGURARE IDS ------------------

WINDOW_SECONDS = 5           # fereastra de timp pentru contorizare
TCP_SYN_THRESHOLD = 10       # SYN catre porturi diferite in fereastra => port scan
UDP_PORT_THRESHOLD = 10      # UDP catre porturi diferite in fereastra => UDP spray
FLOOD_THRESHOLD = 50         # pachete catre acelasi (dst_ip, dst_port) in fereastra => flood suspicios

ALERT_LOG_FILE = "ids_alerts.log"


# ------------------ FUNCTII UTILE PENTRU PARSARE ------------------

def ipv4_addr(raw_ip: bytes) -> str:
    return ".".join(str(b) for b in raw_ip)


def parse_ethernet_header(data: bytes):
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    return dest_mac, src_mac, proto, data[14:]


def parse_ipv4_header(data: bytes):
    if len(data) < 20:
        return None, None, None, None
    version_ihl = data[0]
    ihl = (version_ihl & 0x0F) * 4
    ttl, proto, src, dst = struct.unpack("! 8x B B 2x 4s 4s", data[:20])
    src_ip_str = ipv4_addr(src)
    dst_ip_str = ipv4_addr(dst)
    return src_ip_str, dst_ip_str, proto, ihl


def parse_tcp_header(data: bytes):
    if len(data) < 20:
        return None, None, None

    src_port, dst_port, seq, ack, offset_reserved_flags = struct.unpack(
        "! H H L L H", data[:14]
    )
    flags = offset_reserved_flags & 0x01FF
    syn_flag = bool(flags & 0x002)
    ack_flag = bool(flags & 0x010)
    fin_flag = bool(flags & 0x001)

    return src_port, dst_port, {"SYN": syn_flag, "ACK": ack_flag, "FIN": fin_flag}


def parse_udp_header(data: bytes):
    if len(data) < 8:
        return None, None
    src_port, dst_port, length = struct.unpack("! H H H", data[:6])
    return src_port, dst_port


# ------------------ LOG SI STRUCTURA DE STARE ------------------

def log_alert(message: str):
    """
    Logheaza o alerta atat pe ecran, cat si in fisierul ALERT_LOG_FILE.

    TODO (student):
      - deschideti fisierul in modul append
      - scrieti timestamp + mesaj
      - flush / close
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    print(full_msg)

    # >>> STUDENT TODO: scrieti full_msg intr-un fisier ALERT_LOG_FILE, linie noua

    try:
        with open(ALERT_LOG_FILE, "a") as f:
            f.write(full_msg + "\n")
    except Exception as e:
        # optional: afisati eroarea
        # print(f"[DEBUG] Eroare la scrierea in fisierul de log: {e}")
        pass


def cleanup_old_entries(state_dict, now, window):
    """
    Sterge intrarile mai vechi de 'window' secunde dintr-un dictionar
    de forma:
        { cheie: timestamp }
    unde cheie poate fi un port sau un tuplu (dst_ip, dst_port).
    """
    to_delete = [k for k, ts in state_dict.items() if now - ts > window]
    for k in to_delete:
        del state_dict[k]


# Structura de stare principala:
# ids_state = {
#   "tcp_scan": {
#       src_ip: { dst_port: timestamp, ... }
#   },
#   "udp_spray": {
#       src_ip: { dst_port: timestamp, ... }
#   },
#   "flood": {
#       (dst_ip, dst_port): [timestamps...]
#   }
# }
ids_state = {
    "tcp_scan": {},
    "udp_spray": {},
    "flood": {}
}


# ------------------ LOGICA DE DETECTIE ------------------

def handle_tcp_packet(src_ip, dst_ip, dst_port, flags, now):
    """
    Logica pentru evenimente TCP.

    Vom trata 2 lucruri:
      1) port scan TCP (multi-port SYN fara ACK)
      2) flood catre un anumit (dst_ip, dst_port)

    TODO (student):
      - implementati detectarea port-scan-ului folosind ids_state["tcp_scan"]
      - implementati detectarea flood-ului folosind ids_state["flood"]
    """

    global ids_state

    if dst_port is None or flags is None:
        return

    is_syn = flags.get("SYN", False)
    is_ack = flags.get("ACK", False)

    # ----------------------------------------
    # 1) Detectare port scan TCP (similar cu detect_scan.py)
    # ----------------------------------------
    # Criteriu sugerat:
    #   - contorizam doar pachetele SYN fara ACK
    #   - pentru fiecare src_ip, tinem minte porturile atinse in ultimele WINDOW_SECONDS secunde
    #   - daca numarul de porturi distincte >= TCP_SYN_THRESHOLD => ALERTA

    if is_syn and not is_ack:
        scan_dict = ids_state["tcp_scan"].setdefault(src_ip, {})
        cleanup_old_entries(scan_dict, now, WINDOW_SECONDS)
        scan_dict[dst_port] = now

        port_count = len(scan_dict)
        if port_count >= TCP_SYN_THRESHOLD:
            log_alert(f"Posibil TCP PORT SCAN de la {src_ip}: "
                      f"{port_count} porturi SYN in ultimele {WINDOW_SECONDS}s")
            # optional: resetare
            # scan_dict.clear()

    # ----------------------------------------
    # 2) Detectare flood TCP catre (dst_ip, dst_port)
    # ----------------------------------------
    # Criteriu sugerat:
    #   - pentru fiecare (dst_ip, dst_port), tinem minte un numar de timestamps
    #   - daca lungimea listei in fereastra > FLOOD_THRESHOLD => ALERTA

    key = (dst_ip, dst_port)
    flood_dict = ids_state["flood"].setdefault(key, {})

    # Refolosim dict cu cheie timestamp simplificata (sau un counter)
    cleanup_old_entries(flood_dict, now, WINDOW_SECONDS)
    flood_dict[now] = now

    if len(flood_dict) >= FLOOD_THRESHOLD:
        log_alert(f"Posibil TCP FLOOD catre {dst_ip}:{dst_port} "
                  f"({len(flood_dict)} pachete in ultimele {WINDOW_SECONDS}s)")


def handle_udp_packet(src_ip, dst_ip, dst_port, now):
    """
    Logica pentru evenimente UDP.

    Vom trata:
      - UDP "spray" (multi-port) de la o anumita sursa.

    TODO (student):
      - folositi ids_state["udp_spray"] cu structura similara cu "tcp_scan"
      - daca src_ip atinge >= UDP_PORT_THRESHOLD porturi UDP diferite
        in fereastra WINDOW_SECONDS => ALERTA
    """

    global ids_state

    if dst_port is None:
        return

    spray_dict = ids_state["udp_spray"].setdefault(src_ip, {})
    cleanup_old_entries(spray_dict, now, WINDOW_SECONDS)
    spray_dict[dst_port] = now

    port_count = len(spray_dict)
    if port_count >= UDP_PORT_THRESHOLD:
        log_alert(f"Posibil UDP SPRAY de la {src_ip}: "
                  f"{port_count} porturi UDP in ultimele {WINDOW_SECONDS}s")
        # optional: spray_dict.clear()


# ------------------ BUCLEA PRINCIPALA IDS ------------------

def main():
    if len(sys.argv) < 2:
        print(f"Utilizare: sudo {sys.argv[0]} <INTERFATA>")
        print("Exemplu: sudo python3 mini_ids.py eth0")
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

    print(f"[INFO] Pornim mini_ids pe interfata {interface}")
    print(f"[INFO] WINDOW_SECONDS={WINDOW_SECONDS}, TCP_SYN_THRESHOLD={TCP_SYN_THRESHOLD}, "
          f"UDP_PORT_THRESHOLD={UDP_PORT_THRESHOLD}, FLOOD_THRESHOLD={FLOOD_THRESHOLD}")
    print(f"[INFO] Alerta va fi logata in {ALERT_LOG_FILE}")
    print("[INFO] Oprire cu Ctrl-C.\n")

    try:
        while True:
            raw_data, addr = sniffer.recvfrom(65535)
            now = time.time()

            dest_mac, src_mac, eth_proto, payload = parse_ethernet_header(raw_data)

            # Ne intereseaza doar IPv4
            if eth_proto != 0x0800:
                continue

            src_ip, dst_ip, proto, ip_header_len = parse_ipv4_header(payload)
            if src_ip is None:
                continue

            ip_payload = payload[ip_header_len:]

            # TCP
            if proto == 6:
                src_port, dst_port, flags = parse_tcp_header(ip_payload)
                handle_tcp_packet(src_ip, dst_ip, dst_port, flags, now)

            # UDP
            elif proto == 17:
                src_port, dst_port = parse_udp_header(ip_payload)
                handle_udp_packet(src_ip, dst_ip, dst_port, now)

            # Alte protocoale – ignoram in aceasta versiune
    except KeyboardInterrupt:
        print("\n[INFO] Oprit de utilizator (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] mini_ids oprit.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import socket
import struct
import sys

"""
Seminar 7 – Filtru de pachete (TCP / UDP / IP)

Acest script este o extensie a sniffer-ului simplu. In plus fata de
`packet_sniffer.py`, aici vom:

 - extrage porturile sursa/destinatie pentru TCP si UDP
 - aplica un filtru personalizat in functia `passes_filter`
 - afisa doar pachetele care trec filtrul

Zonele marcate cu
    # >>> STUDENT TODO
trebuie completate de voi.

Rulare (NECESITA sudo):

    sudo python3 packet_filter.py <INTERFATA>

Exemple:

    sudo python3 packet_filter.py eth0
    h1 sudo python3 packet_filter.py h1-eth0
"""

MAX_PACKETS = 100  # numar maxim de pachete de procesat


def mac_addr(raw_mac: bytes) -> str:
    return ":".join(f"{b:02x}" for b in raw_mac)


def ipv4_addr(raw_ip: bytes) -> str:
    return ".".join(str(b) for b in raw_ip)


def parse_ethernet_header(data: bytes):
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    dest_mac_str = mac_addr(dest_mac)
    src_mac_str = mac_addr(src_mac)
    return dest_mac_str, src_mac_str, proto, data[14:]


def parse_ipv4_header(data: bytes):
    """
    Versiunea COMPLETA a parse_ipv4_header din Stage 2.
    Puteti copia aici implementarea voastra din packet_sniffer.py.

    Intoarce:
      (src_ip_str, dst_ip_str, proto, header_length)
    """
    version_ihl = data[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4

    ttl, proto, src, dst = struct.unpack("! 8x B B 2x 4s 4s", data[:20])
    src_ip_str = ipv4_addr(src)
    dst_ip_str = ipv4_addr(dst)
    return src_ip_str, dst_ip_str, proto, ihl


def parse_tcp_header(data: bytes):
    """
    Parseaza header-ul TCP pentru a obtine porturile sursa/destinatie.

    structura (primii 4 octeti):
        - source port (2 octeti)
        - dest port   (2 octeti)

    Intoarce:
      (src_port, dst_port)
    """
    src_port, dst_port = struct.unpack("! H H", data[:4])
    return src_port, dst_port


def parse_udp_header(data: bytes):
    """
    Parseaza header-ul UDP pentru a obtine porturile sursa/destinatie.

    structura (primii 4 octeti):
        - source port (2 octeti)
        - dest port   (2 octeti)

    Intoarce:
      (src_port, dst_port)
    """
    src_port, dst_port = struct.unpack("! H H", data[:4])
    return src_port, dst_port


# -------------------------------------------------------------------------
# FILTRU PERSONALIZAT
# -------------------------------------------------------------------------

def passes_filter(src_ip, dst_ip, proto, src_port=None, dst_port=None) -> bool:
    """
    Aceasta functie decide daca un pachet trece filtrul sau nu.

    Parametri:
      - src_ip, dst_ip: string-uri IPv4 (ex: '10.0.0.1')
      - proto: int (6 = TCP, 17 = UDP, 1 = ICMP etc.)
      - src_port, dst_port: int sau None (doar pentru TCP/UDP)

    TODO (student):
      Implementati aici mai multe reguli de filtrare.
      Puteti porni de la cerintele din fișierul de task-uri.

    Exemple de criterii de implementat (in ordine):

      1) Afiseaza DOAR pachetele TCP (proto == 6).
      2) Afiseaza DOAR pachetele UDP cu port destinatie 53 (DNS).
      3) Afiseaza DOAR pachetele care au adresa sursa dintr-o anumita retea,
         de exemplu 10.0.0.0/8 (string incepe cu '10.').

    Puteti combina criteriile cum doriti, de exemplu:
      - afisati pachetele TCP cu dst_port > 1024
      - afisati pachetele UDP dintr-o anumita sursa

    Deocamdata functia intoarce False pentru toate (nu afiseaza nimic),
    pana o modificati voi.
    """

    # >>> STUDENT TODO: inlocuiti logica de mai jos cu propriul filtru

    # Exemplu simplu (temporar): acceptam tot traficul TCP
    # if proto == 6:
    #     return True

    return False


# -------------------------------------------------------------------------
# BUCLEA PRINCIPALA DE SNIFFING
# -------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(f"Utilizare: sudo {sys.argv[0]} <INTERFATA>")
        print("Exemplu: sudo python3 packet_filter.py eth0")
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

    print(f"[INFO] Pornim packet_filter pe interfata {interface}")
    print(f"[INFO] Vom procesa maximum {MAX_PACKETS} pachete. Oprire cu Ctrl-C.\n")

    packet_count = 0

    try:
        while packet_count < MAX_PACKETS:
            raw_data, addr = sniffer.recvfrom(65535)
            packet_count += 1

            dest_mac, src_mac, eth_proto, payload = parse_ethernet_header(raw_data)

            if eth_proto == 0x0800:  # IPv4
                src_ip, dst_ip, proto, ip_header_len = parse_ipv4_header(payload)
                ip_payload = payload[ip_header_len:]

                src_port = None
                dst_port = None

                proto_str = "ALT"

                # TCP
                if proto == 6 and len(ip_payload) >= 4:
                    src_port, dst_port = parse_tcp_header(ip_payload)
                    proto_str = "TCP"

                # UDP
                elif proto == 17 and len(ip_payload) >= 4:
                    src_port, dst_port = parse_udp_header(ip_payload)
                    proto_str = "UDP"

                elif proto == 1:
                    proto_str = "ICMP"
                else:
                    proto_str = f"ALT({proto})"

                # Aplicam filtrul
                if passes_filter(src_ip, dst_ip, proto, src_port, dst_port):
                    # Afisam doar pachetele care trec de filtru
                    if src_port is not None and dst_port is not None:
                        print(f"{src_ip}:{src_port} -> {dst_ip}:{dst_port}  proto={proto_str}")
                    else:
                        print(f"{src_ip} -> {dst_ip}  proto={proto_str}")

    except KeyboardInterrupt:
        print("\n[INFO] Oprit de utilizator (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] Packet filter oprit.")


if __name__ == "__main__":
    main()

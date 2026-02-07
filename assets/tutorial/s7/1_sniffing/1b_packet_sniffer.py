#!/usr/bin/env python3
import socket
import struct
import sys

"""
Seminar 7 – Sniffer simplu de pachete IPv4

Acest script creeaza un socket RAW si afiseaza informatii de baza
despre pachetele IPv4 care trec printr-o interfata:

 - adresa MAC sursa / destinatie
 - adresa IP sursa / destinatie
 - protocol (TCP / UDP / altul)

Zonele marcate cu
    # >>> STUDENT TODO
trebuie completate de voi.

Rulare (NECESITA sudo):

    sudo python3 packet_sniffer.py <INTERFATA>

Exemple:

    sudo python3 packet_sniffer.py eth0
    sudo python3 packet_sniffer.py lo
    # in Mininet:
    h1 sudo python3 packet_sniffer.py h1-eth0
"""

MAX_PACKETS = 50  # numar maxim de pachete de afisat (puteti modifica)


def mac_addr(raw_mac: bytes) -> str:
    """
    Converteste o adresa MAC in format lizibil, de forma:
    'aa:bb:cc:dd:ee:ff'
    """
    return ":".join(f"{b:02x}" for b in raw_mac)


def ipv4_addr(raw_ip: bytes) -> str:
    """
    Converteste o adresa IPv4 (4 octeti) in format 'x.x.x.x'.
    """
    return ".".join(str(b) for b in raw_ip)


def parse_ethernet_header(data: bytes):
    """
    Parsam header-ul Ethernet (primii 14 octeti):

    structura:
        - destinatie MAC: 6 octeti
        - sursa MAC: 6 octeti
        - ethertype: 2 octeti (0x0800 pentru IPv4)

    Intoarcem:
        (dest_mac_str, src_mac_str, proto) si payload-ul (restul datelor).
    """
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    dest_mac_str = mac_addr(dest_mac)
    src_mac_str = mac_addr(src_mac)
    return dest_mac_str, src_mac_str, proto, data[14:]


def parse_ipv4_header(data: bytes):
    """
    Parsam header-ul IPv4 (minim 20 octeti).

    structura (simplificata):
        - versiune + IHL (1 octet)
        - TOS (1 octet)
        - total length (2 octeti)
        - identificare, flags, fragment offset (4 octeti)
        - TTL (1 octet)
        - protocol (1 octet)
        - checksum (2 octeti)
        - adresa sursa (4 octeti)
        - adresa destinatie (4 octeti)

    Intoarcem:
        (src_ip_str, dst_ip_str, proto, header_length)

    Unde:
        - header_length este in octeti (de ex. 20, 24, 28 etc.)
    """

    # >>> STUDENT TODO
    # 1. Extrage versiunea si IHL (Internet Header Length) din primul octet.
    #    version_ihl = data[0]
    #    version = version_ihl >> 4
    #    ihl = (version_ihl & 0x0F) * 4
    #
    # 2. Foloseste struct.unpack pentru a extrage:
    #       ttl, proto, src, dst
    #    Poti folosi formatul:
    #       '! 8x B B 2x 4s 4s'
    #    care sare peste primele 8 octeti, citeste TTL si protocol,
    #    apoi sare peste checksum si citeste adresele IP.
    #
    # 3. Converteste src si dst in string folosind ipv4_addr().
    #
    # La final intoarce: (src_ip_str, dst_ip_str, proto, ihl)

    # HINT (daca te blochezi, decomenteaza si adapteaza):
    # version_ihl = data[0]
    # version = version_ihl >> 4
    # ihl = (version_ihl & 0x0F) * 4
    # ttl, proto, src, dst = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    # src_ip_str = ipv4_addr(src)
    # dst_ip_str = ipv4_addr(dst)
    # return src_ip_str, dst_ip_str, proto, ihl

    raise NotImplementedError("Completați funcția parse_ipv4_header")


def main():
    if len(sys.argv) < 2:
        print(f"Utilizare: sudo {sys.argv[0]} <INTERFATA>")
        print("Exemplu: sudo python3 packet_sniffer.py eth0")
        sys.exit(1)

    interface = sys.argv[1]

    # Cream un socket RAW la nivel de link (AF_PACKET este specific Linux).
    # htons(0x0003) => primim toate protocoalele (ETH_P_ALL).
    try:
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    except PermissionError:
        print("Eroare: trebuie sa rulati cu privilegii de root (sudo).")
        sys.exit(1)

    # Legam socket-ul de o anumita interfata (ex: 'eth0', 'lo', 'h1-eth0').
    try:
        sniffer.bind((interface, 0))
    except OSError as e:
        print(f"Eroare la bind pe interfata {interface}: {e}")
        sys.exit(1)

    print(f"[INFO] Pornim snifferul pe interfata {interface}")
    print(f"[INFO] Vom afisa maximum {MAX_PACKETS} pachete. Oprire cu Ctrl-C.\n")

    packet_count = 0

    try:
        while packet_count < MAX_PACKETS:
            raw_data, addr = sniffer.recvfrom(65535)

            packet_count += 1

            # 1. Parsam header-ul Ethernet
            dest_mac, src_mac, eth_proto, payload = parse_ethernet_header(raw_data)

            # Afisam doar pachetele IPv4 (Ethertype 0x0800)
            if eth_proto == 0x0800:
                try:
                    src_ip, dst_ip, proto, ip_header_len = parse_ipv4_header(payload)
                except NotImplementedError:
                    print("parse_ipv4_header nu este inca implementata.")
                    break

                # Decodam protocolul in text
                if proto == 6:
                    proto_str = "TCP"
                elif proto == 17:
                    proto_str = "UDP"
                elif proto == 1:
                    proto_str = "ICMP"
                else:
                    proto_str = f"ALT({proto})"

                print(f"[{packet_count}] {src_ip} -> {dst_ip}  proto={proto_str}")
                # Optional: puteti afisa si adresele MAC
                # print(f"    MAC: {src_mac} -> {dest_mac}")

    except KeyboardInterrupt:
        print("\n[INFO] Oprit de utilizator (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] Sniffer oprit.")


if __name__ == "__main__":
    main()

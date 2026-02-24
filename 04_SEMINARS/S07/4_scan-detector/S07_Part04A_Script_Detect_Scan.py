#!/usr/bin/env python3
import socket
import struct
import sys
import time

"""
Seminar 7 -- Detecting a Simple Port Scan (TCP SYN scan / connect scan)

This script:
 - listens for packets at the Ethernet level (AF_PACKET)
 - filters IPv4 packets with TCP protocol
 - inspects TCP flags to detect SYN packets
 - counts, for each source address, how many distinct ports it probes
   within a short time window (e.g. 5 seconds)
 - if the number of ports reaches a threshold (e.g. 10), displays an
   alert message: "probable port scan"

Sections marked with
    # >>> STUDENT TODO
must be completed / adjusted by you.

Execution (REQUIRES sudo):

    sudo python3 detect_scan.py <INTERFACE>

Examples:

    sudo python3 detect_scan.py eth0
    h2 sudo python3 detect_scan.py h2-eth0   (in Mininet)
"""

# Detection configuration
WINDOW_SECONDS = 5       # time window (seconds)
PORT_THRESHOLD = 10      # number of distinct ports within the window => alert


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
    Parse the TCP header to obtain:
      - source port
      - destination port
      - flags

    minimal structure:
      - source port (2 bytes)
      - dest port (2 bytes)
      - seq (4 bytes)
      - ack (4 bytes)
      - offset+reserved+flags (2 bytes)
      - rest...
    """
    if len(data) < 20:
        return None, None, None

    src_port, dst_port, seq, ack, offset_reserved_flags = struct.unpack(
        "! H H L L H", data[:14]
    )
    # offset (upper 4 bits)
    offset = (offset_reserved_flags >> 12) * 4
    # flags are in the lower 9 bits; for our purposes:
    # the bits below (standard TCP flags):
    #  CWR | ECE | URG | ACK | PSH | RST | SYN | FIN
    # We extract only SYN, ACK, FIN for this example.
    flags = offset_reserved_flags & 0x01FF

    # SYN is bit 1 (if we number FIN=1, SYN=2 etc.) — but implementations
    # may vary, so we use a mask for SYN:
    # Typical values: FIN=0x001, SYN=0x002, RST=0x004, PSH=0x008,
    #                ACK=0x010, URG=0x020, ECE=0x040, CWR=0x080
    syn_flag = bool(flags & 0x002)
    ack_flag = bool(flags & 0x010)
    fin_flag = bool(flags & 0x001)

    return src_port, dst_port, {"SYN": syn_flag, "ACK": ack_flag, "FIN": fin_flag}


def main():
    if len(sys.argv) < 2:
        print(f"Usage: sudo {sys.argv[0]} <INTERFACE>")
        print("Example: sudo python3 detect_scan.py eth0")
        sys.exit(1)

    interface = sys.argv[1]

    try:
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    except PermissionError:
        print("Error: you must run with root privileges (sudo).")
        sys.exit(1)

    try:
        sniffer.bind((interface, 0))
    except OSError as e:
        print(f"Error binding to interface {interface}: {e}")
        sys.exit(1)

    print(f"[INFO] Starting detect_scan on interface {interface}")
    print(f"[INFO] Window={WINDOW_SECONDS}s, port threshold={PORT_THRESHOLD}")
    print("[INFO] Stop with Ctrl-C.\n")

    # Counting structure:
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

            # We are interested only in IPv4
            if eth_proto != 0x0800:
                continue

            src_ip, dst_ip, proto, ip_header_len = parse_ipv4_header(payload)

            # We are interested only in TCP
            if proto != 6:
                continue

            ip_payload = payload[ip_header_len:]
            src_port, dst_port, flags = parse_tcp_header(ip_payload)
            if src_port is None:
                continue

            # We are especially interested in packets with SYN (connection initiation)
            # and, optionally, without ACK ("initial" SYN)
            is_syn = flags and flags.get("SYN", False)
            is_ack = flags and flags.get("ACK", False)

            # >>> STUDENT TODO:
            # You may decide what you consider "probable scan":
            # - count only SYN packets without ACK (probable connection initiation)
            # - or count others as well
            #
            # To start, we count only SYN without ACK.

            if not (is_syn and not is_ack):
                continue

            # Initialise structures for the current source if they do not exist
            if src_ip not in scan_state:
                scan_state[src_ip] = {"ports": {}}

            # Remove old ports (outside the time window) from the dictionary
            ports_dict = scan_state[src_ip]["ports"]
            to_delete = []
            for p, ts in ports_dict.items():
                if now - ts > WINDOW_SECONDS:
                    to_delete.append(p)
            for p in to_delete:
                del ports_dict[p]

            # Record the current port with its timestamp
            ports_dict[dst_port] = now

            # Number of distinct ports within the window
            port_count = len(ports_dict)

            # Display some debug info (optional)
            # print(f"[DEBUG] {src_ip} -> port {dst_port}, {port_count} ports in {WINDOW_SECONDS}s")

            # If we exceed the threshold -> ALERT
            if port_count >= PORT_THRESHOLD:
                print(f"[ALERT] Possible port scan from {src_ip}: "
                      f"{port_count} distinct ports in the last {WINDOW_SECONDS} seconds")
                # We may "reset" the state for this IP or not, at your discretion:
                # ports_dict.clear()

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] detect_scan stopped.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import socket
import struct
import sys
import time

"""
Seminar 7 -- mini IDS (Intrusion Detection System)

This script combines ideas from the previous stages:

 - IPv4 packet sniffer (AF_PACKET)
 - TCP and UDP analysis (ports, flags)
 - TCP port scan detection (multi-port)
 - UDP "spray" detection (multi-port)
 - flood detection towards a specific port

The student must complete the detection logic and the logging function.

Sections marked with:
    # >>> STUDENT TODO
must be completed.

Execution (REQUIRES sudo):

    sudo python3 mini_ids.py <INTERFACE>

Examples:

    sudo python3 mini_ids.py eth0
    h2 sudo python3 mini_ids.py h2-eth0   (in Mininet)
"""

# ------------------ IDS CONFIGURATION ------------------

WINDOW_SECONDS = 5           # time window for counting
TCP_SYN_THRESHOLD = 10       # SYN to distinct ports within the window => port scan
UDP_PORT_THRESHOLD = 10      # UDP to distinct ports within the window => UDP spray
FLOOD_THRESHOLD = 50         # packets to the same (dst_ip, dst_port) within the window => suspicious flood

ALERT_LOG_FILE = "ids_alerts.log"


# ------------------ PARSING UTILITY FUNCTIONS ------------------

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


# ------------------ LOG AND STATE STRUCTURE ------------------

def log_alert(message: str):
    """
    Log an alert both on screen and in the ALERT_LOG_FILE.

    TODO (student):
      - open the file in append mode
      - write timestamp + message
      - flush / close
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    print(full_msg)

    # >>> STUDENT TODO: write full_msg to ALERT_LOG_FILE, one line per alert

    try:
        with open(ALERT_LOG_FILE, "a") as f:
            f.write(full_msg + "\n")
    except Exception as e:
        # optional: display the error
        # print(f"[DEBUG] Error writing to log file: {e}")
        pass


def cleanup_old_entries(state_dict, now, window):
    """
    Remove entries older than 'window' seconds from a dictionary
    of the form:
        { key: timestamp }
    where key may be a port or a tuple (dst_ip, dst_port).
    """
    to_delete = [k for k, ts in state_dict.items() if now - ts > window]
    for k in to_delete:
        del state_dict[k]


# Main state structure:
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


# ------------------ DETECTION LOGIC ------------------

def handle_tcp_packet(src_ip, dst_ip, dst_port, flags, now):
    """
    Logic for TCP events.

    We handle two things:
      1) TCP port scan (multi-port SYN without ACK)
      2) flood towards a specific (dst_ip, dst_port)

    TODO (student):
      - implement port-scan detection using ids_state["tcp_scan"]
      - implement flood detection using ids_state["flood"]
    """

    global ids_state

    if dst_port is None or flags is None:
        return

    is_syn = flags.get("SYN", False)
    is_ack = flags.get("ACK", False)

    # ----------------------------------------
    # 1) TCP port scan detection (similar to detect_scan.py)
    # ----------------------------------------
    # Suggested criterion:
    #   - count only SYN packets without ACK
    #   - for each src_ip, track the ports reached in the last WINDOW_SECONDS seconds
    #   - if the number of distinct ports >= TCP_SYN_THRESHOLD => ALERT

    if is_syn and not is_ack:
        scan_dict = ids_state["tcp_scan"].setdefault(src_ip, {})
        cleanup_old_entries(scan_dict, now, WINDOW_SECONDS)
        scan_dict[dst_port] = now

        port_count = len(scan_dict)
        if port_count >= TCP_SYN_THRESHOLD:
            log_alert(f"Possible TCP PORT SCAN from {src_ip}: "
                      f"{port_count} SYN ports in the last {WINDOW_SECONDS}s")
            # optional: reset
            # scan_dict.clear()

    # ----------------------------------------
    # 2) TCP flood detection towards (dst_ip, dst_port)
    # ----------------------------------------
    # Suggested criterion:
    #   - for each (dst_ip, dst_port), track a number of timestamps
    #   - if the list length within the window > FLOOD_THRESHOLD => ALERT

    key = (dst_ip, dst_port)
    flood_dict = ids_state["flood"].setdefault(key, {})

    # Reuse dict with a simplified timestamp key (or a counter)
    cleanup_old_entries(flood_dict, now, WINDOW_SECONDS)
    flood_dict[now] = now

    if len(flood_dict) >= FLOOD_THRESHOLD:
        log_alert(f"Possible TCP FLOOD towards {dst_ip}:{dst_port} "
                  f"({len(flood_dict)} packets in the last {WINDOW_SECONDS}s)")


def handle_udp_packet(src_ip, dst_ip, dst_port, now):
    """
    Logic for UDP events.

    We handle:
      - UDP "spray" (multi-port) from a given source.

    TODO (student):
      - use ids_state["udp_spray"] with a structure similar to "tcp_scan"
      - if src_ip reaches >= UDP_PORT_THRESHOLD distinct UDP ports
        within the WINDOW_SECONDS window => ALERT
    """

    global ids_state

    if dst_port is None:
        return

    spray_dict = ids_state["udp_spray"].setdefault(src_ip, {})
    cleanup_old_entries(spray_dict, now, WINDOW_SECONDS)
    spray_dict[dst_port] = now

    port_count = len(spray_dict)
    if port_count >= UDP_PORT_THRESHOLD:
        log_alert(f"Possible UDP SPRAY from {src_ip}: "
                  f"{port_count} UDP ports in the last {WINDOW_SECONDS}s")
        # optional: spray_dict.clear()


# ------------------ MAIN IDS LOOP ------------------

def main():
    if len(sys.argv) < 2:
        print(f"Usage: sudo {sys.argv[0]} <INTERFACE>")
        print("Example: sudo python3 mini_ids.py eth0")
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

    print(f"[INFO] Starting mini_ids on interface {interface}")
    print(f"[INFO] WINDOW_SECONDS={WINDOW_SECONDS}, TCP_SYN_THRESHOLD={TCP_SYN_THRESHOLD}, "
          f"UDP_PORT_THRESHOLD={UDP_PORT_THRESHOLD}, FLOOD_THRESHOLD={FLOOD_THRESHOLD}")
    print(f"[INFO] Alerts will be logged to {ALERT_LOG_FILE}")
    print("[INFO] Stop with Ctrl-C.\n")

    try:
        while True:
            raw_data, addr = sniffer.recvfrom(65535)
            now = time.time()

            dest_mac, src_mac, eth_proto, payload = parse_ethernet_header(raw_data)

            # We are interested only in IPv4
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

            # Other protocols -- ignored in this version
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] mini_ids stopped.")


if __name__ == "__main__":
    main()

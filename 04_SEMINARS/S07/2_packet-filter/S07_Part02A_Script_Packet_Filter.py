#!/usr/bin/env python3
import socket
import struct
import sys

"""
Seminar 7 -- Packet Filter (TCP / UDP / IP)

This script extends the simple sniffer. In addition to
`packet_sniffer.py`, here we shall:

 - extract source/destination ports for TCP and UDP
 - apply a custom filter in the `passes_filter` function
 - display only the packets that pass the filter

Sections marked with
    # >>> STUDENT TODO
must be completed by you.

Execution (REQUIRES sudo):

    sudo python3 packet_filter.py <INTERFACE>

Examples:

    sudo python3 packet_filter.py eth0
    h1 sudo python3 packet_filter.py h1-eth0
"""

MAX_PACKETS = 100  # maximum number of packets to process


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
    COMPLETE version of parse_ipv4_header from Stage 2.
    You may copy your implementation from packet_sniffer.py here.

    Returns:
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
    Parse the TCP header to obtain the source/destination ports.

    structure (first 4 bytes):
        - source port (2 bytes)
        - dest port   (2 bytes)

    Returns:
      (src_port, dst_port)
    """
    src_port, dst_port = struct.unpack("! H H", data[:4])
    return src_port, dst_port


def parse_udp_header(data: bytes):
    """
    Parse the UDP header to obtain the source/destination ports.

    structure (first 4 bytes):
        - source port (2 bytes)
        - dest port   (2 bytes)

    Returns:
      (src_port, dst_port)
    """
    src_port, dst_port = struct.unpack("! H H", data[:4])
    return src_port, dst_port


# -------------------------------------------------------------------------
# CUSTOM FILTER
# -------------------------------------------------------------------------

def passes_filter(src_ip, dst_ip, proto, src_port=None, dst_port=None) -> bool:
    """
    This function decides whether a packet passes the filter or not.

    Parameters:
      - src_ip, dst_ip: IPv4 strings (e.g. '10.0.0.1')
      - proto: int (6 = TCP, 17 = UDP, 1 = ICMP etc.)
      - src_port, dst_port: int or None (only for TCP/UDP)

    TODO (student):
      Implement several filtering rules here.
      You may start from the requirements in the tasks file.

    Examples of criteria to implement (in order):

      1) Display ONLY TCP packets (proto == 6).
      2) Display ONLY UDP packets with destination port 53 (DNS).
      3) Display ONLY packets whose source address belongs to a specific
         network, for example 10.0.0.0/8 (string starts with '10.').

    You may combine the criteria as you wish, for example:
      - display TCP packets with dst_port > 1024
      - display UDP packets from a specific source

    Currently the function returns False for everything (displays nothing)
    until you modify it.
    """

    # >>> STUDENT TODO: replace the logic below with your own filter

    # Simple example (temporary): accept all TCP traffic
    # if proto == 6:
    #     return True

    return False


# -------------------------------------------------------------------------
# MAIN SNIFFING LOOP
# -------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(f"Usage: sudo {sys.argv[0]} <INTERFACE>")
        print("Example: sudo python3 packet_filter.py eth0")
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

    print(f"[INFO] Starting packet_filter on interface {interface}")
    print(f"[INFO] Processing at most {MAX_PACKETS} packets. Stop with Ctrl-C.\n")

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

                proto_str = "OTHER"

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
                    proto_str = f"OTHER({proto})"

                # Apply the filter
                if passes_filter(src_ip, dst_ip, proto, src_port, dst_port):
                    # Display only packets that pass the filter
                    if src_port is not None and dst_port is not None:
                        print(f"{src_ip}:{src_port} -> {dst_ip}:{dst_port}  proto={proto_str}")
                    else:
                        print(f"{src_ip} -> {dst_ip}  proto={proto_str}")

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] Packet filter stopped.")


if __name__ == "__main__":
    main()

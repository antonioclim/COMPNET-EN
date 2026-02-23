#!/usr/bin/env python3
import socket
import struct
import sys

"""
Seminar 7 -- Simple IPv4 Packet Sniffer

This script creates a RAW socket and displays basic information
about the IPv4 packets traversing a given interface:

 - source / destination MAC address
 - source / destination IP address
 - protocol (TCP / UDP / other)

Sections marked with
    # >>> STUDENT TODO
must be completed by you.

Execution (REQUIRES sudo):

    sudo python3 packet_sniffer.py <INTERFACE>

Examples:

    sudo python3 packet_sniffer.py eth0
    sudo python3 packet_sniffer.py lo
    # in Mininet:
    h1 sudo python3 packet_sniffer.py h1-eth0
"""

MAX_PACKETS = 50  # maximum number of packets to display (you may modify this)


def mac_addr(raw_mac: bytes) -> str:
    """
    Convert a MAC address to a human-readable format:
    'aa:bb:cc:dd:ee:ff'
    """
    return ":".join(f"{b:02x}" for b in raw_mac)


def ipv4_addr(raw_ip: bytes) -> str:
    """
    Convert an IPv4 address (4 bytes) to the 'x.x.x.x' format.
    """
    return ".".join(str(b) for b in raw_ip)


def parse_ethernet_header(data: bytes):
    """
    Parse the Ethernet header (first 14 bytes):

    structure:
        - destination MAC: 6 bytes
        - source MAC: 6 bytes
        - ethertype: 2 bytes (0x0800 for IPv4)

    Returns:
        (dest_mac_str, src_mac_str, proto) and the payload (remaining data).
    """
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    dest_mac_str = mac_addr(dest_mac)
    src_mac_str = mac_addr(src_mac)
    return dest_mac_str, src_mac_str, proto, data[14:]


def parse_ipv4_header(data: bytes):
    """
    Parse the IPv4 header (minimum 20 bytes).

    structure (simplified):
        - version + IHL (1 byte)
        - TOS (1 byte)
        - total length (2 bytes)
        - identification, flags, fragment offset (4 bytes)
        - TTL (1 byte)
        - protocol (1 byte)
        - checksum (2 bytes)
        - source address (4 bytes)
        - destination address (4 bytes)

    Returns:
        (src_ip_str, dst_ip_str, proto, header_length)

    Where:
        - header_length is in bytes (e.g. 20, 24, 28 etc.)
    """

    # >>> STUDENT TODO
    # 1. Extract the version and IHL (Internet Header Length) from the first byte.
    #    version_ihl = data[0]
    #    version = version_ihl >> 4
    #    ihl = (version_ihl & 0x0F) * 4
    #
    # 2. Use struct.unpack to extract:
    #       ttl, proto, src, dst
    #    You may use the format:
    #       '! 8x B B 2x 4s 4s'
    #    which skips the first 8 bytes, reads TTL and protocol,
    #    then skips the checksum and reads the IP addresses.
    #
    # 3. Convert src and dst to strings using ipv4_addr().
    #
    # Finally return: (src_ip_str, dst_ip_str, proto, ihl)

    # HINT (if you get stuck, uncomment and adapt):
    # version_ihl = data[0]
    # version = version_ihl >> 4
    # ihl = (version_ihl & 0x0F) * 4
    # ttl, proto, src, dst = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    # src_ip_str = ipv4_addr(src)
    # dst_ip_str = ipv4_addr(dst)
    # return src_ip_str, dst_ip_str, proto, ihl

    raise NotImplementedError("Complete the parse_ipv4_header function")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: sudo {sys.argv[0]} <INTERFACE>")
        print("Example: sudo python3 packet_sniffer.py eth0")
        sys.exit(1)

    interface = sys.argv[1]

    # Create a RAW socket at the link layer (AF_PACKET is Linux-specific).
    # htons(0x0003) => receive all protocols (ETH_P_ALL).
    try:
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    except PermissionError:
        print("Error: you must run with root privileges (sudo).")
        sys.exit(1)

    # Bind the socket to a specific interface (e.g. 'eth0', 'lo', 'h1-eth0').
    try:
        sniffer.bind((interface, 0))
    except OSError as e:
        print(f"Error binding to interface {interface}: {e}")
        sys.exit(1)

    print(f"[INFO] Starting sniffer on interface {interface}")
    print(f"[INFO] Displaying at most {MAX_PACKETS} packets. Stop with Ctrl-C.\n")

    packet_count = 0

    try:
        while packet_count < MAX_PACKETS:
            raw_data, addr = sniffer.recvfrom(65535)

            packet_count += 1

            # 1. Parse the Ethernet header
            dest_mac, src_mac, eth_proto, payload = parse_ethernet_header(raw_data)

            # Display only IPv4 packets (Ethertype 0x0800)
            if eth_proto == 0x0800:
                try:
                    src_ip, dst_ip, proto, ip_header_len = parse_ipv4_header(payload)
                except NotImplementedError:
                    print("parse_ipv4_header is not yet implemented.")
                    break

                # Decode the protocol to text
                if proto == 6:
                    proto_str = "TCP"
                elif proto == 17:
                    proto_str = "UDP"
                elif proto == 1:
                    proto_str = "ICMP"
                else:
                    proto_str = f"OTHER({proto})"

                print(f"[{packet_count}] {src_ip} -> {dst_ip}  proto={proto_str}")
                # Optional: you may also display MAC addresses
                # print(f"    MAC: {src_mac} -> {dest_mac}")

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl-C).")
    finally:
        sniffer.close()
        print("[INFO] Sniffer stopped.")


if __name__ == "__main__":
    main()

import ipaddress
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cidr-calc.py <ipv4/prefix>")
        print("Example: python3 cidr-calc.py 192.168.23.233/24")
        sys.exit(1)

    net = ipaddress.ip_interface(sys.argv[1]).network
    if net.version != 4:
        raise ValueError("This calculator expects IPv4")
    usable = net.num_addresses if net.prefixlen >= 31 else net.num_addresses - 2
    first = net.network_address if net.prefixlen >= 31 else net.network_address + 1
    last = net.broadcast_address if net.prefixlen >= 31 else net.broadcast_address - 1

    print("Network:", net.network_address)
    print("Prefix:", net.prefixlen)
    print("Netmask:", net.netmask)
    print("Broadcast:", net.broadcast_address)
    if usable > 0:
        print("First host:", first)
        print("Last host:", last)
    print("Usable hosts:", usable)

if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

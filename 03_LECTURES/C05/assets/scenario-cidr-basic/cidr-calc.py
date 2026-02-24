import ipaddress
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cidr-calc.py <ipv4/prefix>")
        print("Example: python3 cidr-calc.py 192.168.23.233/24")
        sys.exit(1)

    net = ipaddress.ip_interface(sys.argv[1]).network
    hosts = list(net.hosts())
    usable = len(hosts)

    print("Network:", net.network_address)
    print("Prefix:", net.prefixlen)
    print("Netmask:", net.netmask)
    print("Broadcast:", net.broadcast_address)
    if usable > 0:
        print("First host:", hosts[0])
        print("Last host:", hosts[-1])
    print("Usable hosts:", usable)

if __name__ == "__main__":
    main()

import ipaddress
import math
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 flsm-split.py <network/prefix> <num_subnets>")
        sys.exit(1)

    base = ipaddress.ip_network(sys.argv[1], strict=True)
    n = int(sys.argv[2])
    if n <= 0:
        raise ValueError("num_subnets must be > 0")

    bits = math.ceil(math.log2(n))
    new_prefix = base.prefixlen + bits
    if new_prefix > 32:
        raise ValueError("Too many subnets for this network")

    subs = list(base.subnets(new_prefix=new_prefix))
    if len(subs) < n:
        raise ValueError("Could not create enough subnets")

    for i, sn in enumerate(subs[:n], start=1):
        hosts = list(sn.hosts())
        print(f"Subnet {i}: {sn}")
        print("  Network:", sn.network_address)
        print("  Broadcast:", sn.broadcast_address)
        if hosts:
            print("  Hosts:", hosts[0], "-", hosts[-1], f"({len(hosts)} usable)")
        else:
            print("  Hosts: none")
        print()

if __name__ == "__main__":
    main()

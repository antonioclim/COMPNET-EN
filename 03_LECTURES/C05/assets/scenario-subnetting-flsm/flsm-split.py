import ipaddress
import math
from itertools import islice
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 flsm-split.py <network/prefix> <num_subnets>")
        sys.exit(1)

    base = ipaddress.ip_network(sys.argv[1], strict=True)
    if base.version != 4:
        raise ValueError("This calculator expects IPv4")
    n = int(sys.argv[2])
    if n <= 0:
        raise ValueError("num_subnets must be > 0")

    bits = math.ceil(math.log2(n))
    new_prefix = base.prefixlen + bits
    if new_prefix > 32:
        raise ValueError("Too many subnets for this network")

    subs = islice(base.subnets(new_prefix=new_prefix), n)
    for i, sn in enumerate(subs, start=1):
        usable = sn.num_addresses if sn.prefixlen >= 31 else sn.num_addresses - 2
        first = sn.network_address if sn.prefixlen >= 31 else sn.network_address + 1
        last = sn.broadcast_address if sn.prefixlen >= 31 else sn.broadcast_address - 1
        print(f"Subnet {i}: {sn}")
        print("  Network:", sn.network_address)
        print("  Broadcast:", sn.broadcast_address)
        if usable:
            print("  Hosts:", first, "-", last, f"({usable} usable)")
        else:
            print("  Hosts: none")
        print()

if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

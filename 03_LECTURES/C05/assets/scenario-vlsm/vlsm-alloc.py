import ipaddress
import math
import sys

def needed_prefix(hosts_needed: int) -> int:
    # include network + broadcast, hence +2
    size = hosts_needed + 2
    bits = math.ceil(math.log2(size))
    return 32 - bits

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 vlsm-alloc.py <base_network/prefix> <hosts1> <hosts2> ...")
        sys.exit(1)

    base = ipaddress.ip_network(sys.argv[1], strict=True)
    req = [int(x) for x in sys.argv[2:]]
    req_sorted = sorted(req, reverse=True)

    cursor = int(base.network_address)
    end = int(base.broadcast_address)

    allocations = []
    for h in req_sorted:
        pfx = needed_prefix(h)
        # align cursor to subnet boundary
        block_size = 2 ** (32 - pfx)
        if cursor % block_size != 0:
            cursor = ((cursor // block_size) + 1) * block_size

        net = ipaddress.ip_network((cursor, pfx))
        if int(net.broadcast_address) > end:
            raise ValueError("Insufficient address space for requirements")

        allocations.append((h, net))
        cursor = int(net.broadcast_address) + 1

    print("Base:", base)
    for h, net in allocations:
        hosts = list(net.hosts())
        usable = len(hosts)
        print(f"- Need {h} hosts -> {net} (usable {usable})")
        print(f"  Network: {net.network_address}")
        print(f"  Broadcast: {net.broadcast_address}")
        if usable:
            print(f"  Hosts: {hosts[0]} - {hosts[-1]}")
    print()
    print("Note: allocations shown in descending host requirement order.")

if __name__ == "__main__":
    main()

import ipaddress
import math
import sys

def needed_prefix(hosts_needed: int) -> int:
    if hosts_needed < 1 or hosts_needed > 2**32 - 2:
        raise ValueError("Host requirement must be between 1 and 4294967294")
    # This allocator models traditional IPv4 LANs: reserve network and broadcast.
    size = hosts_needed + 2
    bits = math.ceil(math.log2(size))
    return 32 - bits

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 vlsm-alloc.py <base_network/prefix> <hosts1> <hosts2> ...")
        sys.exit(1)

    base = ipaddress.ip_network(sys.argv[1], strict=True)
    if base.version != 4:
        raise ValueError("This calculator expects IPv4")
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
        usable = net.num_addresses - 2
        print(f"- Need {h} hosts -> {net} (usable {usable})")
        print(f"  Network: {net.network_address}")
        print(f"  Broadcast: {net.broadcast_address}")
        if usable:
            print(f"  Hosts: {net.network_address + 1} - {net.broadcast_address - 1}")
    print()
    print("Note: allocations shown in descending host requirement order.")

if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

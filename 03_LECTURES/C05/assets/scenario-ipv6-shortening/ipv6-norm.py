import ipaddress
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ipv6-norm.py <ipv6>")
        sys.exit(1)

    addr = ipaddress.IPv6Address(sys.argv[1])
    print("Compressed:", addr.compressed)
    print("Expanded:  ", addr.exploded)

if __name__ == "__main__":
    main()

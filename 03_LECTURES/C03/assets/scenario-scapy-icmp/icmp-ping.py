import sys
from scapy.all import IP, ICMP, sr1

def main():
    dst = sys.argv[1] if len(sys.argv) > 1 else "1.1.1.1"
    pkt = IP(dst=dst) / ICMP()
    resp = sr1(pkt, timeout=2, verbose=False)
    if resp is None:
        print("No reply (timeout)")
    else:
        print("Reply from:", resp.src)

if __name__ == "__main__":
    main()

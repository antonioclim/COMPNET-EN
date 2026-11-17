import time
import argparse
import socket
import dns.resolver

def q():
    r = dns.resolver.Resolver()
    r.nameservers = [socket.gethostbyname("resolver")]
    ans = r.resolve("www.example.test", "A")
    print("A =", [a.to_text() for a in ans], "TTL =", ans.rrset.ttl)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--interval", type=float, default=2)
    args = parser.parse_args()
    if args.repeat < 1 or args.interval < 0:
        parser.error("repeat must be positive and interval non-negative")
    for i in range(args.repeat):
        q()
        if i + 1 < args.repeat:
            time.sleep(args.interval)

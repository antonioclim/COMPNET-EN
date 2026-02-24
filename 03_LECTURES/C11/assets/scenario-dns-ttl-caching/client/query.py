import time
import dns.resolver

def q():
    r = dns.resolver.Resolver()
    r.nameservers = ["resolver"]
    ans = r.resolve("www.example.test", "A")
    print("A =", [a.to_text() for a in ans], "TTL =", ans.rrset.ttl)

if __name__ == "__main__":
    for i in range(5):
        q()
        time.sleep(2)

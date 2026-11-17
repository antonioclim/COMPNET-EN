# Scenario DNS – TTL and caching

## Objective
Observe DNS caching behaviour and the operational effect of TTL.

## What happens
- A recursive resolver queries an authoritative server
- Responses are cached
- The DNS zone is modified

## What to observe
- When the new IP address becomes visible
- How TTL influences propagation

## Run
From this scenario directory, use a subnet that does not overlap another running lab: this stack reserves `172.29.111.0/24`; authoritative BIND is `172.29.111.10`, and Unbound uses it as a stub-zone upstream. Docker's resolver service name is resolved to an IP before dnspython receives it.

```bash
docker compose up -d --build auth resolver
docker compose run --rm client
```

The zone has TTL 30 seconds. To observe an address change, start a longer query run in terminal 1:

```bash
docker compose run --rm client python query.py --repeat 25 --interval 2
```

After the first answer, in terminal 2 in this same directory, change only the demonstration record and increment its serial, then reload the authoritative service by restarting it:

```bash
python3 - <<'PY'
from pathlib import Path
path = Path('auth/zones/example.zone')
s = path.read_text()
assert 'www IN  A   10.0.0.42' in s, 'Restore the initial zone before repeating this step'
s = s.replace('1  ; serial', '2  ; serial').replace('www IN  A   10.0.0.42', 'www IN  A   10.0.0.43')
path.write_text(s)
PY
docker compose restart auth
```

Observe the cached old address and decreasing TTL, followed by the new address after expiry. Do not restart the resolver during this measurement, because that clears the cache. Restore `.42` with a higher serial before another run. Cleanup: `docker compose down`.

## Questions
- Why DNS changes are not instantaneous
- What trade-off TTL introduces

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 46 |
| `auth/` | 1 files |
| `client/` | 2 files |
| `resolver/` | 1 files |

## Cross-References

Parent lecture: [`C11/ — FTP, DNS and SSH`](../../)
  
Lecture slides: [`c11-ftp-dns-ssh.md`](../../c11-ftp-dns-ssh.md)
  
Quiz: [`W11`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C11/assets/scenario-dns-ttl-caching
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C11/assets/scenario-dns-ttl-caching`

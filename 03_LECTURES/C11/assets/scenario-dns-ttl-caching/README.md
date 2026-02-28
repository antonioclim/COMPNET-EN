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
docker compose up --build

## Questions
- Why DNS changes are not instantaneous
- What trade-off TTL introduces

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 25 |
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

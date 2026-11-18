# Scenario FTP – NAT and firewall

## Objective
Demonstrate the limitations of FTP in modern networks that use NAT and firewalls.

## What happens
- The client communicates with the FTP server through a NAT device
- Active vs passive mode is tested
- Points of failure and their causes are observed

## What to observe
- Which side initiates the data connection
- Which ports are used
- Why passive mode is usually preferred

## Run
From this scenario directory:

```bash
docker compose up --build
```

The client uses `natfw:2121` on `172.29.112.0/24`. The firewall DNATs the control connection and passive ports 30000–30009 to `172.29.113.10`; SNAT makes replies return through it. The server advertises `172.29.112.2` for PASV. The client is never attached to the server network. Keep both subnets free of overlap with other running labs.

Passive LIST must succeed. Active mode is expected to fail: the server sees the translated control peer while PORT advertises the client's private address, and pyftpdlib's foreign-address check rejects it. This is a concrete active-mode limitation, not proof that all active FTP through all NAT configurations fails.

For packet evidence, start only services in terminal 1 and capture in the firewall before running the client in terminal 2:

```bash
docker compose up -d --build ftp natfw
docker compose exec natfw tcpdump -ni any 'tcp port 2121 or tcp portrange 30000-30009'
```

```bash
docker compose run --rm client
docker compose exec natfw iptables -t nat -nvL
```

Record the pre/post NAT endpoints and the PORT/PASV control replies. Stop tcpdump with Ctrl+C and run `docker compose down` after the experiment.

## Discussion
- Why FTP is difficult to secure
- Why SFTP and HTTPS are often preferred

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 71 |
| `client/` | 1 files |
| `data/` | 1 files |
| `ftp/` | 3 files |
| `natfw/` | 1 files |

## Cross-References

Parent lecture: [`C11/ — FTP, DNS and SSH`](../../)
  
Lecture slides: [`c11-ftp-dns-ssh.md`](../../c11-ftp-dns-ssh.md)
  
Quiz: [`W11`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C11/assets/scenario-ftp-nat-firewall
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C11/assets/scenario-ftp-nat-firewall`

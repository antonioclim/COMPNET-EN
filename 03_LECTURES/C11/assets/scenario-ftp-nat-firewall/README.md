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
docker compose up --build

## Discussion
- Why FTP is difficult to secure
- Why SFTP and HTTPS are often preferred

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 36 |
| `client/` | 1 files |
| `data/` | 1 files |
| `ftp/` | 2 files |
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

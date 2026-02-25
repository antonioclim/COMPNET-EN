# Scenario FTP – control vs data

## Objective
Observe how FTP operates by inspecting the separation between:
- the control connection
- the data connection

## What happens
- A real FTP server runs (pyftpdlib)
- A Python FTP client connects
- LIST, STOR and RETR commands are executed
- Active vs passive mode is compared

## What to observe
- The ports in use
- When data connections appear
- The difference between PASV and PORT

## Run
docker compose up --build

## Questions
- Why do two separate connections exist?
- Why is active mode problematic?

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 20 |
| `client/` | 1 files |
| `data/` | 1 files |
| `server/` | 1 files |

## Cross-References

Parent lecture: [`C11/ — FTP, DNS and SSH`](../../)
  
Lecture slides: [`c11-ftp-dns-ssh.md`](../../c11-ftp-dns-ssh.md)
  
Quiz: [`W11`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C11/assets/scenario-ftp-baseline
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C11/assets/scenario-ftp-baseline`

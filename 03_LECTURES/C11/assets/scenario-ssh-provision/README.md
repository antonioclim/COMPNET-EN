# Scenario SSH – simple provisioning

## Objective
Demonstrate SSH as a general-purpose control and automation mechanism.

## What happens
- A Python controller reads a JSON plan
- It connects via SSH
- It executes commands
- It transfers files

## What to observe
- SSH as a control protocol
- Multiple channels over a single connection
- Similarities with real DevOps tooling

## Run
docker compose up --build

## Discussion
- What makes SSH versatile
- Why many tools rely on SSH

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 18 |
| `controller/` | 3 files |
| `nodes/` | 0 files |
| `payload/` | 1 files |

## Cross-References

Parent lecture: [`C11/ — FTP, DNS and SSH`](../../)
  
Lecture slides: [`c11-ftp-dns-ssh.md`](../../c11-ftp-dns-ssh.md)
  
Quiz: [`W11`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W11_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C11/assets/scenario-ssh-provision
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C11/assets/scenario-ssh-provision`

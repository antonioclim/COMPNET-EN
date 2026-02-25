### Scenario: local mailbox (SMTP, POP3, IMAP and webmail)

This scenario runs a fully local mail stack and demonstrates interaction from Python:
- send mail via SMTP submission (587)
- read mail via IMAP (143/993)
- read mail via POP3 (110/995)
- optionally: read and send mail via webmail (Roundcube)

#### 0) Prerequisites
- Docker and Docker Compose
- Python 3.10+ (recommended)

#### 1) Start the stack
From this folder:

```bash
docker compose up -d
```

#### 2) Create a mailbox
Create a test user and password (example: alice@example.test / alicepw):

```bash
docker exec -it dms setup email add alice@example.test alicepw
```

You can add more users in the same way.

#### 3) Send an email (SMTP)
```bash
python3 scripts/send_mail_smtp.py --smtp-host localhost --smtp-port 587   --user alice@example.test --password alicepw   --to alice@example.test --subject "Hello" --body "Sent from Python"
```

#### 4) Fetch via IMAP
```bash
python3 scripts/fetch_imap.py --imap-host localhost --imap-port 143   --user alice@example.test --password alicepw
```

#### 5) Fetch via POP3
```bash
python3 scripts/fetch_pop3.py --pop3-host localhost --pop3-port 110   --user alice@example.test --password alicepw
```

#### 6) Send an attachment (MIME)
Put an example file in this folder (e.g. assets/cat.jpg), then:

```bash
python3 scripts/send_attachment_smtp.py --smtp-host localhost --smtp-port 587   --user alice@example.test --password alicepw   --to alice@example.test --file assets/cat.jpg
```

#### 7) Webmail
Open http://localhost:8080 and log in:
- user: alice@example.test
- password: alicepw

Note: For local demonstrations, TLS certificates are self-signed so clients may require explicit trust if you use ports 993 or 995.

#### Clean up
```bash
docker compose down -v
```

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 41 |
| `mailserver.env` | 15 |
| `requirements.txt` | 1 |
| `docker-mailserver/` | 1 files |
| `scripts/` | 4 files |

## Cross-References

Parent lecture: [`C12/ — Email Protocols (SMTP, POP3, IMAP)`](../../)
  
Lecture slides: [`c12-email-protocols.md`](../../c12-email-protocols.md)
  
Quiz: [`W12`](../../../../00_APPENDIX/c%29studentsQUIZes%28multichoice_only%29/COMPnet_W12_Questions.md)

## Selective Clone

**Method A — Git sparse-checkout (Git 2.25+)**

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 03_LECTURES/C12/assets/scenario-local-mailbox
```

**Method B — Direct download**

Browse at: `https://github.com/antonioclim/COMPNET-EN/tree/main/03_LECTURES/C12/assets/scenario-local-mailbox`

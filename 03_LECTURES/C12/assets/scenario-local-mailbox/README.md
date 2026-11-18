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
bash scripts/generate_demo_certs.sh
docker compose run --rm mail setup email add alice@example.test alicepw
docker compose up -d
docker compose logs --tail=50 mail
```

Wait until the mail service is ready before sending messages. The generated CA
certificate is trusted explicitly by the supplied clients. Do not commit private
keys or reuse these classroom credentials on an Internet-facing server.

#### 2) Create a mailbox
The first account was created before startup above. To add another local test account:

```bash
docker compose exec mail setup email add bob@example.test bobpw
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
Create a small attachment in this folder, then:

```bash
printf 'Hello from the MIME attachment exercise.\n' > attachment.txt
python3 scripts/send_attachment_smtp.py --smtp-host localhost --smtp-port 587   --user alice@example.test --password alicepw   --to alice@example.test --file attachment.txt
```

#### 7) Webmail
Open http://localhost:8080 and log in:
- user: alice@example.test
- password: alicepw

All supplied clients verify the local CA and the server name. SMTP 587, IMAP 143 and POP3 110 use STARTTLS; 993 and 995 use implicit TLS. Roundcube uses the same CA through its mounted configuration. Published ports bind only to 127.0.0.1. See the [Docker Mailserver TLS manual](https://docker-mailserver.github.io/docker-mailserver/latest/config/security/ssl/#bring-your-own-certificates).

#### Clean up
```bash
docker compose down
# Only when you intend to erase this lab's saved mail and state:
# docker compose down -v
```

## Files

| Name | Lines |
|------|-------|
| `docker-compose.yml` | 44 |
| `mailserver.env` | 18 |
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

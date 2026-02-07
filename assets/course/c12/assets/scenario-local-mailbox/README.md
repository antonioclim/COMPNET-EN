### Scenario: local mailbox (SMTP + POP3 + IMAP + WebMail)

Goal: run a fully local mail stack and interact with it from Python:
- send mail via SMTP submission (587)
- read mail via IMAP (143/993)
- read mail via POP3 (110/995)
- optionally: read/send from WebMail (Roundcube)

#### 0) Prerequisites
- Docker + Docker Compose
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

You can add more users the same way.

#### 3) Send an email (SMTP)
```bash
python3 scripts/send_mail_smtp.py --smtp-host localhost --smtp-port 587 \
  --user alice@example.test --password alicepw \
  --to alice@example.test --subject "Hello" --body "Sent from Python"
```

#### 4) Fetch via IMAP
```bash
python3 scripts/fetch_imap.py --imap-host localhost --imap-port 143 \
  --user alice@example.test --password alicepw
```

#### 5) Fetch via POP3
```bash
python3 scripts/fetch_pop3.py --pop3-host localhost --pop3-port 110 \
  --user alice@example.test --password alicepw
```

#### 6) Send an attachment (MIME)
Put an example file in this folder (e.g. assets/cat.jpg), then:

```bash
python3 scripts/send_attachment_smtp.py --smtp-host localhost --smtp-port 587 \
  --user alice@example.test --password alicepw \
  --to alice@example.test --file assets/cat.jpg
```

#### 7) WebMail
Open http://localhost:8080 and login:
- user: alice@example.test
- password: alicepw

Note: for local demos, TLS certificates are self-signed, so clients may need to accept them if you switch to 993/995.

#### Cleanup
```bash
docker compose down -v
```

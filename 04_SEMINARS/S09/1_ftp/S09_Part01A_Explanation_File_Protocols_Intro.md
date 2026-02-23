# **Stage 1 — Introduction to File Transfer Protocols**

### Seminar 9 — File Protocols: FTP, Active/Passive, Control + Data

In this seminar we study how files are transferred over a network, using:

- a real FTP server implemented with `pyftpdlib`
- a custom protocol (pseudo-FTP) that uses two connections, similar to FTP
- multi-client testing with containers

The goal of this first stage is to understand **conceptually** how file transfer protocols work.

---

## 1. What Are File Transfer Protocols?

Well-known examples:
- **FTP** — File Transfer Protocol (vintage, still in use, entirely unencrypted)
- **FTPS** — FTP over TLS
- **SFTP** — Secure File Transfer Protocol (part of SSH, completely different from FTP!)
- **HTTP/HTTPS** — very commonly used for downloads/uploads
- **NFS**, **SMB** — for mounting network directories (file sharing)

In this seminar we focus on the idea of **two streams**:
- a **control** channel (commands)
- a **transfer** channel (raw data)

---

## 2. Control Connection vs Data Connection

Classic FTP uses:

1. **Control connection**: port 21
   This carries *commands*: `USER`, `PASS`, `LIST`, `RETR`, `STOR`

2. **Data connection**: various ports
   Used ONLY for the actual file transfer.

In our seminar's pseudo-FTP we replicate exactly this idea.

---

## 3. Active Mode and Passive Mode

### Active Mode
- The client initiates the transfer by **listening on a port**.
- The FTP server connects to the client on the announced port.

Diagram:

```

client ---control---> server
client <---data------ server (connection initiated by server)

```

Issues:
- nearly impossible through modern firewall/NAT

---

### Passive Mode
- The server opens a temporary port.
- The client connects to that port for the transfer.

Diagram:

```

client ---control---> server
client ------data---> server

```

Advantage:
- works far better with NAT/firewall → this is the standard mode today.

Both modes appear explicitly in our pseudo-FTP.

---

## 4. Mini-questions (write in your log file)

1. What is the difference between the **control** connection and the **data** connection?
2. Why is active mode difficult in modern networks?
3. What advantages does passive mode offer?
4. Why are protocols such as SFTP/HTTPS preferred today?

Write your answers in a file:

```

intro_file_protocols_log.txt

```

This will be the deliverable for Stage 1.

### Stage 2 — FTP Server with pyftpdlib and a Minimal FTP Client

In this stage we will:

1. Start a fully functional FTP server using `pyftpdlib`
2. Use a simple Python client to test basic commands
3. (Optional) Use a CLI client: `ftp`, `lftp`, `ncftp`
4. Understand the structure of FTP commands: LIST, RETR, STOR

---

## 1. Pyftpdlib

`pyftpdlib` is a Python library that fully implements the FTP protocol:

- FTP server compliant with RFC 959
- support for users with different permissions
- support for active and passive mode
- file listing, upload, download

Advantage: everything works out of the box, without implementing the protocol from scratch.

---

## 2. Server Structure

The server starts on host + port, has an authoriser for users and uses `FTPHandler`.

A user is defined as follows:

```

authorizer.add_user('test', '12345', './test', perm='elradfmwMT')

```

Key permissions:
- `e` – change directory
- `l` – list files
- `r` – read
- `a` – append
- `d` – delete
- `f` – rename
- `m` – mkdir
- `w` – write
- `M` – create directories
- `T` – change timestamp

---

## 3. Client Structure

The client uses the `ftplib` library, part of the Python standard library.

Typical flow:

```

ftp = FTP()
ftp.connect('localhost', 2121)
ftp.login()
ftp.retrbinary('RETR a.txt', fp.write)

```

---

## 4. What We Will Test

1. Connection
2. `LIST` to see the files
3. `RETR filename` — download
4. `STOR filename` — upload

---

Deliverables (for Stage 2):

- running the server
- running the client
- log with the tested commands (`pyftpd_log.txt`)

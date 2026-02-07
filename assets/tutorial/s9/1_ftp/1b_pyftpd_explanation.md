### Stage 2 – Server FTP cu pyftpdlib și client FTP minimal

În această etapă vom:

1. Porni un server FTP complet funcțional folosind `pyftpdlib`
2. Folosi un client Python simplu pentru a testa comenzi de bază
3. (Opțional) Folosi un client CLI: `ftp`, `lftp`, `ncftp`
4. Înțelege structura comenzilor FTP: LIST, RETR, STOR

---

## 1. Pyftpdlib

`pyftpdlib` este o bibliotecă Python care implementează complet protocolul FTP:

- server FTP conform RFC 959
- suport pentru utilizatori cu permisiuni diferite
- suport pentru mod activ și pasiv
- liste de fișiere, upload, download

Avantaj: totul funcționează imediat, fără să implementăm protocolul de la zero.

---

## 2. Structura serverului

Serverul pornește pe host + port, are un autorizer pentru useri și folosește `FTPHandler`.

Userul este definit astfel:

```

authorizer.add_user('test', '12345', './test', perm='elradfmwMT')

```

Permisiuni importante:
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

## 3. Structura clientului

Clientul folosește biblioteca `ftplib`, parte din standard library Python.

Flux tipic:

```

ftp = FTP()
ftp.connect('localhost', 2121)
ftp.login()
ftp.retrbinary('RETR a.txt', fp.write)

```

---

## 4. Ce vom testa

1. Conectare
2. `LIST` pentru a vedea fișierele
3. `RETR filename` – descărcare
4. `STOR filename` – încărcare

---

Livrabile (în Stage 2):

- rularea serverului
- rularea clientului
- log cu comenzile testate (`pyftpd_log.txt`)


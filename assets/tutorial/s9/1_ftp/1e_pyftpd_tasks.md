### Stage 2 – Task-uri server FTP + client FTP

---

## 1. Porniți serverul pyftpdlib

Într-un terminal rulați:

```

python3 pyftpd_server.py

```

Ar trebui să apară:

```

Server FTP pyftpdlib pornit pe portul 2121...
Utilizator: test / 12345

```

---

## 2. Testați conectarea cu un client FTP CLI (opțional)

```

ftp 127.0.0.1 2121
Name: test
Password: 12345
ftp> ls
ftp> get a.txt
ftp> bye

```

---

## 3. Modificați și rulați clientul Python

```

python3 pyftpd_client.py

```

Completați TODO-urile astfel încât clientul:

- să afișeze lista de fișiere
- să descarce un fișier
- să încarce un fișier

---

## 4. Testele obligatorii (de scris în pyftpd_log.txt)

Executați și salvați output-ul pentru:

1. LIST (afisarea fișierelor)
2. RETR pentru un fișier existent
3. STOR pentru un fișier nou
4. Ce se întâmplă dacă încercați să descărcați un fișier inexistent?
5. (opțional) logare cu username/parolă în loc de anonymous

Format:

```

---- LIST ---- <output aici>

---- RETR ---- <output aici>

---- STOR ---- <output aici>

---- Observații ----
<propoziții scurte despre ce merge, ce nu, ce ați înțeles>

```

Acest fișier log va fi livrabilul pentru Stage 2.

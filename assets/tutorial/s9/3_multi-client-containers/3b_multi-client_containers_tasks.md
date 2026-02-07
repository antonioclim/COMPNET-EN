### Stage 4 – Task-uri: multi-client cu containere (FTP server + 2 clienti)

Scop:
- sa simulam doi clienti care folosesc acelasi server FTP
- sa vedem cum un fisier urcat de client1 poate fi descarcat de client2

Rezultat:
- un fisier de log: `ftp_multi_client_log.txt`
- fisiere in directoarele: `server-data/`, `client1-data/`, `client2-data/`

---

## 1. Pregatirea mediului

Asigurati-va ca aveti urmatoarele fisiere in acelasi director:

- `docker-compose.yml`
- `pyftpd_server.py`
- `pyftpd_multi_client.py`

Creati directoarele necesare:

```bash
mkdir -p server-data server-anon client1-data client2-data
````

(Optional) creati un fisier initial in `client1-data`:

```bash
echo "Hello from client1" > client1-data/from_client1.txt
```

---

## 2. Porniti serviciile Docker

Rulati:

```bash
docker compose up -d
```

Verificati:

```bash
docker ps
```

Ar trebui sa vedeti:

* `seminar9_ftp_server`
* `seminar9_client1`
* `seminar9_client2`

---

## 3. Test: client1 face upload

Intrați in containerul client1:

```bash
docker exec -it seminar9_client1 /bin/sh
```

In interiorul containerului:

```sh
ls client-data
# asigurati-va ca exista from_client1.txt (sau creati unul)

python3 pyftpd_multi_client.py upload from_client1.txt
```

Notati output-ul in `ftp_multi_client_log.txt` sub sectiunea:

```text
--- CLIENT1 UPLOAD ---
<output>
```

Pe host, verificati:

```bash
ls server-data
```

Ar trebui sa contina `from_client1.txt`.

---

## 4. Test: client2 face download

Intrati in containerul client2:

```bash
docker exec -it seminar9_client2 /bin/sh
```

In interior:

```sh
python3 pyftpd_multi_client.py download from_client1.txt
ls client-data
cat client-data/from_client1.txt
```

Notati output-ul (inclusiv continutul fisierului) in `ftp_multi_client_log.txt` sub:

```text
--- CLIENT2 DOWNLOAD ---
<output>
```

---

## 5. Optional: test de pe host

De pe masina host (in afara containerelor):

1. Verificati ca serverul raspunde pe portul 2121:

```bash
ftp 127.0.0.1 2121
# name: test
# password: 12345
ftp> ls
ftp> bye
```

2. Sau folositi clientul Python din Stage 2 (daca este in acelasi director):

```bash
python3 pyftpd_client.py
```

Adaugati cel putin un fragment de output in `ftp_multi_client_log.txt` sub:

```text
--- HOST TEST ---
<output>
```

---

## 6. Intrebari de reflexie (de scris in ftp_multi_client_log.txt)

Raspundeti in cateva propozitii:

1. Care este rolul serverului in acest scenariu? De ce client1 si client2 nu trebuie
   sa se cunoasca direct intre ei?
2. De ce poate fi util un astfel de server intr-o organizatie (ex.: departament, echipa)?
3. Ce avantaje aduce rularea serverului si a clientilor in containere separate?
4. Cum ati extinde acest scenariu spre ceva asemanator cu FXP (transfer server-to-server)?

---

### Deliverable Stage 4

Predati:

* `docker-compose.yml`
* `pyftpd_server.py`
* `pyftpd_multi_client.py`
* `ftp_multi_client_log.txt` cu:

  * output de la upload (client1)
  * output de la download (client2)
  * optional: testul de pe host
  * raspunsurile la intrebarile de reflexie

Astfel se inchide Seminarul 9:

* FTP real (pyftpdlib)
* protocol pseudo-FTP activ/pasiv
* scenariu multi-client cu containere.


### Stage 4 – Testare multi-client cu containere (FTP server + 2 clienti)

In acest stage folosim containere Docker pentru a simula:

- **un server de fisiere** (FTP cu pyftpdlib)
- **doi clienti independenti** (client1 si client2) care:
  - se conecteaza la acelasi server
  - folosesc acelasi protocol (FTP)
  - transfera fisiere prin server

Scenariul de baza:

1. client1 **uploadeaza** un fisier pe server
2. client2 **downloadeaza** acelasi fisier de pe server
3. demonstram ca fisierul a ajuns de la client1 la client2 **prin server**

Acest scenariu este analog cu situatii reale:

- mai multe masinarii care folosesc acelasi server FTP pentru sharing de fisiere
- fluxuri „indirecte”: client A -> server -> client B

---

## 1. Arhitectura cu Docker Compose

Vom avea un `docker-compose.yml` cu 3 servicii:

- `ftp-server`
  - imagine: `python:3`
  - ruleaza `pyftpd_server.py` cu pyftpdlib
  - are un volum `./server-data` montat ca director de date FTP

- `client1`
  - imagine: `python:3`
  - nu face nimic automat (doar sta „in viata” cu `tail -f /dev/null`)
  - intram noi in container cu `docker exec` si rulam scriptul client

- `client2`
  - la fel ca `client1`

Toate serviciile:

- sunt pe aceeasi retea Docker (de exemplu `ftpnet`)
- pot rezolva `ftp-server` ca hostname
- pot folosi portul 2121 pentru FTP

In plus, mapam portul 2121 pe host, astfel incat:

- putem testa serverul si din afara containerelelor:
  - `ftp 127.0.0.1 2121`
  - sau `python3 pyftpd_client.py` de pe host.

---

## 2. Scenariul de laborator

1. `docker compose up -d` porneste:
   - server FTP
   - client1
   - client2

2. In `client1`:
   - rulam un script Python `pyftpd_multi_client.py`
   - scriptul se conecteaza la `ftp-server:2121`
   - face upload (`STOR`) pentru un fisier (ex. `from_client1.txt`)

3. In `client2`:
   - rulam acelasi script, dar pe modul download (`RETR`)
   - descarcam acelasi fișier in containerul `client2`

4. Verificam ca:

- fisierul apare in volumul serverului (`./server-data`)
- fisierul a ajuns la client2

---

## 3. Legatura cu celelalte stage-uri

- Stage 2: ati rulat `pyftpd_server.py` si `pyftpd_client.py` pe masina locala.
- Stage 3: ati lucrat cu pseudo-FTP activ/pasiv (protocol custom peste TCP).
- Stage 4: folositi un server FTP real (pyftpdlib) intr-un mediu cu mai multi clienti
  – scenariu mult mai apropiat de utilizare reala.

---

## 4. Terminologie

- **serviciu** (service) in Docker Compose:
  - defineste o aplicatie (container) + configuratia ei
- **retea** (network):
  - spatiu de adrese virtual pentru comunicatia intre servicii
- **volum**:
  - director persistent pentru date
  - aici: `./server-data` va contine fisierele FTP de pe server


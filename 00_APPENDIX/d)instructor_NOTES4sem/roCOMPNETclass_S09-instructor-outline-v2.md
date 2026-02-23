# Seminar S09 — FTP: două conexiuni, două moduri, o captură

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` → `04_SEMINARS/S09/` |
| **Infra** | MININET-SDN (Ubuntu 24.04, user `stud`, venv `compnet`) + `tshark` + Docker Engine/Compose |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | FTP (File Transfer Protocol, RFC 959) separă comenzile de date în conexiuni TCP distincte; cine inițiază conexiunea de date decide dacă treci sau nu de NAT. |

---

## Obiective operaționale

La final, studenții pot:

1. Arăta pe o captură (Wireshark/tshark) **două conexiuni TCP** distincte corespunzătoare canalului de control și celui de date al unui transfer FTP.
2. Identifica în text clar (plain text) credențialele `USER`/`PASS` și explica **de ce FTP clasic e nesigur** fără TLS.
3. Diferenția **active mode** (`PORT` — serverul se conectează înapoi la client) de **passive mode** (`PASV` — clientul se conectează la un port temporar al serverului) și explica implicația pentru NAT/firewall.
4. Rula un server FTP (pyftpdlib) și un client minimal (ftplib) pentru operații `LIST`, `RETR`, `STOR`.
5. Executa comenzi `active_get` / `passive_get` în pseudo-FTP-ul din kit și identifica pe captură cine trimite pachetul SYN al conexiunii de date.
6. Descrie un scenariu multi-client (client1 → server → client2) și rolul serverului ca intermediar.

---

## Structura seminarului

| Bloc | Conținut | Durată |
|:---:|---|---:|
| **A** | Hook + activare de cunoștințe + conflict cognitiv | 3–4 min |
| **B** | Demo 1 — FTP real (pyftpdlib + ftplib + captură tshark): PASV, apoi PORT | 13–15 min |
| **C** | Demo 2 — pseudo-FTP: `active_get` vs `passive_get` (cine face `listen()`?) | 10–12 min |
| **D** | Mini-demo (opțional) — multi-client cu Docker Compose | 5–6 min |
| **E** | Recap + livrabile + preview S10 | 3–4 min |
| | **Total** | **34–41 min** |

---

## Pregătire (înainte de oră — checklist 5 min)

### Trei terminale deschise pe proiector

- 🔵 **T1 (SERVER):** servere (pyftpdlib, pseudo-FTP)
- 🟢 **T2 (CLIENT):** clienți (ftplib, pseudo-FTP client)
- 🟠 **T3 (CAPTURĂ):** `tshark` → fișier `.pcapng`

### Pregătire fișiere

```bash
# 1. Activare venv (dacă nu e automat)
source ~/venvs/compnet/bin/activate

# 2. Intră în kit
cd ~/compnet-2025-redo/04_SEMINARS/S09

# 3. Stage 2 — pregătește directoarele FTP
cd 1_ftp
mkdir -p test nobody
# test/a.txt există deja în kit ("Hello from the FTP server root directory.")
ls test/a.txt   # verifică

# 4. Stage 3 — pregătește directoarele pseudo-FTP
cd ../2_custom-pseudo-ftp
mkdir -p temp client-temp
echo "server file 1" > temp/server1.txt
echo "server file 2" > temp/server2.txt
echo "client file 1" > client-temp/client1.txt

# 5. Stage 4 — pregătește Docker
cd ../3_multi-client-containers
mkdir -p server-data server-anon client1-data client2-data
echo "Hello from client1" > client1-data/from_client1.txt
```

### Verificare rapidă

```bash
pip show pyftpdlib >/dev/null 2>&1 || pip install -q pyftpdlib
docker compose version   # trebuie Compose v2
```

---

## Bloc A — Hook + activare + conflict cognitiv (3–4 min)

### Hook (scenariu situat)

> *▸ „Imaginați-vă: aveți un server FTP într-o rețea de birou. Deschideți un client, dați `LIST` și vedeți fișierele. Apoi dați `GET raport.pdf` — și transferul funcționează. Dar colegul din altă locație, de acasă, prin NAT, face exact același lucru — și transferul eșuează. Aceleași comenzi, aceeași versiune de client. De ce?"*

**De ce funcționează ca hook:** scenariul e concret (birou vs acasă), produce surpriză (aceleași comenzi, rezultat diferit) și anticipează ideea-cheie a seminarului (active vs passive + NAT).

### Activare

> *▸ „De la S04 știm că TCP e orientat pe conexiune: `connect()` → `accept()` → flux de octeți. La S07 am capturat pachete SYN/ACK. Azi folosim aceste instrumente pe un protocol real."*

### Conflict cognitiv

> *▸ „Întrebare: dacă trimit un fișier prin FTP, câte conexiuni TCP credeți că se stabilesc? Una? Două? Mai multe? Ridicați un deget sau doi."*

Notezi pe tablă distribuția răspunsurilor. **Nu corectezi.** Spui doar:

> *▸ „O să verificăm pe captură. Numărul real s-ar putea să vă surprindă."*

---

## Bloc B — Demo 1: FTP real (pyftpdlib + ftplib + captură) (13–15 min)

### B.1 Pornire server (🔵 T1)

În `04_SEMINARS/S09/1_ftp`:

```bash
python3 S09_Part01C_Script_Pyftpd_Server.py
```

> *▸ „Serverul ascultă pe portul **2121** — portul de control. Userul `test` cu parola `12345` are acces la `./test`. Rețineți: FTP clasic nu criptează nimic."*

### B.2 Pornire captură (🟠 T3)

```bash
sudo tshark -i lo -w /tmp/s09_ftp_demo.pcapng
```

> *▸ „Capturez tot traficul pe loopback. Filtrez după aceea."*

### B.3 Client — passive mode implicit (🟢 T2)

```bash
python3 - <<'PY'
from ftplib import FTP

ftp = FTP()
ftp.connect('127.0.0.1', 2121)
ftp.login('test', '12345')

print('\n--- LIST (PASV implicit) ---')
ftp.retrlines('LIST')

print('\n--- RETR a.txt ---')
with open('/tmp/downloaded_a.txt', 'wb') as fp:
    ftp.retrbinary('RETR a.txt', fp.write)

print('\nConținut descărcat:')
with open('/tmp/downloaded_a.txt') as fp:
    print(fp.read())

ftp.quit()
print('[done]')
PY
```

> *▸ „Implicit, ftplib folosește passive mode. Comanda `LIST` returnează conținutul directorului. `RETR` descarcă fișierul. În spate, pentru fiecare operație de date, se deschide o conexiune TCP separată. O vom vedea pe captură."*

**Predicție (POE — vizează concepția greșită #11: secvență socket):**

> *▸ „Întrebare: în passive mode, cine face `listen()` pe portul de date — clientul sau serverul?"*

Pauză 5 secunde. Apoi:

> *▸ „Serverul. Serverul deschide un port temporar și îl anunță clientului prin mesajul 'Entering Passive Mode (…)'. Clientul face `connect()` la acel port. De asta se numește pasiv — serverul *așteaptă* pasiv."*

### B.4 Epifanie 1 — forțăm active mode (🟢 T2)

```bash
python3 - <<'PY'
from ftplib import FTP

ftp = FTP()
ftp.connect('127.0.0.1', 2121)
ftp.login('test', '12345')
ftp.set_pasv(False)   # ACTIVE mode

print('\n--- LIST (ACTIVE) ---')
ftp.retrlines('LIST')

ftp.quit()
print('[done]')
PY
```

> *▸ „Rezultatul e identic — aceleași fișiere. Dar mecanica e inversată: acum clientul a trimis comanda `PORT`, anunțând serverul pe ce port ascultă. Serverul s-a conectat **înapoi** la client pentru a trimite datele."*

> *▸ „Și asta răspunde la întrebarea de la început: colegul de acasă, prin NAT, era în active mode. Routerul lui bloca conexiunea inițiată de server. În passive mode, clientul inițiază toate conexiunile — trece de NAT fără probleme."*

**(← Hook reluat explicit)**

### B.5 Analiză captură (🟠 T3 → Wireshark)

Oprești tshark (`Ctrl+C`), deschizi captura:

```bash
# Variantă rapidă, în terminal:
tshark -r /tmp/s09_ftp_demo.pcapng -Y "ftp" -T fields \
  -e frame.number -e ip.src -e ip.dst -e ftp.request.command -e ftp.request.arg -e ftp.response.code -e ftp.response.arg
```

Sau deschizi în Wireshark pe host (prin shared folder).

**Ce arăți explicit:**

- `USER test` și `PASS 12345` — **în clar**. Oricine capturează acest trafic vede credențialele.
- `PASV` → răspunsul `227 Entering Passive Mode (127,0,0,1,XXX,YYY)` — serverul anunță portul de date.
- `PORT` → clientul anunță portul pe care ascultă.
- În lista de conversații TCP: **două conexiuni distincte** — una persistentă (control, port 2121), una/mai multe temporare (data).

**Întrebare de fixare (30 sec):**

> *▸ „Câte conexiuni TCP vedeți? Două sau mai multe? Ce le diferențiază: portul, durata, cantitatea de date?"*

**(← Confirmarea sau infirmarea predicției de la Bloc A)**

---

## Bloc C — Demo 2: pseudo-FTP (control + data manual) (10–12 min)

**Tranziție:**

> *▸ „Acum că am văzut FTP real, construim un pas mai jos: un protocol care face exact același lucru — control pe o conexiune, date pe alta — dar fără magia pyftpdlib. Codul din kit implementează totul cu socket-uri simple."*

### C.1 Pornire server (🔵 T1)

Oprești serverul FTP (Ctrl+C), mergi în `2_custom-pseudo-ftp`:

```bash
cd ../2_custom-pseudo-ftp
python3 S09_Part02B_Script_Pseudo_FTP_Server.py
```

> *▸ „Portul **3333** e canalul de control. Fișierele server-side sunt în `./temp`."*

### C.2 (Opțional) Captură separată (🟠 T3)

```bash
sudo tshark -i lo -w /tmp/s09_pseudoftp.pcapng
```

### C.3 Client interactiv (🟢 T2)

```bash
python3 S09_Part02C_Script_Pseudo_FTP_Client.py
```

Prompt:

```text
-> help
-> list
```

**Predicție (POE — vizează concepția greșită #11):**

> *▸ „Acum fac `active_get server1.txt`. Predicție: în active mode, cine pornește `listen()` — clientul sau serverul? Amintiți-vă: 'activ' se referă la cine inițiază conexiunea de date."*

Pauză. Majoritatea vor răspunde „serverul" — pentru că în active mode serverul e cel care *se conectează*. Dar **clientul** e cel care face `listen()`, iar serverul face `connect()`.

```text
-> active_get server1.txt
```

> *▸ „Clientul a deschis un port temporar, a anunțat serverul pe canalul de control, iar serverul s-a conectat la acel port și a trimis fișierul. Clientul a ascultat — deci clientul a făcut `listen()`. Serverul a inițiat conexiunea de date."*

```text
-> passive_get server2.txt
```

> *▸ „Acum invers: serverul a ascultat pe un port temporar, clientul s-a conectat. Rezultatul e același — fișierul ajunge la client. Mecanica e diferită."*

### C.4 Epifanie 2 — framing (30–45 sec)

> *▸ „Dacă vă uitați în codul serverului, transferul trimite: 1 byte = lungimea conținutului, apoi conținutul. E un framing foarte simplist — maximum 255 de octeți. În realitate, de la S04 știm că segmentele TCP se pot fragmenta, retransmite, reordona. Framing-ul real (delimitare robustă, lungime pe 4 bytes, checksums) e o problemă non-trivială. Aici e doar o demonstrație didactică."*

### C.5 (Dacă ai capturat) Verificare SYN

```bash
tshark -r /tmp/s09_pseudoftp.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -e frame.number -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport
```

> *▸ „Căutăm pachetele SYN (fără ACK) — ele arată cine inițiază fiecare conexiune. Vedeți diferența între active și passive?"*

---

## Bloc D — (Opțional) Multi-client cu Docker Compose (5–6 min)

**Când faci acest bloc:** dacă `pip` și demo-urile au mers rapid și ești în grafic. Altfel, rămâne ca temă.

### D.1 Pornire (🔵 T1)

Din `3_multi-client-containers/`:

```bash
cd ../3_multi-client-containers
docker compose -f S09_Part03_Config_Docker_Compose.yml up -d
docker ps --format 'table {{.Names}}\t{{.Status}}'
```

### D.2 Client1 — upload (🟢 T2)

```bash
docker exec -it seminar9_client1 sh -lc \
  "ls client-data && python3 S09_Part03_Script_Pyftpd_Multi_Client.py upload from_client1.txt"
```

### D.3 Client2 — download (🟢 T2)

```bash
docker exec -it seminar9_client2 sh -lc \
  "python3 S09_Part03_Script_Pyftpd_Multi_Client.py download from_client1.txt && cat client-data/from_client1.txt"
```

> *▸ „Client2 nu știe nimic despre client1. Tot traficul trece prin server. E un pattern clasic: centralizare și control. Containerele simulează mașini distincte pe aceeași rețea Docker."*

### D.4 Curățare

```bash
docker compose -f S09_Part03_Config_Docker_Compose.yml down
```

---

## Bloc E — Recap + livrabile + preview S10 (3–4 min)

### Recap (3 idei fixate)

> *▸ „Trei lucruri de reținut:*
>
> *Unu: FTP clasic = **două conexiuni TCP** — una pentru comenzi, una pentru date. Le-am numărat pe captură.*
>
> *Doi: **active vs passive** = diferență de inițiator al conexiunii de date. Passive trece de NAT; active nu — și asta era problema colegului de acasă de la începutul orei.*
>
> *(← Hook reluat)*
>
> *Trei: **credențialele circulă în clar**. Fără TLS (FTPS) sau SSH (SFTP), oricine capturează rețeaua le vede. Observația de securitate nu e opțională — e fundamentală."*

### Livrabile (teme)

| Stage | Fișier livrabil | Ce fac studenții | Script de referință |
|---|---|---|---|
| 1 | `intro_file_protocols_log.txt` | Răspunsuri scurte la 4 întrebări conceptuale | `S09_Part01A_Explanation_File_Protocols_Intro.md` |
| 2 | `pyftpd_log.txt` | LIST/RETR/STOR + observații (modifică TODO-urile din `S09_Part01D_Script_Pyftpd_Client.py`) | `S09_Part01E_Tasks_Pyftpd.md` |
| 3 | `pseudoftp_log.txt` + modificare `help` în server | Toate comenzile din `S09_Part02D_Tasks_Pseudo_FTP.md` + întrebări reflexive | `S09_Part02D_Tasks_Pseudo_FTP.md` |
| 4 | `ftp_multi_client_log.txt` | Upload (client1) + download (client2) + întrebări reflexive | `S09_Part03B_Tasks_Multi_Client_Containers.md` |

> *▸ „La Stage 2, deschideți `S09_Part01D_Script_Pyftpd_Client.py` — e un template cu trei TODO-uri: `LIST`, `RETR`, `STOR`. Completați-le și rulați. Notați output-ul în log."*

### Preview S10

> *▸ „Săptămâna viitoare urcăm un nivel: DNS, SSH și FTP — toate orchestrate cu Docker Compose. O să vedeți cum protocoalele pe care le-am disecat azi coexistă într-o infrastructură realistă."*

---

## Cheat-sheet

### Comenzi FTP (control channel, RFC 959)

| Comandă | Rol | Răspuns tipic |
|---|---|---|
| `USER test` | Autentificare — username | `331 Username ok, send password` |
| `PASS 12345` | Autentificare — parolă | `230 Login successful` |
| `LIST` | Listare fișiere | date pe data channel |
| `RETR file` | Download fișier | date pe data channel |
| `STOR file` | Upload fișier | date pe data channel |
| `PASV` | Cere passive mode | `227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)` |
| `PORT h1,h2,h3,h4,p1,p2` | Anunță port active mode | `200 PORT command successful` |
| `QUIT` | Închide sesiunea | `221 Goodbye` |

### Pseudo-FTP (kit, port 3333)

| Comandă | Cine face `listen()` pe data? | Cine face `connect()` pe data? |
|---|---|---|
| `active_get file` | **client** | server |
| `active_put file` | **client** | server |
| `passive_get file` | **server** | client |
| `passive_put file` | **server** | client |
| `list` | — (doar control) | — |
| `help` | — (doar control) | — |

### Filtre tshark/Wireshark

| Scop | Filtru |
|---|---|
| Comenzi FTP | `ftp` |
| Date FTP | `ftp-data` |
| Ambele | `ftp \|\| ftp-data` |
| Port control specific | `tcp.port == 2121` |
| Doar SYN (inițiator) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |

### Porturi din kit

| Serviciu | Port | Unde |
|---|---|---|
| pyftpdlib FTP control | 2121 | `S09_Part01C`, `S09_Part03_Script_Pyftpd_Server.py` |
| Pseudo-FTP control | 3333 | `S09_Part02B_Script_Pseudo_FTP_Server.py` |
| Data connections | dinamic | alocat la runtime |

---

## Plan de contingență

| # | Problemă | Soluție |
|---|---|---|
| 1 | `pip install pyftpdlib` lent sau eșuează (fără internet) | Sari la Bloc D (multi-client Docker) — serverul își instalează singur dependența în container. Faci doar discuția de captură conceptual. |
| 2 | Portul 2121 ocupat | `ss -tulnp \| grep 2121` → identifici procesul → `kill`. Sau schimbi temporar portul în `S09_Part01C` (linia `FTPServer(('0.0.0.0', XXXX), handler)`). |
| 3 | Portul 3333 ocupat | Același procedeu: `ss -tulnp \| grep 3333` → `kill`. |
| 4 | Wireshark indisponibil pe host | Folosești `tshark -r` direct în VM — exemplu dat în Bloc B.5. |
| 5 | Docker nu pornește / Compose eșuează | `sudo service docker start`. Dacă persistă, renunți la Bloc D — rămâne temă. |
| 6 | `tshark` necesită `sudo` și parola nu merge | Adaugă userul la grupul `wireshark`: `sudo usermod -aG wireshark stud && newgrp wireshark`. |
| 7 | Captură goală (0 pachete pe loopback) | Verifică interfața: `tshark -D`. Pe unele configurări e `lo0` nu `lo`. |

---

## Referințe (APA 7th)

Postel, J. și Reynolds, J. (1985). *File Transfer Protocol* (RFC 959). RFC Editor. https://doi.org/10.17487/RFC0959

Bellovin, S. M. (1994). *Firewall-friendly FTP* (RFC 1579). RFC Editor. https://doi.org/10.17487/RFC1579

Allman, M. și Ostermann, S. (1999). *FTP security considerations* (RFC 2577). RFC Editor. https://doi.org/10.17487/RFC2577

Ford-Hutchinson, P. (2005). *Securing FTP with TLS* (RFC 4217). RFC Editor. https://doi.org/10.17487/RFC4217

Saltzer, J. H., Reed, D. P. și Clark, D. D. (1984). End-to-end arguments in system design. *ACM Transactions on Computer Systems, 2*(4), 277–288. https://doi.org/10.1145/357401.357402

Bellovin, S. M. (1989). Security problems in the TCP/IP protocol suite. *ACM SIGCOMM Computer Communication Review, 19*(2), 32–48. https://doi.org/10.1145/378444.378449

---

## Note pedagogice

**Tipar POE principal (Bloc B.3–B.4):** Predicția „câte conexiuni TCP?" se verifică pe captură. Studenții care au răspuns „una" la Bloc A descoperă pe captură că sunt minim două. Epifania vizuală: lista de conversații TCP din Wireshark.

**Tipar POE secundar (Bloc C.3):** „Cine face `listen()` în active mode?" — invers-intuitiv. Concepția greșită #11 (confuzie secvență server/client) se manifestă aici: studenții tind să creadă că serverul face `listen()` întotdeauna, dar în active mode clientul face `listen()` pe portul de date.

**Legătura cu concepția greșită #12 (recv() parțial):** Pseudo-FTP folosește un framing pe 1 byte + recv(1024) și presupune că totul ajunge într-un singur apel. Comentariul din cod (`[WARN] content_length vs data length mismatch`) evidențiază exact limita discutată la S04. Nu insista prea mult — 30 de secunde, fără deraiere.

**Progresia temelor:** Stage 1–2 sunt auto-studiu + completare template (amintire/înțelegere/aplicare). Stage 3 cere analiză (active vs passive → cine face listen/connect). Stage 4 cere sinteză (scenariu multi-client, întrebări reflexive despre rolul serverului și extensibilitate FXP).

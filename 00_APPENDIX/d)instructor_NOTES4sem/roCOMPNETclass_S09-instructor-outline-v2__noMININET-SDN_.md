# Seminar S09 — FTP: două conexiuni, două moduri, o captură

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` → `04_SEMINARS/S09/` |
| **Infra** | Windows 10/11 + Docker Desktop (Linux containers) + Wireshark (Npcap) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | FTP (File Transfer Protocol, RFC 959) separă comenzile de date în conexiuni TCP distincte; cine inițiază conexiunea de date decide dacă treci sau nu de NAT. |

---

## Obiective operaționale

La final, studenții pot:

1. Arăta pe o captură Wireshark **două conexiuni TCP** distincte corespunzătoare canalului de control și celui de date al unui transfer FTP.
2. Identifica în text clar (plain text) credențialele `USER`/`PASS` și explica **de ce FTP clasic e nesigur** fără TLS.
3. Diferenția **active mode** (`PORT` — serverul se conectează înapoi la client) de **passive mode** (`PASV` — clientul se conectează la un port temporar al serverului) și explica implicația pentru NAT/firewall.
4. Rula un scenariu multi-client (Docker Compose) cu operații `STOR`/`RETR` și verifica transferul client1 → server → client2.
5. Executa comenzi `active_get` / `passive_get` în pseudo-FTP-ul din kit și identifica diferența de inițiator al conexiunii de date.
6. Descrie rolul serverului ca intermediar în scenarii multi-client.

---

## Structura seminarului

| Bloc | Conținut | Durată |
|:---:|---|---:|
| **A** | Hook + activare de cunoștințe + conflict cognitiv | 3–4 min |
| **B** | Demo 1 — multi-client cu Docker Compose (server + 2 clienți) | 10–12 min |
| **C** | Captură cu `tcpdump` în container + analiză în Wireshark | 12–14 min |
| **D** | Demo 2 — pseudo-FTP într-un container interactiv (`active_get` vs `passive_get`) | 8–10 min |
| **E** | Recap + livrabile + preview S10 | 3–4 min |
| | **Total** | **36–44 min** |

> **Regulă de ritm:** dacă Docker trage imagini lent la Bloc B, sari direct la Bloc D (pseudo-FTP într-un singur container, fără Compose). Dacă Wireshark/captura întârzie, faci doar Bloc B și explici conceptual diferența control/data. Dacă totul merge rapid, dedici timp suplimentar analizei Wireshark din Bloc C.

---

## Pregătire (înainte de oră — checklist 5 min)

### Pe Windows

1. PowerShell:
   ```powershell
   docker version
   docker compose version
   ```

2. Poziționare în directorul seminarului:
   ```powershell
   cd C:\...\compnet-2025-redo\04_SEMINARS\S09
   dir
   ```
   Trebuie să vezi: `1_ftp\`, `2_custom-pseudo-ftp\`, `3_multi-client-containers\`.

3. Deschide Wireshark (să nu pierzi timp cu UI-ul mai târziu).

### Pre-pull imagini (recomandat, o singură dată înainte de oră)

```powershell
cd .\3_multi-client-containers
mkdir server-data, server-anon, client1-data, client2-data -Force
docker compose -f .\S09_Part03_Config_Docker_Compose.yml pull
```

---

## Bloc A — Hook + activare + conflict cognitiv (3–4 min)

### Hook (scenariu situat)

> *▸ „Imaginați-vă: aveți un server FTP într-o rețea de birou. Deschideți un client, dați `LIST` și vedeți fișierele. Apoi dați `GET raport.pdf` — și transferul funcționează. Dar colegul din altă locație, de acasă, prin NAT, face exact același lucru — și transferul eșuează. Aceleași comenzi, aceeași versiune de client. De ce?"*

**De ce funcționează ca hook:** scenariul e concret (birou vs acasă), produce surpriză (aceleași comenzi, rezultat diferit) și anticipează ideea-cheie (active vs passive + NAT).

### Activare

> *▸ „De la S04 știm că TCP e orientat pe conexiune: `connect()` → `accept()` → flux de octeți. La S07 am capturat pachete SYN/ACK. Azi folosim aceste instrumente pe un protocol real."*

### Conflict cognitiv

> *▸ „Întrebare: dacă trimit un fișier prin FTP, câte conexiuni TCP credeți că se stabilesc? Una? Două? Mai multe? Ridicați un deget sau doi."*

Notezi pe tablă distribuția. **Nu corectezi.** Spui doar:

> *▸ „O să verificăm pe captură. Numărul real s-ar putea să vă surprindă."*

### Mini-model mental (60 sec)

Desenezi rapid pe tablă:

```
Client ──[control, port 2121]──▶ Server
Client ──[data, port dinamic]──▶ Server   (passive)
Client ◀──[data, port dinamic]── Server   (active)
```

> *▸ „FTP clasic = două conexiuni. Comenzi pe una, fișiere pe alta. Întrebarea e: cine inițiază a doua?"*

---

## Bloc B — Demo 1: multi-client cu Docker Compose (10–12 min)

> *▸ „Simulăm 3 mașini: un server FTP și 2 clienți independenți, pe aceeași rețea Docker."*

### B.1 Pornire servicii

Din PowerShell, în `S09\3_multi-client-containers`:

```powershell
cd .\3_multi-client-containers
mkdir server-data, server-anon, client1-data, client2-data -Force
"Hello from client1" | Out-File -Encoding ascii .\client1-data\from_client1.txt

docker compose -f .\S09_Part03_Config_Docker_Compose.yml up -d
```

Verificare:

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
```

> *▸ „Avem 3 containere: `seminar9_ftp_server`, `seminar9_client1`, `seminar9_client2`. DNS-ul intern Docker rezolvă `ftp-server` între containere. Serverul ascultă pe portul 2121, user `test/12345`."*

### B.2 Client1 — upload (STOR)

```powershell
docker exec -it seminar9_client1 sh -lc "ls client-data && python3 S09_Part03_Script_Pyftpd_Multi_Client.py upload from_client1.txt"
```

> *▸ „Client1 s-a logat, a făcut `STOR` și a încărcat fișierul pe server. Observați output-ul: vedeți lista de fișiere de pe server după upload."*

### B.3 Client2 — download (RETR)

```powershell
docker exec -it seminar9_client2 sh -lc "python3 S09_Part03_Script_Pyftpd_Multi_Client.py download from_client1.txt && cat client-data/from_client1.txt"
```

**Epifanie 1 (20 sec):**

> *▸ „Client2 nu știe nimic despre client1. Totul e mediat de server. E un pattern clasic: centralizare — client A depune, client B ridică, serverul e singurul punct de contact."*

**Predicție:**

> *▸ „Întrebare: credențialele `test/12345` pe care le-au folosit ambii clienți — sunt criptate pe rețea sau circulă în clar?"*

Pauză. Apoi:

> *▸ „Verificăm pe captură."*

---

## Bloc C — Captură cu `tcpdump` în container + analiză Wireshark (12–14 min)

> *▸ „Pe Windows, captura traficului intern Docker poate fi inconsistentă. Soluția: capturăm direct din interiorul containerului server, apoi deschidem pcap-ul în Wireshark."*

### C.1 Instalare `tcpdump` în containerul server

```powershell
docker exec -it seminar9_ftp_server sh -lc "apk add --no-cache tcpdump"
```

### C.2 Pornire captură (în background)

```powershell
docker exec -d seminar9_ftp_server sh -lc "tcpdump -i eth0 -s 0 -w /tmp/s09_ftp.pcap tcp"
```

> *▸ „Capturez tot TCP pe interfața `eth0` a containerului. Rulează în background."*

### C.3 Generare trafic (repetare upload + download)

Repetă rapid comenzile din Bloc B (sau măcar doar un `LIST` + `RETR`):

```powershell
docker exec -it seminar9_client1 sh -lc "python3 S09_Part03_Script_Pyftpd_Multi_Client.py upload from_client1.txt"
docker exec -it seminar9_client2 sh -lc "python3 S09_Part03_Script_Pyftpd_Multi_Client.py download from_client1.txt"
```

### C.4 Oprire captură și copiere pe Windows

```powershell
docker exec seminar9_ftp_server sh -lc "pkill tcpdump"
docker cp seminar9_ftp_server:/tmp/s09_ftp.pcap .\s09_ftp.pcap
```

### C.5 Analiză în Wireshark

Wireshark → **File → Open** → `s09_ftp.pcap`.

Filtru: `ftp || ftp-data` (alternativ: `tcp.port == 2121`).

**Ce arăți explicit:**

- `USER test` și `PASS 12345` — **în text clar**. Oricine capturează traficul vede credențialele.

  > *▸ „Și asta răspunde la întrebarea de adineauri: da, credențialele circulă necriptate. De aceea SFTP (prin SSH) și FTPS (FTP peste TLS) au înlocuit practic FTP-ul clasic în producție."*

- `PASV` + răspuns `227 Entering Passive Mode (…)` — serverul anunță portul de date.
- Două conversații TCP: una persistentă (control), una/mai multe temporare (data).

**Epifanie 2 — numărarea conexiunilor:**

> *▸ „Câte conexiuni TCP distincte vedeți? Cel puțin două. Și asta confirmă sau infirmă predicția de la început."*

**(← Hook reluat implicit prin confirmarea predicției de la Bloc A)**

**Întrebare de fixare (30 sec):**

> *▸ „Ce diferențiază conexiunea de control de cea de date: portul, durata, direcția, cantitatea de date?"*

---

## Bloc D — Pseudo-FTP într-un container interactiv (8–10 min)

**Tranziție:**

> *▸ „Am văzut FTP real cu pyftpdlib. Acum privim mecanica de jos: un protocol care face același lucru cu socket-uri simple — control pe o conexiune, date pe alta, active și passive implementate manual."*

### D.1 Pornire container de lucru

Din folderul `S09` (revin din `3_multi-client-containers`):

```powershell
cd ..\

docker run -it --rm -v ${PWD}:/work -w /work python:3.12-slim bash
```

În interiorul containerului:

```bash
# Pregătire fișiere
mkdir -p 2_custom-pseudo-ftp/temp 2_custom-pseudo-ftp/client-temp
echo "server file 1" > 2_custom-pseudo-ftp/temp/server1.txt
echo "server file 2" > 2_custom-pseudo-ftp/temp/server2.txt
echo "client file 1" > 2_custom-pseudo-ftp/client-temp/client1.txt

# Pornire server (background)
python3 2_custom-pseudo-ftp/S09_Part02B_Script_Pseudo_FTP_Server.py &
sleep 1   # așteptăm ca serverul să facă listen()

# Pornire client (interactiv)
python3 2_custom-pseudo-ftp/S09_Part02C_Script_Pseudo_FTP_Client.py
```

### D.2 Comenzi în client

```text
-> help
-> list
```

**Predicție (POE — vizează concepția greșită #11):**

> *▸ „Fac `active_get server1.txt`. Predicție: în active mode, cine face `listen()` pe portul de date — clientul sau serverul?"*

Pauză 5 secunde. Majoritatea vor răspunde „serverul". Corect e **clientul**.

```text
-> active_get server1.txt
```

> *▸ „Clientul a deschis un port temporar, l-a anunțat pe canalul de control, iar serverul s-a conectat la acel port. Clientul a ascultat — deci clientul a făcut `listen()`. Serverul a inițiat conexiunea de date."*

```text
-> passive_get server2.txt
```

> *▸ „Acum invers: serverul a ascultat pe un port temporar, clientul s-a conectat. Rezultatul e același — fișierul ajunge. Mecanica e diferită."*

> *▸ „Și asta răspunde complet la întrebarea de la început: colegul de acasă, prin NAT, era în active mode. Routerul lui bloca conexiunea inițiată de server. În passive mode, clientul inițiază totul — trece de NAT fără probleme."*

**(← Hook reluat explicit)**

### D.3 Observație framing (20 sec)

> *▸ „Protocolul demo trimite 1 byte = lungimea conținutului, apoi conținutul. Maximum 255 de octeți. În realitate, de la S04 știm că segmentele TCP se pot fragmenta. Ăsta e un framing didactic, nu unul de producție."*

La final: `exit` (containerul se oprește automat).

---

## Bloc E — Recap + livrabile + preview S10 (3–4 min)

### Recap (3 idei fixate)

> *▸ „Trei lucruri de reținut:*
>
> *Unu: FTP clasic = **două conexiuni TCP** — una pentru comenzi, una pentru date. Le-am văzut pe captură.*
>
> *Doi: **active vs passive** = diferență de inițiator al conexiunii de date. Passive trece de NAT; active nu — și asta era problema colegului de acasă de la începutul orei.*
>
> *(← Hook reluat)*
>
> *Trei: **credențialele circulă în clar**. Fără TLS (FTPS) sau SSH (SFTP), oricine capturează rețeaua le vede."*

### Livrabile (teme)

| Stage | Fișier livrabil | Ce fac studenții | Script de referință |
|---|---|---|---|
| 1 | `intro_file_protocols_log.txt` | Răspunsuri scurte la 4 întrebări conceptuale | `S09_Part01A_Explanation_File_Protocols_Intro.md` |
| 2 | `pyftpd_log.txt` | LIST/RETR/STOR + observații (modifică TODO-urile din `S09_Part01D_Script_Pyftpd_Client.py`); pot rula serverul local sau în container (portul 2121 e mapat pe host) | `S09_Part01E_Tasks_Pyftpd.md` |
| 3 | `pseudoftp_log.txt` + modificare `help` în server | Toate comenzile din `S09_Part02D_Tasks_Pseudo_FTP.md` + întrebări reflexive | `S09_Part02D_Tasks_Pseudo_FTP.md` |
| 4 | `ftp_multi_client_log.txt` | Upload (client1) + download (client2) + întrebări reflexive | `S09_Part03B_Tasks_Multi_Client_Containers.md` |

> *▸ „Stage 1 și Stage 2 le faceți acasă. Citiți explicațiile din `S09_Part01A` și `S09_Part01B`, apoi modificați template-ul client (`S09_Part01D_Script_Pyftpd_Client.py`) — are trei TODO-uri: `LIST`, `RETR`, `STOR`. Serverul FTP rulează deja în container (portul 2121 e mapat pe host), deci puteți testa fără să instalați pyftpdlib local."*

> *▸ „Stage 3: porniți un container cu `python:3.12-slim` (exact ca în demo) și rulați pseudo-FTP-ul. Stage 4: scenariul multi-client l-ați văzut deja — refaceți-l și documentați."*

### Preview S10

> *▸ „Săptămâna viitoare: DNS, SSH și FTP — toate orchestrate cu Docker Compose. O să vedeți cum protocoalele pe care le-am disecat azi coexistă într-o infrastructură realistă."*

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

### Docker (comenzi uzuale)

| Comandă | Ce face |
|---|---|
| `docker compose -f FILE.yml up -d` | Pornește serviciile în background |
| `docker compose -f FILE.yml down` | Oprește și curăță serviciile |
| `docker ps --format "table {{.Names}}\t{{.Status}}"` | Listare containere |
| `docker exec -it CONTAINER sh -lc "CMD"` | Execută comandă într-un container |
| `docker exec -d CONTAINER sh -lc "CMD"` | Execută în background (detached) |
| `docker cp CONTAINER:PATH LOCAL` | Copiază fișier din container pe host |
| `docker run -it --rm -v ${PWD}:/work -w /work IMAGE bash` | Container temporar cu volum montat |

### Filtre Wireshark

| Scop | Filtru |
|---|---|
| Comenzi FTP | `ftp` |
| Date FTP | `ftp-data` |
| Ambele | `ftp \|\| ftp-data` |
| Port control specific | `tcp.port == 2121` |
| Doar SYN (inițiator) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |

---

## Plan de contingență

| # | Problemă | Soluție |
|---|---|---|
| 1 | Docker Desktop nu e pornit / Docker trage imagini lent | Pre-pull înainte de oră (`docker compose pull`). Dacă persistă, sari direct la Bloc D (pseudo-FTP într-un singur container, fără Compose). |
| 2 | `apk add tcpdump` eșuează (container fără internet) | Renunți la captură live. Explici conceptual diferența control/data folosind diagrama de pe tablă. Studenții vor face captura acasă. |
| 3 | Wireshark nu deschide `s09_ftp.pcap` | Verifică dacă fișierul e nenul: `dir s09_ftp.pcap`. Dacă e gol, repetă captura. Alternativ, folosește `tcpdump -r` direct în container. |
| 4 | Portul 2121 ocupat pe host | Modifică mapping-ul în `S09_Part03_Config_Docker_Compose.yml`: schimbă `"2121:2121"` cu `"21210:2121"`. |
| 5 | PowerShell: `${PWD}` nu funcționează (versiune veche) | Înlocuiește cu `$pwd.Path` sau cu calea absolută. |
| 6 | Container pseudo-FTP: `connect()` eșuează (server nu e ready) | Mărește `sleep` de la 1 la 3 secunde. Sau pornește serverul manual, apoi clientul. |
| 7 | Studenții nu au Docker Desktop | Alternativă: rulează pseudo-FTP direct pe Windows (`python S09_Part02B...py` într-un terminal, `python S09_Part02C...py` în altul). Necesită Python 3.x instalat local. |

---

## Referințe (APA 7th)

Postel, J. și Reynolds, J. (1985). *File Transfer Protocol* (RFC 959). RFC Editor. https://doi.org/10.17487/RFC0959

Bellovin, S. M. (1994). *Firewall-friendly FTP* (RFC 1579). RFC Editor. https://doi.org/10.17487/RFC1579

Allman, M. și Ostermann, S. (1999). *FTP security considerations* (RFC 2577). RFC Editor. https://doi.org/10.17487/RFC2577

Ford-Hutchinson, P. (2005). *Securing FTP with TLS* (RFC 4217). RFC Editor. https://doi.org/10.17487/RFC4217

Saltzer, J. H., Reed, D. P. și Clark, D. D. (1984). End-to-end arguments in system design. *ACM Transactions on Computer Systems, 2*(4), 277–288. https://doi.org/10.1145/357401.357402

---

## Note pedagogice

**Ordonarea blocurilor — diferență față de varianta VM:** pe Windows nativ, pseudo-FTP fără Compose e mai simplu de pornit decât pe VM (nu necesită `pip install`), dar multi-client Docker e mai spectaculos ca punct de intrare. Ordinea B (Docker multi-client) → C (captură) → D (pseudo-FTP) asigură un demo vizual imediat și amână pseudo-FTP-ul (mai abstract) pentru după ce studenții au văzut traficul real.

**Stage 1 și Stage 2 ca teme:** spre deosebire de varianta VM (unde pyftpdlib rulează nativ), pe Windows fără VM nu avem Python cu pip într-un mediu controlat. Soluția: serverul FTP rulează deja în container (portul 2121 mapat pe host). Studenții pot rula `S09_Part01D_Script_Pyftpd_Client.py` de pe Windows dacă au Python instalat, sau dintr-un container temporar. Explicațiile din `S09_Part01A` și `S09_Part01B` se citesc ca auto-studiu.

**Tipar POE principal (Bloc C.5):** credențialele în clar pe captură. Studenții care au anticipat „sunt criptate" descoperă vizual pe ecran `USER test` / `PASS 12345`.

**Tipar POE secundar (Bloc D.2):** „cine face listen() în active mode?" — concepție greșită #11 (confuzia secvență server/client). Clientul face `listen()` pe data, nu serverul.

**Progresia temelor:** Stage 1–2 sunt auto-studiu (amintire/înțelegere/aplicare). Stage 3 cere analiză (active vs passive → cine face listen/connect). Stage 4 cere sinteză (scenariu multi-client, întrebări reflexive).

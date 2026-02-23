# Seminar S02 — Socket programming TCP/UDP și analiză de trafic

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` · `04_SEMINARS/S02/` (11 fișiere: exemple, template-uri, scenarii) |
| **Infra** | Windows nativ + Docker Desktop + Wireshark (fără MININET-SDN) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un socket e punctul unde codul tău întâlnește rețeaua; TCP (Transmission Control Protocol) livrează un stream de octeți — dacă vrei „mesaje", le definești tu. |

---

## Obiective operaționale

La finalul seminarului (și după lucrul individual pe template-uri), studenții pot:

1. **Porni** un server TCP concurent și un client TCP în Python (în container Docker) și **explica** rolurile: serverul execută `bind → listen → accept`, clientul execută `connect`.
2. **Identifica** într-o captură Wireshark cele trei faze ale unei conversații TCP: handshake (SYN → SYN-ACK → ACK), payload și teardown (FIN/ACK sau RST).
3. **Argumenta** de ce portul clientului este efemer și de ce portul serverului este fix.
4. **Demonstra** că TCP livrează un stream de octeți, nu „mesaje" — folosind o captură cu două conexiuni separate.
5. **Compara** TCP cu UDP (User Datagram Protocol) la nivel de pachete: prezența/absența handshake-ului, noțiunea de stream vs. datagramă, comportament la server oprit.
6. **Produce** artefacte verificabile: fișiere `.txt` cu log-uri și comentarii + fișiere `.pcapng` cu capturi relevante.

---

## Precondiții (trimise studenților cu 24-48h înainte)

1. **Docker Desktop** instalat și funcțional pe Windows (WSL2 sau Hyper-V — indiferent).
2. **Wireshark** instalat pe Windows (cu Npcap).
3. Starterkit-ul extras local — folderul `04_SEMINARS\S02\` cu fișierele `S02_Part01_…` etc.
4. **(Instructor)** Imaginea Docker pregătită în avans:

```dockerfile
# Fișier: Dockerfile.s02 (în folderul S02)
FROM python:3.12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    tcpdump netcat-openbsd iproute2 procps \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
CMD ["bash"]
```

```powershell
# O singură dată, înainte de oră:
cd D:\compnet-2025-redo-main\04_SEMINARS\S02
docker build -t compnet-s02lab:1.0 -f Dockerfile.s02 .
docker run --rm compnet-s02lab:1.0 python --version   # test
```

---

## Structura seminarului

| Bloc | Temă | Durată | Tip |
|:---:|---|:---:|:---:|
| **A** | Hook + activare + conflict cognitiv | 3 min | Interactiv |
| **B** | Pornire container laborator | 3 min | Setup |
| **C** | TCP în practică: server + client + captură + analiză | 14 min | Demo + POE |
| **D** | Template-uri TCP: ghidare pentru temă | 7 min | Ghidare + hands-on |
| **E** | UDP: demo + captură + comparație TCP vs UDP | 8 min | Demo + „Ce dacă…?" |
| **F** | Recap + livrabile + cleanup Docker + direcție S03 | 5 min | Sinteză |
| | **Total** | **40 min** | |

**Variabilă de ajustare:** dacă timpul se comprimă, sacrifică demonstrația opțională „client de 2 ori" din C și comentariul extins la conversie `.pcap` → `.pcapng`. Sub nicio formă nu se sacrifică blocul C (epifanie stream) sau E (comparație UDP).

---

## Pregătire „de regie" (înainte de cronometru)

- **Windows Terminal** cu 3 tab-uri PowerShell, etichetate: **CAPTURE**, **SERVER**, **CLIENT**.
- **Wireshark** deschis (fără captură activă — se va folosi la „Open file").
- Folderul S02 deschis în File Explorer (pentru confirmare vizuală a fișierelor `.pcap` generate).

---

## Bloc A (0:00–0:03) — Hook, activare, conflict cognitiv

> *▸ „Pornesc un client TCP fără server. Ce se întâmplă?"*

**Ce faci (pe mașina locală, înainte de Docker — intenționat):**

Deschide un terminal Python rapid:
```powershell
python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 12345))"
```

Pauză de 2 secunde. Eroare:
```
ConnectionRefusedError: [Errno 10061] ...
```

**Ce spui:**

> *▸ „La S01 am văzut rețeaua din exterior, cu netcat și Wireshark. Azi intrăm în mecanism: scriem noi procesul care vorbește pe rețea."*

> *▸ „Clientul a vrut să se conecteze, dar nimeni nu ascultă. TCP refuză — activ, explicit. Rețineți asta: o comparăm cu UDP mai târziu."*

**Întrebare rapidă (2-3 mâini):** „Când un server 'ascultă', ce face fizic? Alocă memorie? Blochează un port? Trimite ceva?"

**De ce funcționează hook-ul:** e situat (eroare reală, pe ecran), afectiv (surpriza eșecului), tematic (diferența TCP vs UDP), concis (sub 30 sec de execuție) și returnabil (la recap reluăm: „acum știm de ce TCP refuză iar UDP nu").

---

## Bloc B (0:03–0:06) — Pornire container laborator

**Ce faci (tab-ul CAPTURE, PowerShell):**

```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S02
ls
```

Confirmă vizual: fișierele `S02_Part01_…` etc. sunt prezente.

```powershell
docker rm -f s02lab 2>$null
docker run -d --name s02lab `
  -v "${PWD}:/work" -w /work `
  --cap-add=NET_RAW --cap-add=NET_ADMIN `
  compnet-s02lab:1.0 sleep infinity
```

Verificare:
```powershell
docker exec s02lab python --version
docker exec s02lab ls
```

> *▸ „Docker servește strict ca mediu reproductibil: toți aveți aceeași versiune de Python (3.12) și aceleași unelte. Tot ce rulăm e din folderul S02 — Docker doar execută."*

> *▸ „Containerul are `--cap-add=NET_RAW` ca să putem rula `tcpdump`. Fișierele din S02 sunt montate ca volum (`-v`): ce modificați pe Windows apare imediat în container."*

---

## Bloc C (0:06–0:20) — TCP: server + client + captură + Wireshark

### C1. Pornire captură TCP (în container)

🟠 **CAPTURĂ:**
```powershell
docker exec -it s02lab tcpdump -i lo -nn -w /work/tcp_demo.pcap "tcp port 12345"
```

> *▸ „Captăm pe loopback (`lo`) — traficul rămâne în container, controlat. Fișierul `.pcap` se scrie direct în folderul vostru prin volum."*

### C2. Pornire server TCP exemplu

🔵 **SERVER:**
```powershell
docker exec -it s02lab python S02_Part01_Example_TCP_Server.py
```

**Output așteptat:**
```
[INFO] TCP server listening on 127.0.0.1:12345
```

> *▸ „Serverul ascultă pe `127.0.0.1:12345`. Modelul: `socketserver.ThreadingMixIn` — un thread per conexiune. Concurență elementară, dar suficientă."*

### C3. Rulare client TCP (predicție → observație → explicație)

**Predicție (5 sec):** „Câte pachete credeți că generează un singur request-response TCP?"

🟢 **CLIENT:**
```powershell
docker exec -it s02lab python S02_Part04_Example_TCP_Client.py
```

**Output client:**
```
[CLIENT] Sent: Hello, world
[CLIENT] Received: HELLO, WORLD
```

**Output server:**
```
[SERVER] Received from ('127.0.0.1', 54xxx): Hello, world
```

**Moment POE — port efemer (vizează misconception #11):**

> *▸ „Portul clientului: 54-și-ceva-mii. Nu 12345. OS-ul alocă un port efemer (de regulă 49152–65535, cf. RFC 6335). Serverul are port fix ca să poată fi găsit. Clientul e cel care inițiază."*

### C4. Oprire captură + analiză în Wireshark

🟠 `Ctrl+C` în tab-ul CAPTURE.

**Pe Windows — Wireshark:** File → Open → `tcp_demo.pcap` (din folderul S02).

Display filter:
```
tcp.port == 12345
```

**Ce arăți (pe proiector, strict 3 lucruri):**

1. **Handshake:** SYN → SYN-ACK → ACK (3 pachete)
   > *▸ „TCP stabilește conexiune înainte de date. Aceste 3 pachete creează stare comună: porturi, numere de secvență, dimensiune de fereastră."*

2. **Payload:** segmentul cu `Hello, world` → `HELLO, WORLD`
   > *▸ „Datele voastre, vizibile în clar."*

3. **Teardown:** FIN/ACK (sau RST)
   > *▸ „TCP își ia la revedere explicit."*

**Răspuns la predicție:** „Cel puțin 7 pachete: 3 handshake + 2 payload + 2 teardown. Overhead-ul TCP e prețul fiabilității."

### C5. Epifanie: TCP = stream, nu „mesaje" (vizează misconception #12)

**Ce faci (opțional dacă ritmul permite):** rulezi clientul de 2 ori:
```powershell
docker exec s02lab python S02_Part04_Example_TCP_Client.py
docker exec s02lab python S02_Part04_Example_TCP_Client.py
```

Reîmprospătează Wireshark (F5 sau re-open). Două handshake-uri cu porturi efemere diferite.

**Ce spui:**

> *▸ „`recv(1024)` nu înseamnă 'primește un mesaj'. Înseamnă 'dă-mi până la 1024 de bytes din stream'. TCP nu știe unde se termină un mesaj — asta e treaba aplicației."*

> *▸ „Dacă vreți mesaje, definiți framing: newline, prefix de lungime, structură fixă. HTTP face exact asta cu `Content-Length`. Nu pentru că TCP ar cere, ci pentru că TCP nu garantează granularitate."*

**Moment de fixare:** „TCP = stream de octeți. Mesajul e invenția aplicației."

---

## Bloc D (0:20–0:27) — Template-uri TCP: ghidare pentru temă

### D1. Template TCP server — ce completează

**Deschide** (în VS Code sau Notepad++, pe Windows) `S02_Part02_Template_TCP_Server.py`.

Arată zona `>>> STUDENT CODE STARTS HERE`:

> *▸ „Trei lucruri de implementat: (1) log complet — IP, port, mesaj, lungime în bytes; (2) construiți răspunsul `b"OK: " + mesaj.upper()`; (3) trimiteți cu `sendall()`."*

**Subliniază:**
- `self.client_address` → `(ip, port)` — tuplu
- `self.data` → bytes, decodați cu `.decode(errors='replace')` (misconception #10)
- `sendall()` vs `send()` — `sendall` garantează trimiterea integrală

> *▸ „Scenariul complet, pas cu pas: `S02_Part03_Scenario_TCP_Server_Netcat_Wireshark.md`. Citiți-l înainte de a începe — conține secvența exactă de testare și fișierele de încărcat."*

### D2. Cum testează (30 sec, în Docker)

🔵 **SERVER:**
```powershell
docker exec -it s02lab python S02_Part02_Template_TCP_Server.py
```

🟢 **CLIENT:**
```powershell
docker exec -it s02lab sh -c "echo salut | nc 127.0.0.1 12345"
```

Așteptați `OK: SALUT`.

> *▸ „Tot ce modificați pe Windows apare imediat în container — volumul e sincron."*

### D3. Template TCP client — buclă + RTT

**Deschide** `S02_Part05_Template_TCP_Client.py`. Arată zona TODO:

> *▸ „Buclă `while True`, citire de la tastatură, trimitere, recepție, măsurare RTT cu `time.time()`. Ieșire la comanda `exit`."*

> *▸ „Scenariul detaliat: `S02_Part06_Scenario_TCP_Client.py` (citiți docstring-ul). Atenție: scenariul referă niște nume de fișiere vechi — folosiți numele reale din folderul S02."*

### D4. Livrabile TCP

| Fișier | Conținut |
|---|---|
| `tcp_server_activity_output.txt` | Comenzi + min. 5 linii log server + comentariu 3-5 propoziții |
| `tcp_client_activity_output.txt` | Log-uri client (mesaje, răspunsuri, RTT) + statistici |
| `tcp_traffic_capture.pcapng` | Captură Wireshark (Save As `.pcapng` din `.pcap`) |

**Conversie format:** în Wireshark, File → Save As → format implicit (`.pcapng`).

---

## Bloc E (0:27–0:35) — UDP: demo + captură + comparație

### E1. Pornire captură UDP

🟠 **CAPTURĂ:**
```powershell
docker exec -it s02lab tcpdump -i lo -nn -w /work/udp_demo.pcap "udp port 12345"
```

### E2. Pornire server UDP exemplu

🔵 **SERVER:**
```powershell
docker exec -it s02lab python S02_Part07_Example_UDP_Server.py 12345
```

**Output așteptat:**
```
[INFO] UDP server listening on 0.0.0.0:12345
```

> *▸ „API diferit: `recvfrom`/`sendto`. Nu există `connect`/`accept` — UDP nu creează conexiune."*

### E3. Test cu client UDP Python (predicție)

**Predicție:** „Câte pachete pentru un request-response UDP?"

🟢 **CLIENT:**
```powershell
docker exec s02lab python S02_Part09_Example_UDP_Client.py 127.0.0.1 12345 "Hello from client"
```

**Output client:**
```
[INFO] Sending 17 bytes to 127.0.0.1:12345 ...
[INFO] Received 17 bytes from ('127.0.0.1', 12345): b'HELLO FROM CLIENT'
```

**Răspuns la predicție:** „Două pachete. Zero handshake."

### E4. „Ce s-ar fi întâmplat dacă…?" — server oprit, client trimite (vizează hook-ul)

🔵 **SERVER:** `Ctrl+C` (oprește serverul).

🟢 **CLIENT:**
```powershell
docker exec s02lab python S02_Part09_Example_UDP_Client.py 127.0.0.1 12345 "ping"
```

**Output (după ~3 sec):**
```
[WARN] No response received (timeout).
```

> *▸ „Rețineți hook-ul: la TCP, clientul primea 'Connection refused' — imediat. La UDP, clientul trimite și așteptă. Nimeni nu-l anunță. Asta e fire-and-forget."*

**Moment de fixare:** „TCP refuză. UDP tace."

### E5. Oprire captură + analiză rapidă

🟠 `Ctrl+C`.

Wireshark: File → Open → `udp_demo.pcap`. Filtru:
```
udp.port == 12345
```

> *▸ „Datagrame independente. Nu există handshake. Nu există 'stream'. Doar perechi request-response — dacă serverul răspunde."*

### E6. Template-uri UDP + livrabile (30 sec)

> *▸ „Template-urile UDP (`S02_Part08_Template_UDP_Server.py`, `S02_Part10_Template_UDP_Client.py`) — completați TODO, testați, produceți dovezi. Scenariul complet: `S02_Part11_Scenario_UDP_Server_Client_Wireshark.md`."*

| Fișier | Conținut |
|---|---|
| `udp_server_activity_output.txt` | Comenzi + min. 5 linii log + comentariu 3-5 propoziții |
| `udp_client_activity_output.txt` | Log-uri client + RTT + statistici (sent/received/loss) |
| `udp_traffic_capture.pcapng` | Captură UDP cu datagrame request-response |

---

## Bloc F (0:35–0:40) — Recap + livrabile + cleanup Docker + direcție S03

**Reluarea hook-ului:**

> *▸ „La început am pornit un client TCP fără server și am primit 'Connection refused'. Acum știm de ce: TCP impune un handshake — dacă nimeni nu ascultă, refuză. La UDP, clientul a trimis și a așteptat degeaba. Două filosofii de transport, două comportamente."*

**Trei idei fixate:**

1. TCP = stream de octeți. „Mesajul" e definit de aplicație (framing).
2. TCP creează conexiune (handshake + teardown). UDP trimite datagrame independente.
3. Portul serverului e fix (convenție). Portul clientului e efemer (alocat de OS).

**Cleanup Docker:**

```powershell
docker rm -f s02lab
```

> *▸ „Containerul se șterge — nu lasă reziduuri. Fișierele `.pcap` rămân pe disc, în folderul S02."*

**Direcție S03:**

> *▸ „La S03: server TCP multi-client, broadcast și multicast UDP. Ce ați fixat azi — socket, stream, datagramă — e fundația."*

**Fișiere de referință:**

| Fișier din kit | Rol |
|---|---|
| `S02_Part03_Scenario_TCP_Server_Netcat_Wireshark.md` | Pași compleți TCP: server → netcat → client → Wireshark → livrabile |
| `S02_Part06_Scenario_TCP_Client.py` (docstring) | Pași client TCP + RTT (atenție: conține nume vechi de fișiere) |
| `S02_Part11_Scenario_UDP_Server_Client_Wireshark.md` | Pași compleți UDP |

---

## Cheat-sheet

### Pornire laborator Docker

```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S02

docker rm -f s02lab 2>$null
docker run -d --name s02lab `
  -v "${PWD}:/work" -w /work `
  --cap-add=NET_RAW --cap-add=NET_ADMIN `
  compnet-s02lab:1.0 sleep infinity
```

### TCP demo

```powershell
# 🟠 CAPTURĂ
docker exec -it s02lab tcpdump -i lo -nn -w /work/tcp_demo.pcap "tcp port 12345"

# 🔵 SERVER
docker exec -it s02lab python S02_Part01_Example_TCP_Server.py

# 🟢 CLIENT
docker exec -it s02lab python S02_Part04_Example_TCP_Client.py
```

Wireshark display filter: `tcp.port == 12345`

### UDP demo

```powershell
# 🟠 CAPTURĂ
docker exec -it s02lab tcpdump -i lo -nn -w /work/udp_demo.pcap "udp port 12345"

# 🔵 SERVER
docker exec -it s02lab python S02_Part07_Example_UDP_Server.py 12345

# 🟢 CLIENT
docker exec s02lab python S02_Part09_Example_UDP_Client.py 127.0.0.1 12345 "Hello from client"
```

Wireshark display filter: `udp.port == 12345`

### Cleanup

```powershell
docker rm -f s02lab
```

---

## Plan de contingență

| # | Problemă | Diagnostic | Rezolvare |
|---|---|---|---|
| 1 | Docker Desktop nu pornește / nu are permisiuni | Docker service down sau WSL2 neactivat | Rulează demonstrația pe mașina instructorului (proiector). Studenții notează pașii; rezolvă instalarea acasă. |
| 2 | Imaginea `compnet-s02lab:1.0` nu e construită, internet lent | `docker build` nu a fost rulat sau a eșuat | Plan B: `docker run --rm -it python:3.12-slim bash` + `apt-get install -y tcpdump netcat-openbsd` (rapid, dar necesită internet). |
| 3 | Fișierele nu apar în container (`ls` gol) | Volum montat greșit (cale Windows incorectă) | Verifică: `docker exec s02lab ls /work`. Dacă gol: re-rulează `docker run` cu calea absolută corecte (nu relative). |
| 4 | Captura e goală (0 pachete) | `tcpdump` pornit după ce clientul a terminat | Ordine strictă: captură → server → client. Captură înainte de orice trafic. |
| 5 | Wireshark afișează zgomot | Filtru de display lipsă sau fișier greșit | Aplică `tcp.port == 12345` / `udp.port == 12345`. Confirmă fișierul deschis: `tcp_demo.pcap` vs `udp_demo.pcap`. |
| 6 | `Address already in use` la pornire server | Container anterior cu server activ | `docker rm -f s02lab` → re-creează containerul. |
| 7 | `tcpdump: lo: No such device` | Container fără interfață loopback | Adaugă `--network bridge` la `docker run` (implicit, dar verifică). Alternativ: captează pe `eth0` și ajustează filtrul. |

---

## Referințe

| Referință | DOI |
|---|---|
| Driver, R., Asoko, H., Leach, J., Mortimer, E., & Scott, P. (1994). Constructing scientific knowledge in the classroom. *Educational Researcher, 23*(7), 5–12. | https://doi.org/10.3102/0013189X023007005 |
| Hmelo-Silver, C. E. (2004). Problem-based learning: What and how do students learn? *Educational Psychology Review, 16*, 235–266. | https://doi.org/10.1023/B:EDPR.0000034022.16470.f3 |
| Matthews, J. N. (2005). Hands-on approach to teaching computer networking using packet traces. In *Proceedings of the 6th Conference on Information Technology Education* (pp. 361–367). ACM. | https://doi.org/10.1145/1095714.1095777 |
| Toll, W. E. (1995). Socket programming in the data communications laboratory. In *Proceedings of the 26th SIGCSE Technical Symposium on Computer Science Education* (pp. 39–43). ACM. | https://doi.org/10.1145/199688.199711 |
| Postel, J. (1981). Transmission Control Protocol (RFC 793). Internet Engineering Task Force. | https://doi.org/10.17487/RFC0793 |
| Postel, J. (1980). User Datagram Protocol (RFC 768). Internet Engineering Task Force. | https://doi.org/10.17487/RFC0768 |
| Merkel, D. (2014). Docker: Lightweight Linux containers for consistent development and deployment. *Linux Journal, 2014*(239). | https://doi.org/10.5555/2600239.2600241 |

---

## Note pedagogice

**Tipare socratice folosite:**

1. **POE — port efemer** (bloc C3): predicție „câte pachete?", observație (≥7), explicație (overhead TCP + port efemer).
2. **POE — pachete UDP** (bloc E3): predicție „câte pachete?", observație (2), explicație (zero overhead).
3. **„Ce s-ar fi întâmplat dacă…?"** (bloc E4): server UDP oprit → timeout → contrast cu TCP (Connection refused).

**Concepții greșite vizate:**

- #11 (secvență server ≠ client): bloc C3 — port efemer demonstrează că clientul nu face `bind`/`listen`.
- #12 (`recv()` parțial): bloc C5 — TCP=stream, `recv(1024)` nu e „primește un mesaj".
- #10 (bytes ≠ UTF-8): bloc D1 — `decode(errors='replace')` la procesarea datelor primite.

**Epifanii vizuale:**

1. **Bloc C4:** Wireshark cu 7+ pachete pentru un singur mesaj → overhead TCP.
2. **Bloc E4:** timeout UDP vs. Connection refused TCP → „TCP refuză, UDP tace."

**Diferență față de varianta MININET-SDN:** această variantă adaugă un bloc de setup Docker (B, 3 min) și folosește `tcpdump` + Wireshark pe Windows (nu `tshark` nativ). Captura e `.pcap` (tcpdump), nu `.pcapng` (tshark) — studentul convertește din Wireshark la Save As. Demonstrația cu netcat interactiv nu e disponibilă direct (din container, `nc` funcționează doar prin `docker exec -it`), deci testarea se face cu clientul Python.

# Seminar S02 — Socket programming TCP/UDP și analiză de trafic

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` · `04_SEMINARS/S02/` (11 fișiere: exemple, template-uri, scenarii) |
| **Infra** | MININET-SDN (Ubuntu 24.04 LTS, VirtualBox) · user `stud` / pass `stud` |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un socket e punctul unde codul tău întâlnește rețeaua; TCP (Transmission Control Protocol) livrează un stream de octeți — dacă vrei „mesaje", le definești tu. |

---

## Obiective operaționale

La finalul seminarului (și după lucrul individual pe template-uri), studenții pot:

1. **Porni** un server TCP concurent și un client TCP în Python și **explica** rolurile: serverul execută `bind → listen → accept`, clientul execută `connect`.
2. **Identifica** într-o captură Wireshark/tshark cele trei faze ale unei conversații TCP: handshake (SYN → SYN-ACK → ACK), payload și teardown (FIN/ACK sau RST).
3. **Argumenta** de ce portul clientului este efemer și de ce portul serverului este fix.
4. **Demonstra** că TCP livrează un stream de octeți, nu „mesaje" — folosind o captură cu două request-uri pe aceeași conexiune sau pe conexiuni separate.
5. **Compara** TCP cu UDP (User Datagram Protocol) la nivel de pachete: prezența/absența handshake-ului, noțiunea de stream vs. datagramă, comportament la server oprit.
6. **Produce** artefacte verificabile: fișiere `.txt` cu log-uri și comentarii + fișiere `.pcapng` cu capturi relevante.

---

## Structura seminarului

| Bloc | Temă | Durată | Tip |
|:---:|---|:---:|:---:|
| **A** | Hook + activare + conflict cognitiv | 3 min | Interactiv |
| **B** | TCP în practică: server + netcat + observații | 10 min | Demo + POE |
| **C** | TCP în pachete: captură + epifanie „stream" | 10 min | Demo + POE |
| **D** | Template-uri TCP: ghidare pentru temă | 7 min | Ghidare + hands-on |
| **E** | UDP: demo + captură + comparație TCP vs UDP | 7 min | Demo + „Ce dacă…?" |
| **F** | Recap + livrabile + direcție S03 | 3 min | Sinteză |
| | **Total** | **40 min** | |

**Variabilă de ajustare:** dacă timpul se comprimă, sacrifică micro-demo concurență (B3) și demonstrația opțională „client de 2 ori" din C. Sub nicio formă nu se sacrifică blocul C (epifanie stream) sau E (comparație UDP).

---

## Bloc A (0:00–0:03) — Hook, activare, conflict cognitiv

> *▸ „Pornesc un client TCP fără server. Ce se întâmplă?"*

**Ce faci:**

1. Asigură-te că **niciun server** nu ascultă pe portul 12345:
   ```bash
   ss -tlnp | grep 12345
   ```
   (output gol — bine)

2. Rulează clientul TCP exemplu:
   ```bash
   python3 S02_Part04_Example_TCP_Client.py
   ```

3. Pauză de 2 secunde. Lasă eroarea să apară:
   ```
   ConnectionRefusedError: [Errno 111] Connection refused
   ```

**Ce spui:**

> *▸ „La S01 am văzut rețeaua din exterior, cu netcat și Wireshark. Azi intrăm în mecanism: scriem noi procesul care vorbește pe rețea."*

> *▸ „Întrebarea de start: ce s-a întâmplat aici? Clientul a vrut să trimită, dar nimeni nu-l așteaptă. De ce 'Connection refused' și nu doar... tăcere? (Hint: e TCP, nu UDP. Rețineți asta — o reluăm la final.)"*

**Întrebare rapidă (2-3 mâini):** „Când un server 'ascultă', ce face fizic? Alocă memorie? Blochează un port? Trimite ceva?"

**De ce funcționează hook-ul:** e situat (eroare reală, pe ecran), afectiv (surpriza eșecului), tematic (diferența TCP vs UDP), concis (sub 1 minut de execuție) și returnabil (la recap reluăm: „acum știm de ce TCP refuză iar UDP nu").

---

## Bloc B (0:03–0:13) — TCP în practică: server + netcat + port efemer

### B1. Pornire server TCP exemplu

🔵 **SERVER:**
```bash
python3 S02_Part01_Example_TCP_Server.py
```

**Output așteptat:**
```
[INFO] TCP server listening on 127.0.0.1:12345
```

**Ce spui:**

> *▸ „Serverul ascultă pe `127.0.0.1:12345`. Adresa 127.0.0.1 e loopback — traficul nu iese din mașină. Ideal pentru laborator: eliminăm variabilele de rețea fizică."*

> *▸ „Modelul intern: `socketserver.ThreadingMixIn` — fiecare conexiune primește un thread separat. E concurență elementară, nu 'high-performance', dar e suficientă ca să nu blocheze alți clienți."*

### B2. Test cu netcat (predicție → observație → explicație)

**Predicție (5 sec):** „Trimit `salut tcp` prin netcat. Ce credeți că primesc înapoi?"

🟢 **CLIENT:**
```bash
echo "salut tcp" | nc 127.0.0.1 12345
```

**Observație (pe ecrane):**
- 🟢 CLIENT: răspuns `SALUT TCP`
- 🔵 SERVER: log `[SERVER] Received from ('127.0.0.1', 54xxx): salut tcp`

**Explicație (moment POE — port efemer, vizează concepția greșită #11):**

> *▸ „Observați portul clientului: 54-și-ceva-mii. Nu e 12345. De ce? Clientul nu face `bind` pe un port fix — OS-ul îi alocă un port efemer (de obicei între 49152 și 65535, cf. RFC 6335). Serverul e cel cu port fix, ca să poată fi găsit. Clientul e cel care inițiază."*

**Întrebare scurtă:** „Dacă rulez din nou comanda, portul clientului va fi la fel?" (Răspuns: nu — e alocat dinamic.)

### B3. Micro-demo concurență (opțional — sacrificabil)

🟢 **CLIENT** (terminal 1):
```bash
echo "client 1" | nc 127.0.0.1 12345
```
🟢 **CLIENT** (terminal 2, simultan):
```bash
echo "client 2" | nc 127.0.0.1 12345
```

🔵 **SERVER:** log-uri consecutive cu porturi efemere diferite.

> *▸ „Fiecare conexiune are handler-ul ei, pe un thread separat. Pe loopback, simultaneitatea e greu de vizualizat, dar arhitectura contează."*

---

## Bloc C (0:13–0:23) — TCP în pachete: handshake, payload, teardown + epifania „stream"

### C1. Pornire captură tshark

🟠 **CAPTURĂ:**
```bash
sudo tshark -i lo -f "tcp port 12345" -w /tmp/tcp_demo.pcapng
```

> *▸ „Capture filter (`-f`) selectează ce intră în fișier. Display filter e altceva — acela filtrează ce vezi pe ecran. Distincția contează: capture filter-ul reduce dimensiunea capturii, display filter-ul doar ascunde."*

### C2. Generare trafic: client TCP exemplu (predicție → observație)

**Predicție:** „Câte pachete credeți că generează o singură comandă client → server → răspuns → deconectare?"

🟢 **CLIENT:**
```bash
python3 S02_Part04_Example_TCP_Client.py
```

**Output client:**
```
[CLIENT] Sent: Hello, world
[CLIENT] Received: HELLO, WORLD
```

**Oprire captură:**
🟠 `Ctrl+C` în terminalul tshark.

### C3. Analiză captură — trei faze (predicție dezvăluită)

**Deschide captura** (opțional — poți folosi `tshark -r`):
```bash
tshark -r /tmp/tcp_demo.pcapng
```

**Ce arăți, pe rând:**

1. **Handshake (3 pachete):** SYN → SYN-ACK → ACK
   > *▸ „TCP nu trimite date fără să stabilească mai întâi o conexiune. Aceste 3 pachete creează stare comună: ambele părți știu porturi, numere de secvență, dimensiune de fereastră."*

2. **Payload:** segmentul cu `Hello, world` (client→server) și `HELLO, WORLD` (server→client)
   > *▸ „Datele voastre, vizibile în clar. Fără TLS, oricine captează traficul le poate citi."*

3. **Teardown:** FIN/ACK (sau RST)
   > *▸ „Închiderea e explicită. TCP nu 'dispare' — își ia la revedere."*

**Răspuns la predicție:** „Au fost cel puțin 7 pachete: 3 handshake + 2 payload + 2 teardown. Pentru un singur mesaj de câțiva bytes. Overhead-ul e prețul fiabilității."

### C4. Epifanie: TCP livrează un stream, nu „mesaje" (vizează misconception #12)

**Ce faci:** Rulezi clientul de două ori rapid:
```bash
python3 S02_Part04_Example_TCP_Client.py
python3 S02_Part04_Example_TCP_Client.py
```

**Ce spui:**

> *▸ „Două rulări, două conexiuni separate — în captură vedeți două handshake-uri cu porturi efemere diferite. TCP nu 'știe' ce e un mesaj. Apelul `recv(1024)` înseamnă 'dă-mi până la 1024 de bytes din stream'. Dacă trimiți 1000 de bytes, `recv(1024)` s-ar putea să returneze doar 500 — restul vine la al doilea apel."*

> *▸ „Dacă vreți 'mesaje', trebuie framing la nivel de aplicație: delimitatori (newline), prefixe de lungime, sau structuri fixe. HTTP face exact asta cu `Content-Length` și headere. Nu pentru că TCP ar cere, ci pentru că TCP nu garantează granularitatea."*

**Moment de fixare (o propoziție, va reveni la recap):** „TCP = stream de octeți. Mesajul e invenția aplicației."

---

## Bloc D (0:23–0:30) — Template-uri TCP: ghidare pentru temă

### D1. Template TCP server — ce completează

**Deschide:**
```bash
nano S02_Part02_Template_TCP_Server.py
```

**Arată cu cursorul** (pe proiector) zona `>>> STUDENT CODE STARTS HERE`:

> *▸ „Trei lucruri de implementat: (1) log complet — IP, port, mesaj, lungime în bytes; (2) construiți răspunsul `b"OK: " + mesaj.upper()`; (3) trimiteți cu `sendall()`."*

**Subliniază:**
- `self.client_address` → `(ip, port)` — tuplu, nu string
- `self.data` → bytes, trebuie decodat cu `.decode(errors='replace')` (misconception #10)
- `sendall()` vs `send()` — `sendall` garantează trimiterea integrală

> *▸ „Scenariul complet e descris pas cu pas în `S02_Part03_Scenario_TCP_Server_Netcat_Wireshark.md`. Citiți-l — conține secvența exactă de testare și ce fișiere încărcați."*

### D2. Cum testează (30 sec)

🔵 **SERVER:**
```bash
python3 S02_Part02_Template_TCP_Server.py
```

🟢 **CLIENT:**
```bash
nc 127.0.0.1 12345
```
Tastați: `salut`, Enter. Așteptați `OK: SALUT`.

> *▸ „Când testați, nu vă mulțumiți cu 'merge'. Vreți dovezi: log de server + captură. Și verificați portul efemer — e un indiciu bun la debug."*

### D3. Template TCP client — buclă + RTT

**Deschide:**
```bash
nano S02_Part05_Template_TCP_Client.py
```

**Arată zona TODO:**

> *▸ „Buclă `while True`, citire de la tastatură, trimitere, recepție, măsurare RTT (Round-Trip Time) cu `time.time()`. Ieșire la comanda `exit`."*

> *▸ „RTT-ul pe loopback va fi sub-milisecundă. Nu e relevant ca valoare absolută, dar procesul de măsurare contează: e același pe care-l folosiți când depanați latență pe rețea reală."*

> *▸ „Scenariul detaliat: `S02_Part06_Scenario_TCP_Client.py` (citiți docstring-ul). Atenție: scenariul referă niște nume de fișiere vechi — folosiți numele din folderul S02 pe care le vedeți cu `ls`."*

### D4. Livrabile TCP (explicit)

| Fișier | Conținut |
|---|---|
| `tcp_server_activity_output.txt` | Comenzi folosite + min. 5 linii log server + comentariu 3-5 propoziții |
| `tcp_client_activity_output.txt` | Log-uri client (mesaje, răspunsuri, RTT) + statistici |
| `tcp_traffic_capture.pcapng` | Captură cu handshake + payload + teardown vizibil |

---

## Bloc E (0:30–0:37) — UDP: demo + captură + comparație

### E1. Pornire server UDP exemplu

🔵 **SERVER:**
```bash
python3 S02_Part07_Example_UDP_Server.py 12345
```

**Output așteptat:**
```
[INFO] UDP server listening on 0.0.0.0:12345
```

> *▸ „Observați: portul e argument de linie de comandă, nu hardcodat ca la serverul TCP. Și ascultă pe `0.0.0.0` — toate interfețele, nu doar loopback."*

> *▸ „API-ul e diferit: `recvfrom`/`sendto` în loc de `recv`/`send`. Nu există `connect`/`accept` — UDP nu creează conexiune."*

### E2. Test cu client UDP Python

🟢 **CLIENT:**
```bash
python3 S02_Part09_Example_UDP_Client.py 127.0.0.1 12345 "hello udp"
```

**Output așteptat (client):**
```
[INFO] Sending 9 bytes to 127.0.0.1:12345 ...
[INFO] Received 9 bytes from ('127.0.0.1', 12345): b'HELLO UDP'
```

### E3. Captură UDP (tshark) — predicție

**Predicție:** „Câte pachete pentru un singur request-response UDP?"

🟠 **CAPTURĂ:**
```bash
sudo tshark -i lo -f "udp port 12345"
```

🟢 **CLIENT:** (repetă comanda de mai sus)

🟠 `Ctrl+C`.

**Răspuns:** „Două. Un datagram request, un datagram response. Zero handshake. Asta e diferența fundamentală."

### E4. „Ce s-ar fi întâmplat dacă…?" — server oprit, client trimite (vizează hook-ul)

🔵 **SERVER:** `Ctrl+C` (oprește serverul).

🟢 **CLIENT:**
```bash
python3 S02_Part09_Example_UDP_Client.py 127.0.0.1 12345 "ping"
```

**Output așteptat (după ~3 sec):**
```
[WARN] No response received (timeout).
```

> *▸ „Rețineți ce am văzut la hook: la TCP, clientul primea `Connection refused` — imediat, categoric. La UDP, clientul trimite și... așteptă. Nimeni nu-l anunță că n-a ajuns. Asta e fire-and-forget: dacă vreți fiabilitate pe UDP, o construiți voi, la nivel de aplicație."*

**Moment de fixare:** „TCP refuză. UDP tace."

### E5. Template-uri UDP + livrabile (30 sec)

> *▸ „Template-urile UDP (`S02_Part08_Template_UDP_Server.py`, `S02_Part10_Template_UDP_Client.py`) urmează aceeași logică: completați TODO, testați, produceți dovezi. Scenariul complet: `S02_Part11_Scenario_UDP_Server_Client_Wireshark.md`."*

| Fișier | Conținut |
|---|---|
| `udp_server_activity_output.txt` | Comenzi + min. 5 linii log + comentariu 3-5 propoziții |
| `udp_client_activity_output.txt` | Log-uri client + RTT + statistici (sent/received/loss) |
| `udp_traffic_capture.pcapng` | Captură UDP: datagrame request-response |

---

## Bloc F (0:37–0:40) — Recap + livrabile + direcție S03

**Reluarea hook-ului:**

> *▸ „La început am pornit un client TCP fără server și am primit 'Connection refused'. Acum știm de ce: TCP impune un handshake — dacă nimeni nu ascultă, refuză. La UDP, clientul a trimis și a așteptat degeaba. Două filosofii de transport, două comportamente diferite."*

**Trei idei fixate:**

1. TCP = stream de octeți. „Mesajul" e definit de aplicație (framing).
2. TCP creează conexiune (handshake + teardown). UDP trimite datagrame independente.
3. Portul serverului e fix (convenție). Portul clientului e efemer (alocat de OS).

**Direcție S03:**

> *▸ „La S03 trecem la server TCP multi-client (nu doar threaded, ci cu accept într-o buclă) și la UDP broadcast/multicast. Ce ați fixat azi — socket, stream, datagramă — e fundația."*

**Fișiere de referință:**

| Fișier din kit | Rol |
|---|---|
| `S02_Part03_Scenario_TCP_Server_Netcat_Wireshark.md` | Pași compleți TCP: server → netcat → client → Wireshark → livrabile |
| `S02_Part06_Scenario_TCP_Client.py` (docstring) | Pași client TCP + RTT (atenție: conține nume vechi de fișiere) |
| `S02_Part11_Scenario_UDP_Server_Client_Wireshark.md` | Pași compleți UDP: server → netcat → client → Wireshark → livrabile |

---

## Cheat-sheet

### TCP (port 12345)

```bash
# 🔵 SERVER
python3 S02_Part01_Example_TCP_Server.py

# 🟢 CLIENT (netcat)
echo "salut tcp" | nc 127.0.0.1 12345

# 🟢 CLIENT (Python exemplu)
python3 S02_Part04_Example_TCP_Client.py

# 🟠 CAPTURĂ
sudo tshark -i lo -f "tcp port 12345" -w /tmp/tcp_demo.pcapng

# Filtre Wireshark (display)
tcp.port == 12345
tcp.stream eq 0
```

### UDP (port 12345)

```bash
# 🔵 SERVER
python3 S02_Part07_Example_UDP_Server.py 12345

# 🟢 CLIENT (Python exemplu)
python3 S02_Part09_Example_UDP_Client.py 127.0.0.1 12345 "hello udp"

# 🟢 CLIENT (netcat, mai puțin fiabil)
echo "hello udp" | nc -u 127.0.0.1 12345

# 🟠 CAPTURĂ
sudo tshark -i lo -f "udp port 12345" -w /tmp/udp_demo.pcapng

# Filtru Wireshark (display)
udp.port == 12345
```

### Verificare port ocupat

```bash
ss -tlnp | grep 12345        # TCP
ss -ulnp | grep 12345        # UDP
sudo lsof -i :12345          # ambele protocoale
```

---

## Plan de contingență

| # | Problemă | Diagnostic | Rezolvare |
|---|---|---|---|
| 1 | `Address already in use` la pornire server | Proces anterior încă ocupă portul | `sudo lsof -i :12345` → `kill <PID>`. Sau: `ss -tlnp \| grep 12345`. |
| 2 | `tshark` nu captează nimic | Interfață greșită (nu `lo`) sau captură pornită după trafic | Verifică: `ip link show` — folosește `lo` pentru loopback. Repornește captură, apoi generează trafic. |
| 3 | `Permission denied` la tshark | Lipsă `sudo` | Rulează `sudo tshark …`. În laborator restricționat, capturează ca instructor și distribuie `.pcapng`. |
| 4 | `nc` nu răspunde / se comportă diferit | Variante netcat (OpenBSD vs. GNU) | Folosește clientul Python (Part04/Part09). E consistent. |
| 5 | Captură TCP arată RST în loc de FIN/ACK | Clientul sau serverul nu închide „civilizat" | Nu e eroare; explicația: „RST e o închidere abruptă, validă. FIN/ACK e închidere grace-ful. Ambele apar în practica reală." |
| 6 | `python3: command not found` | `compnet` venv nu e activat | `source ~/compnet/bin/activate` sau `which python3` pentru depanare. |
| 7 | Wireshark GUI nu pornește în VM | Lipsa X forwarding sau display | Folosește `tshark` (linie de comandă). Deschide `.pcapng` pe Windows (host) prin Shared Folder. |

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

---

## Note pedagogice

**Tipare socratice folosite:**

1. **POE — port efemer** (bloc B2): predicție „ce port are clientul?", observație (54xxx), explicație (port efemer, RFC 6335).
2. **POE — câte pachete?** (bloc C2): predicție „câte pachete pentru un mesaj?", observație (≥7), explicație (overhead TCP).
3. **„Ce s-ar fi întâmplat dacă…?"** (bloc E4): server UDP oprit → timeout → contrast cu TCP (Connection refused).

**Concepții greșite vizate:**

- #11 (secvență server ≠ client): bloc B2 — port efemer demonstrează că clientul nu face `bind`/`listen`.
- #12 (`recv()` parțial): bloc C4 — TCP=stream, recv(1024) nu e „primește un mesaj".
- #10 (bytes ≠ UTF-8): bloc D1 — `decode(errors='replace')` la procesarea datelor primite.

**Epifanii vizuale:**

1. **Bloc C3:** captura tshark cu 7+ pachete pentru un singur mesaj de câțiva bytes → overhead-ul TCP.
2. **Bloc E4:** timeout UDP vs. Connection refused TCP → „TCP refuză, UDP tace."

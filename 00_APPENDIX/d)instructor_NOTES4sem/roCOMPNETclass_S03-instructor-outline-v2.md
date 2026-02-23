# Seminar S03 — Concurență TCP multi-client + UDP broadcast / multicast / anycast

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (arhiva: `claudev11_EN_compnet-2025-redo-main.zip`) |
| **Infra** | MININET-SDN VM (Ubuntu 24.04 în VirtualBox) + `python3`, `nc`, `tshark`/Wireshark |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | „One-to-many" nu e un singur mecanism: serverul replică la nivel de aplicație (fan-out), broadcast-ul adresează toată rețeaua locală, multicast-ul adresează doar abonații, iar anycast-ul lasă rutarea să aleagă instanța. |

---

## Obiective operaționale

La finalul seminarului, studenții pot:

1. Rula și explica un server TCP (Transmission Control Protocol) multi-client cu câte un thread per conexiune și să identifice stream-urile distincte în tshark/Wireshark.
2. Completa un template de mini-chat în care serverul forward-ează mesajul unui client către toți ceilalți (fan-out la nivel de aplicație).
3. Captura traficul TCP și filtra pe `tcp.stream` pentru a demonstra că fan-out-ul generează segmente separate.
4. Rula exemplele UDP (User Datagram Protocol) broadcast și multicast și distinge în captură adresa destinație: `255.255.255.255` vs `224.0.0.1`.
5. Formula conceptual diferența unicast / broadcast / multicast / anycast pe baza adresei destinație și a mecanismului de replicare.

---

## Structura seminarului (35–40 min)

| Bloc | Conținut | Durată |
|:--:|---|---:|
| **A** | Hook: scenariu concret + predicție | 3 min |
| **B** | Demo: server TCP multi-client (exemplu) + 2–3 clienți `nc` | 10–12 min |
| **C** | Template mini-chat: completare TODO + test cu 3 clienți | 10–12 min |
| **D** | Captură TCP cu `tshark` + analiză `tcp.stream` în Wireshark | 6–7 min |
| **E** | UDP broadcast vs multicast: demo-uri + observare în captură | 7–8 min |
| **F** | Anycast (opțional) + temă + închidere cu revenire la hook | 2–3 min |

**Plan de sacrificare:** dacă la minutul 30 nu ai terminat Blocul D, treci direct la E doar cu broadcast (săriți multicast live — rămâne ca temă). Anycast (F) se menține doar conceptual, fără demo.

---

## Înainte de seminar (checklist de instructor)

1. Pornește VM-ul MININET-SDN, conectează-te prin SSH.
2. Verifică uneltele:
   ```bash
   python3 --version
   nc -h 2>/dev/null | head -n 1 || true
   tshark -v | head -n 2
   ```
3. Deschide **3 terminale** (ferestre sau tab-uri):
   - 🔵 Terminal 1 — **SERVER**
   - 🟢 Terminal 2 — **CLIENT / SENDER**
   - 🟠 Terminal 3 — **CAPTURĂ**
4. Intră în folderul seminarului:
   ```bash
   cd ~/compnet-2025-redo/04_SEMINARS/S03
   ```

---

## Bloc A (3 min) — Hook: „câte pachete pleacă?"

### Ce spui

> *▸ „La S02 am lucrat unicast: un client, un server, o conexiune. Azi complicăm: ce se întâmplă când 10 persoane sunt într-un chat? Când scriu un mesaj, rețeaua trimite un pachet sau zece?"*

(Lași 2–3 răspunsuri. Nu corectezi.)

> *▸ „Două predicții rapide: întâi — dacă 3 clienți TCP sunt conectați simultan și doi scriu în același timp, se amestecă mesajele pe server? Doi — se poate face 'send once, deliver to all' la nivel de TCP?"*

(Din nou, 2–3 răspunsuri.)

> *▸ „Bun. Verificăm cu cod și cu captură."*

### Ce faci

Doar verifici că ești în `04_SEMINARS/S03` și ai cele 3 terminale pregătite.

---

## Bloc B (10–12 min) — Demo: server TCP multi-client (exemplu)

### B1. Pornești serverul (🔵 Terminal 1)

```bash
python3 S03_Part01_Example_TCP_Multi_client_Server.py
```

Pe ecran apar:
```
[START] TCP multi-client server on 127.0.0.1:3333
[INFO] Server ready, listening on 127.0.0.1:3333
```

### Ce spui

> *▸ „Serverul ascultă pe 127.0.0.1:3333. Diferența față de serverul simplu din S02: fiecare client nou primește un socket separat și un thread dedicat. E o decizie de arhitectură, nu magie."*

### B2. Conectezi 2–3 clienți `nc` (🟢 Terminal 2 + alte terminale)

În fiecare terminal de client:

```bash
nc 127.0.0.1 3333
```

Testezi mesaje scurte:
- Client 1: `c1: salut`
- Client 2: `c2: test`
- Client 3: `c3: merge?`

### Ce arăți pe ecran

1. În 🔵 (server) apar:
   - `[CONNECT] New client from 127.0.0.1:<port_efemer>`
   - `[THREAD START] Client 127.0.0.1:<port_efemer> connected`
   - `[INFO] Currently connected clients: 2` (apoi 3)

2. Pe fiecare mesaj:
   - `[RECV] From 127.0.0.1:<port> -> b'c1: salut\n'`
   - `[SEND] To   127.0.0.1:<port> -> b'C1: salut\n'` (capitalize)

### Epifanie 1 — porturi efemere și 4-tuple

> *▸ „Uitați-vă la porturile de client: 54xxx, 55xxx… Nu le-am ales noi — sunt ephemeral ports, alocate de sistemul de operare. Asta e modul în care TCP distinge conexiunile: prin 4-tuple (IP sursă, port sursă, IP destinație, port destinație). În Wireshark, asta se traduce prin `tcp.stream` diferite, chiar dacă IP-ul e același."*

### Predicție — fără threaduri (POE)

> *▸ „Dacă aș scoate thread-urile și aș trata fiecare client secvențial, ce pățește al doilea client când primul nu trimite nimic? … Exact: blochează. Concurența nu e gratuită — e un compromis de design."*

---

## Bloc C (10–12 min) — Template mini-chat: fan-out la nivel de aplicație

### C1. Oprești serverul exemplu

În 🔵: `Ctrl+C`.

### C2. Completezi TODO (rapid, „paste controlat")

```bash
nano S03_Part02_Template_TCP_Multi_client_Server.py
```

Cauți zona delimitată:
```python
# >>> STUDENT CODE STARTS HERE
...
# <<< STUDENT CODE ENDS HERE
```

Inserezi codul de mai jos:

```python
text = data.decode('utf-8', errors='ignore')
print(f"[RECV] From {ip}:{port} -> {text!r}")

msg = f"[{ip}:{port}] {text}".encode('utf-8', errors='ignore')

with clients_lock:
    for other in clients:
        if other is client_socket:
            continue
        other_ip, other_port = other.getpeername()
        try:
            other.sendall(msg)
            print(f"[FWD] To {other_ip}:{other_port} -> {msg!r}")
        except BaseException as err:
            print(f"[WARN] Forward to {other_ip}:{other_port} failed: {err}")
```

Salvezi (`Ctrl+O`, Enter, `Ctrl+X`).

### Ce spui în timp ce editezi

> *▸ „Acum facem un mini-chat: serverul primeșete mesajul de la un client și îl forward-ează separat către fiecare alt client. Două detalii de reținut: lista `clients` e stare partajată între threaduri, de aceea folosim `clients_lock` — altfel riscăm corupere dacă cineva se deconectează fix când iterăm."*

### C3. Rulezi serverul chat (🔵)

```bash
python3 S03_Part02_Template_TCP_Multi_client_Server.py
```

### C4. Test cu 3 clienți `nc` — mesaj încrucișat

1. Pornești 3 instanțe `nc` (🟢 + alte terminale):
   ```bash
   nc 127.0.0.1 3333
   ```
2. Client 1 scrie: `Salut, eu sunt C1`
3. Arăți că în clientul 2 și 3 apare: `[127.0.0.1:<port>] Salut, eu sunt C1`

### Epifanie 2 — fan-out ≠ multicast de rețea (capcana de concepție greșită)

> *▸ „Atenție: asta seamănă cu multicast, dar nu e multicast. E replicare la nivel de aplicație — serverul trimite separat către fiecare client. În captură veți vedea câte un segment TCP pentru fiecare destinatar, nu un singur pachet magic care ajunge la toți. E diferența pe care o demonstrăm imediat."*

---

## Bloc D (6–7 min) — Captură TCP și analiză `tcp.stream`

### D1. Pornești captura (🟠 Terminal 3)

```bash
sudo tshark -i any -f "tcp port 3333" -w tcp_multiclient_chat_capture.pcapng
```

### Ce spui

> *▸ „Filtrul de captură (`-f`) limitează ce înregistrăm — doar port 3333. În Wireshark vom aplica apoi display filters, care filtrează ce vedem din ce am înregistrat deja."*

### D2. Generezi trafic (1–2 min)

Cu serverul chat și 3 clienți porniți, trimiți 4–6 mesaje scurte din clienți diferiți.

### D3. Oprești captura

În 🟠: `Ctrl+C`.

### D4. Deschizi captura în Wireshark

**Opțiunea 1 (rapid, dacă ai Wireshark în VM):** deschizi direct `tcp_multiclient_chat_capture.pcapng`.

**Opțiunea 2 (de obicei preferată):** copiezi pe Windows:
```powershell
scp -P 2222 stud@127.0.0.1:~/compnet-2025-redo/04_SEMINARS/S03/tcp_multiclient_chat_capture.pcapng .
```

### D5. Predicție + analiză (POE pe captură)

Înainte de a filtra, întrebi:

> *▸ „Predicție: dacă am avut 3 clienți conectați și unul a scris un mesaj, câte pachete TCP vedem pentru acel mesaj — ignorând ACK-urile?"*

(Răspuns așteptat: 3 — unul de la client la server, plus câte unul de la server la fiecare din ceilalți 2 clienți.)

Apoi arăți:

1. Display filter: `tcp.port == 3333`
2. Click pe un pachet → câmpul `tcp.stream`
3. Filtrezi: `tcp.stream eq 0`, apoi `eq 1`, `eq 2`

### Epifanie 3 — vizualizarea fan-out-ului

> *▸ „Fiecare client are propriul stream. Când clientul 1 scrie, serverul primește pe stream 0 și trimite pe stream 1 și stream 2 — separat. Asta e fan-out-ul vizibil în rețea. Dacă ar fi fost multicast, am fi văzut un singur pachet cu destinația 224.x.x.x."*

---

## Bloc E (7–8 min) — UDP broadcast vs multicast

### Tranziție

> *▸ „Am văzut cum arată one-to-many construit de aplicație. Acum vedem cum arată one-to-many construit de rețea: broadcast și multicast. Diferența se vede în adresa destinație."*

### E1. UDP broadcast (3–4 min)

**🔵 Receiver (Terminal 1):**
```bash
python3 4_udp-broadcast/S03_Part04B_Example_UDP_Broad_Receiver.py
```

**🟠 Captură (Terminal 3):**
```bash
sudo tshark -i any -f "udp port 5007" -w udp_broadcast_capture.pcapng
```

**🟢 Sender (Terminal 2):**
```bash
python3 4_udp-broadcast/S03_Part04A_Example_UDP_Broad_Sender.py "Hello, broadcast"
```

Lași 2–3 mesaje (sender-ul trimite automat la fiecare secundă cu contor: `Hello, broadcast #0`, `#1`…), apoi `Ctrl+C` în sender, apoi în captură.

**Predicție înainte de Wireshark:**

> *▸ „Ce adresă destinație credeți că vedem în captură?"*

(Răspuns: `255.255.255.255`)

Deschizi captura:
- `udp.port == 5007`
- `ip.dst == 255.255.255.255 && udp.port == 5007`

> *▸ „Broadcast = toată lumea din segmentul local de rețea. Adresa 255.255.255.255 e adresa de broadcast limitată — nu trece de router."*

### E2. UDP multicast (3–4 min)

Oprești receiver-ul broadcast (`Ctrl+C` în 🔵).

**🔵 Receiver (Terminal 1):**
```bash
python3 5_udp-multicast/S03_Part05B_Example_UDP_Multicast_Receiver.py
```

**🟠 Captură (Terminal 3):**
```bash
sudo tshark -i any -f "udp port 5001" -w udp_multicast_capture.pcapng
```

**🟢 Sender (Terminal 2):**
```bash
python3 5_udp-multicast/S03_Part05A_Example_UDP_Multicast_Sender.py "Hello, multicast"
```

Oprești captura după 1–2 mesaje.

**Contrast direct (diagramă progresivă — mental):**

> *▸ „Acum filtrăm: `ip.dst == 224.0.0.1 && udp.port == 5001`. Diferența față de broadcast: adresa destinație e un grup multicast (clasă D, 224.x.x.x). Primește doar cine s-a abonat cu `IP_ADD_MEMBERSHIP`. Broadcast trimite la toți indiferent; multicast trimite doar la abonați."*

### Mini-sinteză tabelară (spusă verbal sau scrisă rapid pe tablă)

| Mecanism | Cine primește | Adresa destinație | Cine replică |
|---|---|---|---|
| Fan-out aplicație (mini-chat) | Doar clienții serverului | Unicast (IP-ul fiecărui client) | Serverul (aplicația) |
| Broadcast | Toți din segmentul local | `255.255.255.255` | Rețeaua (layer 2) |
| Multicast | Doar abonații grupului | `224.x.x.x` | Rețeaua + switch/router |

---

## Bloc F (2–3 min) — Anycast (opțional) + temă + închidere

### Anycast: idee, nu demonstrație completă

> *▸ „Anycast nu e un alt protocol de transport. E un mod de adresare: aceeași adresă IP e anunțată de mai multe servere în locații diferite. Routerul decide care instanță e 'cea mai apropiată'. Din perspectiva clientului, e unicast — trimite la o singură adresă. Din perspectiva rețelei, e o decizie de rutare."*

**Dacă ai 2 min în plus** — rulezi rapid exemplul (port `5007`, deci oprește orice receiver broadcast):

🔵 Terminal 1:
```bash
python3 6_udp-anycast/S03_Part06A_Example_UDP_Anycast_Server.py
```

🟢 Terminal 2:
```bash
python3 6_udp-anycast/S03_Part06B_Example_UDP_Anycast_Client.py
```

> *▸ „Nu demonstrăm selecția 'nearest server' — nu avem rutare reală. Demonstrăm doar că pentru client e o singură adresă destinație, iar serverul poate fi 'etichetat' cu server_id."*

### Temă — livrabile (conform scenariilor din kit)

1. **TCP mini-chat** (scenariul din `S03_Part03_Scenario_TCP_Multi_client_Server.md`):
   - completează template-ul;
   - livrează: `tcp_multiclient_server_output.txt` (comanda de pornire + log-uri de la min. 5 mesaje + explicație 5–7 propoziții) + `tcp_multiclient_chat_capture.pcapng`.

2. **UDP broadcast** (scenariul din `4_udp-broadcast/S03_Part04D_Scenario_UDP_Broad.py`):
   - completează template-ul cu contor + filtrare pe prefix;
   - testează și cu `nc`: `echo "Hello manual" | nc -u 255.255.255.255 5007`;
   - livrează: `udp_broadcast_activity_output.txt` (log-uri cu `[OK]` și `[SKIP]` + comentariu 3–5 propoziții) + `udp_broadcast_capture.pcapng`.

3. **UDP multicast** (scenariul din `5_udp-multicast/S03_Part05D_Scenario_UDP_Multicast.md`):
   - completează template-ul cu timestamp + contor;
   - livrează: `udp_multicast_activity_output.txt` (log-uri + comparație broadcast vs multicast în 5–7 propoziții) + `udp_multicast_capture.pcapng`.

4. **(Opțional) UDP anycast** (scenariul din `6_udp-anycast/S03_Part06D_Scenario_UDP_Anycast.md`):
   - adaugă `server_id` în template;
   - livrează: `udp_anycast_activity_output.txt` (+ captură, dacă e posibilă).

### Închidere — revenire la hook

> *▸ „Revenim la întrebarea de la început: câte pachete pleacă? Depinde de cine face replicarea. Dacă o face aplicația (mini-chat-ul nostru) — câte un pachet per destinatar. Dacă o face rețeaua (broadcast/multicast) — un singur pachet, distribuit de infrastructură. Asta e diferența de reținut. La S04 vom trece de la 'cum trimiți' la 'ce trimiți': protocoale text și binare peste TCP și UDP."*

---

## Cheat-sheet

### Comenzi folosite în seminar

| Acțiune | Comandă |
|---|---|
| Pornire server TCP multi-client | `python3 S03_Part01_Example_TCP_Multi_client_Server.py` |
| Conectare client TCP (nc) | `nc 127.0.0.1 3333` |
| Pornire server chat (template) | `python3 S03_Part02_Template_TCP_Multi_client_Server.py` |
| Captură TCP tshark | `sudo tshark -i any -f "tcp port 3333" -w tcp_multiclient_chat_capture.pcapng` |
| Pornire receiver broadcast | `python3 4_udp-broadcast/S03_Part04B_Example_UDP_Broad_Receiver.py` |
| Pornire sender broadcast | `python3 4_udp-broadcast/S03_Part04A_Example_UDP_Broad_Sender.py "Hello, broadcast"` |
| Captură UDP broadcast | `sudo tshark -i any -f "udp port 5007" -w udp_broadcast_capture.pcapng` |
| Pornire receiver multicast | `python3 5_udp-multicast/S03_Part05B_Example_UDP_Multicast_Receiver.py` |
| Pornire sender multicast | `python3 5_udp-multicast/S03_Part05A_Example_UDP_Multicast_Sender.py "Hello, multicast"` |
| Captură UDP multicast | `sudo tshark -i any -f "udp port 5001" -w udp_multicast_capture.pcapng` |
| Verificare port ocupat | `ss -tulnp \| grep -E ":3333\|:5001\|:5007"` |

### Display filters Wireshark

| Ce vrei să vezi | Filtru |
|---|---|
| Tot traficul TCP pe portul 3333 | `tcp.port == 3333` |
| Un singur stream TCP | `tcp.stream eq 0` |
| Broadcast UDP pe 5007 | `ip.dst == 255.255.255.255 && udp.port == 5007` |
| Multicast UDP pe 5001 | `ip.dst == 224.0.0.1 && udp.port == 5001` |

### Porturi din seminar

| Port | Protocol | Folosit de |
|---|---|---|
| 3333 | TCP | Server multi-client + mini-chat |
| 5007 | UDP IPv4 | Broadcast sender/receiver |
| 5007 | UDP IPv6 | Anycast server/client |
| 5001 | UDP | Multicast sender/receiver |

---

## Plan de contingență

| Problemă | Simptom | Rezolvare |
|---|---|---|
| „Address already in use" la pornirea serverului | `OSError: [Errno 98] Address already in use` | Verifică: `ss -tulnp \| grep :3333`. Oprește procesul existent sau așteaptă ~60 s (TIME_WAIT). |
| `tshark`: permisiuni insuficiente | `You don't have permission to capture on that device` | Folosește `sudo tshark ...`. Nu reconfigura dumpcap în timpul seminarului. |
| Nu vezi broadcast/multicast în captură | Fișierul pcapng e gol sau lipsesc pachete | Nu captura pe `lo` separat; folosește `-i any`. Verifică portul din capture filter. |
| Mesajele par „lipite" sau trunchiate în `nc` | Clientul vede `[127.0.0.1:55432] Salut,[127.0.0.1:55433] Test` | Normal: TCP e stream, nu are delimitatori. Log-urile serverului sunt sursa de adevăr. Menționează misconception #12 (recv partial). |
| Anycast server nu pornește (IPv6 dezactivat) | `OSError: [Errno 97] Address family not supported` | Verifică: `cat /proc/sys/net/ipv6/conf/all/disable_ipv6`. Dacă e `1`, renunță la demo-ul live, rămâi la teorie. |
| Clientul `nc` nu se conectează | `Connection refused` | Serverul nu e pornit sau portul e greșit. Verifică cu `ss -tlnp \| grep 3333`. |
| Wireshark nu e disponibil în VM | — | Captura cu `tshark`, copiază `.pcapng` pe Windows cu `scp` și deschide acolo. |
| Timpul depășește 35 min la finalul Blocului D | Nu ai ajuns la UDP | Sacrifică: fă doar broadcast (E1), menționează multicast verbal, totul altceva rămâne temă. |

---

## Referințe

Ballani, H., & Francis, P. (2005). Towards a global IP anycast service. In *Proceedings of the 2005 ACM SIGCOMM Conference* (pp. 301–312). ACM. https://doi.org/10.1145/1080091.1080127

Deering, S. E., & Cheriton, D. R. (1990). Multicast routing in datagram internetworks and extended LANs. *ACM Transactions on Computer Systems, 8*(2), 85–110. https://doi.org/10.1145/78952.78953

Deering, S. (1989). *Host extensions for IP multicasting* (RFC 1112). RFC Editor. https://doi.org/10.17487/RFC1112

Mogul, J. C. (1984). *Broadcasting Internet datagrams* (RFC 919). RFC Editor. https://doi.org/10.17487/RFC0919

Pariag, D., Brecht, T., Harji, A. S., Buhr, P. A., Shukla, A., & Cheriton, D. R. (2007). Comparing the performance of web server architectures. In *EuroSys 2007* (pp. 231–243). ACM. https://doi.org/10.1145/1272996.1273021

Postel, J. (1980). *User Datagram Protocol* (RFC 768). RFC Editor. https://doi.org/10.17487/RFC0768

Postel, J. (1981). *Transmission Control Protocol* (RFC 793). RFC Editor. https://doi.org/10.17487/RFC0793

Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley. (Cap. 12: Broadcasting and Multicasting; Cap. 18: TCP Connection Establishment and Termination.)

---

## Note pedagogice

**Arc cognitiv vizat:** hook (predicție: câte pachete?) → conflict (intuiția „un pachet" e greșită pentru fan-out) → explorare ghidată (demo TCP → captură → demo UDP) → formalizare (tabelul din E, comparație) → aplicare (template-uri) → recap (revenire la hook).

**Concepție greșită principală:** „serverul de chat trimite un singur pachet tuturor" — demontată vizual în Bloc D prin filtrarea pe `tcp.stream`.

**Tipare socratice folosite:**
- POE în Bloc A (predicție mesaje concurente), Bloc B (fără threaduri), Bloc D (câte pachete pentru un mesaj?), Bloc E (adresa destinație broadcast).
- Capcana de concepție greșită în Bloc C (fan-out ≠ multicast).
- Diagramă progresivă (mentală) în E: tabel comparativ construit incremental.

**Dacă grupul e rapid (termini Bloc D la minutul 25):** rulează și demo-ul anycast complet + discuție despre CDN-uri (exemplu real: DNS anycast la Cloudflare).

**Dacă grupul e lent (la minutul 30 nu ai terminat D):** sacrifică multicast live și anycast. Fă doar broadcast rapid și treci la recap.

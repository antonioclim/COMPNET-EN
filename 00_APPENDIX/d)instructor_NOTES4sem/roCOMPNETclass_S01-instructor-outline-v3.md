# Seminar S01 — Analiză de rețea

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (versiune `claudev11_EN`) |
| **Infra** | MININET-SDN (Ubuntu 24.04, VirtualBox) |
| **Durată țintă** | 35–40 min (conținut tehnic; restul ședinței → prezentare semestru, fișă, evaluare) |
| **Ideea-cheie** | Diagnosticul de rețea se construiește în straturi: nume → IP → conectivitate → porturi → trafic → pachete; diferența TCP / UDP se *vede* în comportament și se *confirmă* în captură. |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. **Diagnostica** conectivitatea, rezolvarea DNS și starea porturilor folosind `ping`, `nslookup` și `netstat`/`ss`.
2. **Genera** trafic TCP și UDP controlat cu `netcat` și **descrie** diferența de comportament (conexiune persistentă vs. datagrame independente).
3. **Captura** pachete pe interfața loopback cu `tshark` (sau Wireshark) și **identifica** three-way handshake-ul TCP și absența acestuia la UDP.
4. **Distinge** între capture filter (BPF, înainte de captură) și display filter (după captură) în Wireshark/tshark.
5. **Explica** de ce UDP nu semnalează eroare la trimiterea către un port fără receptor.
6. **Produce** dovezile de lucru cerute de fișierele de task (`S01_Part02`, `S01_Part04`, `S01_Part06`).

---

## Structura seminarului

| Bloc | Ce faci | Durată |
|:----:|---------|-------:|
| **A0** | Prezentare generală: semestru, fișă, reguli, evaluare, mediu de lucru | 30–40 min |
| **A** | Hook + activare + conflict cognitiv | 3 min |
| **B** | Diagnostic de bază: `ping`, `nslookup`, `netstat`/`ss` | 8 min |
| **C** | Netcat TCP și UDP — comportament observabil | 12 min |
| **D** | Captură: tshark/Wireshark pe trafic netcat (TCP + UDP) | 12 min |
| **E** | Recapitulare, hook reluat, temă, preview S02 | 5 min |
| | **Total conținut tehnic** | **40 min** |

> *▸ Dacă timpul se comprimă: Blocul D (captură) se sacrifică primul — se recuperează la debutul S02, unde Wireshark e oricum necesar. Blocurile A–C sunt non-negociabile.*

---

## Bloc A0 — Prezentarea generală (administrativ, NU din buget tehnic)

**1. Cine ești tu** — scurtă prezentare, date de contact, canal de comunicare (Teams / e-mail / Moodle).

**2. Fișa disciplinei** — obiective, competențe, bibliografie, pondere examen vs. seminar.

**3. Regulile jocului** — prezență, plagiat, cum se evaluează activitatea de seminar, condiții de promovabilitate.

**4. Calendarul semestrului** — cele 14 seminarii cu temele aferente (poți proiecta `current-outline.md` din kit).

**5. Mediul de lucru: MININET-SDN** — explici *ce este* și *de ce*:

- Mașină virtuală Ubuntu 24.04, pre-configurată, rulează sub Oracle VirtualBox.
- Conține tot ce le va trebui pe semestru: Docker Engine + Compose v2, Mininet 2.3, Open vSwitch 3.3, Python 3.12 cu venv `compnet`, tshark, Scapy, nmap, Paramiko, Flask etc.
- Se descarcă ca fișier `.ova` (~2–3 GB) și se importă în VirtualBox (File → Import Appliance).
- Credențiale: `stud` / `stud`.
- Conexiunea la VM se face prin SSH (PuTTY sau `ssh -p 2222 stud@127.0.0.1`) — consola VirtualBox e doar de avarie.
- Arată schema de arhitectură din ghidul de setup (`SETUP-GUIDE-COMPNET-EN.md`): Windows host ↔ VirtualBox NAT ↔ VM cu Docker, Mininet, Python.

**6. Indică ghidul de instalare** — studenții trebuie să vină cu VM-ul funcțional la S02.

> *▸ Dacă sala are stații cu VM-ul pre-instalat, pornește una și fă live `ssh -p 2222 stud@127.0.0.1`. Dacă nu — arată de pe laptopul tău. Studenții trebuie să vadă prompt-ul `(compnet) stud@mininet-vm:~$` și să înțeleagă că acolo se lucrează tot semestrul.*

---

## Bloc A — Hook + activare + conflict cognitiv (~3 min)

### Deschidere (scenariu situat, 60 sec)

> *▸ „Imaginați-vă: colegul vă scrie la 3 noaptea — 'site-ul nu merge'. Tastați `ping site-ul.ro` și primiți răspuns. Dar browserul dă eroare. E pică rețeaua, sau e altceva? Până la finalul orei de azi, o să aveți un arbore de diagnostic care vă răspunde în 30 de secunde."*

### Activare (30 sec)

> *▸ „Câți din voi au folosit vreodată `ping`? Dar `netcat`? Dar Wireshark? — Nu contează dacă nu. Azi construim de la zero."*

### Conflict cognitiv — 3 predicții rapide (90 sec)

Cere 2–3 răspunsuri din sală la fiecare, notează pe tablă/slide:

1. „Dacă `ping google.com` eșuează, înseamnă sigur că nu am internet?"
2. „TCP și UDP — diferența e doar 'rapid vs. lent', sau e ceva structural?"
3. „Câte pachete credeți că apar la *începutul* unei conexiuni TCP, înainte de orice mesaj?"

> *▸ Nu corectezi acum. Păstrezi răspunsurile pentru confruntare pe parcurs.*

---

## Bloc B — Diagnostic de bază: `ping`, `nslookup`, `netstat` (~8 min)

**Fișier kit:** `04_SEMINARS/S01/S01_Part01_Scenario_Basic_Tools.md`
**Unde rulezi:** în VM, prin SSH (PuTTY sau terminal pe `127.0.0.1:2222`)
**Obiective vizate:** 1

### Narativ de legătură

> *▸ „Trei comenzi vă rezolvă 80% din problemele de debugging: `nslookup` (funcționează DNS-ul?), `ping` (funcționează drumul?) și `netstat` (cine ascultă pe ce port?). Ordinea contează: dacă DNS-ul e stricat, nici `ping pe nume` nu merge — dar IP-ul poate funcționa."*

### B1. `nslookup` — rezolvarea DNS (2 min)

```bash
nslookup google.com
```

Arată: serverul DNS utilizat, adresa IP rezolvată.

**🎯 Predicție (POE):** „Ce se întâmplă dacă întreb un domeniu care nu există?"

```bash
nslookup domeniu-inexistent-xyz123.com
```

Arată eroarea `server can't find` — **NXDOMAIN**.

> *▸ „DNS eșuează diferit de conectivitate. O eroare de rezolvare nu înseamnă că rețeaua e căzută."*

### B2. `ping` — conectivitate (2 min)

```bash
ping -c 4 google.com
```

Arată: rezolvarea DNS (IP-ul apare în output), RTT (round-trip time), packet loss.

`ping` trimite pachete ICMP Echo Request și așteaptă Echo Reply. Dacă merge, conexiunea funcționează end-to-end.

**🎯 Confruntare cu predicția 1:** „Deci dacă `ping google.com` eșuează — poate fi DNS stricat, poate fi rută, poate fi ICMP filtrat. Nu e o concluzie unică."

Opțional: `ping -c 2 10.0.2.2` (gateway-ul NAT din VirtualBox) — ping pe IP, fără DNS.

### B3. `netstat`/`ss` — porturi și conexiuni (3 min)

```bash
netstat -tulnp
```

Explică flag-urile: `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric (fără DNS invers), `-p` procesul proprietar.

Arată output-ul: un port în LISTEN (ex. sshd pe :22), eventual ESTABLISHED (sesiunea SSH curentă).

> *▸ Alternativă modernă: `ss -tulnp` — aceleași flag-uri, disponibil pe distribuțiile recente. Vom folosi `netstat` și `ss` alternativ pe tot semestrul.*

### Ce NU faci aici

Nu dai exercițiul individual (`S01_Part02_Tasks_Basic_Tools.md`) — rămâne ca temă. Nu intri în detalii despre protocolul ICMP, DNS intern sau ARP — vin la cursurile C05–C06.

---

## Bloc C — Netcat TCP și UDP (~12 min)

**Fișier kit:** `04_SEMINARS/S01/S01_Part03_Scenario_Netcat_Basics.md`
**Obiective vizate:** 2, 5

### Narativ de tranziție

> *▸ „Trecem de la diagnostic la trafic real. `netcat` — prescurtat `nc` — poate fi server, client, poate trimite și primi pe TCP sau UDP. Îl folosim ca să vedem diferența între cele două protocoale de transport, fără o linie de cod."*

### Pregătire

Deschide **două sesiuni SSH** către VM (două ferestre PuTTY sau două tab-uri). Pune-le **side-by-side pe proiector**. Studenții trebuie să vadă simultan ce se întâmplă în fiecare.

---

### 🔵 PAS 1 — Server TCP (port 9000)

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `$ nc -l -p 9000` | *(așteaptă)* |
| *(cursor blocat — serverul ascultă)* | |

> *▸ „`-l` = listen, `-p 9000` = portul. Comanda se blochează. Serverul așteaptă o conexiune."*

### 🟢 PAS 2 — Client TCP

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| *(blocat, dar conexiunea e stabilită)* | `$ nc 127.0.0.1 9000` |
| | *(conectat)* |

> *▸ „Clientul s-a conectat la loopback pe portul 9000. Conexiunea TCP există acum."*

### PAS 3 — Schimb bidirecțional

Client tastează `salut` → apare în SERVER. Server tastează `răspuns` → apare în CLIENT.

> *▸ „Conexiunea e BIDIRECȚIONALĂ și PERSISTENTĂ. Orice scrii într-o parte apare instantaneu în cealaltă."*

### PAS 4 — Închidere TCP

| 🔵 TERMINAL SERVER | 🟢 TERMINAL CLIENT |
|:----|:----|
| **Ctrl+C** → se oprește | *(se deconectează automat)* |

> *▸ „TCP are o procedură de terminare — FIN/ACK. Când o parte închide, cealaltă află imediat."*

---

### 🔵 PAS 5 — Server UDP (port 9001)

| 🔵 TERMINAL SERVER | 🟢 TERMINAL CLIENT |
|:----|:----|
| `$ nc -u -l -p 9001` | *(așteaptă)* |
| *(așteaptă datagrame)* | |

> *▸ „Flag-ul `-u` = UDP. Serverul ascultă datagrame, NU conexiuni. Niciun handshake."*

### PAS 6 — Trimitere datagramă UDP

| 🔵 TERMINAL SERVER | 🟢 TERMINAL CLIENT |
|:----|:----|
| `test UDP` ← *apare* | `$ echo "test UDP" \| nc -u 127.0.0.1 9001` |

> *▸ „Nu există conexiune persistentă. Fiecare mesaj e o datagramă independentă."*

### PAS 7 — Epifanie: UDP „trimis în gol" ⚡

**🎯 Predicție (POE):** „Ce se întâmplă dacă trimit un mesaj UDP și nimeni nu ascultă? Primesc eroare?"

1. Oprește serverul: **Ctrl+C** în SERVER.
2. Trimite din CLIENT:

| 🔵 TERMINAL SERVER | 🟢 TERMINAL CLIENT |
|:----|:----|
| *(oprit — nimeni nu ascultă)* | `$ echo "mesaj pierdut" \| nc -u 127.0.0.1 9001` |
| | *(nicio eroare!)* |

> *▸ „Clientul NU primește eroare. Mesajul s-a pierdut în tăcere. Asta e UDP — fire and forget. Aplicațiile care folosesc UDP trebuie să-și construiască singure mecanismele de confirmare."*

**🎯 Confruntare cu predicția 2:** „TCP și UDP nu diferă doar în viteză — diferă structural: TCP are stare (conexiune, confirmări, ordine); UDP nu are nimic din astea."

### Mini-recap verbal (20 sec)

> *▸ „TCP = conexiune stabilă, bidirecțională, cu garanții. UDP = datagrame independente, rapid, fără garanții. TCP pentru web, SSH, e-mail; UDP pentru DNS, streaming, jocuri."*

---

## Bloc D — Captură: tshark/Wireshark pe trafic netcat (~12 min)

**Fișier kit:** `04_SEMINARS/S01/S01_Part05_Scenario_Wireshark_Netcat.md`
**Obiective vizate:** 3, 4

### Pregătire logistică — acum ai 3 terminale

Pe lângă cele două sesiuni SSH de la Bloc C (SERVER și CLIENT), deschide un **al treilea terminal SSH** dedicat capturii. Alternativ, Wireshark pe Windows.

> *▸ Dacă configurația NAT face capturile dificile în Wireshark pe host, fă toată demonstrația cu `tshark` din VM. Pedagogic e identic; doar interfața e text în loc de grafic.*

### Narativ de tranziție

> *▸ „Până acum am trimis și am primit date — dar nu am văzut ce se întâmplă pe fir. Acum capturăm fiecare pachet și-l descompunem strat cu strat."*

---

### Scenariul TCP

#### 🟠 PAS 1 — Pornește captura (capture filter = BPF)

| 🟠 TERMINAL CAPTURĂ (SSH #3) |
|:----|
| `$ sudo tshark -i lo -f "tcp port 9200"` |
| *(sau Wireshark pe host: Capture Filter → `tcp port 9200` → Start)* |

> *▸ „Asta e un capture filter — filtrare la nivel libpcap/BPF, înainte de captură. Doar traficul care se potrivește se înregistrează."*

#### 🔵🟢 PAS 2 — Server + client + mesaje

| 🔵 TERMINAL SERVER | 🟢 TERMINAL CLIENT |
|:----|:----|
| `$ nc -l -p 9200` | `$ nc 127.0.0.1 9200` |

Client trimite 3 mesaje scurte (câte unul pe linie).

#### 🟠 PAS 3 — Oprește netcat (Ctrl+C), apoi oprește captura (Ctrl+C în CAPTURĂ)

**🎯 Confruntare cu predicția 3 — Epifanie ⚡:**

> *▸ „Câte pachete ați prezis la început? Uitați-vă: primele 3 pachete sunt SYN → SYN-ACK → ACK. Acesta este three-way handshake-ul TCP (RFC 793). Abia DUPĂ handshake apar pachetele cu date."*

Ce arăți pe ecran:

- **Handshake:** SYN → SYN-ACK → ACK — primele 3 pachete.
- **Payload:** pachetele cu date (marcate PSH/ACK).
- **ACK-uri:** după fiecare pachet cu date, cealaltă parte confirmă.

**Display filter (după captură):** `tcp.stream eq 0` — izolează conversația.

> *▸ „Diferența: capture filter = înainte de captură, nu poți schimba; display filter = după captură, poți filtra și re-filtra oricât."*

---

### Scenariul UDP

#### 🟠 PAS 4 — Captură nouă

| 🟠 TERMINAL CAPTURĂ |
|:----|
| `$ sudo tshark -i lo -f "udp port 9201"` |
| *(sau Wireshark: Capture Filter → `udp port 9201`)* |

#### 🔵🟢 PAS 5 — Server + mesaj UDP

| 🔵 TERMINAL SERVER | 🟢 TERMINAL CLIENT |
|:----|:----|
| `$ nc -u -l -p 9201` | `$ echo "test UDP" \| nc -u 127.0.0.1 9201` |

#### 🟠 PAS 6 — Oprește captura. Ce vezi:

**Zero handshake** — prima datagramă conține deja datele. Nu există SYN, nu există ACK.

**Display filter:** `udp.port == 9201`

### Tabel comparativ (proiectat sau verbalizat)

| Aspect | TCP | UDP |
|--------|-----|-----|
| Conexiune | Da (three-way handshake) | Nu |
| Confirmare livrare | Da (ACK) | Nu |
| Ordine garantată | Da (sequence/ack numbers) | Nu |
| Overhead în captură | Handshake + ACK-uri + date | Doar date |
| Display filter util | `tcp.stream eq 0` | `udp.port == 9201` |

---

## Bloc E — Recapitulare, hook reluat, temă (~5 min)

### Hook reluat (30 sec)

> *▸ „Vă amintiți scenariul de la început — 'site-ul nu merge, dar ping răspunde'? Acum aveți instrumentele: verificați DNS (`nslookup`), verificați portul (`netstat` — poate serviciul nu ascultă), capturați traficul (`tshark`) și vedeți ce se întâmplă. Nu mai ghiciți."*

### Confruntare finală cu predicțiile (30 sec)

> *▸ „Predicțiile de la început: (1) `ping` eșuat ≠ internet picat — confirmat; (2) TCP vs UDP e structural, nu doar viteză — confirmat prin comportamentul netcat; (3) TCP începe cu 3 pachete — confirmat în captură."*

### Ce iau cu ei (3 idei)

1. Diagnosticul de rețea se face în straturi: DNS → conectivitate → porturi → trafic → pachete.
2. TCP = conexiune cu stare, UDP = datagrame fără stare.
3. Wireshark/tshark: capture filter (înainte) ≠ display filter (după).

### Temă

Indică pe repo/Moodle cele trei fișiere de exerciții din `04_SEMINARS/S01/`:

| Fișier task | Ce produce | Livrabil |
|---|---|---|
| `S01_Part02_Tasks_Basic_Tools.md` | Comenzi + output + interpretare pentru `ping`, `netstat`, `nslookup` | `S01_Part02_Output_Basic_Tools.txt` |
| `S01_Part04_Tasks_Netcat_Basics.md` | Comenzi TCP/UDP + comparație 3–5 propoziții | `S01_Part04_Output_Netcat_Activity.txt` |
| `S01_Part06_Tasks_Wireshark_Netcat.md` | Screenshoturi filtre + pachete + explicație 5–7 propoziții | `wireshark_activity_output.zip` |

> *▸ Porturile din tasks diferă de cele din demo (9100/9101 pentru netcat, 9300/9301 pentru Wireshark) — e intenționat: exercițiul cere muncă proprie, nu copie.*

Opțional — pentru studenți care vor exersare suplimentară: simulatorul interactiv HTML `04_SEMINARS/_HTMLsupport/S01/S01_CLI_NetcatTCP-UDP_Wireshark_sim.html` (se deschide local în browser).

### Preview S02

> *▸ „Data viitoare scriem cod — server și client TCP în Python. Vom folosi Wireshark ca să vedem ce produc scripturile noastre."*

### Cerință logistică pentru S02

> *▸ „Toată lumea trebuie să aibă VM-ul funcțional. Test: PuTTY → `127.0.0.1:2222` → `stud/stud` → vedeți `(compnet) stud@mininet-vm:~$`. Dacă merge asta, sunteți pregătiți."*

---

## Cheat-sheet

| Element | Locație / Acțiune |
|---------|-------------------|
| VM MININET-SDN | Pornită în VirtualBox, SSH pe `127.0.0.1:2222`, `stud/stud` |
| 🔵 Terminal SERVER | Sesiune SSH #1 — etichetată „SERVER" |
| 🟢 Terminal CLIENT | Sesiune SSH #2 — etichetată „CLIENT" |
| 🟠 Terminal CAPTURĂ | Sesiune SSH #3 — pentru `tshark` (sau Wireshark pe host) |
| Proiector | Split-screen SERVER / CLIENT |
| Fișiere kit S01 | `04_SEMINARS/S01/` |
| Soluții (instructor) | `04_SEMINARS/_tutorial-solve/s1/` |
| Simulator HTML | `04_SEMINARS/_HTMLsupport/S01/S01_CLI_NetcatTCP-UDP_Wireshark_sim.html` |
| Ghid setup | `01_GHID_MININET-SDN/SETUP-GUIDE-COMPNET-EN.md` |

---

## Plan de contingență

| Problemă | Soluție rapidă |
|----------|---------------|
| VM-ul nu pornește | Demonstrezi de pe laptopul personal (orice Linux / WSL). Dacă nici asta nu merge — folosește simulatorul HTML ca plan C. |
| `nc` lipsește | `sudo apt install netcat-openbsd` (include `nc`). Alternativ: `ncat` din pachetul `nmap`. |
| Wireshark pe host nu vede traficul loopback | Treci pe `tshark` din VM: `sudo tshark -i lo -f "tcp port 9200"`. Pedagogic e identic. |
| Studenții nu au VM-ul instalat | Normal la S01 — Blocul A0 explică setup-ul. Trebuie să-l aibă funcțional la S02. |
| Nu ai internet în VM | `ping 10.0.2.2` (gateway NAT VirtualBox) funcționează. Folosește IP-uri în loc de domenii. La `nslookup` explici că DNS-ul nu răspunde, ceea ce e un caz real de diagnostic. |
| Depășești 40 min | Sacrifică Blocul D (captură). Recuperezi la debutul S02, cu demonstrație scurtă de 5 min. |
| `tshark` cere permisiuni | `sudo tshark ...` (parola `stud`). Dacă `sudo` nu merge, verifică grupul `wireshark`: `sudo usermod -aG wireshark stud`. |

---

## Referințe

Postel, J. (Ed.). (1981). Transmission Control Protocol. RFC 793. Internet Engineering Task Force. https://doi.org/10.17487/RFC0793

Postel, J. (1980). User Datagram Protocol. RFC 768. Internet Engineering Task Force. https://doi.org/10.17487/RFC0768

McCanne, S. & Jacobson, V. (1993). The BSD packet filter: A new architecture for user-level packet capture. In *Proceedings of the USENIX Winter 1993 Conference* (pp. 259–270). USENIX Association. https://doi.org/10.5555/1267303.1267305

Matthews, J. N. (2005). Hands-on approach to teaching computer networking using packet traces. In *Proceedings of the 6th Conference on Information Technology Education* (pp. 361–367). ACM. https://doi.org/10.1145/1095714.1095777

Driver, R., Asoko, H., Leach, J., Mortimer, E. & Scott, P. (1994). Constructing scientific knowledge in the classroom. *Educational Researcher, 23*(7), 5–12. https://doi.org/10.3102/0013189X023007005

---

## Note pedagogice

**Tipare socratice folosite:**
- POE 1 (Bloc B1): predicție DNS inexistent → observație NXDOMAIN → explicație diferență DNS vs. conectivitate.
- POE 2 (Bloc C, PAS 7): predicție UDP fără receptor → observație zero erori → explicație fire and forget.
- Confruntare cu predicția 3 (Bloc D, PAS 3): handshake TCP vizibil = 3 pachete → confirmare.

**Epifanii marcate (⚡):**
1. Bloc C PAS 7 — UDP nu semnalează pierderea. Momentul cel mai memorabil al seminarului.
2. Bloc D PAS 3 — three-way handshake vizibil în captură vs. absența totală la UDP.

**Concepții greșite vizate:**
- „ping eșuat = internet picat" → ramuri multiple de diagnostic (Bloc B).
- „TCP și UDP = diferență de viteză" → diferență structurală (Bloc C).
- „TCP: un mesaj = un pachet" → TCP este stream, vizibil în captură (Bloc D, menționat la recap).
- Legatură indirectă cu misconception #11 (secvența server/client) — ordinea de pornire netcat (server întâi) prefigurează `bind → listen → accept` din S02.

**Legătura cu S02:** S02 (socket programming Python) folosește Wireshark/tshark pentru analiza traficului generat programatic. Dacă Blocul D se sacrifică azi, se recuperează în primele 5 minute ale S02 cu o demonstrație compactă.

---

*Outline S01 MININET-SDN — verificat pe baza kit-ului `compnet-2025-redo` (versiune `claudev11_EN`), directorul `04_SEMINARS/S01/` și `04_SEMINARS/_tutorial-solve/s1/`.*

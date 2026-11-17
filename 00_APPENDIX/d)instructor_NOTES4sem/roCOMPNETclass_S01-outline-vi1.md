# Seminar 1 — Analiză de rețea

**Wireshark, netcat TCP/UDP, debugging trafic**

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — ASE-CSIE |
| **Kit** | `v0compnet-2025-redo-main` |
| **Infra** | MININET-SDN (Ubuntu 24.04, VirtualBox) |
| **Buget timp util** | 35–50 minute (restul → prezentare semestru, fișa disciplinei, obligații, evaluare) |

---

## Structura completă a ședinței

| Bloc | Ce faci | Durată |
|:----:|---------|-------:|
| **A** | Prezentare generală: semestru, fișă, reguli, evaluare, mediu de lucru | 30–40 min |
| **B** | Etapa 1 — Comenzi de bază: `ping`, `netstat`, `nslookup` | ~10 min |
| **C** | Etapa 2 — Netcat TCP și UDP | ~15 min |
| **D** | Etapa 3 — Wireshark pe trafic netcat | ~15 min |
| **E** | Recapitulare + temă individuală + încheiere | ~5 min |

> *▸ Notă de ritm: Etapele B–D sunt progresive: fiecare se construiește pe precedenta. Dacă rămâi fără timp, Etapa D (Wireshark) poate fi amânată la începutul S2, fiindcă S2 din backbone (socket programming Python) presupune deja familiaritatea cu Wireshark. Etapele B și C sunt non-negociabile pentru primul seminar.*

---

## Bloc A — Prezentarea generală

> *▸ Acest bloc NU face parte din cele 35–50 min de conținut tehnic. E blocul administrativ/introductiv.*

**1. Cine ești tu** — scurtă prezentare, date de contact, canal de comunicare (Teams / email / Moodle).

**2. Fișa disciplinei** — obiective, competențe, bibliografie, pondere examen vs. seminar.

**3. Regulile jocului** — prezență, plagiat, cum se evaluează activitatea de seminar, condiții de promovabilitate.

**4. Calendarul semestrului** — cele 13–14 seminarii cu temele aferente (poți proiecta `current-outline.md` din backbone).

**5. Mediul de lucru: MININET-SDN** — explici *ce este* și *de ce*:

- Mașină virtuală Ubuntu 24.04, pre-configurată, rulează sub Oracle VirtualBox.
- Conține tot ce le va trebui pe semestru: Docker Engine + Compose v2, Mininet 2.3, Open vSwitch 3.3, Python 3.12 cu venv `compnet`, tshark, Scapy, nmap, Paramiko, Flask etc.
- Se descarcă ca fișier `.ova` (~2–3 GB) și se importă în VirtualBox (File → Import Appliance).
- Credențiale: `stud` / `stud`.
- Conexiunea la VM se face prin SSH (PuTTY sau `ssh -p 2222 stud@127.0.0.1`) — consola VirtualBox e doar de avarie.
- Arată schema de arhitectură din ghidul de setup (Windows host ↔ VirtualBox NAT ↔ VM cu Docker, Mininet, Python).

**6. Indică ghidul de instalare** (`SETUP-GHID-COMPNET_-RO.md`) — studenții trebuie să vină cu VM-ul funcțional de data viitoare.

> *▸ Sfat practic: Dacă sala are stațiile cu VM-ul pre-instalat, pornește una și fă live un `ssh -p 2222 stud@127.0.0.1` ca să vadă prompt-ul. Dacă nu — arată de pe laptopul tău. Obiectivul: studenții văd `(compnet) stud@mininet-vm:~$` și înțeleg că acolo se lucrează tot semestrul.*

---

## Bloc B — Etapa 1: Comenzi de bază (~10 min)

**Fișier backbone:** `assets/tutorial/s1/1_basic-tools_scenario.md`
**Unde rulezi:** direct în VM (prin SSH/PuTTY) — sau orice terminal Linux
**Ce demonstrezi:** vizibilitate asupra conectivității, stării conexiunilor și rezolvării DNS

### Narativ de deschidere

> *▸ „Înainte de orice programare de rețea, trebuie să știm să diagnosticăm. Trei comenzi vă rezolvă 80% din problemele de debugging: `ping` (funcționează drumul?), `netstat` (cine ascultă pe ce port?) și `nslookup` (funcționează DNS-ul?). Le încercăm pe toate trei chiar acum."*

### 1. `ping` — Verificarea conectivității

```bash
ping -c 4 google.com
```

Arată: rezolvarea DNS (IP-ul), timpii de RTT (round-trip time), packet loss.

Explică: `ping` trimite pachete ICMP Echo Request și așteaptă Echo Reply. Dacă merge, conexiunea funcționează end-to-end. Dacă nu, fie DNS-ul e stricat, fie nu ai rută.

Opțional: `ping -c 4 10.0.2.2` (gateway-ul NAT din VirtualBox) — exemplu de ping pe IP, fără DNS.

### 2. `netstat` — Conexiuni și porturi active

```bash
netstat -tulnp
```

Explică fiecare flag: `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric (fără DNS invers), `-p` procesul proprietar.

Arată un port în LISTEN (ex. sshd pe :22). Pentru ESTABLISHED (sesiunea SSH curentă), rulează separat `netstat -tnp` sau `ss -tnp`; `-l` selectează listeners.

> *▸ Alternativă modernă: `ss -tulnp` — exact aceleași flag-uri, disponibil pe distribuțiile mai noi.*

### 3. `nslookup` — Interogare DNS

```bash
nslookup google.com
```

Arată: serverul DNS utilizat, adresa IP rezolvată.

```bash
nslookup domeniu-inexistent-xyz123.com
```

Arată eroarea „server can't find" — diferența între un domeniu rezolvabil și unul inexistent.

### Ce NU faci aici

Nu dai exercițiul individual acum (`2_basic-tools_task.md`). Rămâne ca temă sau se face dacă rămâne timp la final. Nu intri în detalii despre ICMP, protocolul DNS intern sau ARP — vin la cursurile 5–6.

> *▸ Durată țintă: 8–10 minute (inclusiv eventuale întrebări).*

---

## Bloc C — Etapa 2: Netcat TCP și UDP (~15 min)

**Fișier backbone:** `assets/tutorial/s1/3_netcat-basics_scenario.md`
**Ce demonstrezi:** diferența fundamentală TCP (conexiune, bidirecțional, cu stare) vs. UDP (datagrame, fără stare)

### Narativ de deschidere

> *▸ „Trecem de la diagnostic la trafic real. `netcat` (sau `nc`) e cuțitul elvețian al rețelelor: poate fi server, client, poate trimite și primi pe TCP sau UDP. Îl folosim ca să înțelegem diferența între cele două protocoale de transport — fără o linie de cod."*

### Pregătire

Deschide **două sesiuni SSH** către VM (două ferestre PuTTY sau două tab-uri în terminal). Pune-le **side-by-side pe proiector**. Studenții trebuie să vadă simultan ce se întâmplă în fiecare.

---

### 🔷 PAS 1 — Pornește serverul TCP

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `$ nc -l -p 9000` | *— nu face nimic încă, așteaptă* |
| *(cursor blocat — așteaptă conexiune)* | |

> *▸ Explică: `-l` = listen (mod server), `-p 9000` = portul. Comanda se blochează — serverul așteaptă.*

---

### 🔷 PAS 2 — Conectează clientul

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| *(tot blocat, dar acum conexiunea e stabilită)* | `$ nc 127.0.0.1 9000` |
| | *(conectat — poți scrie)* |

> *▸ Explică: clientul se conectează la loopback (127.0.0.1) pe portul 9000. Conexiunea TCP e stabilită.*

---

### 🔷 PAS 3 — Schimb de mesaje bidirecțional

**Client → Server:**

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `salut de la client` | `> salut de la client` ⏎ |
| ↑ *apare automat* | ↑ *tastezi și apeși Enter* |

**Server → Client:**

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `> salut de la server` ⏎ | `salut de la server` |
| ↑ *tastezi și apeși Enter* | ↑ *apare automat* |

> *▸ Subliniază: conexiunea e BIDIRECȚIONALĂ și PERSISTENTĂ — orice scrii într-o parte apare în cealaltă instantaneu.*

---

### 🔷 PAS 4 — Închidere conexiune

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| **Ctrl+C** → serverul se oprește | *(deconectat automat)* |
| | ↑ *clientul detectează închiderea* |

> *▸ Explică: TCP are o procedură de terminare (FIN/ACK). Când o parte închide, cealaltă află.*

---

### 🔷 PAS 5 — Pornește serverul UDP

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `$ nc -u -l -p 9001` | *— nu face nimic încă* |
| *(așteaptă datagrame)* | |

> *▸ Explică: `-u` = UDP. Serverul ascultă datagrame, NU conexiuni. Niciun handshake.*

---

### 🔷 PAS 6 — Trimite un mesaj UDP

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `test UDP` | `$ echo "test UDP" \| nc -u 127.0.0.1 9001` |
| ↑ *apare mesajul primit* | |

> *▸ Subliniază: nu există conexiune persistentă. Fiecare mesaj e o datagramă independentă.*

---

### 🔷 PAS 7 — Pierderea UDP (opțional, dar puternic pedagogic)

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| **Ctrl+C** → serverul OPRIT | *← serverul nu mai ascultă* |

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| *(nimic — nimeni nu ascultă)* | `$ echo "mesaj pierdut" \| nc -u 127.0.0.1 9001` |
| | *(nicio eroare — dar mesajul a dispărut!)* |

**Punchline:** Clientul NU primește eroare. Mesajul s-a pierdut în liniște. ***Asta e UDP — fire and forget.***

### Recapitulare verbală (30 secunde)

> *▸ „TCP = conexiune stabilă, bidirecțională, cu garanții de livrare. UDP = datagrame independente, rapid, fără garanții. Ambele sunt esențiale: TCP pentru web, email, SSH; UDP pentru DNS, streaming, jocuri online."*

> *▸ Durată țintă: 12–15 minute.*

---

## Bloc D — Etapa 3: Wireshark pe trafic netcat (~15 min)

**Fișier backbone:** `assets/tutorial/s1/5_wireshark-netcat_scenario.md`
**Ce demonstrezi:** cum arată TCP vs. UDP la nivel de pachete; diferența între capture filter și display filter

### Aspect logistic — acum ai 3 terminale

Pe lângă cele două sesiuni SSH de la Bloc C (SERVER și CLIENT), deschide un **al treilea terminal SSH** dedicat capturii. Alternativ, folosește Wireshark pe Windows în loc de al treilea terminal.

> *▸ Sfat pragmatic: Dacă configurația NAT face capturile dificile în Wireshark pe host, fă toată demonstrația cu tshark din VM. Pedagogic e identic, doar interfața e text în loc de grafic.*

### Narativ de deschidere

> *▸ „Până acum am trimis și am primit date — dar nu am văzut ce se întâmplă pe fir. Wireshark ne permite să capturăm fiecare pachet și să-l descompunem strat cu strat. Vedem cu ochii noștri handshake-ul TCP și înțelegem de ce UDP arată altfel."*

---

### Scenariul TCP

#### 🟠 PAS 1 — Pornește captura — TERMINAL CAPTURĂ (SSH #3)

| 🟠 TERMINAL CAPTURĂ (SSH #3 sau Wireshark pe host) |
|:----|
| **Varianta tshark:** `$ sudo tshark -i lo -f "tcp port 9200"` |
| **Varianta Wireshark:** Capture Filter → `tcp port 9200` → Start |

---

#### 🟠 PAS 2 — Server + client netcat + mesaje

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `$ nc -l -p 9200` | `$ nc 127.0.0.1 9200` |
| *(așteaptă...)* | |

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `mesaj1` | `> mesaj1` ⏎ |
| `mesaj2` | `> mesaj2` ⏎ |
| `mesaj3` | `> mesaj3` ⏎ |

---

#### 🟠 PAS 3 — Oprește captura. Ce vezi și ce explici:

**Handshake-ul TCP (SYN → SYN-ACK → ACK):** primele 3 pachete. Modul în care TCP stabilește conexiunea. Three-way handshake.

**Pachetele cu payload:** datele voastre — mesaj1, mesaj2, mesaj3 — încapsulate în segmente TCP.

**ACK-urile:** după fiecare pachet cu date, cealaltă parte confirmă primirea.

**Display filter (după captare):** `tcp.stream eq 0` — izolează conversația.

---

### Scenariul UDP

#### 🟠 PAS 4 — Captură nouă — TERMINAL CAPTURĂ

| 🟠 TERMINAL CAPTURĂ |
|:----|
| `$ sudo tshark -i lo -f "udp port 9201"` sau Capture Filter: `udp port 9201` |

---

#### 🟠 PAS 5 — Server + mesaj UDP

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `$ nc -u -l -p 9201` | *← așteaptă* |
| *(așteaptă datagrame...)* | |

| 🔵 TERMINAL SERVER (SSH #1) | 🟢 TERMINAL CLIENT (SSH #2) |
|:----|:----|
| `test UDP` | `$ echo "test UDP" \| nc -u 127.0.0.1 9201` |

---

#### 🟠 PAS 6 — Oprește captura. Ce vezi și ce explici:

**Zero handshake** — prima datagramă conține deja datele. Nu există SYN, nu există ACK. Fiecare pachet e independent.

**Display filter:** `udp.port == 9201`

---

### Tabel comparativ TCP vs. UDP (verbalizat sau proiectat)

| Aspect | TCP | UDP |
|--------|-----|-----|
| Conexiune | Da (3-way handshake) | Nu |
| Confirmare | Da (ACK) | Nu |
| Ordine garantată | Da (seq/ack numbers) | Nu |
| Overhead | Mai mare | Mai mic |
| Vizibil în captură | Handshake + ACK-uri + date | Doar date |

> *▸ Durată țintă: 12–15 minute.*

---

## Bloc E — Recapitulare și temă (~5 min)

### Ce spui

> *▸ „Astăzi am pus bazele: știți să diagnosticați o rețea cu `ping`/`netstat`/`nslookup`, știți să creați trafic cu `netcat` pe TCP și UDP, și ați văzut la nivel de pachete cum arată diferența. Data viitoare scriem cod — server și client TCP în Python."*

### Temă pentru acasă / pentru ora curentă

Distribuie (sau indică pe repo/Moodle) cele trei fișiere de exerciții din backbone:

1. `2_basic-tools_task.md` → Producerea fișierului `basic_tools_output.txt`
2. `4_netcat-basics_task.md` → Producerea fișierului `netcat_activity_output.txt`
3. `6_wireshark-netcat_task.md` → Producerea fișierului `wireshark_activity_output.zip`

Explică: fiecare exercițiu cere o dovadă de lucru — fișier text cu comenzile rulate, output-urile și interpretarea.

### Cerință logistică pentru Seminarul 2

> *▸ „Data viitoare, toată lumea trebuie să aibă VM-ul MININET-SDN funcțional. Cel mai important test: deschideți PuTTY, vă conectați pe `127.0.0.1:2222`, `stud/stud`, și vedeți prompt-ul `(compnet) stud@mininet-vm:~$`. Dacă merge asta, sunteți pregătiți."*

---

## Cheat-sheet: ce ai de deschis înainte de oră

| Element | Locație / Acțiune |
|---------|-------------------|
| Stația MININET-SDN | Pornită în VirtualBox, conectat prin SSH pe `127.0.0.1:2222` |
| Terminal 1 (SERVER) | Sesiune SSH deschisă — etichetată „SERVER" |
| Terminal 2 (CLIENT) | Sesiune SSH deschisă — etichetată „CLIENT" |
| Terminal 3 (captură) | Sesiune SSH — pentru `tshark` (sau Wireshark pe host) |
| Wireshark (pe host) | Opțional — deschis, gata de selectare interfață |
| Proiector | Split-screen SERVER / CLIENT |
| Fișiere backbone S1 | `assets/tutorial/s1/` |
| Ghidul de setup | `SETUP-GHID-COMPNET_-RO.md` |

---

## Plan de contingență

| Problemă | Soluție rapidă |
|----------|---------------|
| VM-ul nu pornește | Demonstrezi totul de pe laptopul personal (orice Linux / WSL) |
| `netcat` lipsește | `sudo apt install ncat` sau `nmap` (ncat e inclus) |
| Wireshark nu vede traficul loopback | Treci pe `tshark` din VM: `sudo tshark -i lo -f "tcp port 9200"` |
| Studenții nu au VM-ul instalat | Normal la S1 — de aia Blocul A explică setup-ul; trebuie să-l aibă la S2 |
| Nu ai internet în VM | `ping 10.0.2.2` (gateway VBox) funcționează; folosește IP-uri |
| Depășești timpul | Sacrifică Etapa D (Wireshark) — o recuperezi la S2 |

---

*Outline generat pe baza backbone-ului `v0compnet-2025-redo-main`, seminarul S1 (`assets/tutorial/s1/`), stația MININET-SDN și ghidul de setup asociat.*

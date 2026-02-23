# Seminar S05 — Subnetting IPv4/IPv6 + routing inter-subrețea în Mininet (h1 — r1 — h2)

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (arhiva: `claudev11_EN_compnet-2025-redo-main.zip`) |
| **Infra** | MININET-SDN VM (Ubuntu 24.04, VirtualBox) + `python3` + Mininet 2.3 + `iproute2` + `traceroute` + `tcpdump` |
| **Durată țintă** | **35–40 min** (ritm alert; exercițiile „lungi" → temă) |
| **Ideea-cheie** | **Prefixul (masca) definește granița subrețelei.** Comunicarea între subrețele cere: (1) rute pe hosturi și (2) un router care face IP forwarding. Fără oricare dintre ele, pachetele nu trec. |

---

## Obiective operaționale

La finalul S05, studenții vor fi capabili să:

1. **Deriveze rapid** (manual, fără calculator) pentru o subrețea IPv4: adresă de rețea, broadcast, interval de hosturi, număr de hosturi utilizabile — de exemplu pentru /28.
2. **Realizeze equal-size subnetting**: împărțirea unui /24 în N subrețele egale (ex.: 8 → /27) cu verificarea incrementului.
3. **Aplice VLSM** (Variable Length Subnet Masking) cu regula „largest first" și să aleagă prefixul minim pentru o cerință de hosturi dată.
4. **Justifice de ce IPv6 folosește /64** pe LAN (SLAAC + interoperabilitate) și să construiască /64-uri consecutive dintr-un /48.
5. **Configureze și verifice rutarea** într-o topologie `h1 — r1 — h2` în Mininet: adrese IP, rute, `ip_forward`, `ping`, `traceroute`, captură `tcpdump`.

> Notă: în 35–40 min nu rezolvăm toate exercițiile de subnetting. În clasă construim metoda + 1–2 exemple ghidate; restul rămâne activitate individuală, cu livrabile clare.

---

## Structura seminarului

| Bloc | Ce construiești | Durată |
|---:|---|---:|
| A | Hook + activare: „două IP-uri care *par* în aceeași rețea, dar nu sunt" | 3 min |
| B | IPv4: /28 ghidat (network/broadcast/hosts) + metoda „block size" | 9 min |
| C | IPv4: /24 împărțit în 8 subrețele (→ /27) + verificare | 5 min |
| D | VLSM: regula „largest first" + 1 mini-alocare | 3 min |
| E | IPv6: scurtare + /48 → /64 (de ce /64 e standard) | 4 min |
| F | Mininet: `h1 — r1 — h2`, rute + `ip_forward`, `ping`, `traceroute`, `tcpdump` | 12 min |
| G | Recap (cu revenire la hook) + livrabile + preview S06 | 3 min |
| | **Total** | **39 min** |

**Plan de sacrificare (dacă timpul se comprimă):**
- Bloc D (VLSM): redu la 1 min — enunți regula și trimiți direct la temă.
- Bloc E (IPv6): redu la 2 min — arăți doar /48 → /64, fără exemplul de scurtare.
- Bloc F: renunți la captură `tcpdump`; rămâi la `ping` + `traceroute`.

---

## Checklist înainte de seminar

1. **VM-ul MININET-SDN pornit** — intri prin SSH sau direct în terminal.
2. Ai kit-ul disponibil local; știi unde e `04_SEMINARS/S05/`.
3. Verifici uneltele:
   ```bash
   python3 --version
   mn --version
   ip -V
   traceroute --version || true
   tcpdump --version
   ```
4. Copiezi fișierele într-un director de lucru:
   ```bash
   mkdir -p ~/compnet-labs/S05
   cp -r 04_SEMINARS/S05/* ~/compnet-labs/S05/
   cd ~/compnet-labs/S05
   ```
5. Deschizi pe ecran fișierele cu exerciții (ca să nu cauți în timpul orei):
   - `1_ipv4-subnetting/S05_Part01B_Exercises_I_Pv4_Subnetting.md`
   - `2_ipv6-subnetting/S05_Part02B_Exercises_I_Pv6_Subnetting.md`

---

## Bloc A (3 min) — Hook + activare cunoștințe

### Ce spui

1. Legătura cu seminarul anterior:
   > *▸ „La S04 am trimis mesaje între procese. Azi mergem un nivel mai jos: procesele erau pe aceeași mașină sau pe mașini din aceeași rețea. Ce se întâmplă când destinația e într-o altă subrețea?"*

2. Scrii pe tablă (sau proiectezi) două întrebări:
   - **Q1:** „`172.16.12.70/28` și `172.16.12.90/28` — sunt în aceeași subrețea?"
   - **Q2:** „Dacă schimb /28 în /24, răspunsul se schimbă?"

3. Ceri vot rapid (mâini ridicate). Scopul: să greșească natural.

4. Punchline:
   > *▸ „Greșeala tipică: te uiți la primii octeți și ignori prefixul. Prefixul decide granița. În 10 minute vreau să răspundeți corect în 15 secunde — și apoi demonstrăm cu un lab de routing."*

### Ce faci
- Nu intri în calcule. Doar setezi motivul pentru Bloc B.

---

## Bloc B (9 min) — IPv4 /28: network, broadcast, hosts (metoda „block size")

> Fișier de referință: `S05_Part01A_Explanation_I_Pv4_Subnetting.md` + Exercise 1 din `S05_Part01B_Exercises_I_Pv4_Subnetting.md`.

### Ce spui (1 min — definiții)

- Network address = toți biții de host pe 0.
- Broadcast address = toți biții de host pe 1.
- Hosturi utilizabile = între ele.
- Număr hosturi = `2^(biți_host) − 2` (excepții /31, /32 — nu intrăm azi).

### Ce faci (8 min — rezolvi ghidat Exercise 1)

Subrețeaua: `172.16.12.64/28`.

Pași (scriiți și verbalizați, pe tablă/ecran):

1. `/28` = 24 biți (primele 3 octeți) + 4 biți în octetul 4.
2. Masca în octetul 4: `11110000` = `240`. Block size = `256 − 240 = 16`.
3. Subrețelele în ultimul octet merg din 16 în 16: `0, 16, 32, 48, 64, 80, ...`
4. Ultimul octet = 64 → fix multiplu de 16 → **network = 172.16.12.64**.
5. Broadcast = `64 + 16 − 1 = 79` → **172.16.12.79**.
6. Host range: `.65 … .78`.
7. Hosturi utilizabile: `16 − 2 = 14`.

> 💡 *▸ „/28 nu e un număr abstract: înseamnă blocuri de 16 adrese. Dacă înțelegi blocul, ai network și broadcast fără să scrii binar."*

**Tipar socratic — capcană de concepție greșită (30 sec):**
> *▸ „Acum revenim la hook: `.70/28` e în blocul `.64–.79`. Iar `.90/28`? Block size 16: `80, 96...` — deci `.90` e în blocul `.80–.95`. Subrețele diferite. Câți ați răspuns greșit?"*

---

## Bloc C (5 min) — /24 în 8 subrețele egale → /27

> Fișier de referință: Exercise 2 din `S05_Part01B_Exercises_I_Pv4_Subnetting.md`.

### Predicție (30 sec — rupe seria pasivă)

> *▸ „Vreau 8 subrețele egale din `192.168.100.0/24`. Cine știe ce prefix rezultă? Gândiți 10 secunde."*

Lași pauză. Aduni câteva răspunsuri.

### Ce faci (4 min 30 sec)

Regula:
- `8 = 2³` → împrumuți 3 biți → `/24 + 3 = /27`.
- /27 → masca octetului 4: 224 → block size = `256 − 224 = 32`.

Scrii primele 3, le dictezi pe celelalte:

| # | Subrețea | Broadcast |
|---|---|---|
| 1 | `192.168.100.0/27` | `.31` |
| 2 | `192.168.100.32/27` | `.63` |
| 3 | `192.168.100.64/27` | `.95` |
| … | din 32 în 32 | … |
| 8 | `192.168.100.224/27` | `.255` |

**Verificare rapidă:** `8 × 32 = 256` → acoperă fix un /24. Hosturi per subrețea: `32 − 2 = 30`.

---

## Bloc D (3 min) — VLSM: „largest first"

> Fișier de referință: Exercise 3 din `S05_Part01B_Exercises_I_Pv4_Subnetting.md`.

### Ce spui

1. VLSM = Variable Length Subnet Masking — prefixe diferite în funcție de nevoie, pentru a nu irosi spațiu.
2. Regula:
   > *▸ „Întotdeauna aloci întâi subrețelele mari. Dacă faci invers, riști overlap."*
3. Exemplu rapid (din `10.10.0.0/24`):
   - ≥ 60 hosts → 64 adrese → `/26` (62 hosturi utilizabile)
   - `Subnet A` → `10.10.0.0/26` (broadcast `10.10.0.63`)
   - Următoarea alocare: de la `10.10.0.64` în sus.

### Ce faci
- Scrii doar primul pas complet. Restul trimis la exerciții (temă).

> Menționezi: „Exercise 4 din IPv4 e un al doilea scenariu VLSM — testați-vă acasă."

---

## Bloc E (4 min) — IPv6: scurtare + /64 ca model standard

> Fișiere de referință: `S05_Part02A_Explanation_I_Pv6_Subnetting.md` + Exercises 1-2 din `S05_Part02B_Exercises_I_Pv6_Subnetting.md`.

### Ce spui

1. IPv6 = 128 biți. Pe LAN, /64 nu e „preferință" — e convenția care face SLAAC (Stateless Address Autoconfiguration) să funcționeze + maximizează interoperabilitatea.
2. Într-un /48, ai 16 biți pentru subnet ID → 65 536 subrețele /64.

### Ce faci (2 micro-exemple)

**1. Scurtare (Exercise 1 IPv6, primul exemplu):**
- `2001:0db8:0000:0000:abcd:0000:0000:0001`
- Eliminăm zerourile de la început: `2001:db8:0:0:abcd:0:0:1`
- Comprimăm cel mai lung șir de grupuri all-zero (RFC 5952 — la egalitate, primul câștigă): `2001:db8::abcd:0:0:1`

**2. /48 → /64 (Exercise 2 IPv6):**
- Prefix: `2001:db8:1234::/48`
- Subrețele /64: `2001:db8:1234:1::/64`, `...:2::/64`, `...:3::/64`, ..., `...:ff::/64`

> 💡 *▸ „În IPv6, subnetting-ul e mai mult despre ordine decât despre economie. Nu numeri hosturi — ai 2⁶⁴ pe fiecare /64."*

---

## Bloc F (12 min) — Mininet: două subrețele + router

> Fișiere de referință: `S05_Part03A_Explanation_Mininet_Topology.md`, `S05_Part03B_Script_Mininet_Topology.py`, `S05_Part03C_Tasks_Mininet_Config.md`.

### Setup (1 min)

> *▸ „Punem în practică: două subrețele diferite nu comunică direct. Avem nevoie de un router și de rute corecte."*

🔵 **TERMINAL (VM):**
```bash
cd ~/compnet-labs/S05/3_network-simulation
sudo python3 S05_Part03B_Script_Mininet_Topology.py
```

Desenezi topologia pe tablă:
```
h1 (10.0.1.10/24) —— r1 (10.0.1.1 | 10.0.2.1) —— h2 (10.0.2.10/24)
          subnet A                                      subnet B
```

> Notă: scriptul setează automat IP-urile, adaugă default routes pe h1/h2 și activează forwarding pe r1 (clasa `LinuxRouter`). Dezactivăm forwarding-ul live, ca să vedem efectul.

---

### Pas 1 — Verifici IP-urile (1 min 30 sec)

🟢 **MININET CLI:**
```
mininet> h1 ip a
mininet> r1 ip a
mininet> h2 ip a
```

Ce punctezi:
- h1 și h2 sunt în **subrețele diferite** (10.0.1.0/24 vs 10.0.2.0/24).
- r1 are **două interfețe**: `r1-eth0` (10.0.1.1) și `r1-eth1` (10.0.2.1) — câte una în fiecare subrețea.

---

### Pas 2 — Test local: host → router (1 min)

🟢 **MININET CLI:**
```
mininet> h1 ping -c 2 10.0.1.1
mininet> h2 ping -c 2 10.0.2.1
```

Dacă merge → L2/L3 pe fiecare legătură e funcțional.

---

### Pas 3 — Creezi intenționat eșecul: forwarding OFF (2 min)

**Predicție (POE):**
> *▸ „Acum opresc forwarding-ul pe r1. Ce credeți că se va întâmpla când h1 dă ping la h2?"*

Aduni 2-3 răspunsuri. Apoi:

🟢 **MININET CLI:**
```
mininet> r1 sysctl -w net.ipv4.ip_forward=0
mininet> r1 sysctl net.ipv4.ip_forward
```

🟢 **TEST:**
```
mininet> h1 ping -c 2 10.0.2.10
```

**Observație:** pachete pierdute — 100% packet loss.

**Explicație:**
> *▸ „Pachetele ajung la r1, dar r1 nu le trimite mai departe. Asta e diferența dintre un host cu 2 plăci de rețea și un router: routerul face forwarding."*

---

### Pas 4 — Repari: forwarding ON + test (1 min 30 sec)

🟢 **MININET CLI:**
```
mininet> r1 sysctl -w net.ipv4.ip_forward=1
mininet> h1 ping -c 3 10.0.2.10
```

> 💡 *▸ „Un singur bit — `ip_forward` — decide dacă mașina e router sau host. În producție, pe un Linux obișnuit, forwarding-ul e dezactivat implicit."*

---

### Pas 5 — `traceroute`: vezi hop-ul r1 (2 min)

🟢 **MININET CLI:**
```
mininet> h1 traceroute -n 10.0.2.10
```

Ce punctezi:
- Primul hop: `10.0.1.1` (r1).
- `traceroute` nu „ghicește" — exploatează TTL (Time To Live) și mesajele ICMP Time Exceeded (RFC 792).

---

### Pas 6 — Captură `tcpdump` (3 min)

🟠 **CAPTURĂ (pe r1):**
```
mininet> h1 ping -c 4 10.0.2.10 &
mininet> r1 tcpdump -i r1-eth0 -n icmp -c 8
```

Ce arăți în output:
- **Echo Request** (h1 → h2) și **Echo Reply** (h2 → h1).
- Adresele sursă/destinație: r1 nu le schimbă (nu face NAT — doar forwarding).

> Dacă vrei fișier `.pcap` (bonus, nu obligatoriu în timpul alocat):
> ```
> mininet> r1 tcpdump -i r1-eth0 -n icmp -w /tmp/s05_icmp.pcap -c 20
> ```

---

## Bloc G (3 min) — Recap + livrabile + preview S06

### Recap (revenire la hook)

> *▸ „La început ați votat dacă `.70/28` și `.90/28` sunt în aceeași subrețea. Acum știți metoda: block size 16, deci `.64–.79` vs. `.80–.95` — subrețele diferite. Și ați văzut practic ce se întâmplă când routerul nu face forwarding."*

Trei idei de fixat:
1. **Subnetting IPv4:** prefix → block size → network/broadcast, fără binar.
2. **Routing:** rute pe host + forwarding pe router. Fără oricare, ping nu trece.
3. **IPv6:** /64 pe LAN e standard; dintr-un /48 ai 65 536 subrețele.

### Preview S06

> *▸ „Data viitoare intrăm în SDN: topologii mai complexe, switch-uri virtuale, și cum se gestionează traficul la scară. Componentele de azi — subrețele, rute, forwarding — rămân fundația."*

### Livrabile (ce predau studenții)

1. **IPv4:** `S05_Part01C_Solutions_Template_I_Pv4_Subnetting.md` completat (toate cele 6 exerciții).
2. **IPv6:** `S05_Part02C_Solutions_Template_I_Pv6_Subnetting.md` completat (toate cele 6 exerciții).
3. **Mininet lab:** fișierul `mininet_lab_output.txt` cu:
   - comenzile rulate (`ip a`, `ip route`, `sysctl`, `ping`, `traceroute`) + output-ul lor
   - 5–7 propoziții: de ce a fost necesar routerul, ce face `ip_forward`, rolul default route

> Notă: fișierele de task-uri menționează nume `index_*` care nu apar ca atare în kit. Recomandare: folosiți template-urile din kit cu numele lor originale, sau faceți o copie cu numele cerut.

---

## Cheat-sheet

### Block size rapid (prefixe /25–/30)

| Prefix | Masca octet 4 | Block size | Hosturi utilizabile |
|---|---|---|---|
| /25 | 128 | 128 | 126 |
| /26 | 192 | 64 | 62 |
| /27 | 224 | 32 | 30 |
| /28 | 240 | 16 | 14 |
| /29 | 248 | 8 | 6 |
| /30 | 252 | 4 | 2 |

### Mininet — comenzi frecvente

| Comandă | Ce face |
|---|---|
| `sudo python3 <script>.py` | Pornește topologia |
| `h1 ip a` | Afișează interfețe + adrese pe h1 |
| `h1 ip route` | Afișează tabela de rutare pe h1 |
| `r1 sysctl net.ipv4.ip_forward` | Verifică starea forwarding |
| `r1 sysctl -w net.ipv4.ip_forward=1` | Activează forwarding |
| `h1 ping -c 3 10.0.2.10` | Test conectivitate |
| `h1 traceroute -n 10.0.2.10` | Traseu cu hop-uri |
| `r1 tcpdump -i r1-eth0 -n icmp -c 8` | Captură ICMP |
| `sudo mn -c` | Curăță sesiunea Mininet (după erori) |

---

## Plan de contingență

| # | Problemă | Soluție |
|---|---|---|
| 1 | Mininet rămâne „murdar" după rulare eșuată | `sudo mn -c` și relansează scriptul |
| 2 | `traceroute` lipsește | Folosește `tracepath 10.0.2.10` ca alternativă |
| 3 | `ping` nu merge deși forwarding = 1 | Verifică rutele: `h1 ip route`, `h2 ip route`. Dacă lipsesc, adaugă manual: `h1 ip route add default via 10.0.1.1` / `h2 ip route add default via 10.0.2.1` |
| 4 | Studenții se blochează la subnetting | Redu la algoritmul minimal: „block size → network → broadcast". Restul derivă. |
| 5 | Captura `tcpdump` nu prinde pachete | Verifică interfața corectă (`r1-eth0`). Alternativ, captează pe `any`: `r1 tcpdump -i any -n icmp -c 8` |
| 6 | Scriptul Python dă eroare la import Mininet | Verifică venv-ul: `which python3` trebuie să fie din `(compnet)`. Dacă nu: `source ~/.bashrc` sau `workon compnet`. |
| 7 | Timpul se comprimă sub 30 min | Sacrifică Bloc D (VLSM → 1 min), Bloc E (IPv6 → 2 min), tcpdump (sari). Asigură hook + B + F. |

---

## Referințe (APA 7th ed.)

| Referință | DOI / URL |
|---|---|
| Postel, J. (1981). *Internet Protocol* (RFC 791). RFC Editor. | https://doi.org/10.17487/RFC0791 |
| Mogul, J., & Postel, J. (1985). *Internet Standard Subnetting Procedure* (RFC 950). RFC Editor. | https://doi.org/10.17487/RFC0950 |
| Fuller, V., & Li, T. (2006). *Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan* (RFC 4632). RFC Editor. | https://doi.org/10.17487/RFC4632 |
| Deering, S., & Hinden, R. (2017). *Internet Protocol, Version 6 (IPv6) Specification* (RFC 8200). RFC Editor. | https://doi.org/10.17487/RFC8200 |
| Deering, S., & Hinden, R. (2006). *IP Version 6 Addressing Architecture* (RFC 4291). RFC Editor. | https://doi.org/10.17487/RFC4291 |
| Kawamura, S., & Kawashima, M. (2010). *A Recommendation for IPv6 Address Text Representation* (RFC 5952). RFC Editor. | https://doi.org/10.17487/RFC5952 |
| Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: Rapid prototyping for software-defined networks. *Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks.* | https://doi.org/10.1145/1868447.1868466 |

---

## Note pedagogice

**Tipar socratic principal (POE):** Forwarding OFF → ping fail → forwarding ON → ping works. Vizează concepția greșită: „dacă un host are două interfețe, e automat router".

**Tipar socratic secundar (capcană):** Hook-ul cu `.70/28` vs `.90/28` — voturi incorecte → rezolvare cu block size → reluare la recap. Vizează concepția greșită: „primii 3 octeți identici = aceeași subrețea".

**Progresia cognitivă:** amintire (definiții) → înțelegere (block size) → aplicare (exercise ghidat) → analiză (de ce forwarding contează) → evaluare (interpretare traceroute/tcpdump). Crearea rămâne la temă (completare template-uri).

**Epifanii marcate:**
- 💡 Bloc B: „/28 = blocuri de 16, fără binar"
- 💡 Bloc E: „IPv6 subnetting = ordine, nu economie"
- 💡 Bloc F Pas 4: „un singur bit decide: host sau router"

**Timing-ul cel mai riscant:** Bloc F. Dacă Mininet nu pornește, se pierd 2-3 min pe troubleshooting. Soluția: pregătirea sesiunii înainte de oră + `sudo mn -c` în checklist.

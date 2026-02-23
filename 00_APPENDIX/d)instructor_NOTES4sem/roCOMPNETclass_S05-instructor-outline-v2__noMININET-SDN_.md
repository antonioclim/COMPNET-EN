# Seminar S05 — Subnetting IPv4/IPv6 + routing inter-subrețea cu Docker (h1 — r1 — h2)

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (arhiva: `claudev11_EN_compnet-2025-redo-main.zip`) |
| **Infra** | Windows 10/11 + Docker Desktop (WSL2) + Wireshark (Windows) + containere Linux cu `iproute2`, `ping`, `traceroute`, `tcpdump` |
| **Durată țintă** | **35–40 min** (în clasă: rulare + interpretare; build-ul imaginii Docker — înainte de oră) |
| **Ideea-cheie** | **Prefixul (masca) definește granița subrețelei.** Comunicarea între subrețele cere: (1) rute pe hosturi și (2) un router care face IP forwarding. Verificăm cu `tcpdump` în container + Wireshark pe Windows. |

---

## Obiective operaționale

La finalul S05, studenții vor fi capabili să:

1. **Deriveze rapid** (manual) adresa de rețea, broadcast, interval de hosturi și număr de hosturi utilizabile pentru un prefix IPv4 (ex.: /28).
2. **Realizeze equal-size subnetting**: împărțirea unui /24 în N subrețele egale (ex.: 8 → /27) cu verificarea incrementului.
3. **Aplice VLSM** (Variable Length Subnet Masking) cu regula „largest first" și să aleagă prefixul minim pentru o cerință dată.
4. **Justifice de ce IPv6 folosește /64** pe LAN (SLAAC + interoperabilitate) și să construiască /64-uri consecutive dintr-un /48.
5. **Reproducă o topologie** `h1 — r1 — h2` folosind două Docker networks (două subrețele) și un container-router cu IP forwarding.
6. **Producă o captură `.pcap`** a traficului ICMP între subrețele și să o interpreteze în Wireshark.

> Notă: în 35–40 min nu rezolvăm toate exercițiile de subnetting. În clasă construim metoda + 1–2 exemple ghidate; restul rămâne activitate individuală, cu livrabile clare.

---

## Ce folosești din kit (S05) și ce adaugi

### Din kit (exerciții, explicații)
- `04_SEMINARS/S05/1_ipv4-subnetting/S05_Part01A_Explanation_I_Pv4_Subnetting.md`
- `04_SEMINARS/S05/1_ipv4-subnetting/S05_Part01B_Exercises_I_Pv4_Subnetting.md`
- `04_SEMINARS/S05/1_ipv4-subnetting/S05_Part01C_Solutions_Template_I_Pv4_Subnetting.md`
- `04_SEMINARS/S05/2_ipv6-subnetting/S05_Part02A_Explanation_I_Pv6_Subnetting.md`
- `04_SEMINARS/S05/2_ipv6-subnetting/S05_Part02B_Exercises_I_Pv6_Subnetting.md`
- `04_SEMINARS/S05/2_ipv6-subnetting/S05_Part02C_Solutions_Template_I_Pv6_Subnetting.md`

### Adaugi (fișiere Docker în **Anexa A**)
- Un folder local `s05_dockerlab/` cu: `Dockerfile`, `docker-compose.yml`, `captures/`.

---

## Structura seminarului

| Bloc | Ce construiești | Durată |
|---:|---|---:|
| A | Hook + activare: „două IP-uri care *par* în aceeași rețea, dar nu sunt" | 3 min |
| B | IPv4: /28 ghidat (network/broadcast/hosts) + metoda „block size" | 9 min |
| C | IPv4: /24 împărțit în 8 subrețele (→ /27) + verificare | 5 min |
| D | VLSM: regula „largest first" + 1 mini-alocare | 3 min |
| E | IPv6: scurtare + /48 → /64 (de ce /64 e standard) | 4 min |
| F | Docker lab: routing între două subrețele + captură `.pcap` + Wireshark | 12 min |
| G | Recap (cu revenire la hook) + livrabile + preview S06 | 3 min |
| | **Total** | **39 min** |

**Plan de sacrificare (dacă timpul se comprimă):**
- Bloc D (VLSM): redu la 1 min — enunți regula și trimiți la temă.
- Bloc E (IPv6): redu la 2 min — arăți doar /48 → /64, fără exemplu de scurtare.
- Bloc F: renunți la captură `.pcap` / Wireshark; rămâi la `ping` + `traceroute`.

---

## Checklist înainte de seminar

### Pregătirea instructorului (faci înainte de oră)

1. **Docker Desktop rulează** și folosește backend WSL2.
2. Creezi folderul `s05_dockerlab` (ex.: pe Desktop) cu fișierele din **Anexa A**.
3. Construiești imaginea și pornești containerele (PowerShell, în folderul `s05_dockerlab`):
   ```powershell
   docker compose build
   docker compose up -d
   docker compose ps
   ```
4. Verifici accesul:
   ```powershell
   docker exec -it s05-h1 bash
   # (exit)
   ```
5. Verifici că folderul `captures\` există pe host (montat în `r1`).

> Build-ul durează 1-2 min (descarcă pachete). În clasă nu vrei să aștepți `apt-get`.

### Ce le ceri studenților (dacă vor să reproducă)
- Docker Desktop instalat + Wireshark instalat.
- Un editor text (VS Code) pentru a copia `docker-compose.yml`.

---

## Bloc A (3 min) — Hook + activare cunoștințe

### Ce spui

1. Legătura cu seminarul anterior:
   > *▸ „La S04 am construit protocoale peste TCP/UDP. Procesele comunicau — dar erau pe aceeași mașină sau în aceeași rețea. Ce se întâmplă când destinația e într-o altă subrețea?"*

2. Scrii pe ecran (slide / tablă):
   - **Q1:** „`172.16.12.70/28` și `172.16.12.90/28` — sunt în aceeași subrețea?"
   - **Q2:** „Dacă /28 devine /24, răspunsul se schimbă?"

3. Vot rapid (mâini ridicate). Scopul: să greșească natural.

4. Punchline:
   > *▸ „Greșeala tipică: te uiți la primii octeți și ignori prefixul. Prefixul decide granița. În 10 minute vreau să răspundeți corect în 15 secunde — și apoi verificăm cu un lab Docker."*

### Ce faci
- Nu intri în calcule. Motivul e setat pentru Bloc B.

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

Pași (scriiți pe tablă/ecran):

1. `/28` = 24 biți (primele 3 octeți) + 4 biți în octetul 4.
2. Masca în octetul 4: `11110000` = `240`. Block size = `256 − 240 = 16`.
3. Subrețelele în ultimul octet merg din 16 în 16: `0, 16, 32, 48, 64, 80, ...`
4. Ultimul octet = 64 → fix multiplu de 16 → **network = 172.16.12.64**.
5. Broadcast = `64 + 16 − 1 = 79` → **172.16.12.79**.
6. Host range: `.65 … .78`.
7. Hosturi utilizabile: `16 − 2 = 14`.

> 💡 *▸ „/28 nu e un număr abstract: înseamnă blocuri de 16 adrese. Dacă înțelegi blocul, ai network și broadcast fără binar."*

**Tipar socratic — capcană de concepție greșită (30 sec):**
> *▸ „Revenim la hook: `.70/28` e în blocul `.64–.79`. Iar `.90/28`? Block size 16: `80, 96...` — deci `.90` e în blocul `.80–.95`. Subrețele diferite. Câți ați răspuns greșit?"*

---

## Bloc C (5 min) — /24 în 8 subrețele egale → /27

> Fișier de referință: Exercise 2 din `S05_Part01B_Exercises_I_Pv4_Subnetting.md`.

### Predicție (30 sec — rupe seria pasivă)

> *▸ „Vreau 8 subrețele egale din `192.168.100.0/24`. Ce prefix rezultă? Gândiți 10 secunde."*

Pauză. Aduni răspunsuri.

### Ce faci (4 min 30 sec)

Regula:
- `8 = 2³` → împrumuți 3 biți → `/24 + 3 = /27`.
- /27 → masca octet 4: 224 → block size = `256 − 224 = 32`.

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

1. VLSM = Variable Length Subnet Masking — prefixe diferite în funcție de nevoie, ca să nu irosești spațiu.
2. Regula:
   > *▸ „Întotdeauna aloci întâi subrețelele mari. Dacă faci invers, riști overlap."*
3. Exemplu rapid (din `10.10.0.0/24`):
   - ≥ 60 hosts → 64 adrese → `/26` (62 hosturi utilizabile)
   - `Subnet A` → `10.10.0.0/26` (broadcast `10.10.0.63`)
   - Următoarea alocare: de la `10.10.0.64` în sus.

### Ce faci
- Scrii doar primul pas complet. Restul → temă.
- Menționezi: „Exercise 4 din IPv4 e un al doilea scenariu VLSM — testați-vă acasă."

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

## Bloc F (12 min) — Docker lab: routing între două subrețele + captură `.pcap`

### Context (30 sec)

> *▸ „Docker ne permite să construim un laborator cu două subrețele și un router — tot cu stack IP complet, ca mașinile reale. Containerele sunt 'hosturi' cu interfețe de rețea proprii."*

### Topologia (o desenezi pe tablă / slide)

```
h1 (10.0.1.10/24) —— r1 (10.0.1.2 | 10.0.2.2) —— h2 (10.0.2.10/24)
       netA                                             netB
```

> Notă: pe rețelele Docker bridge, adresa `.1` e gateway-ul intern al Docker Engine. Routerul nostru folosește `.2` ca să evităm conflictul.

---

### Pas 1 — Pornești labul (1 min)

🔵 **PowerShell** (în `s05_dockerlab/`):
```powershell
docker compose up -d
docker compose ps
```

Arăți: 3 containere active — `s05-h1`, `s05-r1`, `s05-h2`.

---

### Pas 2 — Verifici IP-urile și rutele (2 min)

Deschizi 3 ferestre (sau pe rând):

🟢 **CONTAINER h1:**
```powershell
docker exec -it s05-h1 bash
```
```bash
ip a
ip route
```

Repeți pe `s05-h2` și `s05-r1`.

Ce punctezi:
- Fiecare host vede doar subrețeaua lui.
- `r1` are două interfețe (de obicei `eth0` și `eth1`) — câte una în fiecare rețea Docker.

---

### Pas 3 — Adaugi rute specifice (2 min)

> *▸ „De ce rute specifice, nu default route? Docker a creat deja un default route către gateway-ul bridge-ului. Pedagogic e și mai interesant: vedem prioritatea 'most specific route wins'."*

🟢 **În s05-h1:**
```bash
ip route add 10.0.2.0/24 via 10.0.1.2
ip route get 10.0.2.10
```

🟢 **În s05-h2:**
```bash
ip route add 10.0.1.0/24 via 10.0.2.2
ip route get 10.0.1.10
```

> *▸ „Acum hosturile știu: pentru cealaltă subrețea, next hop este routerul."*

---

### Pas 4 — Creezi intenționat eșecul: forwarding OFF (2 min)

**Predicție (POE):**
> *▸ „Routerul r1 pornește cu forwarding dezactivat. Ce credeți că se întâmplă când h1 dă ping la h2?"*

Aduni 2-3 răspunsuri. Apoi testezi:

🟢 **În s05-r1:**
```bash
sysctl net.ipv4.ip_forward
```
(trebuie să afișeze 0 — conform `docker-compose.yml`)

🟢 **În s05-h1:**
```bash
ping -c 2 10.0.2.10
```

**Observație:** 100% packet loss.

**Explicație:**
> *▸ „Rutele există, dar routerul refuză să trimită pachetele mai departe. Asta e diferența: un host cu 2 interfețe nu e router până nu activezi forwarding."*

---

### Pas 5 — Repari: forwarding ON + ping + traceroute (2 min)

🟢 **În s05-r1:**
```bash
sysctl -w net.ipv4.ip_forward=1
```

🟢 **În s05-h1:**
```bash
ping -c 3 10.0.2.10
traceroute -n 10.0.2.10
```

Ce punctezi:
- Hop-ul intermediar e r1.
- `traceroute` exploatează TTL (Time To Live) și mesajele ICMP Time Exceeded (RFC 792).

> 💡 *▸ „Un singur bit — `ip_forward` — transformă un host obișnuit în router."*

---

### Pas 6 — Captură `.pcap` + Wireshark (3 min)

🟠 **CAPTURĂ — Fereastra 1 (PowerShell):**
```powershell
docker exec -it s05-r1 tcpdump -i any -n icmp -w /captures/s05_icmp.pcap -c 20
```

🟢 **TEST — Fereastra 2 (PowerShell, în paralel):**
```powershell
docker exec -it s05-h1 ping -c 5 10.0.2.10
```

Oprești captură (Ctrl+C sau aștepți 20 pachete). Dacă fișierul nu e deja în folderul montat:
```powershell
docker cp s05-r1:/captures/s05_icmp.pcap .\s05_icmp.pcap
```

**În Wireshark (Windows):**
- Deschizi `s05_icmp.pcap`.
- Display filter: `icmp`.
- Observi **Echo Request** vs **Echo Reply**.
- (Opțional) Verifici TTL — de ce hop-urile apar în `traceroute`.

---

## Bloc G (3 min) — Recap + livrabile + preview S06

### Recap (revenire la hook)

> *▸ „La început ați votat dacă `.70/28` și `.90/28` sunt în aceeași subrețea. Acum știți metoda: block size 16, deci `.64–.79` vs. `.80–.95` — subrețele diferite. Și ați văzut practic ce se întâmplă când routerul nu face forwarding."*

Trei idei de fixat:
1. **Subnetting IPv4:** prefix → block size → network/broadcast, fără binar.
2. **Routing:** rute pe host + forwarding pe router. Fără oricare, ping nu trece.
3. **IPv6:** /64 pe LAN e standard; dintr-un /48 ai 65 536 subrețele.

### Preview S06

> *▸ „Data viitoare intrăm în SDN: topologii mai complexe, switch-uri virtuale, analiza traficului la scară. Subrețelele, rutele, forwarding-ul — toate rămân fundația."*

### Livrabile (ce predau studenții)

1. **IPv4:** `S05_Part01C_Solutions_Template_I_Pv4_Subnetting.md` completat (toate cele 6 exerciții).
2. **IPv6:** `S05_Part02C_Solutions_Template_I_Pv6_Subnetting.md` completat (toate cele 6 exerciții).
3. **Docker lab:** un fișier `docker_routing_lab_output.txt` cu:
   - comenzile rulate (`ip a`, `ip route`, `sysctl`, `ping`, `traceroute`) + output-ul lor
   - 5–7 propoziții: de ce a fost necesar routerul, ce face ruta specifică vs default route, rolul lui `ip_forward`

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

### Docker — comenzi frecvente

| Comandă | Ce face |
|---|---|
| `docker compose up -d` | Pornește containerele în background |
| `docker compose ps` | Listează starea containerelor |
| `docker exec -it s05-h1 bash` | Intră în container |
| `ip a` / `ip route` | Interfețe / tabela de rutare (în container) |
| `sysctl net.ipv4.ip_forward` | Verifică starea forwarding (în container) |
| `ping -c 3 10.0.2.10` | Test conectivitate |
| `traceroute -n 10.0.2.10` | Traseu cu hop-uri |
| `tcpdump -i any -n icmp -w /captures/file.pcap -c 20` | Captură ICMP |
| `docker cp s05-r1:/captures/file.pcap .\file.pcap` | Copiază `.pcap` pe Windows |
| `docker compose down -v` | Oprește și curăță tot |

---

## Anexa A — Fișierele pentru `s05_dockerlab/` (copy/paste)

### A1) `Dockerfile` (imagine minimală cu unelte de rețea)

```dockerfile
FROM ubuntu:24.04

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      iproute2 iputils-ping traceroute tcpdump ca-certificates \
 && rm -rf /var/lib/apt/lists/*

CMD ["bash"]
```

### A2) `docker-compose.yml` (două subrețele + router)

```yaml
services:
  h1:
    build: .
    container_name: s05-h1
    command: ["bash", "-lc", "sleep infinity"]
    cap_add: ["NET_ADMIN"]
    networks:
      netA:
        ipv4_address: 10.0.1.10

  h2:
    build: .
    container_name: s05-h2
    command: ["bash", "-lc", "sleep infinity"]
    cap_add: ["NET_ADMIN"]
    networks:
      netB:
        ipv4_address: 10.0.2.10

  r1:
    build: .
    container_name: s05-r1
    command: ["bash", "-lc", "sleep infinity"]
    cap_add: ["NET_ADMIN"]
    sysctls:
      net.ipv4.ip_forward: "0"
    volumes:
      - ./captures:/captures
    networks:
      netA:
        ipv4_address: 10.0.1.2
      netB:
        ipv4_address: 10.0.2.2

networks:
  netA:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.1.0/24
  netB:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.2.0/24
```

### A3) Reset rapid (dacă s-au încurcat rutele)

```powershell
docker compose down -v
docker compose up -d --build
```

---

## Plan de contingență

| # | Problemă | Soluție |
|---|---|---|
| 1 | Build-ul durează prea mult | Faci build-ul înainte de oră. În clasă doar `docker compose up -d`. |
| 2 | `traceroute` lipsește (rar) | Folosește `tracepath` (adaugă-l în Dockerfile) sau rămâi la `ping` + `tcpdump`. |
| 3 | Ping nu merge deși forwarding = 1 | Verifică: rutele specifice există pe ambele hosturi (`ip route`), IP-urile sunt corecte (`ip a`). |
| 4 | Wireshark nu deschide fișierul `.pcap` | Verifică: fișierul copiat pe Windows are dimensiune > 0. Dacă e gol, captură nu a prins pachete — relansează ping în paralel. |
| 5 | Docker Desktop nu pornește / eroare WSL2 | Deschide Docker Desktop manual, verifică Settings → General → „Use the WSL 2 based engine". Restart dacă e necesar. |
| 6 | Containerele nu primesc IP-uri corecte | `docker compose down -v` (șterge rețelele) apoi `docker compose up -d` (le recreează). |
| 7 | Timpul se comprimă sub 30 min | Sacrifică Bloc D (VLSM → 1 min), Bloc E (IPv6 → 2 min), tcpdump/Wireshark (sari). Asigură hook + B + F. |

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

---

## Note pedagogice

**Tipar socratic principal (POE):** Forwarding OFF → ping fail → forwarding ON → ping works. Vizează concepția greșită: „dacă un host are două interfețe, e automat router".

**Tipar socratic secundar (capcană):** Hook-ul cu `.70/28` vs `.90/28` — voturi incorecte → rezolvare cu block size → reluare la recap. Vizează concepția greșită: „primii 3 octeți identici = aceeași subrețea".

**Element pedagogic specific Docker:** ruta specifică vs default route. Docker adaugă automat un default route. Prin adăugarea unei rute specifice, studenții observă regula „longest prefix match / most specific wins" — un concept pe care îl vor reîntâlni la S06 (SDN) și la S07 (routing protocols).

**Progresia cognitivă:** amintire (definiții) → înțelegere (block size) → aplicare (exercise ghidat) → analiză (de ce forwarding contează, rută specifică vs default) → evaluare (interpretare captură Wireshark). Crearea rămâne la temă (completare template-uri).

**Epifanii marcate:**
- 💡 Bloc B: „/28 = blocuri de 16, fără binar"
- 💡 Bloc E: „IPv6 subnetting = ordine, nu economie"
- 💡 Bloc F Pas 5: „un singur bit decide: host sau router"

**Timing-ul cel mai riscant:** Bloc F. Dacă Docker nu pornește sau build-ul nu a fost făcut dinainte, se pierd 3-5 min. Soluția: build obligatoriu înainte de oră + procedura de reset din Anexa A3.

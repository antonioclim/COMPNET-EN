# Seminar S06 — Routare statică și politici match–action (Windows + Docker + Wireshark)

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (arhiva: `claudev11_EN_compnet-2025-redo-main.zip`) |
| **Infra** | **Windows nativ** + Docker Desktop + Wireshark + PowerShell. Fără Mininet / OVS / Os‑Ken. |
| **Durată țintă** | 35–40 min (demo ghidat + ancorare conceptuală). Exercițiile complete rămân ca lucru individual, cu livrabile. |
| **Ideea‑cheie** | **Clasic:** fiecare router decide local pe baza *routing table*. **SDN (Software‑Defined Networking):** decizia e centrală și se materializează ca reguli match–action. Aici reproducem ideea SDN prin `iptables` într‑un nod central — analog funcțional, nu OpenFlow real. |

> **Delimitare explicită:** Această variantă înlocuiește Mininet + OVS + Os‑Ken cu containere Docker și `iptables`. Studenții experimentează aceleași concepte (decizie distribuită vs centralizată, match–action, permit/drop), dar **nu** folosesc OpenFlow propriu‑zis. Pentru OpenFlow și controller real, există varianta MININET‑SDN.

---

## Obiective operaționale

La finalul S06 (și după finalizarea temelor), studenții ar trebui să poată:

1. Porni o topologie de containere multi‑homed (routere + hosturi) și explica de ce **IP forwarding** (`net.ipv4.ip_forward=1`) este condiție necesară pentru routare.
2. Interpreta și modifica rute statice cu `ip route`, validând traseul cu `traceroute`.
3. Înțelege noțiunea de **politică instalată central** ca set de reguli match–action (analog funcțional cu flow table) și observa efectul asupra traficului.
4. Genera trafic aplicație TCP și UDP (scripturile S06) și corela reușita/eșecul cu regulile active.
5. Produce „proof‑of‑work": `ip route`, `iptables -L -v -n`, capturi `.pcap`, rulări client/server.

---

## Structura seminarului

| Interval | Bloc | Ce construiești |
|---:|---|---|
| 0:00–0:03 | **A** | Hook + activare S05: „cine decide drumul? cine impune politica?" |
| 0:03–0:16 | **B** | Triangle routing în Docker: `ping` + `traceroute`, comutare rută, traseu schimbat |
| 0:16–0:19 | **C** | Tranziție: routing distribuit vs politică centralizată (match–action) |
| 0:19–0:35 | **D** | Politici match–action cu `iptables` în nod central + trafic TCP/UDP + captură `.pcap` |
| 0:35–0:40 | **E** | Recap (revenire la hook) + livrabile + cleanup |

---

## Fișierele din kit folosite (S06)

> Directorul de lucru: `04_SEMINARS/S06/`

### Din kit (existente în arhivă)
- `1_routing/S06_Part01A_Explanation_Routing_Triangle.md` — schema de adresare, concepte (referință)
- `3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py` — echo server TCP
- `3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py` — echo client TCP
- `3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py` — echo server UDP
- `3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py` — echo client UDP
- `3_sdn-app-traffic/S06_Part03A_Explanation_SDN_App_Traffic.md` — concepte, porturi, obiective
- `3_sdn-app-traffic/S06_Part03B_Tasks_SDN_App_Traffic.md` — exerciții (adaptate la Docker)

> **Scripturile Mininet** (`S06_Part01B`, `S06_Part02B`, `S06_Part02C`) nu se folosesc direct în această variantă. Topologia se reproduce cu Docker compose, iar „controllerul" este simulat cu `iptables`.

### Create de instructor (NU fac parte din kit)
- `Dockerfile.s06` — imagine Docker cu Python + unelte de rețea
- `docker-compose.s06-triangle.yml` — topologie triangle (r1–r2–r3 + h1/h3)
- `docker-compose.s06-policy.yml` — topologie policy (h1–h2–h3 + gw central)

---

## Pregătirea instructorului (de făcut înainte de oră)

### Precondiții studenți (trimise cu 24–48h înainte)
- Docker Desktop instalat și funcțional pe Windows.
- Wireshark instalat pe Windows (Npcap inclus).
- Kit‑ul extras local (cel puțin `04_SEMINARS/S06/`).

### Imagine Docker (o singură dată)

În `04_SEMINARS\S06\` creezi `Dockerfile.s06`:

```dockerfile
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    iproute2 iputils-ping traceroute tcpdump iptables procps netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work
CMD ["bash", "-lc", "sleep infinity"]
```

Construiești imaginea:
```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S06
docker build -t compnet-s06lab:1.0 -f Dockerfile.s06 .
```

Verificare:
```powershell
docker run --rm compnet-s06lab:1.0 python --version
# Python 3.12.x
```

> Notă: în această imagine, `python` (fără `3`) indică Python 3.12. Comenzile din outline folosesc `python` (nu `python3`) pentru consistență cu imaginea Docker.

---

## Bloc A (0:00–0:03) — Hook: „Cine decide? Cine impune?"

### Ce spui

> *▸ „La S05 am configurat rute manual într‑o topologie simplă. Astăzi complicăm. Două întrebări:"*
>
> *▸ „(1) Avem 3 routere în triunghi, deci două căi posibile. Dacă schimb o singură rută pe un singur router, se schimbă traseul complet de la h1 la h3?"*

Pauză — votați cu mâna: DA / NU / nu știu.

> *▸ „(2) Dacă un nod central ar controla ce trafic trece și ce nu, cum ar vedea un observator diferența între TCP permis și UDP permis?"*

> *▸ „Rețineți predicțiile. Revenim la final."*

---

## Bloc B (0:03–0:16) — Triangle routing în Docker

### B0. Topologia (conceptual — de proiectat)

Reproducem topologia din S06 Stage 1, adaptată la Docker:

```
h1 (10.0.1.3)
 |
r1 ——— r2
 \     /
  \   /
   r3
    |
h3 (10.0.3.3)
```

> Notă tehnică (spusă scurt): în Docker bridge, o adresă din fiecare subnet este rezervată gateway‑ului bridge‑ului. De aceea folosim subnete /29 și alocări `.2`/`.3` pentru noduri. Didactic nu schimbă ideea: rute statice + forwarding.

### B1. Docker compose pentru triangle

În `04_SEMINARS/S06/` creezi `docker-compose.s06-triangle.yml`:

```yaml
services:
  h1:
    image: compnet-s06lab:1.0
    container_name: s06-h1
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    networks:
      n_h1_r1:
        ipv4_address: 10.0.1.3
    volumes:
      - ./:/work
    command: [ "bash", "-lc", "ip route del default || true; ip route add default via 10.0.1.2; sleep infinity" ]

  h3:
    image: compnet-s06lab:1.0
    container_name: s06-h3
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    networks:
      n_r3_h3:
        ipv4_address: 10.0.3.3
    volumes:
      - ./:/work
    command: [ "bash", "-lc", "ip route del default || true; ip route add default via 10.0.3.2; sleep infinity" ]

  r1:
    image: compnet-s06lab:1.0
    container_name: s06-r1
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    sysctls:
      net.ipv4.ip_forward: "1"
    networks:
      n_h1_r1:
        ipv4_address: 10.0.1.2
      n_r1_r2:
        ipv4_address: 10.0.12.2
      n_r1_r3:
        ipv4_address: 10.0.13.2
    command: [ "bash", "-lc",
      "ip route add 10.0.3.0/29 via 10.0.13.3 || true; sleep infinity"
    ]

  r2:
    image: compnet-s06lab:1.0
    container_name: s06-r2
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    sysctls:
      net.ipv4.ip_forward: "1"
    networks:
      n_r1_r2:
        ipv4_address: 10.0.12.3
      n_r2_r3:
        ipv4_address: 10.0.23.2
    command: [ "bash", "-lc",
      "ip route add 10.0.3.0/29 via 10.0.23.3 || true; ip route add 10.0.1.0/29 via 10.0.12.2 || true; sleep infinity"
    ]

  r3:
    image: compnet-s06lab:1.0
    container_name: s06-r3
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    sysctls:
      net.ipv4.ip_forward: "1"
    networks:
      n_r2_r3:
        ipv4_address: 10.0.23.3
      n_r1_r3:
        ipv4_address: 10.0.13.3
      n_r3_h3:
        ipv4_address: 10.0.3.2
    command: [ "bash", "-lc",
      "ip route add 10.0.1.0/29 via 10.0.13.2 || true; sleep infinity"
    ]

networks:
  n_h1_r1:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.1.0/29 } ]
  n_r1_r2:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.12.0/29 } ]
  n_r2_r3:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.23.0/29 } ]
  n_r1_r3:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.13.0/29 } ]
  n_r3_h3:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.3.0/29 } ]
```

### B2. Pornirea topologiei (1 min)

**PowerShell:**
```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S06
docker compose -f docker-compose.s06-triangle.yml up -d
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### B3. Verificare conectivitate inițială (3 min)

**POE 1 — Predicție:** > *▸ „Câte hop‑uri va arăta `traceroute` de la h1 la h3?"*

```powershell
docker exec -it s06-h1 ping -c 2 10.0.3.3
docker exec -it s06-h1 traceroute -n 10.0.3.3
```

**Epifanie 1:**
> *▸ „r1 are rută directă către r3. Traceroute arată: r1 → r3 → h3, deci 2–3 hop‑uri (r1 + r3, eventual cu gateway‑ul bridge Docker). Ruta e determinată de ce scrie în tabelul lui r1."*

### B4. Comutarea rutei: forțăm drumul prin r2 (5–6 min)

```powershell
# Ștergem ruta directă din r1 și punem ruta via r2
docker exec -it s06-r1 ip route del 10.0.3.0/29
docker exec -it s06-r1 ip route add 10.0.3.0/29 via 10.0.12.3

# Validăm
docker exec -it s06-h1 traceroute -n 10.0.3.3
docker exec -it s06-h1 ping -c 2 10.0.3.3
```

> *▸ „r2 are deja ruta către h3 (configurată în compose). Dacă nu ar avea‑o, pachetul s‑ar opri la r2."*

**Epifanie 2:**
> *▸ „Schimbarea e locală (în r1), dar efectul e global pentru fluxul h1→h3. Cine a votat DA la hook avea dreptate. Routerele nu ghicesc — urmează tabelele."*

### B5. (Opțional, dacă ai 2 min) Tabelele complete

```powershell
docker exec -it s06-r1 ip route
docker exec -it s06-r2 ip route
docker exec -it s06-r3 ip route
```

> *▸ „Fiecare router vede doar fragmentul lui. Niciun router nu are imaginea completă a topologiei."*

---

## Bloc C (0:16–0:19) — Tranziție: de la routing distribuit la politică centralizată

> *▸ „Până acum, controlul este distribuit: fiecare router are propriul tabel. Dacă am avea 50 de routere, ar trebui să configurez rute în fiecare."*
>
> *▸ „SDN propune altceva: separăm **cine decide** (controller) de **cine execută** (switch). Switch‑ul nu ia decizii — execută reguli match–action din flow table, instalate de controller prin OpenFlow."*
>
> *▸ „Fără mediul Mininet/OVS, putem totuși reproduce ideea de match–action: un nod central (gateway) care rutează tot traficul și aplică politică prin `iptables`. Ce ne interesează didactic este: **politica este explicită și verificabilă** — o vezi cu `iptables -L`, cu counters, cu pcap."*

**POE 2 (pregătire):** > *▸ „Predicție: dacă nodul central are o regulă care blochează traficul de la h1 către h3, și adaug o excepție doar pentru UDP, ce se va întâmpla cu un client TCP vs un client UDP?"*

---

## Bloc D (0:19–0:35) — Politici match–action cu `iptables` + trafic TCP/UDP

### D0. Topologie „stea" cu gateway central

Noua topologie: h1, h2, h3 conectate la un gateway central (`gw`), care impune politica.

```
h1 (10.0.11.10) ---\
h2 (10.0.12.10) ----+--- gw (10.0.11/12/13.254) [iptables policy]
h3 (10.0.13.10) ---/
```

#### Docker compose: `docker-compose.s06-policy.yml`

```yaml
services:
  h1:
    image: compnet-s06lab:1.0
    container_name: s06p-h1
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    networks:
      n_h1_gw:
        ipv4_address: 10.0.11.10
    volumes:
      - ./:/work
    command: [ "bash", "-lc", "ip route del default || true; ip route add default via 10.0.11.254; sleep infinity" ]

  h2:
    image: compnet-s06lab:1.0
    container_name: s06p-h2
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    networks:
      n_h2_gw:
        ipv4_address: 10.0.12.10
    volumes:
      - ./:/work
    command: [ "bash", "-lc", "ip route del default || true; ip route add default via 10.0.12.254; sleep infinity" ]

  h3:
    image: compnet-s06lab:1.0
    container_name: s06p-h3
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    networks:
      n_h3_gw:
        ipv4_address: 10.0.13.10
    volumes:
      - ./:/work
    command: [ "bash", "-lc", "ip route del default || true; ip route add default via 10.0.13.254; sleep infinity" ]

  gw:
    image: compnet-s06lab:1.0
    container_name: s06p-gw
    cap_add: [ "NET_ADMIN", "NET_RAW" ]
    sysctls:
      net.ipv4.ip_forward: "1"
    networks:
      n_h1_gw:
        ipv4_address: 10.0.11.254
      n_h2_gw:
        ipv4_address: 10.0.12.254
      n_h3_gw:
        ipv4_address: 10.0.13.254
    volumes:
      - ./:/work
    command: [ "bash", "-lc",
      "iptables -P FORWARD DROP; \
       iptables -F FORWARD; \
       iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT; \
       iptables -A FORWARD -s 10.0.11.0/24 -d 10.0.12.0/24 -j ACCEPT; \
       iptables -A FORWARD -s 10.0.12.0/24 -d 10.0.11.0/24 -j ACCEPT; \
       iptables -A FORWARD -s 10.0.11.0/24 -d 10.0.13.0/24 -j DROP; \
       sleep infinity"
    ]

networks:
  n_h1_gw:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.11.0/24 } ]
  n_h2_gw:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.12.0/24 } ]
  n_h3_gw:
    driver: bridge
    ipam:
      config: [ { subnet: 10.0.13.0/24 } ]
```

### D1. Pornire topologie (1 min)

```powershell
docker compose -f docker-compose.s06-policy.yml up -d
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### D2. Test: permis vs blocat + „unde se vede politica" (4 min)

```powershell
docker exec -it s06p-h1 ping -c 2 10.0.12.10   # h1→h2: ar trebui să meargă
docker exec -it s06p-h1 ping -c 2 10.0.13.10   # h1→h3: ar trebui să NU meargă
```

> *▸ „Vedem efectul. Dar unde e **decizia**?"*

```powershell
docker exec -it s06p-gw iptables -L FORWARD -v -n --line-numbers
```

> *▸ „`iptables` joacă rol de tabel match–action: reguli ordonate, cu match (src/dst/protocol/port) și action (ACCEPT/DROP). Counters‑urile indică câte pachete au „nimerit" regula. Este echivalentul funcțional al flow table din SDN."*

| Ce cauți | Match | Target | Analog SDN |
|---|---|---|---|
| Regula conntrack | stare ESTABLISHED,RELATED | ACCEPT | — (implicit în OF) |
| Regula h1↔h2 | src=10.0.11.0/24, dst=10.0.12.0/24 | ACCEPT | flow: permit, OUTPUT:port |
| Regula h1→h3 | src=10.0.11.0/24, dst=10.0.13.0/24 | DROP | flow: drop (acțiuni goale) |
| Policy implicită | FORWARD | DROP | table-miss |

### D3. Captură `.pcap` + Wireshark (3 min)

> Dacă nu ai Wireshark la toți studenții: faci demo pe un ecran, analiza individuală devine temă.

**Tab PowerShell separat — captură pe gw:**
```powershell
docker exec -it s06p-gw tcpdump -i any -nn -w /work/s06_policy_demo.pcap "(host 10.0.12.10 or host 10.0.13.10)" &
```

**În alt tab — generezi trafic:**
```powershell
docker exec -it s06p-h1 ping -c 2 10.0.12.10
docker exec -it s06p-h1 ping -c 2 10.0.13.10
```

Oprești `tcpdump` cu Ctrl+C.

**În Wireshark (Windows):** File → Open → `s06_policy_demo.pcap`. Filtru: `icmp && (ip.addr == 10.0.12.10 || ip.addr == 10.0.13.10)`.

> *▸ „Veți vedea: ICMP echo request + reply pentru h2, dar pentru h3 — doar request‑uri fără reply (sau nimic, dacă drop‑ul se aplică înainte de captură). Captura confirmă empiric ce politica impune."*

### D4. Trafic aplicație: TCP permis vs blocat (4 min)

Acum trecem de la ICMP la trafic de nivel aplicație — scripturile din kit.

**🔵 Tab 1 — server TCP pe h2:**
```powershell
docker exec -it s06p-h2 python /work/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000
```

**🟢 Tab 2 — client TCP din h1 către h2 (permis):**
```powershell
docker exec -it s06p-h1 bash -lc 'printf "hello\nexit\n" | python /work/3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.12.10 5000'
```

**🟢 Tab 2 — client TCP din h1 către h3 (blocat):**
```powershell
docker exec -it s06p-h1 bash -lc 'printf "x\nexit\n" | python /work/3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.13.10 5000'
```

> *▸ „Nu e doar ICMP. E o conexiune TCP: SYN, SYN‑ACK, ACK (RFC 793). Conexiunea fie se stabilește, fie nu, în funcție de politica din nodul central."*

**Capcana de concepție greșită:** > *▸ „Predicție: eșecul TCP către h3 — e din cauza lipsei serverului pe h3 sau a politicii din gw?"*
>
> *▸ „Răspuns: politica. SYN‑ul nici nu ajunge la h3 — e distrus de gw. Chiar dacă am avea server pe h3, conexiunea tot ar eșua."*

### D5. Modificare politică: UDP permis, TCP blocat către h3 (5–6 min)

Scop: aceeași destinație, tratament diferit pe protocol — exact ideea din Stage 3 al kit‑ului.

**🔵 Tab 1 — server UDP pe h3:**
```powershell
docker exec -it s06p-h3 python /work/3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py 6000
```

**🟢 Tab 2 — modifici politica în gw:**
```powershell
# Vizualizezi regulile cu numerele de linie
docker exec -it s06p-gw iptables -L FORWARD -n --line-numbers

# Ștergi regula generică de DROP h1→h3 (verifici numărul de linie — presupunem linia 4)
docker exec -it s06p-gw iptables -D FORWARD 4

# Adaugi: permit UDP către h3:6000, blochează TCP către h3
docker exec -it s06p-gw iptables -I FORWARD 3 -s 10.0.11.0/24 -d 10.0.13.0/24 -p udp --dport 6000 -j ACCEPT
docker exec -it s06p-gw iptables -I FORWARD 4 -s 10.0.11.0/24 -d 10.0.13.0/24 -p tcp -j DROP

# Verifici regulile + counters
docker exec -it s06p-gw iptables -L FORWARD -v -n --line-numbers
```

**🟢 Tab 2 — test UDP (permis):**
```powershell
docker exec -it s06p-h1 bash -lc 'printf "udp1\nexit\n" | python /work/3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py 10.0.13.10 6000'
```

**🟢 Tab 2 — retest TCP (blocat):**
```powershell
docker exec -it s06p-h1 bash -lc 'printf "tcp\nexit\n" | python /work/3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.13.10 5000'
```

**Epifanie 3:**
> *▸ „Aceeași pereche de hosturi, protocoale diferite, tratament diferit. În `iptables` e `-p udp` vs `-p tcp`. În SDN real, ar fi `match ip_proto=17` (UDP, RFC 768) vs `ip_proto=6` (TCP, RFC 793) — reguli separate în flow table. Principiul e identic: match pe câmpuri din header → acțiune."*

---

## Bloc E (0:35–0:40) — Recap + livrabile + cleanup

### Recap — revenire la hook

> *▸ „La început am întrebat: schimbi o rută, se schimbă traseul? Da — am demonstrat cu traceroute."*
>
> *▸ „Am întrebat și: ce diferență vede un observator între TCP permis și UDP permis? Diferența e în regula din tabelul match–action: un câmp (protocolul) și o acțiune (ACCEPT vs DROP). Counters‑urile confirmă."*

Trei idei de fixat:
1. Routarea statică se vede în `ip route`; traseul se validează cu `traceroute`.
2. Un punct central de politică impune reguli match–action; regula este explicită și verificabilă (dump + counters).
3. Traficul aplicație (TCP/UDP) este testul relevant: handshake vs datagramă, nivel de transport vs nivel de rețea. Wireshark (captura `.pcap`) confirmă empiric.

### Livrabile (adaptate la Docker)

1. **Triangle routing:** `triangle_routing_output.txt` — `ip route` pentru r1/r2/r3 + `traceroute` înainte/după comutare + paragraf explicativ (6–8 propoziții).
2. **Politici match–action:** `sdn_lab_output.txt` — ping permis/blocat, `iptables -L -v -n` înainte și după modificare, rulări TCP/UDP client/server, explicație politicii (8–10 propoziții).
3. **Captură** (recomandat): `s06_policy_demo.pcap` — analiză scurtă în Wireshark.

### Conexiune cu seminarele adiacente
> *▸ „De la S05 am preluat `ip route`, `traceroute`, configurarea manuală. La S07 vom construi un filtru de pachete — ceea ce azi am văzut prin counters `iptables` și pcap, acolo o vedem la nivel de octeți, cu Python."*

### Cleanup (20 secunde)
```powershell
docker compose -f docker-compose.s06-triangle.yml down
docker compose -f docker-compose.s06-policy.yml down
```

---

## Cheat‑sheet

### Triangle routing (Docker)
| Ce vrei | Comanda |
|---|---|
| Pornire | `docker compose -f docker-compose.s06-triangle.yml up -d` |
| Status containere | `docker ps --format "table {{.Names}}\t{{.Status}}"` |
| Ping h1→h3 | `docker exec -it s06-h1 ping -c 2 10.0.3.3` |
| Traceroute | `docker exec -it s06-h1 traceroute -n 10.0.3.3` |
| Tabel rutare r1 | `docker exec -it s06-r1 ip route` |
| Adăugare rută | `docker exec -it s06-r1 ip route add 10.0.3.0/29 via 10.0.12.3` |
| Ștergere rută | `docker exec -it s06-r1 ip route del 10.0.3.0/29` |
| Oprire | `docker compose -f docker-compose.s06-triangle.yml down` |

### Politici match–action (Docker)
| Ce vrei | Comanda |
|---|---|
| Pornire | `docker compose -f docker-compose.s06-policy.yml up -d` |
| Ping h1→h2 | `docker exec -it s06p-h1 ping -c 2 10.0.12.10` |
| Ping h1→h3 | `docker exec -it s06p-h1 ping -c 2 10.0.13.10` |
| Regulile iptables | `docker exec -it s06p-gw iptables -L FORWARD -v -n --line-numbers` |
| Ștergere regulă (linia N) | `docker exec -it s06p-gw iptables -D FORWARD N` |
| Permit UDP h1→h3:6000 | `docker exec -it s06p-gw iptables -I FORWARD 3 -s 10.0.11.0/24 -d 10.0.13.0/24 -p udp --dport 6000 -j ACCEPT` |
| Block TCP h1→h3 | `docker exec -it s06p-gw iptables -I FORWARD 4 -s 10.0.11.0/24 -d 10.0.13.0/24 -p tcp -j DROP` |
| Captură pcap | `docker exec -it s06p-gw tcpdump -i any -nn -w /work/capture.pcap -c 50` |
| Server TCP h2 | `docker exec -it s06p-h2 python /work/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000` |
| Client TCP h1→h2 | `docker exec -it s06p-h1 bash -lc 'printf "msg\nexit\n" \| python /work/3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.12.10 5000'` |
| Server UDP h3 | `docker exec -it s06p-h3 python /work/3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py 6000` |
| Client UDP h1→h3 | `docker exec -it s06p-h1 bash -lc 'printf "msg\nexit\n" \| python /work/3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py 10.0.13.10 6000'` |
| Oprire | `docker compose -f docker-compose.s06-policy.yml down` |

---

## Plan de contingență

| # | Problemă | Soluție |
|---|---|---|
| 1 | Un student nu poate rula containere cu `cap_add` (NET_ADMIN) | Lucrează în pereche. Sau: instructorul face demo central, studentul notează și reproduce ulterior. |
| 2 | `traceroute` lipsește sau se comportă ciudat | Folosești `tracepath` (dacă există) sau `ip route get <IP>` pe fiecare router. |
| 3 | Client UDP rămâne blocat așteptând reply | Oprești cu Ctrl+C; revii după ce ai permis UDP în politica gw. Dacă persistă: verifici regulile cu `iptables -L -v -n`. |
| 4 | Wireshark nu e instalat la toți | Deschizi pcap‑ul pe un singur ecran; discuți în plen. Analiza individuală devine temă. |
| 5 | Docker Desktop nu pornește sau e instabil | Restart Docker Desktop; dacă continuă: studentul folosește Docker pe WSL2 nativ (dacă are) sau urmărește demo‑ul. |
| 6 | Eroare la ștergerea regulii iptables (număr greșit de linie) | Relistezi cu `--line-numbers`. Dacă s‑a stricat totul: `docker compose -f docker-compose.s06-policy.yml down && up -d` repornește cu regulile inițiale. |
| 7 | Eroare „Address already in use" la server TCP/UDP | `docker exec -it s06p-h2 ss -tlnp` → identifici procesul → `kill <PID>` sau repornești containerul. |

---

## Referințe (APA 7th ed.)

| Referință | DOI |
|---|---|
| Baker, F. (1995). *Requirements for IP Version 4 Routers* (RFC 1812). RFC Editor. | https://doi.org/10.17487/RFC1812 |
| Kreutz, D., Ramos, F. M. V., Veríssimo, P., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-Defined Networking: A Comprehensive Survey. *Proceedings of the IEEE, 103*(1), 14–76. | https://doi.org/10.1109/JPROC.2014.2371999 |
| Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: Rapid prototyping for software-defined networks. *Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks*. | https://doi.org/10.1145/1868447.1868466 |
| McKeown, N., Anderson, T., Balakrishnan, H., Parulkar, G., Peterson, L., Rexford, J., Shenker, S., & Turner, J. (2008). OpenFlow: Enabling innovation in campus networks. *ACM SIGCOMM Computer Communication Review, 38*(2), 69–74. | https://doi.org/10.1145/1355734.1355746 |
| Postel, J. (1981). *Internet Protocol* (RFC 791). RFC Editor. | https://doi.org/10.17487/RFC0791 |
| Postel, J. (1981). *Internet Control Message Protocol* (RFC 792). RFC Editor. | https://doi.org/10.17487/RFC0792 |
| Postel, J. (1980). *User Datagram Protocol* (RFC 768). RFC Editor. | https://doi.org/10.17487/RFC0768 |
| Postel, J. (1981). *Transmission Control Protocol* (RFC 793). RFC Editor. | https://doi.org/10.17487/RFC0793 |

---

## Note pedagogice

### Ce se pierde și ce se câștigă față de varianta MININET‑SDN

| Aspect | MININET‑SDN | Docker + iptables |
|---|---|---|
| Protocolul OpenFlow | real (OF 1.3) | absent — analog funcțional |
| Controller extern | Os‑Ken (Python) | absent — regulile sunt statice în `gw` |
| Flow table reală | `ovs-ofctl dump-flows` | `iptables -L -v -n --line-numbers` |
| Match–action | pe câmpuri OF (eth_type, ip_proto, ipv4_src/dst) | pe câmpuri iptables (-s, -d, -p, --dport) |
| Counters pachete | da (OVS) | da (iptables) |
| Separation control/data plane | reală | simulată (gw e și „controller" și „switch") |
| Accesibilitate setup | necesită VM cu Mininet | Windows nativ, orice Docker |

> Concluzia didactică: ambele variante livrează obiectivele 1–5. Varianta Docker nu livrează *experiența* OpenFlow (packet_in, flow_mod), dar livrează *principiul* match–action, care este transferabil.

### Misconcepții anticipate

| Concepția greșită | Unde se adresează | Tipar socratic |
|---|---|---|
| „Routerul alege automat cel mai scurt drum" | Bloc B4 (comutare manuală) | POE 1 |
| „Dacă ping merge, TCP merge sigur" | Bloc D4 (TCP blocat, ping OK anterior) | Capcana la D4 |
| „iptables = firewall, nu match–action" | Bloc D2 (tabla comparativă SDN) | Explicație directă |

### Plan de sacrificare (dacă ai doar 30 min)

| Prioritate | Ce scoți | Ce păstrezi |
|---|---|---|
| Prima tăietură | D3 (captură pcap / Wireshark) — devine temă | Blocuri A–D2, D4–D5, E |
| A doua tăietură | D5 (modificare politică UDP) — devine temă | Blocuri A–D4, E |
| A treia tăietură | B5 (tabelele complete) + D4 reducere la demo rapid | A–B4, C–D2, E (25 min) |

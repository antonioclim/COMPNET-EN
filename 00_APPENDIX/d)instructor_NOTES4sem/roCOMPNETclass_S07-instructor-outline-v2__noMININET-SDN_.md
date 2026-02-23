# Seminar S07 — Capturare pachete, filtrare și port scanning

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (v11, `04_SEMINARS/S07/`) |
| **Infra** | Windows nativ + Docker Desktop (WSL2 backend) + Wireshark |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un RAW socket vede toate pachetele de pe interfață; din tiparele repetitive ale header-elor poți deduce automat dacă cineva scanează. |

---

## De ce funcționează fără Mininet

Elementul critic al S07 este accesul la `AF_PACKET` / RAW sockets — funcționalitate strict Linux. Containerele Docker pe Windows (prin WSL2) oferă un kernel Linux complet. Topologia de laborator devine: două containere într-un bridge network Docker (`attacker` ↔ `victim`), cu IP-uri statice. Capabilitățile `NET_RAW` și `NET_ADMIN` (acordate prin `cap_add` în Docker Compose) permit deschiderea de RAW sockets fără `sudo` suplimentar.

---

## Obiective operaționale

La finalul seminarului, studentul:

1. explică de ce sniffing-ul cu `AF_PACKET` necesită Linux + privilegii (capabilități), chiar dacă lucrează pe Windows;
2. completează `parse_ipv4_header` și interpretează câmpurile `version`, `IHL`, `proto`, `src`, `dst` în pachete capturate;
3. implementează o regulă de filtrare în Python (protocol + port) și explică de ce filtrarea după port poate fi înșelătoare;
4. rulează un connect scan (`port_scanner.py`) pe un container „victim" și interpretează stările `OPEN`, `CLOSED`, `FILTERED`;
5. declanșează și observă o alertă `[ALERT]` într-un detector de scanare bazat pe fereastră temporală + prag;
6. deschide o captură `.pcap` din container în Wireshark (pe Windows) și corelează vizual semnătura scanării;
7. produce fișierele de output cerute ca dovadă de parcurgere.

---

## Structura seminarului

| Interval | Bloc | Scop | Durată |
|---:|---|---|---:|
| 0:00–0:04 | A — Hook + cadru etic | Scenariu concret, predicție, regulă etică | 4 min |
| 0:04–0:13 | B — RAW sniffing (Stage 2) | Completare `parse_ipv4_header`, demo sniffer, ICMP + TCP | 9 min |
| 0:13–0:19 | C — Packet filter (Stage 3) | `passes_filter`, filtrare TCP:5000, ephemeral ports | 6 min |
| 0:19–0:27 | D — Port scanner (Stage 4) | Connect scan, interpretare OPEN/CLOSED/FILTERED | 8 min |
| 0:27–0:34 | E — Detect scan (Stage 5) | Detector pe victim, alertă, sensibilitate vs. alarme false | 7 min |
| 0:34–0:40 | F — Wireshark pcap + mini-IDS + recap + livrabile | Captură pcap, corelație vizuală, revenire la hook, livrabile | 6 min |

> **Regulă de sacrificare:** dacă timpul se comprimă, se păstrează B + D + E. Blocul C devine temă ghidată; din F se păstrează recap-ul (2 min) și lista de livrabile. Epifania Wireshark poate fi mutată ca temă (studenții fac singuri).

---

## Pregătirea instructorului (înainte de oră)

### Precondiții pentru studenți (trimise cu 24–48h înainte)

- Docker Desktop instalat și funcțional (WSL2 backend).
- Wireshark instalat pe Windows (Npcap inclus).
- Kit-ul extras local (minim `04_SEMINARS/S06/` și `04_SEMINARS/S07/`).

### Construire imagine Docker (o singură dată, înainte de seminar)

În folderul `04_SEMINARS\S07\`, creezi `Dockerfile.s07`:

```dockerfile
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    iproute2 iputils-ping tcpdump netcat-openbsd procps nano iptables \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work
CMD ["bash", "-lc", "sleep infinity"]
```

Construiești imaginea (necesită internet — de făcut **înainte** de oră):

```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S07
docker build -t compnet-s07lab:1.0 -f Dockerfile.s07 .
```

### Topologie Docker (2 containere)

Creezi folderul pentru capturi și fișierul Docker Compose. **Atenție la volume:** montăm directorul părinte (`04_SEMINARS/`) pentru a avea acces atât la S07 cât și la scriptul TCP server din S06.

`docker-compose.s07.yml`:

```yaml
services:
  attacker:
    image: compnet-s07lab:1.0
    container_name: s07-attacker
    cap_add: ["NET_RAW", "NET_ADMIN"]
    volumes:
      - ../:/seminars
    working_dir: /seminars/S07
    networks:
      s07net:
        ipv4_address: 172.30.7.10

  victim:
    image: compnet-s07lab:1.0
    container_name: s07-victim
    cap_add: ["NET_RAW", "NET_ADMIN"]
    volumes:
      - ../:/seminars
    working_dir: /seminars/S07
    networks:
      s07net:
        ipv4_address: 172.30.7.20

networks:
  s07net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.30.7.0/24
```

Creezi folderul de capturi și pornești:

```powershell
mkdir captures 2>$null
docker compose -f docker-compose.s07.yml up -d
docker ps
```

Deschizi două terminale (PowerShell sau Windows Terminal):

```powershell
# Terminal 1 — attacker
docker exec -it s07-attacker bash

# Terminal 2 — victim
docker exec -it s07-victim bash
```

Verificare rapidă din attacker:
```bash
ping -c 1 172.30.7.20
```

---

## Bloc A (0:00–0:04) — Hook + cadru etic + activare cunoștințe

### Narativ

> *▸ „Imaginați-vă: administratorul de rețea primește o alertă — un host intern a trimis SYN-uri către 200 de porturi diferite în ultimele 3 secunde. E un atac? E un serviciu prost configurat? Cum distingem? Asta facem azi: construim instrumentul care generează acea alertă."*

### Activare cunoștințe (60 sec)

> *▸ „Până acum am lucrat cu Wireshark (S01) și cu socket-uri TCP/UDP (S02–S04). Întrebare rapidă: un socket TCP obișnuit, pe care l-ați folosit la S02, vede pachetele altor conexiuni de pe aceeași mașină? [Răspuns așteptat: nu.] Exact. Azi coborâm un strat: deschidem un socket care vede tot ce trece pe interfață."*

### Predicție + conflict cognitiv (30 sec)

> *▸ „Predicție de instinct: dacă cineva scanează 100 de porturi în 5 secunde, câtă informație nouă este în acele pachete? Mult payload, sau mult header repetat?"*

Lași 5 secunde. Majoritatea vor zice „mult header". Notezi pe tablă: „100 pachete × ~60 bytes header, 0 bytes payload util".

### Nota etică (20 sec)

> *▸ „Tot ce facem azi se rulează strict în rețeaua Docker locală, pe containere pe care le controlăm. Scanarea rețelelor reale fără autorizare este ilegală."*

> *▸ „De ce containere? Deoarece AF_PACKET este o facilitate Linux. Chiar dacă lucrați pe Windows, WSL2 vă oferă un kernel Linux complet în spatele Docker Desktop. Capabilitățile NET_RAW și NET_ADMIN din docker-compose sunt echivalentul lui `sudo` pentru RAW sockets."*

Afișezi pe ecran planul pe minute și obiectivele.

---

## Bloc B (0:04–0:13) — RAW sniffing (Stage 2)

### B1) Context (30 sec)

> *▸ „Avem doi actori: containerul attacker (172.30.7.10) și containerul victim (172.30.7.20). Ne interesează ce vede victim pe interfața sa."*

### B2) Completare `parse_ipv4_header` — live coding (3 min)

> *▸ „Funcția asta citește primul byte din header-ul IPv4. De ce? Pentru că IHL (Internet Header Length) ne spune unde se termină header-ul și începe payload-ul. Fără IHL, nu știm unde e granița."*

**🟢 TERMINAL VICTIM:**
```bash
nano /seminars/S07/1_sniffing/S07_Part01B_Script_Packet_Sniffer.py
```

Cauți `# >>> STUDENT TODO` în `parse_ipv4_header`. Scrii (explicând fiecare linie):

```python
version_ihl = data[0]
version = version_ihl >> 4
ihl = (version_ihl & 0x0F) * 4

ttl, proto, src, dst = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
src_ip_str = ipv4_addr(src)
dst_ip_str = ipv4_addr(dst)
return src_ip_str, dst_ip_str, proto, ihl
```

Ștergi/comentezi `raise NotImplementedError(...)`. Salvezi.

> **Epifanie:** „`! 8x B B 2x 4s 4s` — fiecare caracter descrie un câmp din header. `8x` sare peste 8 bytes (TOS, total length, identification, flags, fragment). `B B` citește TTL și protocolul. `2x` sare checksum-ul. `4s 4s` citește cele două adrese IPv4 de câte 4 bytes."

### B3) Rulare sniffer pe victim + generare trafic (4 min)

> *▸ „Sniffer-ul nostru nu «știe» despre conexiuni. El vede pachete brute, indiferent cine le-a generat."*

**Predicție (POE):** „Dacă dau ping din attacker în victim, câte linii apar în sniffer pentru fiecare ping? Una sau două?"

(Răspuns: două — request + reply.)

**🟠 TERMINAL VICTIM (captură):**
```bash
python3 /seminars/S07/1_sniffing/S07_Part01B_Script_Packet_Sniffer.py eth0
```

**🟢 TERMINAL ATTACKER (trafic):**
```bash
ping -c 2 172.30.7.20
```

Output așteptat (în victim):
```text
[1] 172.30.7.10 -> 172.30.7.20  proto=ICMP
[2] 172.30.7.20 -> 172.30.7.10  proto=ICMP
[3] 172.30.7.10 -> 172.30.7.20  proto=ICMP
[4] 172.30.7.20 -> 172.30.7.10  proto=ICMP
```

Oprești sniffer-ul cu `Ctrl+C`. Acum generezi trafic TCP:

**🔵 TERMINAL VICTIM (server TCP):**
```bash
python3 /seminars/S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

Repornești sniffer-ul:
```bash
python3 /seminars/S07/1_sniffing/S07_Part01B_Script_Packet_Sniffer.py eth0
```

**🟢 TERMINAL ATTACKER:**
```bash
echo "hello_s07" | nc 172.30.7.20 5000
```

**Ce apare:** linii cu `proto=ICMP` (din ping-ul anterior, dacă nu s-a ajuns la MAX_PACKETS) și `proto=TCP`.

**Micro-întrebare (10 sec):** „Sniffer-ul arată `proto=TCP` dar nu arată porturile. Ce ar trebui să decodăm în plus?" (Răspuns: header-ul TCP, primii 4 bytes — porturile sursă și destinație.)

Oprești sniffer-ul cu `Ctrl+C`.

> **Notă:** Serverul TCP din S06 acceptă un singur client, apoi se oprește. Trebuie repornit înaintea fiecărui demo care necesită portul 5000 deschis.

### B4) Trimitere studenți la pagina HTML interactivă (20 sec)

> *▸ „Pentru studiu individual, aveți o pagină interactivă în `_HTMLsupport/S07/1_sniffing/S07_Part01_Page_Sniffing.html`. O deschideți local în browser, pe Windows."*

---

## Bloc C (0:13–0:19) — Packet filter (Stage 3)

### C1) Tranziție

> *▸ „Sniffer-ul vede tot — cam ca o cameră de supraveghere fără zoom. Acum adăugăm zoom: filtrul. Wireshark folosește BPF (Berkeley Packet Filter) în kernel. Noi facem un prim pas, mai simplu: filtrare în user space, în Python."*

**Observație importantă (spusă explicit):** „În `packet_filter.py`, funcția `parse_ipv4_header` este deja completă — nu mai e TODO. Singurul lucru de completat este `passes_filter`."

### C2) Implementare filtru + demo (4 min)

Regula aleasă: „afișăm doar TCP către portul 5000".

**🟠 TERMINAL VICTIM:**
```bash
nano /seminars/S07/2_packet-filter/S07_Part02A_Script_Packet_Filter.py
```

În `passes_filter(...)`:
```python
if proto == 6 and dst_port == 5000:
    return True
return False
```

Repornești serverul TCP pe victim:
```bash
python3 /seminars/S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

Rulezi filtrul:
```bash
python3 /seminars/S07/2_packet-filter/S07_Part02A_Script_Packet_Filter.py eth0
```

**🟢 TERMINAL ATTACKER:**
```bash
echo "again" | nc 172.30.7.20 5000
```

**Ce apare:** linii de forma `172.30.7.10:<port_efemer> -> 172.30.7.20:5000  proto=TCP`

> **Epifanie:** „Portul clientului nu e «aleator magic»: e un ephemeral port alocat de kernel (de obicei 32768–60999 pe Linux). În capturi, acest port identifică fiecare conexiune unică."

### C3) Întrebare de proiectare — constructivistă (1 min)

> *▸ „Ce condiție ați adăuga ca să vedeți doar traficul de la attacker (172.30.7.10)?"*

Lași studenții să propună: `if src_ip == "172.30.7.10": ...`

Apoi: „Dar dacă aș vrea să detectez «doar DNS» (UDP către port 53), de ce ar fi înșelător în practică?" (Port reuse, tunnelling DNS, servicii non-standard.)

Oprești procesele cu `Ctrl+C`.

---

## Bloc D (0:19–0:27) — Mini TCP port scanner (Stage 4)

### D1) Cadru (1 min)

> *▸ „Un scan nu «sparge» nimic. Este o operație de reconnaissance: testezi ce porturi răspund. Aceeași operație o face orice administrator de rețea când verifică suprafața expusă a unui server."*

### D2) Repornire server + scan pe fereastră îngustă (3 min)

Repornești serverul pe victim:
```bash
python3 /seminars/S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

**Predicție (POE):** „Scanez porturile 4990–5010. Câte vor fi OPEN?" (Răspuns: 1 — doar 5000.)

**🟢 TERMINAL ATTACKER:**
```bash
python3 /seminars/S07/3_port-scanning/S07_Part03A_Script_Port_Scanner.py 172.30.7.20 4990 5010
```

**Output așteptat:**
```text
[INFO] Scanning host 172.30.7.20 on ports 4990-5010 ...
PORT 4990 CLOSED
...
PORT 5000 OPEN
...
PORT 5010 CLOSED
```

### D3) Interpretare (2 min)

> *▸ „Trei stări posibile:*
> - *`OPEN` — `connect()` a reușit. Cineva ascultă.*
> - *`CLOSED` — RST imediat. Port-ul există, dar nimeni nu ascultă.*
> - *`FILTERED` — timeout. Pachetul a fost probabil aruncat de un firewall (DROP, nu REJECT)."*

**Capcană de concepție greșită:** „Mulți confundă CLOSED cu FILTERED. CLOSED e un răspuns rapid — kernel-ul trimite RST. FILTERED e absența răspunsului."

### D4) (Opțional, 1 min) Demo FILTERED cu iptables

**🔵 TERMINAL VICTIM:**
```bash
iptables -A INPUT -p tcp --dport 5001 -j DROP
```

**🟢 TERMINAL ATTACKER:**
```bash
python3 /seminars/S07/3_port-scanning/S07_Part03A_Script_Port_Scanner.py 172.30.7.20 5000 5002
```

Observi: 5000 OPEN (dacă serverul încă rulează), 5001 FILTERED, 5002 CLOSED.

Cureți regula:
```bash
iptables -D INPUT -p tcp --dport 5001 -j DROP
```

> *▸ „DROP → timeout → FILTERED. Dacă ar fi fost REJECT, vedeai RST → CLOSED."*

---

## Bloc E (0:27–0:34) — Detectarea scanării (Stage 5)

### E1) Pornire detector pe victim (1 min)

> *▸ „Detectorul nu «știe» cine e atacator. El doar numără: câte porturi distincte au primit SYN de la aceeași sursă, într-o fereastră de timp."*

**🔵 TERMINAL VICTIM:**
```bash
python3 /seminars/S07/4_scan-detector/S07_Part04A_Script_Detect_Scan.py eth0
```

### E2) Scanare suficient de densă (2 min)

**Predicție:** „Pragul implicit e 10 porturi în 5 secunde. Dacă scanez porturile 1–120, se va declanșa alerta?"

**🟢 TERMINAL ATTACKER:**
```bash
python3 /seminars/S07/3_port-scanning/S07_Part03A_Script_Port_Scanner.py 172.30.7.20 1 120
```

**Output așteptat pe victim:**
```text
[ALERT] Possible port scan from 172.30.7.10: 10 distinct ports in the last 5 seconds
```

### E3) Sensibilitate vs. alarme false (2 min)

Oprești detectorul (`Ctrl+C`). Deschizi fișierul:
```bash
nano /seminars/S07/4_scan-detector/S07_Part04A_Script_Detect_Scan.py
```

Arăți variabilele:
```python
WINDOW_SECONDS = 5       # fereastra temporală
PORT_THRESHOLD = 10      # porturi distincte care declanșează alerta
```

> *▸ „Două «butoane»: fereastra și pragul. Dacă scad ambele (2 secunde, prag 5), detectez mai rapid — dar un health-check intern care verifică 6 porturi declanșează alarma."*

**Tipar „Ce s-ar fi întâmplat dacă…?":** „Ce trafic legitim ar putea semăna cu o scanare?"

Răspunsuri așteptate: health-checks de load balancer, service discovery (mDNS, Consul), monitorizare Prometheus, micro-servicii cu retry agresiv.

---

## Bloc F (0:34–0:40) — Wireshark pcap + mini-IDS + recap + livrabile

### F1) Captură pcap din container + deschidere în Wireshark (2 min)

> *▸ „Până acum am detectat scanări din cod. Acum vedem cum arată vizual, în Wireshark."*

**🔵 TERMINAL VICTIM — pornești captură:**
```bash
tcpdump -i eth0 -nn -w /seminars/S07/captures/s07_scan.pcap &
```

**🟢 TERMINAL ATTACKER — scanare scurtă:**
```bash
python3 /seminars/S07/3_port-scanning/S07_Part03A_Script_Port_Scanner.py 172.30.7.20 1 80
```

Oprești tcpdump pe victim:
```bash
kill %tcpdump
```

**Pe Windows:** deschizi `04_SEMINARS\S07\captures\s07_scan.pcap` în Wireshark. Aplici display filter:

```text
tcp.flags.syn == 1 and tcp.flags.ack == 0
```

> **Epifanie vizuală:** „Vedeți? Zeci de SYN-uri către porturi diferite, toate de la aceeași sursă. Asta e «semnătura» unei scanări. Detectorul nostru face aceeași observație, dar automat și fără interfață grafică."

### F2) Mini-IDS — prezentare structurală (1 min)

> *▸ „Un IDS (Intrusion Detection System) real combină filtrare cu detecție de tipare. `mini_ids.py` face exact asta."*

```bash
head -45 /seminars/S07/5_mini-ids/S07_Part05A_Script_Mini_IDS.py
```

Menționezi cele trei detectoare: TCP scan, UDP spray, flood către un port.

> *▸ „Ca temă, finalizați Stage-urile, rulați `mini_ids.py` cu scenariile din fișierul de task-uri, și scrieți `explanation.md`."*

### F3) Recap — revenire la hook (1.5 min)

> *▸ „La început am văzut un scenariu: un host trimite 200 de SYN-uri în 3 secunde. Acum putem răspunde:*
>
> 1. *Un RAW socket vede toate pachetele — nu doar pe cele ale «propriei» conexiuni.*
> 2. *Header-ul IPv4 are câmpul IHL care ne spune unde începe payload-ul TCP/UDP. Fără parsarea corectă a acestui câmp, totul se decalează.*
> 3. *Detecția unei scanări se reduce la: numără porturi distincte per sursă, într-o fereastră de timp. Simplu ca idee — provocarea e calibrarea pragurilor."*

Adăugare specifică variantei Docker:

> *▸ „Și ați văzut în Wireshark exact cum arată acel tipar: SYN-uri fără ACK, unul după altul, fiecare către un port diferit."*

### F4) Livrabile (30 sec)

- `sniffer_log.txt` — minim 20 pachete + răspunsuri la întrebări de reflecție
- `filter_results.txt` — minim 20 linii filtrate + răspunsuri la întrebări de reflecție
- `S07_Part03_Output_Scan_Results.txt` — minim 50 porturi scanate + reflecții
- `scan_detection.txt` — fragment cu cel puțin un `[ALERT]` + trafic normal + sumar
- `ids_alerts.log` + `explanation.md` — pentru mini-IDS

Pagini interactive pentru studiu: `_HTMLsupport/S07/` (5 pagini, câte una per stage).

### F5) Cleanup

```powershell
docker compose -f docker-compose.s07.yml down
```

---

## Cheat-sheet

### Comenzi Docker esențiale

| Comandă | Scop |
|---|---|
| `docker compose -f docker-compose.s07.yml up -d` | Pornire topologie |
| `docker exec -it s07-attacker bash` | Conectare la attacker |
| `docker exec -it s07-victim bash` | Conectare la victim |
| `docker compose -f docker-compose.s07.yml down` | Oprire + ștergere containere |
| `docker compose -f docker-compose.s07.yml up -d --force-recreate` | Repornire curată |

### IP-uri în topologia Docker

| Container | IP | Rol |
|---|---|---|
| `s07-attacker` | 172.30.7.10 | Generează scanări, trafic |
| `s07-victim` | 172.30.7.20 | Rulează sniffer, filtru, detector |

### Fișiere din kit (S07) — căi în container

| Stage | Script | Cale în container |
|---|---|---|
| 2 — Sniffing | `S07_Part01B_Script_Packet_Sniffer.py` | `/seminars/S07/1_sniffing/` |
| 3 — Filter | `S07_Part02A_Script_Packet_Filter.py` | `/seminars/S07/2_packet-filter/` |
| 4 — Scanner | `S07_Part03A_Script_Port_Scanner.py` | `/seminars/S07/3_port-scanning/` |
| 5 — Detector | `S07_Part04A_Script_Detect_Scan.py` | `/seminars/S07/4_scan-detector/` |
| 6 — Mini-IDS | `S07_Part05A_Script_Mini_IDS.py` | `/seminars/S07/5_mini-ids/` |

### Server TCP auxiliar (din S06)

```bash
python3 /seminars/S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

Atenție: serverul acceptă un singur client, apoi se oprește. Trebuie repornit înaintea fiecărui demo care necesită port 5000 deschis.

### Numere protocol IP (RFC 791)

| Valoare | Protocol |
|---|---|
| 1 | ICMP |
| 6 | TCP |
| 17 | UDP |

### struct.unpack — formatul header-ului IPv4

```
'! 8x B B 2x 4s 4s'
 │  │  │ │  │   │
 │  │  │ │  │   └── dst IP (4 bytes)
 │  │  │ │  └────── src IP (4 bytes)
 │  │  │ └───────── skip checksum (2 bytes)
 │  │  └──────────── protocol (1 byte)
 │  └─────────────── TTL (1 byte)
 └────────────────── skip VER+IHL+TOS+TotalLen+ID+Flags+FragOff (8 bytes)
! = network byte order (big-endian)
```

### Wireshark display filters utile

| Filtru | Ce arată |
|---|---|
| `tcp.flags.syn == 1 and tcp.flags.ack == 0` | SYN inițiale (semnătura scanării) |
| `ip.src == 172.30.7.10` | Trafic de la attacker |
| `tcp.dstport == 5000` | Trafic TCP către serverul nostru |

---

## Plan de contingență

| # | Problemă | Soluție rapidă |
|---|---|---|
| 1 | RAW socket nu pornește în container | Verifici `cap_add: ["NET_RAW", "NET_ADMIN"]` în compose. Refaci: `docker compose -f docker-compose.s07.yml up -d --force-recreate`. |
| 2 | Nu vezi trafic pe `eth0` | Verifici IP-urile (`ip a`) și conectivitatea (`ping 172.30.7.20`). Dacă ping nu merge, repornești compose. |
| 3 | Portul 5000 nu apare OPEN | Serverul TCP s-a oprit (acceptă un singur client). Repornești. Alternativă: `nc -l 5000 &`. |
| 4 | `[ALERT]` nu se declanșează | Scazi `PORT_THRESHOLD=5` sau mărești plaja (1–200). Verifici că detectorul rulează pe victim și scanezi IP-ul corect. |
| 5 | Fișierul `.pcap` nu apare pe Windows | Verifici: `ls /seminars/S07/captures/`. Pe Windows, calea e `04_SEMINARS\S07\captures\`. Dacă lipsește, verifici mount-ul din compose. |
| 6 | Imaginea Docker nu se construiește | Verifici conexiunea la internet. Alternativă: `docker pull python:3.12-slim` separat, apoi rebuild. |
| 7 | Lipsă timp — nu ajungi la Bloc E | Faci Bloc D + arăți `detect_scan.py` 60 sec structural + treci la livrabile. Detecția devine temă. |

---

## Referințe (APA 7th ed.)

Denning, D. E. (1987). An intrusion-detection model. *IEEE Transactions on Software Engineering, SE-13*(2), 222–232. https://doi.org/10.1109/TSE.1987.232894

Jung, J., Paxson, V., Berger, A. W., & Balakrishnan, H. (2004). Fast portscan detection using sequential hypothesis testing. In *Proceedings of the 2004 IEEE Symposium on Security and Privacy* (pp. 211–225). IEEE. https://doi.org/10.1109/SECPRI.2004.1301325

Paxson, V. (1999). Bro: A system for detecting network intruders in real-time. *Computer Networks, 31*(23–24), 2435–2463. https://doi.org/10.1016/S1389-1286(99)00112-7

Postel, J. (1980). *User Datagram Protocol* (RFC 768). RFC Editor. https://doi.org/10.17487/RFC0768

Postel, J. (1981a). *Internet Protocol* (RFC 791). RFC Editor. https://doi.org/10.17487/RFC0791

Postel, J. (Ed.). (1981b). *Transmission Control Protocol* (RFC 793). RFC Editor. https://doi.org/10.17487/RFC0793

Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley. (Cap. 3 — IP header, Cap. 18 — TCP connection establishment.)

---

## Note pedagogice

**Concepții greșite vizate:**
- „Un scan sparge ceva" — Bloc D1 demontează explicit: scan = reconnaissance.
- „CLOSED = FILTERED" — Bloc D3 diferențiază: RST vs. timeout.
- „Portul clientului e fix" — epifania din C2: ephemeral port alocat de kernel.
- „RAW socket = socket normal cu mai multe drepturi" — Bloc A/B subliniază diferența calitativă.

**Tipare socratice folosite:**
- POE în B3 (câte linii per ping?) și D2 (câte porturi OPEN?).
- Capcană de concepție greșită în D3 (CLOSED ≠ FILTERED).
- „Ce s-ar fi întâmplat dacă…?" în E3 (trafic legitim vs. scanare).
- Întrebare de proiectare (constructivistă) în C3 (filtrare IP sursă).

**Diferențe față de varianta MININET-SDN:**
- Epifania Wireshark (F1) este specifică acestei variante și adaugă o dimensiune vizuală.
- Explicația despre capabilități Docker (`NET_RAW`) este specifică — înlocuiește discuția despre `sudo` din Mininet.
- Căile sunt diferite (`/seminars/S07/` vs. căi relative în Mininet).
- IP-urile sunt 172.30.7.x (Docker bridge) vs. 10.0.10.x (Mininet).

**Hook returnabil:** revenire explicită în F3 — cele 3 idei fixate răspund direct scenariului din A.

**Progresie:** sniffer (observ) → filtru (selectez) → scanner (generez) → detector (detectez) → IDS (integrez). Fiecare stage adaugă o competență peste cea anterioară.

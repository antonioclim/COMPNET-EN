# Seminar S07 — Capturare pachete, filtrare și port scanning

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (v11, `04_SEMINARS/S07/`) |
| **Infra** | MININET-SDN (VM Ubuntu 24.04, VirtualBox) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un RAW socket vede toate pachetele de pe interfață; din tiparele repetitive ale header-elor poți deduce automat dacă cineva scanează. |

---

## Obiective operaționale

La finalul seminarului, studentul:

1. deosebește un RAW socket (`AF_PACKET`) de un socket TCP/UDP obișnuit — ca perspectivă (pachet vs. stream/datagramă) și ca privilegii necesare;
2. completează `parse_ipv4_header` și interpretează câmpurile `version`, `IHL`, `proto`, `src`, `dst` în pachete capturate;
3. implementează o regulă de filtrare în Python (protocol + port) și explică de ce filtrarea după port poate fi înșelătoare;
4. rulează un connect scan (`port_scanner.py`) pe o țintă din laborator și interpretează stările `OPEN`, `CLOSED`, `FILTERED`;
5. declanșează și observă o alertă `[ALERT]` într-un detector de scanare bazat pe fereastră temporală + prag;
6. produce fișierele de output cerute (log-uri, rezultate scanare, explicație scurtă) ca dovadă de parcurgere.

---

## Structura seminarului

| Interval | Bloc | Scop | Durată |
|---:|---|---|---:|
| 0:00–0:04 | A — Hook + cadru etic | Scenariu concret, predicție, regulă etică | 4 min |
| 0:04–0:13 | B — RAW sniffing (Stage 2) | Completare `parse_ipv4_header`, demo sniffer, ICMP + TCP | 9 min |
| 0:13–0:19 | C — Packet filter (Stage 3) | `passes_filter`, filtrare TCP:5000, ephemeral ports | 6 min |
| 0:19–0:27 | D — Port scanner (Stage 4) | Connect scan, interpretare OPEN/CLOSED/FILTERED | 8 min |
| 0:27–0:35 | E — Detect scan (Stage 5) | Detector pe victim, alertă, sensibilitate vs. alarme false | 8 min |
| 0:35–0:40 | F — Mini-IDS + recap + livrabile | Structura `mini_ids.py`, revenire la hook, livrabile, cleanup | 5 min |

> **Regulă de sacrificare:** dacă timpul se comprimă, se păstrează B + D + E. Blocul C devine temă ghidată; din F se păstrează recap-ul (2 min) și lista de livrabile.

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

> *▸ „Tot ce facem azi se rulează strict în Mininet, pe hosturi pe care le controlăm. Scanarea rețelelor reale fără autorizare este ilegală."*

Afișezi pe ecran planul pe minute și obiectivele.

---

## Bloc B (0:04–0:13) — RAW sniffing (Stage 2)

### B1) Pornire Mininet (2 min)

> *▸ „Avem doi actori: h1 — cel care generează trafic (potențial atacator), h2 — victima. Ne interesează ce vede h2."*

**🔵 TERMINAL PRINCIPAL (SSH pe VM):**
```bash
cd ~/compnet-2025-redo-main/04_SEMINARS/S07
sudo mn --topo single,2 --mac --ipbase 10.0.10.0/24
```

Verificare conectivitate:
```text
mininet> h1 ping -c 1 10.0.10.2
```

### B2) Completare `parse_ipv4_header` — live coding (3 min)

> *▸ „Funcția asta citește primul byte din header-ul IPv4. De ce? Pentru că IHL (Internet Header Length) ne spune unde se termină header-ul și începe payload-ul. Fără IHL, nu știm unde e granița."*

**🟢 TERMINAL EDITOR (pe VM, înainte de Mininet sau într-un alt tab):**
```bash
nano 1_sniffing/S07_Part01B_Script_Packet_Sniffer.py
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

> **Epifanie (scurt):** „`! 8x B B 2x 4s 4s` — fiecare caracter descrie un câmp din header. `8x` sare peste 8 bytes (TOS, total length, identification, flags, fragment). `B B` citește TTL și protocolul. `2x` sare checksum-ul. `4s 4s` citește cele două adrese IPv4 de câte 4 bytes."

### B3) Rulare sniffer pe h2 + generare trafic (3 min)

> *▸ „Sniffer-ul nostru nu «știe» despre conexiuni. El vede pachete brute, indiferent cine le-a generat."*

**Predicție (POE):** „Dacă dau ping din h1 în h2, câte linii apar în sniffer pentru fiecare ping? Una sau două?"

Studenții răspund. (Răspuns: două — request + reply.)

**🟠 TERMINAL CAPTURĂ (Mininet CLI):**
```text
mininet> h2 python3 1_sniffing/S07_Part01B_Script_Packet_Sniffer.py h2-eth0 &
mininet> h1 ping -c 2 10.0.10.2
```

Output așteptat (aproximativ):
```text
[1] 10.0.10.1 -> 10.0.10.2  proto=ICMP
[2] 10.0.10.2 -> 10.0.10.1  proto=ICMP
[3] 10.0.10.1 -> 10.0.10.2  proto=ICMP
[4] 10.0.10.2 -> 10.0.10.1  proto=ICMP
```

Acum generezi trafic TCP — pornești server pe h2, trimiți din h1:
```text
mininet> h2 python3 ../S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
mininet> h1 bash -c "echo 'hello_s07' | nc 10.0.10.2 5000"
```

**Micro-întrebare (10 sec):** „Sniffer-ul arată `proto=TCP` dar nu arată porturile. Ce ar trebui să decodăm în plus?" (Răspuns: header-ul TCP, primii 4 bytes — porturile sursă și destinație.)

> **Notă:** Serverul TCP din S06 acceptă un singur client, apoi se oprește. Dacă e nevoie de portul 5000 deschis mai târziu (Bloc D), va trebui repornit.

Oprești sniffer-ul (dacă nu s-a oprit singur la `MAX_PACKETS`):
```text
mininet> h2 kill %python3 2>/dev/null
```

### B4) Trimitere studenți la pagina HTML interactivă (20 sec)

> *▸ „Pentru studiu individual, aveți o pagină interactivă în `_HTMLsupport/S07/1_sniffing/S07_Part01_Page_Sniffing.html`. O deschideți local în browser."*

---

## Bloc C (0:13–0:19) — Packet filter (Stage 3)

### C1) Tranziție

> *▸ „Sniffer-ul vede tot — cam ca o cameră de supraveghere fără zoom. Acum adăugăm zoom: filtrul. Wireshark folosește BPF (Berkeley Packet Filter) în kernel. Noi facem un prim pas, mai simplu: filtrare în user space, în Python."*

**Observație importantă (spusă explicit):** „În `packet_filter.py`, funcția `parse_ipv4_header` este deja completă — nu mai e TODO. Singurul lucru de completat este `passes_filter`."

### C2) Implementare filtru + demo (4 min)

Regula aleasă: „afișăm doar TCP către portul 5000".

**🟢 TERMINAL EDITOR:**
```bash
nano 2_packet-filter/S07_Part02A_Script_Packet_Filter.py
```

În `passes_filter(...)`:
```python
if proto == 6 and dst_port == 5000:
    return True
return False
```

Repornești serverul TCP pe h2 (pentru că cel anterior s-a oprit — vezi nota de la B3):
```text
mininet> h2 python3 ../S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

Rulezi filtrul:
```text
mininet> h2 python3 2_packet-filter/S07_Part02A_Script_Packet_Filter.py h2-eth0 &
```

Generezi trafic:
```text
mininet> h1 bash -c "echo 'again' | nc 10.0.10.2 5000"
```

**Ce apare:** linii de forma `10.0.10.1:<port_efemer> -> 10.0.10.2:5000  proto=TCP`

> **Epifanie:** „Portul clientului nu e «aleator magic»: e un ephemeral port alocat de kernel (de obicei 32768–60999 pe Linux). În capturi, acest port identifică fiecare conexiune unică."

### C3) Întrebare de proiectare — constructivistă (1 min)

> *▸ „Dacă aș vrea să detectez «doar DNS» (UDP către portul 53), aș filtra după port. Dar de ce poate fi înșelător în practică?"*

Lași studenții să răspundă. Răspunsuri posibile: port reuse, tunnelling DNS, servicii non-standard pe port 53.

Oprești procesele background:
```text
mininet> h2 kill %python3 2>/dev/null
```

---

## Bloc D (0:19–0:27) — Mini TCP port scanner (Stage 4)

### D1) Cadru (1 min)

> *▸ „Un scan nu «sparge» nimic. Este o operație de reconnaissance: testezi ce porturi răspund. Aceeași operație o face orice administrator de rețea când verifică suprafața expusă a unui server."*

### D2) Repornire server + scan pe fereastră îngustă (3 min)

Repornești serverul (dacă nu rulează deja):
```text
mininet> h2 python3 ../S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
```

**Predicție (POE):** „Scanez porturile 4990–5010. Câte vor fi OPEN?" (Răspuns așteptat: 1 — doar 5000.)

**🟢 TERMINAL ATTACKER:**
```text
mininet> h1 python3 3_port-scanning/S07_Part03A_Script_Port_Scanner.py 10.0.10.2 4990 5010
```

**Output așteptat:**
```text
[INFO] Scanning host 10.0.10.2 on ports 4990-5010 ...
PORT 4990 CLOSED
...
PORT 5000 OPEN
...
PORT 5010 CLOSED
[INFO] Scan complete. Results saved to S07_Part03_Output_Scan_Results.txt.
```

### D3) Interpretare (2 min)

> *▸ „Trei stări posibile:*
> - *`OPEN` — `connect()` a reușit. Cineva ascultă.*
> - *`CLOSED` — RST imediat. Port-ul există, dar nimeni nu ascultă.*
> - *`FILTERED` — timeout. Pachetul a fost probabil aruncat de un firewall (DROP, nu REJECT)."*

**Capcană de concepție greșită:** „Mulți confundă CLOSED cu FILTERED. CLOSED e un răspuns rapid — kernel-ul trimite RST. FILTERED e absența răspunsului."

### D4) (Opțional, doar dacă rămâne 1 min) Demo FILTERED cu iptables

Pe h2:
```text
mininet> h2 iptables -A INPUT -p tcp --dport 5001 -j DROP
```
Re-scanezi portul 5001 din h1 și observi `FILTERED`. Apoi cureți:
```text
mininet> h2 iptables -D INPUT -p tcp --dport 5001 -j DROP
```

> *▸ „DROP → timeout → FILTERED. Dacă ar fi fost REJECT, vedeai RST → CLOSED."*

---

## Bloc E (0:27–0:35) — Detectarea scanării (Stage 5)

### E1) Pornire detector pe h2 (1 min)

> *▸ „Detectorul nu «știe» cine e atacator. El doar numără: câte porturi distincte au primit SYN de la aceeași sursă, într-o fereastră de timp."*

**🔵 TERMINAL VICTIM:**
```text
mininet> h2 python3 4_scan-detector/S07_Part04A_Script_Detect_Scan.py h2-eth0 &
```

### E2) Scanare suficient de densă (2 min)

**Predicție:** „Pragul implicit e 10 porturi în 5 secunde. Dacă scanez porturile 1–120, se va declanșa alerta?"

**🟢 TERMINAL ATTACKER:**
```text
mininet> h1 python3 3_port-scanning/S07_Part03A_Script_Port_Scanner.py 10.0.10.2 1 120
```

**Output așteptat pe h2:**
```text
[ALERT] Possible port scan from 10.0.10.1: 10 distinct ports in the last 5 seconds
```

(Alerta poate apărea de mai multe ori, pe măsură ce scanarea continuă.)

### E3) Sensibilitate vs. alarme false (3 min)

Deschizi fișierul detectorului:
```bash
nano 4_scan-detector/S07_Part04A_Script_Detect_Scan.py
```

Arăți variabilele:
```python
WINDOW_SECONDS = 5       # fereastra temporală
PORT_THRESHOLD = 10      # numărul de porturi distincte care declanșează alerta
```

> *▸ „Două «butoane»: fereastra și pragul. Dacă scad ambele (2 secunde, prag 5), detectez mai rapid — dar un health-check intern care verifică 6 porturi declanșează alarma."*

**Tipar „Ce s-ar fi întâmplat dacă…?":** „Ce trafic legitim ar putea semăna cu o scanare?"

Răspunsuri așteptate: health-checks de load balancer, service discovery (mDNS, Consul), monitorizare Prometheus, micro-servicii cu retry agresiv.

### E4) Oprire procese

```text
mininet> h2 kill %python3 2>/dev/null
```

---

## Bloc F (0:35–0:40) — Mini-IDS + recap + livrabile

### F1) Mini-IDS — prezentare structurală (1.5 min)

> *▸ „Un IDS (Intrusion Detection System) real face două lucruri: reduce traficul la evenimente relevante — ca filtrul nostru — și caută tipare — ca detectorul nostru. `mini_ids.py` combină exact aceste idei."*

Arăți structura fișierului (fără să-l rulezi):
```text
mininet> h2 head -45 5_mini-ids/S07_Part05A_Script_Mini_IDS.py
```

Menționezi cele trei detectoare: TCP scan (SYN către porturi distincte), UDP spray (datagrame către porturi distincte), flood către un port (multe pachete către același tuple).

> *▸ „Ca temă, finalizați Stage-urile, rulați `mini_ids.py` cu scenariile din fișierul de task-uri, și scrieți `explanation.md`."*

### F2) Recap — revenire la hook (1.5 min)

> *▸ „La început am văzut un scenariu: un host trimite 200 de SYN-uri în 3 secunde. Acum putem răspunde:*
>
> 1. *Un RAW socket vede toate pachetele — nu doar pe cele ale «propriei» conexiuni.*
> 2. *Header-ul IPv4 are câmpul IHL care ne spune unde începe payload-ul TCP/UDP. Fără parsarea corectă a acestui câmp, totul se decalează.*
> 3. *Detecția unei scanări se reduce la: numără porturi distincte per sursă, într-o fereastră de timp. Simplu ca idee — provocarea e calibrarea pragurilor."*

### F3) Livrabile (1 min — spuse explicit)

- `sniffer_log.txt` — minim 20 pachete + răspunsuri la întrebări de reflecție
- `filter_results.txt` — minim 20 linii filtrate + răspunsuri la întrebări de reflecție
- `S07_Part03_Output_Scan_Results.txt` — minim 50 porturi scanate + reflecții
- `scan_detection.txt` — fragment cu cel puțin un `[ALERT]` + trafic normal + sumar (6–8 propoziții)
- `ids_alerts.log` + `explanation.md` — pentru mini-IDS (10–15 propoziții)

Pagini interactive pentru studiu: `_HTMLsupport/S07/` (5 pagini, câte una per stage).

### F4) Cleanup

```text
mininet> exit
```
```bash
sudo mn -c
```

---

## Cheat-sheet

### Comenzi Mininet esențiale

| Comandă | Scop |
|---|---|
| `sudo mn --topo single,2 --mac --ipbase 10.0.10.0/24` | Topologie cu 2 hosturi |
| `h1 ping -c 2 10.0.10.2` | Verificare conectivitate |
| `h2 python3 <script> h2-eth0 &` | Rulare script pe h2, background |
| `h2 kill %python3` | Oprire procese Python pe h2 |
| `exit` apoi `sudo mn -c` | Cleanup complet |

### Fișiere din kit (S07)

| Stage | Script | Tasks | Livrabil |
|---|---|---|---|
| 2 — Sniffing | `1_sniffing/S07_Part01B_Script_Packet_Sniffer.py` | `S07_Part01C_Tasks_Packet_Sniffing.md` | `sniffer_log.txt` |
| 3 — Filter | `2_packet-filter/S07_Part02A_Script_Packet_Filter.py` | `S07_Part02B_Tasks_Packet_Filter.md` | `filter_results.txt` |
| 4 — Scanner | `3_port-scanning/S07_Part03A_Script_Port_Scanner.py` | `S07_Part03B_Tasks_Port_Scanner.md` | `S07_Part03_Output_Scan_Results.txt` |
| 5 — Detector | `4_scan-detector/S07_Part04A_Script_Detect_Scan.py` | `S07_Part04B_Tasks_Detect_Scan.md` | `scan_detection.txt` |
| 6 — Mini-IDS | `5_mini-ids/S07_Part05A_Script_Mini_IDS.py` | `S07_Part05B_Tasks_Mini_IDS.md` | `ids_alerts.log` + `explanation.md` |

### Server TCP auxiliar (din S06)

```text
h2 python3 ../S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &
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

---

## Plan de contingență

| # | Problemă | Soluție rapidă |
|---|---|---|
| 1 | Scripturile RAW „cer sudo" / nu pornesc | Verifică interfața (`h2-eth0`). În Mininet, hosturile NU cer `sudo` separat dacă Mininet e pornit cu `sudo`. Verifică cu `h2 whoami`. |
| 2 | Nu apare trafic în sniffer | Rulezi `h1 ping -c 3 10.0.10.2`. Dacă ping nu merge, `pingall`. La nevoie, `exit` + `sudo mn -c` + repornire. |
| 3 | Portul 5000 nu apare OPEN la scan | Serverul TCP s-a oprit (acceptă un singur client). Repornești: `h2 python3 ../S06/3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 &`. Alternativă: `h2 nc -l 5000 &`. |
| 4 | `[ALERT]` nu se declanșează | Scazi `PORT_THRESHOLD=5` în `detect_scan.py`. Sau mărești plaja scanată (1–200). Verifici că detectorul rulează pe `h2-eth0`. |
| 5 | Mininet rămâne „murdar" după crash | `sudo mn -c && sudo pkill -f 'python3.*S07' \|\| true` |
| 6 | `MAX_PACKETS` atins prea repede în sniffer | Mărește valoarea la 100 în script (`nano`), sau oprește și repornește sniffer-ul. |
| 7 | Lipsă timp — nu ajungi la Bloc E | Faci Bloc D + arăți `detect_scan.py` 60 sec structural + treci direct la livrabile. Detecția devine temă. |

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
- „Un scan sparge ceva" — Bloc D1 demontează explicit: scan = reconnaissance, nu exploatare.
- „CLOSED = FILTERED" — Bloc D3 diferențiază: RST vs. timeout.
- „Portul clientului e fix" — epifania din C2: ephemeral port alocat de kernel.
- „RAW socket = socket normal cu mai multe drepturi" — B2 subliniază diferența calitativă: pachet vs. stream.

**Tipare socratice folosite:**
- POE în B3 (câte linii per ping?) și D2 (câte porturi OPEN?).
- Capcană de concepție greșită în D3 (CLOSED ≠ FILTERED).
- „Ce s-ar fi întâmplat dacă…?" în E3 (trafic legitim vs. scanare).
- Întrebare de proiectare (constructivistă) în C3 (filtrare DNS — port reuse).

**Hook returnabil:** revenire explicită în F2 — cele 3 idei fixate răspund direct scenariului din A.

**Progresie:** sniffer (observ) → filtru (selectez) → scanner (generez) → detector (detectez) → IDS (integrez). Fiecare stage adaugă o competență peste cea anterioară.

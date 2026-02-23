# Seminar S01 — Analiză de rețea

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (versiune `claudev11_EN`) |
| **Infra** | Windows nativ + Docker Desktop (sau Docker în WSL2) + Wireshark |
| **Durată țintă** | 35–40 min (predare + demonstrații ghidate; exercițiile complete rămân ca lucru individual) |
| **Ideea-cheie** | Diagnosticul de rețea se construiește în straturi: nume → IP → conectivitate → porturi → trafic → pachete; diferența TCP / UDP se *vede* în comportament și se *confirmă* în captură. |

> Materialele din kit (`04_SEMINARS/S01/`) sunt în engleză. Comenzile sunt universale. În predare folosești româna; termenii tehnici consacrați rămân în engleză: *handshake*, *payload*, *capture filter*, *display filter*, *loopback*, *stream*, *datagram*.

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. **Diagnostica** conectivitatea, rezolvarea DNS și starea porturilor folosind `ping`, `nslookup` și `netstat`/`ss`.
2. **Genera** trafic TCP și UDP controlat cu `netcat` și **descrie** diferența de comportament (conexiune persistentă vs. datagrame independente).
3. **Captura** pachete cu `tcpdump` (în container) și **analiza** fișierul `.pcap` rezultat în Wireshark pe Windows.
4. **Distinge** între capture filter (BPF, înainte de captură) și display filter (după captură).
5. **Explica** de ce UDP nu semnalează eroare la trimiterea către un port fără receptor.
6. **Produce** dovezile de lucru cerute de fișierele de task (`S01_Part02`, `S01_Part04`, `S01_Part06`).

---

## Structura seminarului

| Bloc | Ce faci | Durată |
|:----:|---------|-------:|
| **A** | Hook + activare + conflict cognitiv | 3 min |
| **B** | Pornire laborator Docker | 4 min |
| **C** | Diagnostic de bază: `nslookup`, `ping`, `netstat`/`ss` | 7 min |
| **D** | Netcat TCP și UDP + `netstat` în context | 13 min |
| **E** | Captură cu `tcpdump` + analiză în Wireshark | 9 min |
| **F** | Recapitulare, hook reluat, livrabile, cleanup | 4 min |
| | **Total** | **40 min** |

> *▸ Dacă timpul se comprimă: Blocul E (captură) se sacrifică primul — se recuperează la debutul S02. Blocurile A–D sunt non-negociabile.*

---

## Ce ai în kit (și ce folosești la S01)

În `04_SEMINARS/S01/`:

| Fișier | Rol | Livrabil student |
|---|---|---|
| `S01_Part01_Scenario_Basic_Tools.md` | Scenariu demonstrație | — |
| `S01_Part02_Tasks_Basic_Tools.md` | Exercițiu individual | `S01_Part02_Output_Basic_Tools.txt` |
| `S01_Part03_Scenario_Netcat_Basics.md` | Scenariu demonstrație | — |
| `S01_Part04_Tasks_Netcat_Basics.md` | Exercițiu individual | `S01_Part04_Output_Netcat_Activity.txt` |
| `S01_Part05_Scenario_Wireshark_Netcat.md` | Scenariu demonstrație | — |
| `S01_Part06_Tasks_Wireshark_Netcat.md` | Exercițiu individual | `wireshark_activity_output.zip` |

Suplimentar: `04_SEMINARS/_HTMLsupport/S01/S01_CLI_NetcatTCP-UDP_Wireshark_sim.html` — simulator interactiv (opțional, pentru exersare individuală).

---

## Pregătirea instructorului (înainte de oră)

### Precondiții (comunicate studenților cu 24–48h înainte)

1. **Docker** funcțional pe Windows (Docker Desktop sau Docker în WSL2; contează doar ca `docker` să meargă din terminal).
2. **Wireshark** instalat pe Windows (cu Npcap). Nu insistăm pe captură live — vom deschide un `.pcap` generat în container.
3. Kit-ul extras local: studenții trebuie să aibă `04_SEMINARS\S01\`.

### Imagine Docker „laborator" (se construiește o singură dată)

> *▸ Nota: Acest Dockerfile NU face parte din kit. E un adaos specific variantei fără-VM, pentru a evita pierderile de timp cu instalări `apt-get` în sală.*

În `04_SEMINARS\S01\`, creezi `Dockerfile.s01`:

```dockerfile
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    iputils-ping \
    net-tools \
    dnsutils \
    netcat-openbsd \
    tcpdump \
    procps \
    iproute2 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work
CMD ["bash"]
```

Construire (PowerShell, din folderul S01):

```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S01
docker build -t compnet-s01lab:1.0 -f Dockerfile.s01 .
```

Test rapid:

```powershell
docker run --rm compnet-s01lab:1.0 ping -c 1 1.1.1.1
```

### Checklist de sală

- Folderul `S01` deschis în editor / File Explorer.
- Wireshark deschis pe Windows.
- Windows Terminal cu 3 tab-uri denumite: **SERVER**, **CLIENT**, **CAPTURE**.

---

## Bloc A — Hook + activare + conflict cognitiv (~3 min)

### Deschidere (scenariu situat, 60 sec)

> *▸ „Imaginați-vă: colegul vă scrie la 3 noaptea — 'site-ul nu merge'. Tastați `ping site-ul.ro` și primiți răspuns. Dar browserul dă eroare. E pică rețeaua, sau e altceva? Până la finalul orei, o să aveți un arbore de diagnostic care vă răspunde în 30 de secunde."*

### Activare (30 sec)

> *▸ „Câți din voi au folosit vreodată `ping`? Dar `netcat`? Dar Wireshark? Nu contează dacă nu. Azi construim de la zero."*

### Predicții rapide (90 sec)

Cere 2–3 răspunsuri din sală, notează pe tablă/slide:

1. „Dacă `ping google.com` eșuează, înseamnă sigur că nu am internet?"
2. „TCP și UDP — diferența e doar 'rapid vs. lent', sau e ceva structural?"
3. „Câte pachete credeți că apar la *începutul* unei conexiuni TCP, înainte de orice mesaj?"

> *▸ Nu corectezi acum. Răspunsurile se confruntă pe parcurs.*

---

## Bloc B — Pornire laborator Docker (~4 min)

### Ce faci (PowerShell, orice tab)

1. Intri în folderul S01:

```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S01
ls
```

2. Pornești container persistent:

```powershell
# cleanup (ignoră eroarea dacă nu există)
docker rm -f s01lab 2>$null

# laborator cu volume mount + capabilități rețea
docker run -d --name s01lab `
  -v "${PWD}:/work" -w /work `
  --cap-add=NET_RAW --cap-add=NET_ADMIN `
  compnet-s01lab:1.0 sleep infinity
```

3. Deschizi shell-uri interactive în tab-urile SERVER și CLIENT:

```powershell
docker exec -it s01lab bash
```

4. Verificare:

```bash
pwd    # /work
ls     # fișierele S01
```

> *▸ „Docker e doar cutia — un Linux curat, identic pentru toți. Nu e subiectul seminarului; e instrumentul care ne scapă de 'la mine merge, la tine nu'."*

---

## Bloc C — Diagnostic: `nslookup`, `ping`, `netstat` (~7 min)

**Fișier kit:** `04_SEMINARS/S01/S01_Part01_Scenario_Basic_Tools.md`
**Unde rulezi:** într-un singur shell din container (tab-ul CLIENT), ca să nu fragmentezi atenția
**Obiective vizate:** 1

### C1. `nslookup` — rezolvare DNS (2 min)

```bash
nslookup google.com
```

Arată: serverul DNS utilizat, IP-urile rezolvate.

**🎯 Predicție (POE):** „Ce se întâmplă dacă întreb un domeniu care nu există?"

```bash
nslookup domeniu-inexistent-xyz123.com
```

Arată: `server can't find` — **NXDOMAIN**.

> *▸ „DNS eșuează diferit de conectivitate. O eroare de rezolvare nu înseamnă că rețeaua e căzută."*

### C2. `ping` — conectivitate (2 min)

```bash
ping -c 2 google.com
```

Dacă merge: ai testat simultan DNS + ICMP.

Dacă nu merge (ICMP blocat de rețea): comută fără dramă:

```bash
ping -c 2 1.1.1.1
```

Explică: unele rețele filtrează ICMP — e o practică reală de securitate, nu o eroare.

**🎯 Confruntare cu predicția 1:** „Deci dacă `ping` eșuează — poate fi DNS stricat, poate fi rută, poate fi ICMP filtrat. E prima ramură din arborele de troubleshooting."

### C3. `netstat`/`ss` — porturi (2 min)

```bash
netstat -tulnp
```

Flag-urile: `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric, `-p` procesul proprietar.

> *▸ Alternativă modernă: `ss -tulnp` — aceleași flag-uri.*

> *▸ „`netstat`/`ss` nu e un exercițiu de memorare, ci o radiografie: cine ascultă, cine e conectat. În laboratoarele următoare, când 'nu merge', primul reflex sănătos e să verifici aici."*

Nu dai exercițiul individual acum — `S01_Part02_Tasks_Basic_Tools.md` rămâne temă. Nu intri în detalii ICMP, DNS intern, ARP — vin la C05–C06.

---

## Bloc D — Netcat TCP și UDP + `netstat` în context (~13 min)

**Fișier kit:** `04_SEMINARS/S01/S01_Part03_Scenario_Netcat_Basics.md`
**Unde rulezi:** în 2 shell-uri din container (SERVER + CLIENT)
**Obiective vizate:** 2, 5

### Narativ de tranziție

> *▸ „Trecem de la diagnostic la trafic real. Înainte de a începe, uitați-vă în paralel la cele două ferestre — rețelele sunt despre două capete."*

---

### D1. TCP: server + client (6–7 min)

**🔵 SERVER:**

```bash
nc -l -p 9100
```

> *▸ „Serverul ascultă și blochează terminalul. E normal: așteaptă conexiuni."*

**🟢 CLIENT (alt tab):**

```bash
nc 127.0.0.1 9100
```

**Schimb de mesaje (1 min):** cere unui student din sală să dicteze un mesaj scurt — tastezi în CLIENT, apare în SERVER. Apoi un mesaj pe 2–3 linii (Enter între linii) ca să simtă stream-ul.

**Moment de legătură cu diagnostic — `netstat` în context (1 min):**

Cu conexiunea TCP deschisă, dintr-un al treilea exec (din PowerShell, fără a ieși din netcat):

```powershell
docker exec -it s01lab netstat -tulnp
```

Arată intenționat:
- portul `:9100` în **LISTEN** (procesul `nc`);
- o conexiune **ESTABLISHED** (client ↔ server).

> *▸ „Acum `netstat` nu mai e abstract — vedeți exact procesul `nc` care ascultă și conexiunea dintre cele două capete."*

**Închidere TCP:** Ctrl+C în SERVER → CLIENT se deconectează.

> *▸ „TCP are terminare cu FIN/ACK. Când o parte închide, cealaltă află."*

---

### D2. UDP: server + datagrame (5–6 min)

**🔵 SERVER:**

```bash
nc -u -l -p 9101
```

**🟢 CLIENT:**

```bash
echo "test UDP 1" | nc -u 127.0.0.1 9101
echo "test UDP 2" | nc -u 127.0.0.1 9101
```

> *▸ „Nu există conexiune. Fiecare `echo | nc` trimite o datagramă separată."*

### Epifanie: UDP „trimis în gol" ⚡

**🎯 Predicție (POE):** „Dacă opresc serverul și trimit un mesaj, ce se întâmplă?"

1. Oprește serverul: Ctrl+C.
2. Trimite din CLIENT:

```bash
echo "mesaj pierdut" | nc -u 127.0.0.1 9101
```

3. Întreabă: „Ați primit eroare? Nu. Unde s-a dus mesajul?"

> *▸ „UDP nu are confirmări la transport. Poți trimite 'corect', iar mesajul să nu ajungă nicăieri. Aplicațiile care folosesc UDP își construiesc propriile mecanisme — timeout, retransmisie, verificare la nivel de aplicație."*

**🎯 Confruntare cu predicția 2:** „TCP vs UDP nu e 'rapid vs. lent' — e structural: TCP are stare, UDP nu."

---

## Bloc E — Captură `tcpdump` + analiză Wireshark (~9 min)

**Fișier kit:** `04_SEMINARS/S01/S01_Part05_Scenario_Wireshark_Netcat.md`
**Obiective vizate:** 3, 4

> *▸ În varianta Windows + Docker, captura se face cu `tcpdump` în container, iar analiza în Wireshark pe Windows. Fișierele `.pcap` ajung pe disc prin volume mount.*

### E1. TCP: captură + trafic + interpretare (5–6 min)

**🟠 CAPTURE (PowerShell, tab-ul CAPTURE):**

```powershell
docker exec -it s01lab tcpdump -i lo -nn -w /work/S01_tcp_9200.pcap tcp port 9200
```

> *▸ „Asta e un capture filter — BPF, la nivel libpcap. Se aplică înainte de captură."*

**🔵 SERVER:** `nc -l -p 9200`
**🟢 CLIENT:** `nc 127.0.0.1 9200` → trimite 3 mesaje scurte.

Oprește netcat, apoi oprește captura (Ctrl+C în CAPTURE).

**Wireshark pe Windows:** `File → Open` → `S01_tcp_9200.pcap`

Display filter: `tcp.port == 9200`

**🎯 Confruntare cu predicția 3 — Epifanie ⚡:**

> *▸ „Câte pachete ați prezis? Primele 3: SYN → SYN-ACK → ACK. Three-way handshake — RFC 793. Abia apoi vin datele."*

Arată rapid:
- **Handshake:** primele 3 pachete.
- **Payload:** un pachet marcat PSH/ACK.
- **Follow → TCP Stream:** conversația ca text (30 sec — motivant).

> *▸ „TCP e stream: mesajele aplicației nu au 'granițe sfinte' la transport. Pachetele sunt o decizie a stack-ului; aplicația trebuie să-și facă framing. Vom vedea asta concret la S02–S04."*

### E2. UDP: captură + interpretare (3 min)

**🟠 CAPTURE:**

```powershell
docker exec -it s01lab tcpdump -i lo -nn -w /work/S01_udp_9201.pcap udp port 9201
```

**🔵 SERVER:** `nc -u -l -p 9201`
**🟢 CLIENT:** `echo "UDP test" | nc -u 127.0.0.1 9201`

Oprește captura. Wireshark → `S01_udp_9201.pcap` → display filter: `udp.port == 9201`

> *▸ „Zero handshake. Pachetul UDP apare direct cu date. `tcp.stream eq 0` are sens la TCP; la UDP nu ai stream, ai datagrame."*

### Tabel comparativ (proiectat sau verbalizat)

| Aspect | TCP | UDP |
|--------|-----|-----|
| Conexiune | Da (three-way handshake) | Nu |
| Confirmare livrare | Da (ACK) | Nu |
| Ordine garantată | Da (sequence/ack numbers) | Nu |
| Overhead în captură | Handshake + ACK-uri + date | Doar date |
| Display filter util | `tcp.stream eq 0` | `udp.port == 9201` |

---

## Bloc F — Recapitulare, hook reluat, livrabile, cleanup (~4 min)

### Hook reluat (30 sec)

> *▸ „Scenariul de la început — 'site-ul nu merge, dar ping răspunde'. Acum aveți instrumentele: verificați DNS, verificați portul, capturați traficul. Nu mai ghiciți."*

### Confruntare finală cu predicțiile (30 sec)

> *▸ „(1) `ping` eșuat ≠ internet picat — confirmat. (2) TCP vs UDP e structural — confirmat în netcat. (3) TCP începe cu 3 pachete — confirmat în captură."*

### Ce iau cu ei (3 idei)

1. Diagnosticul de rețea se face în straturi: DNS → conectivitate → porturi → trafic → pachete.
2. TCP = conexiune cu stare, UDP = datagrame fără stare.
3. Capture filter (BPF, înainte) ≠ display filter (Wireshark, după).

### Livrabile

| Fișier task | Ce produce | Livrabil |
|---|---|---|
| `S01_Part02_Tasks_Basic_Tools.md` | Comenzi + output + interpretare | `S01_Part02_Output_Basic_Tools.txt` |
| `S01_Part04_Tasks_Netcat_Basics.md` | Comenzi TCP/UDP + comparație 3–5 propoziții | `S01_Part04_Output_Netcat_Activity.txt` |
| `S01_Part06_Tasks_Wireshark_Netcat.md` | Screenshoturi filtre + explicație 5–7 propoziții | `wireshark_activity_output.zip` |

> *▸ Porturile din tasks diferă de cele din demo (9100/9101 pentru netcat, 9300/9301 pentru Wireshark) — exercițiul cere reproducere independentă, nu copie din seminar.*

> *▸ Pentru capturi, studenții pot folosi `tcpdump ... tcp port 9300` / `udp port 9301` și să includă screenshot cu comanda ca dovadă de capture filter (BPF). E la fel de valid ca folosirea câmpului Capture Filter din Wireshark.*

Opțional — simulator interactiv: `04_SEMINARS/_HTMLsupport/S01/S01_CLI_NetcatTCP-UDP_Wireshark_sim.html`.

### Preview S02

> *▸ „Data viitoare scriem cod — server și client TCP în Python. Wireshark va fi instrumentul nostru de verificare."*

### Cleanup (pe proiector, 5 sec)

```powershell
docker rm -f s01lab
```

---

## Cheat-sheet

### Pornire laborator

```powershell
cd D:\compnet-2025-redo-main\04_SEMINARS\S01

docker rm -f s01lab 2>$null

docker run -d --name s01lab `
  -v "${PWD}:/work" -w /work `
  --cap-add=NET_RAW --cap-add=NET_ADMIN `
  compnet-s01lab:1.0 sleep infinity

docker exec -it s01lab bash
```

### Comenzi cheie (în container)

```bash
nslookup google.com
ping -c 2 google.com

nc -l -p 9100                          # TCP server
nc 127.0.0.1 9100                      # TCP client

nc -u -l -p 9101                       # UDP server
echo "test" | nc -u 127.0.0.1 9101     # UDP client
```

### Captură (din PowerShell)

```powershell
# TCP
docker exec -it s01lab tcpdump -i lo -nn -w /work/S01_tcp_9200.pcap tcp port 9200

# UDP
docker exec -it s01lab tcpdump -i lo -nn -w /work/S01_udp_9201.pcap udp port 9201
```

### Display filters (Wireshark)

```text
tcp.port == 9200
udp.port == 9201
tcp.stream eq 0
```

---

## Plan de contingență

| Problemă | Soluție rapidă |
|----------|---------------|
| Docker nu pornește pe un PC din sală | Demonstrezi de pe laptopul instructorului (proiector). Studentul lucrează ulterior acasă. Nu consumi 20 min pe instalări. |
| `ping` nu funcționează (ICMP blocat) | Testezi `nslookup` separat și folosești `ping 1.1.1.1`. Explici că filtrarea ICMP e o practică reală de securitate. |
| Captura e goală | Ordinea a fost greșită: `tcpdump` trebuie pornit *înainte* de trafic. Reiei strict: captură → server → client → stop. |
| Wireshark pare „zgomotos" | Deschide fișierul `.pcap` corect și aplică display filter. În fișierele generate cu BPF nu ar trebui trafic irelevant. |
| Container-ul nu are rețea | `docker exec -it s01lab ping -c 1 1.1.1.1`. Dacă nu merge, verifică Docker Desktop / daemon. Ca plan B, tot traficul loopback funcționează fără internet. |
| Depășești 40 min | Sacrifică Blocul E (captură). Recuperezi la debutul S02 cu demonstrație de 5 min. |
| Imaginea Docker nu e construită | Construiește live: `docker build -t compnet-s01lab:1.0 -f Dockerfile.s01 .` (~30 sec cu internet). Fără internet — folosește simulatorul HTML ca plan C. |

---

## Referințe

Postel, J. (Ed.). (1981). Transmission Control Protocol. RFC 793. Internet Engineering Task Force. https://doi.org/10.17487/RFC0793

Postel, J. (1980). User Datagram Protocol. RFC 768. Internet Engineering Task Force. https://doi.org/10.17487/RFC0768

McCanne, S. & Jacobson, V. (1993). The BSD packet filter: A new architecture for user-level packet capture. In *Proceedings of the USENIX Winter 1993 Conference* (pp. 259–270). USENIX Association. https://doi.org/10.5555/1267303.1267305

Matthews, J. N. (2005). Hands-on approach to teaching computer networking using packet traces. In *Proceedings of the 6th Conference on Information Technology Education* (pp. 361–367). ACM. https://doi.org/10.1145/1095714.1095777

Driver, R., Asoko, H., Leach, J., Mortimer, E. & Scott, P. (1994). Constructing scientific knowledge in the classroom. *Educational Researcher, 23*(7), 5–12. https://doi.org/10.3102/0013189X023007005

Merkel, D. (2014). Docker: Lightweight Linux containers for consistent development and deployment. *Linux Journal, 2014*(239). https://doi.org/10.5555/2600239.2600241

---

## Note pedagogice

**Tipare socratice folosite:**
- POE 1 (Bloc C1): predicție DNS inexistent → observație NXDOMAIN → explicație separare DNS / conectivitate.
- POE 2 (Bloc D2, epifanie): predicție UDP fără receptor → observație zero erori → explicație fire and forget.
- Confruntare cu predicția 3 (Bloc E1): handshake TCP = 3 pachete vizibile în captură.

**Epifanii marcate (⚡):**
1. Bloc D2 — UDP nu semnalează pierderea.
2. Bloc E1 — three-way handshake vizibil vs. absența totală la UDP.

**Concepții greșite vizate:**
- „ping eșuat = internet picat" → ramuri multiple de diagnostic (Bloc C).
- „TCP și UDP = viteză" → diferență structurală (Bloc D).
- „un mesaj TCP = un pachet" → TCP este stream (Bloc E, Follow TCP Stream, prefigurare S02–S04).

**Specificități variantă fără-VM:**
- Toate comenzile de rețea rulează într-un container Docker (`compnet-s01lab`), nu în VM.
- Capturile se fac cu `tcpdump` (nu `tshark`), deoarece `tcpdump` e inclus în imaginea Docker minimală.
- Fișierele `.pcap` ajung pe Windows prin volume mount (`-v "${PWD}:/work"`) — se deschid direct în Wireshark.
- Dockerfile-ul `Dockerfile.s01` este un adaos specific acestei variante, nu face parte din kit.
- Studenții folosesc `docker exec` pentru shell-uri multiple în loc de sesiuni SSH multiple.

**Legătura cu S02:** S02 (socket programming Python) folosește Wireshark pentru analiza traficului generat programatic. Dacă Blocul E se sacrifică azi, se recuperează la debutul S02.

---

*Outline S01 fără-VM — verificat pe baza kit-ului `compnet-2025-redo` (versiune `claudev11_EN`), directorul `04_SEMINARS/S01/` și `04_SEMINARS/_tutorial-solve/s1/`. Document autonom — zero referințe la varianta MININET-SDN.*

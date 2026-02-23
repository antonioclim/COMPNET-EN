# Seminar S13 — Scanning și enumerarea vulnerabilităților

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (claudev11) |
| **Infra** | Windows (host) + Docker Desktop (WSL2 backend) + Wireshark |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un port deschis nu este o vulnerabilitate; vulnerabilitatea apare la intersecția dintre versiune, configurare și context de expunere — iar măsurarea e primul pas. |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. **Porni** o infrastructură de laborator cu Docker Compose și **verifica** funcționalitatea minimă a serviciilor (HTTP/FTP) prin metode benigne.
2. **Executa** un scan de descoperire și un scan țintit cu `nmap` dintr-un container de unelte, apoi **interpreta** output-ul: IP → port → serviciu/versiune.
3. **Rula** un scanner TCP minimal în Python (într-un container Python) și **explica** de ce nu detectează UDP, nu identifică versiuni și depinde de timeout.
4. **Colecta** evidențe prin enumerare (Nmap Scripting Engine, headers HTTP) și **formula** un triplet observație–risc–control.
5. **Distinge** între scanning (inventar de suprafață) și exploatare (acces neautorizat), pe baza cadrului etic prezentat.
6. **Conecta** semnalele observate (banner vechi, port backdoor) cu decizii defensive concrete (patching, segmentare, monitorizare).

---

## Particularitate pe Windows: de ce folosim un „tool container"

Pe Windows + Docker Desktop, accesul direct al host-ului la IP-urile interne din bridge-ul Docker (de forma `172.20.0.x`) este adesea limitat sau inconsistent (depinde de backend și de setări de rețea). Ca să evităm problemele de conectivitate, scanning-ul se face **dintr-un container atașat la rețeaua Docker a laboratorului** (`nicolaka/netshoot`), unde conectivitatea internă e nativă.

Pe Windows nu dispunem nici de `nc` (netcat) nativ, nici de `nmap`. Toate uneltele de rețea rulează în containere.

---

## Structura seminarului

| Bloc | Conținut | Durată | Tip |
|---|---|---:|---|
| A | Hook + cadru etic + activare cunoștințe | 4 min | interactiv |
| B | Model mental + pornire infrastructură + verificări minimale | 8 min | demo + predicție |
| C | Scanning din tool container (nmap) | 9 min | demo + predicție |
| D | Scanner TCP minimal în Python (container Python) | 6 min | demo + întrebări |
| E | Enumerare: evidențe → risc → control | 6 min | demo + micro-exercițiu |
| F | Mini-demo Wireshark: semnătura unui scan | 4 min | demo + observație |
| G | Recap + temă + preview S14 | 3 min | interactiv |
| **Total** | | **40 min** | |

---

## Pregătirea instructorului (5–10 minute înainte)

### Checklist pe Windows

1. Docker Desktop pornit (WSL2 backend recomandat).
2. Wireshark instalat (cu Npcap inclus).
3. Repo-ul starterkit local, cu fișierele S13.
4. Deschizi **trei ferestre PowerShell**:
   - 🔵 PS#1: Docker Compose + monitorizare
   - 🟢 PS#2: tool container pentru scanning (netshoot)
   - 🟠 PS#3: container Python (sau captură pcap, mai târziu)

### Verificări rapide (🔵 PS#1)

```powershell
docker version
docker compose version
cd .\04_SEMINARS\S13
ls
```

---

## Bloc A — Hook + cadru etic + activare (0:00–0:04)

### Hook (situat, afectiv)

> *▸ „Vă arăt un singur rând de text: `220 (vsFTPd 2.3.4)`. E un banner FTP. Cine poate spune, doar din aceste 5 cuvinte, dacă mașina e vulnerabilă sau nu? Și dacă da — la ce anume?"*

Lași 5–10 secunde de gândire. Nu dai răspunsul.

> *▸ „Păstrați răspunsul vostru — revenim la el la final. Poate vă surprinde ce aflăm."*

### Cadru etic (30 secunde, ferm)

> *▸ „Tot ce facem astăzi se întâmplă strict în containere Docker locale. Aceleași tehnici, aplicate pe un sistem fără consimțământ, sunt infracțiune. Scopul e să înțelegem cum se măsoară expunerea, nu să reproducem atacuri."*

Deschizi pe scurt `S13_Part01_Explanation_Pentest_Intro.md` și arăți paragraful de avertizare etică (10 secunde).

### Activare cunoștințe

> *▸ „La S12 am lucrat cu RPC — am expus servicii pe porturi. Astăzi inversăm perspectiva: cum descoperi ce porturi sunt deschise și ce servicii rulează, din postura cuiva care nu știe nimic despre rețea."*

**Fișiere din kit referite:** `S13_Part01_Explanation_Pentest_Intro.md`

---

## Bloc B — Model mental + pornire + verificări minimale (0:04–0:12)

### Ce faci: model mental (🔵 PS#1)

Deschizi Compose-ul și subliniezi topologia:

```powershell
Get-Content .\S13_Part02_Config_Docker_Compose_Pentest.yml
```

Pe tablă sau slide, notezi:

- Subnet: `172.20.0.0/24`
- `172.20.0.10` — DVWA (port 80→8888)
- `172.20.0.11` — WebGoat (port 8080→8080)
- `172.20.0.12` — vsftpd 2.3.4 (port 21→2121, port 6200→6200)

### 🎯 Predicție (tipar POE)

> *▸ „Fără să scanați — doar din Compose: câte porturi vă așteptați să fie deschise pe `.12`?"*

Răspunsuri așteptate: 21 și 6200. „De ce 6200? Ce ar putea fi?" — lași suspensia.

> **Epifanie urmărită:** Porturile sunt interfețe ale funcțiilor expuse — fiecare port e o decizie de design (sau o greșeală).

### Ce faci: pornire infrastructură (🔵 PS#1)

```powershell
docker compose -p s13pentest -f .\S13_Part02_Config_Docker_Compose_Pentest.yml up -d
```

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Verificări benigne (🔵 PS#1, pe host)

Headers HTTP (pe Windows, `curl.exe` explicit, ca să evităm alias-ul `Invoke-WebRequest`):

```powershell
curl.exe -I http://localhost:8888/ | Select-Object -First 10
curl.exe -I http://localhost:8080/ | Select-Object -First 10
```

> Banner FTP: pe Windows nu avem `nc` nativ. Facem banner grabbing din tool container (Blocul C).

**Fișiere din kit referite:** `S13_Part02_Config_Docker_Compose_Pentest.yml`, `S13_Part02_Tasks_Pentest.md`

---

## Bloc C — Scanning din tool container (0:12–0:21)

### Ce spui

> *▸ „Un auditor își fixează un mediu de unelte reproductibil. Container-ul de unelte e «trusa» noastră — aceleași versiuni de nmap, curl, netcat, indiferent de ce e instalat pe host."*

### Ce faci (🟢 PS#2)

1. Identifici rețeaua Docker a proiectului:

```powershell
docker network ls | findstr pentest
```

> Apare `s13pentest_pentestnet`.

2. Pornești container-ul de unelte (`nicolaka/netshoot`):

```powershell
docker run --rm -it --network s13pentest_pentestnet nicolaka/netshoot bash
```

> De acum, ești „în interiorul" rețelei Docker.

### 🎯 Predicție (tipar POE)

> *▸ „Vom scana `172.20.0.0/24`. Câte gazde active vă așteptați? Gândiți-vă: trei containere — dar sunt doar trei?"*

### În interiorul containerului (shell Linux)

3. Descoperire de gazde:

```bash
nmap -sn 172.20.0.0/24
```

> Apar mai mult de 3 gazde (.1 gateway, .10, .11, .12, posibil .2). „Gateway-ul Docker e și el o gazdă activă."

4. Scan țintit cu version detection:

```bash
nmap -sV -p 21,80,8080,6200 172.20.0.10
nmap -sV -p 21,80,8080,6200 172.20.0.11
nmap -sV -p 21,80,8080,6200 172.20.0.12
```

5. Banner grabbing FTP (doar conectare + citire banner):

```bash
nc -v 172.20.0.12 21
```

> Apare: `220 (vsFTPd 2.3.4)`. Revii la hook: „Iată bannerul din deschidere."

### 🎯 Capcana de concepție greșită (tipar B)

> *▸ „Port 80 pe `.10` e deschis. Asta înseamnă că e vulnerabil?"*

Răspuns intuitiv: da. Răspuns corect: nu. Un port deschis = un serviciu ascultă. Vulnerabilitatea depinde de **versiune + configurare + context de expunere**.

> **Epifanie urmărită:** Deschis ≠ vulnerabil. Vulnerabilitatea e o funcție de trei variabile, nu de una.

**Fișiere din kit referite:** `S13_Part03_Explanation_Scanning.md`

---

## Bloc D — Scanner TCP minimal în Python (0:21–0:27)

### Ce spui

> *▸ „Înțelegerea mecanismului bate memorarea comenzilor. Scriem un scanner simplu ca să vedem cum arată scanning-ul la nivel de sockets."*

### Ce faci (🟠 PS#3)

Rulezi scriptul într-un container Python (ca să nu depinzi de instalarea locală):

```powershell
docker run --rm -it --network s13pentest_pentestnet -v ${PWD}:/lab python:3.12-slim bash
```

În containerul Python, rulezi pe un set mic de porturi (pentru timp):

```bash
python3 -c "
import socket
TARGET = '172.20.0.12'
for port in [21, 80, 6200, 8080]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    r = s.connect_ex((TARGET, port))
    if r == 0:
        print(f'[OPEN] {port}')
    s.close()
print('Done.')
"
```

> Alternativ, scriptul complet: `python3 /lab/S13_Part04_Script_Simple_Scanner.py`. Avertisment: pe 1024 porturi cu timeout 0.2s, durează ~200 secunde. Oprești cu `Ctrl+C` după primele porturi descoperite.

### 🎯 „Ce s-ar fi întâmplat dacă…?" (tipar D)

> *▸ „Ce se întâmplă dacă pun timeout-ul la 0.01 secunde?"*

Răspuns: false negatives — porturi raportate ca „closed" înainte ca serverul să răspundă.

### Întrebări (închid bucla)

> *▸ „De ce nu detectează versiunile? [nu trimite probe de fingerprinting] De ce nu funcționează pentru UDP? [`connect_ex()` e specific TCP]"*

> **Epifanie urmărită:** Scannerele sunt politici de măsurare: ce trimiți, cât aștepți, cum clasifici răspunsul.

**Fișiere din kit referite:** `S13_Part04_Script_Simple_Scanner.py`, `_HTMLsupport/S13/S13_Part04_Page_S13_A_Simple_Scanner.html`

---

## Bloc E — Enumerare: evidențe → risc → control (0:27–0:33)

### Ce spui

> *▸ „Enumerarea e colectare de evidențe. Nu raportezi «am găsit vulnerabilități» — raportezi ce ai observat, cât de credibil e semnalul și ce control recomanzi."*

### Ce faci (🟢 PS#2, în netshoot)

1. Fingerprinting HTTP — headers:

```bash
curl -I http://172.20.0.10/ | egrep -i 'HTTP/|Server|X-Powered-By' || true
```

2. Enumerare automată cu Nmap Scripting Engine (NSE) pe o singură țintă:

```bash
nmap -sV --script vuln -p 80,8080,21 172.20.0.10
```

> NSE = Nmap Scripting Engine — rulează scripturi de verificare a vulnerabilităților cunoscute.

### Micro-exercițiu (90 secunde, pe tablă)

Trei coloane:

| Observație | Risc | Control |
|---|---|---|
| Port 21 deschis, vsftpd 2.3.4 | Backdoor CVE-2011-2523 | Actualizare versiune / închidere port |
| Header `X-Powered-By: PHP/5.x` | Vulnerabilități cunoscute PHP vechi | Patching PHP / eliminare header |
| *(studentul completează)* | | |

> *▸ „Cine completează a treia linie? Orice observație din scan."*

### Ce spui la output NSE

> *▸ „Un output «vuln» nu e sentință — e semnal. Regula: tool output → triere → confirmare → recomandare."*

**Fișiere din kit referite:** `S13_Part05_Explanation_Vuln_Enumeration.md`, `S13_Part06_Tasks_Vuln_Enumeration.md`

---

## Bloc F — Mini-demo Wireshark: semnătura unui scan (0:33–0:37)

### Scop

Scanning-ul are o „semnătură" de trafic vizibilă în captură. Analiza de pachete e instrumentul defensiv complementar.

### Ce faci

1. În netshoot (🟢 PS#2) sau într-un al doilea netshoot dedicat capturii, pornești `tcpdump`:

Deschizi un netshoot dedicat capturii (🟠 PS#3, sau refolosești):

```powershell
docker run --rm -it --name s13cap --network s13pentest_pentestnet -v ${PWD}:/lab nicolaka/netshoot bash
```

În container (`s13cap`):

```bash
tcpdump -i eth0 -w /lab/s13_scan_demo.pcap &
```

2. În celălalt netshoot (🟢 PS#2), rulezi un scan scurt:

```bash
nmap -sV -p 21,80 172.20.0.10
```

3. Oprești tcpdump (`Ctrl+C` sau `kill %1`).

4. Deschizi `s13_scan_demo.pcap` în Wireshark pe Windows și arăți:

   - Filtru de afișare: `tcp.flags.syn == 1 && tcp.flags.ack == 0` (SYN-urile de inițializare)
   - „Fan-out" — multe SYN-uri către porturi diferite într-un interval scurt

> *▸ „Un IDS (Intrusion Detection System) caută exact acest pattern: multe SYN-uri de la aceeași sursă. Asta e «semnătura» unui scan."*

> Nu insista pe detalii Wireshark — conectezi instrumentarea de interpretarea defensivă.

---

## Bloc G — Recap + temă + preview (0:37–0:40)

### Reluarea hook-ului

> *▸ „La început am văzut un banner: `220 (vsFTPd 2.3.4)`. Acum știm: versiunea 2.3.4 conține un backdoor documentat (CVE-2011-2523), portul 6200 e expus în Compose, nmap confirmă. Doar din 5 cuvinte de banner am putut trage un fir care duce la o vulnerabilitate reală."*

### Ce fixăm (3 idei)

1. **Suprafață de atac = inventar**, nu intuiție. Scanarea o măsoară.
2. **Port deschis ≠ vulnerabil.** Vulnerabilitatea e la intersecția versiune–configurare–expunere.
3. **Evidență → interpretare → control.** Fluxul din partea „științifică" a securității.

### Temă (livrabile din kit)

- **Stage 1:** `S13_Part02_Tasks_Pentest.md` — pornire infrastructură, verificări manuale, log.
- **Stage 2:** `S13_Part04_Tasks_Scanning.md` — nmap complet, scanner Python, comparație, reflecție.
- **Stage 3:** `S13_Part06_Tasks_Vuln_Enumeration.md` — NSE, fingerprinting curl, banner FTP, CVE.

> **Notă:** Task-ul de Stage 3 cere și `nikto`. Studenții pot: (a) rula `docker run --rm -it frapsoft/nikto -h http://172.20.0.10:8888` din PowerShell, sau (b) se limita la nmap NSE + curl manual (rezultate echivalente pentru scopul exercițiului).

> **Etapele 4–5** (exploitation, script Python de exploit) sunt disponibile ca lectură ghidată și exercițiu opțional, cu respectarea cadrului etic.

### Preview S14

> *▸ „La S14 avem evaluarea proiectelor de echipă."*

---

## Cheat-sheet

| Acțiune | Comandă (PowerShell, dacă nu e specificat altfel) |
|---|---|
| Pornire lab | `docker compose -p s13pentest -f .\S13_Part02_Config_Docker_Compose_Pentest.yml up -d` |
| Verificare containere | `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` |
| Oprire lab | `docker compose -p s13pentest -f .\S13_Part02_Config_Docker_Compose_Pentest.yml down -v` |
| Headers HTTP (Windows) | `curl.exe -I http://localhost:8888/ \| Select-Object -First 10` |
| Identificare rețea Docker | `docker network ls \| findstr pentest` |
| Pornire netshoot | `docker run --rm -it --network s13pentest_pentestnet nicolaka/netshoot bash` |
| Descoperire gazde (în netshoot) | `nmap -sn 172.20.0.0/24` |
| Scan țintit (în netshoot) | `nmap -sV -p 21,80,8080,6200 172.20.0.X` |
| Banner FTP (în netshoot) | `nc -v 172.20.0.12 21` |
| Enumerare NSE (în netshoot) | `nmap -sV --script vuln -p 80,8080,21 172.20.0.X` |
| Pornire container Python | `docker run --rm -it --network s13pentest_pentestnet -v ${PWD}:/lab python:3.12-slim bash` |
| Scanner Python (în container) | `python3 /lab/S13_Part04_Script_Simple_Scanner.py` |
| Captură pcap (în netshoot) | `tcpdump -i eth0 -w /lab/s13_scan_demo.pcap` |
| Filtru Wireshark (SYN) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` |

---

## Plan de contingență

| # | Problemă | Remediu rapid |
|---|---|---|
| 1 | **Rețeaua `s13pentest_pentestnet` nu apare** | Verifici că ai rulat `docker compose -p s13pentest ... up -d` din folderul corect. `docker network ls` pentru confirmare. |
| 2 | **`nicolaka/netshoot` nu se descarcă (internet blocat)** | Alternativ: `instrumentisto/nmap` pentru scanare (doar nmap); `curlimages/curl` pentru HTTP fingerprinting. |
| 3 | **Wireshark nu deschide captura** | Verifici că `tcpdump` a rulat suficient timp și că ai generat trafic (nmap). Verifici mărimea fișierului: `ls -la s13_scan_demo.pcap`. |
| 4 | **Porturile host (8080/8888) sunt ocupate** | `netstat -ano \| findstr :8080` → identifici PID → oprești procesul sau schimbi mapping-ul în Compose. |
| 5 | **Scanner Python durează mult (~200s pe 1024 porturi)** | Folosești one-liner-ul cu porturi explicite (4 porturi) sau reduci `PORT_END = 100` în script. |
| 6 | **Docker Desktop nu e pornit** | Pornești Docker Desktop. Aștepți ~30 secunde. Verifici cu `docker version`. |
| 7 | **WebGoat pornește lent (Java, ~30s)** | Pornești Compose cu 2–3 minute înainte de seminar. Verifici cu `docker logs webgoat --tail 5`. |

---

## Referințe

Alhamed, M., & Rahman, M. M. H. (2023). A systematic literature review on penetration testing in networks: Future research directions. *Applied Sciences, 13*(12), 6986. https://doi.org/10.3390/app13126986

Holm, H. (2012). Performance of automated network vulnerability scanning at remediating security issues. *Computers & Security, 31*(2), 164–175. https://doi.org/10.1016/j.cose.2011.12.014

Deepa, G., & Santhi Thilagam, P. (2016). Securing web applications from injection and logic vulnerabilities: Approaches and challenges. *Information and Software Technology, 74*, 160–180. https://doi.org/10.1016/j.infsof.2016.02.005

Bagyalakshmi, G., Rajkumar, G., Arunkumar, N., Easwaran, M., Narasimhan, K., Elamaran, V., Solarte, M., Hernández, I., & Ramirez-Gonzalez, G. (2018). Network vulnerability analysis on brain signal/image databases using Nmap and Wireshark tools. *IEEE Access, 6*, 57144–57151. https://doi.org/10.1109/ACCESS.2018.2872775

Neu, C. V., Tatsch, C. G., Lunardi, R. C., Michelin, R. A., Orozco, A. M. S., & Zorzo, A. F. (2018). Lightweight IPS for port scan in OpenFlow SDN networks. In *2018 IEEE/IFIP Network Operations and Management Symposium (NOMS)*. https://doi.org/10.1109/NOMS.2018.8406313

---

## Note pedagogice

**Tipare socratice folosite:**
- POE (Predicție-Observație-Explicație): Bloc B (câte porturi pe `.12`?), Bloc C (câte gazde active?).
- Capcana de concepție greșită: Bloc C (port deschis = vulnerabil? — nu).
- „Ce s-ar fi întâmplat dacă…?": Bloc D (timeout 0.01 secunde).

**Concepții greșite vizate:**
- „Port deschis = vulnerabil" — Bloc C.
- „nmap arată totul" — Bloc D (scannerul Python ilustrează limitările).
- „Un banner spune adevărul" — Bloc E implicit (banner-ul poate fi falsificat).

**Momente de epifanie:**
- Bloc B: Porturile sunt interfețe ale funcțiilor expuse.
- Bloc C: Deschis ≠ vulnerabil.
- Bloc D: Scannerele sunt politici de măsurare.

**Diferențe specifice față de varianta MININET-SDN:**
- Toate uneltele CLI (nmap, nc, curl, tcpdump) rulează în containere, nu pe host.
- Banner grabbing FTP se face din netshoot, nu cu `nc` pe host.
- Bloc F adaugă o mini-demo Wireshark (avantaj Windows: Wireshark nativ, cu GUI).
- Containerul Python (`python:3.12-slim`) înlocuiește Python-ul din VM.

**Cross-referințe:**
- De la S12: RPC — servicii expuse pe porturi → acum inversăm perspectiva.
- De la S07: Captură de pachete, filtrare TCP → semnătura unui scan.
- Spre S14: Evaluarea proiectelor de echipă.

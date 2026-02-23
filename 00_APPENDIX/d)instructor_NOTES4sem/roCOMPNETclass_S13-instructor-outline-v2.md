# Seminar S13 — Scanning și enumerarea vulnerabilităților

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (claudev11) |
| **Infra** | MININET-SDN (VM Ubuntu 24.04, VirtualBox) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un port deschis nu este o vulnerabilitate; vulnerabilitatea apare la intersecția dintre versiune, configurare și context de expunere — iar măsurarea e primul pas. |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. **Porni** o infrastructură de laborator cu Docker Compose și **verifica** funcționalitatea minimă a serviciilor (HTTP/FTP) prin metode benigne (`curl -I`, `nc`).
2. **Executa** un scan de descoperire și un scan țintit cu `nmap` într-o rețea izolată, apoi **interpreta** output-ul: IP → port → serviciu/versiune.
3. **Rula** un scanner TCP minimal în Python și **explica** de ce nu detectează UDP, nu identifică versiuni și depinde de timeout.
4. **Colecta** evidențe prin enumerare (Nmap Scripting Engine, headers HTTP) și **formula** un triplet observație–risc–control.
5. **Distinge** între scanning (inventar de suprafață) și exploatare (acces neautorizat), pe baza cadrului etic prezentat.
6. **Conecta** semnalele observate (banner vechi, port backdoor) cu decizii defensive concrete (patching, segmentare, monitorizare).

---

## Structura seminarului

| Bloc | Conținut | Durată | Tip |
|---|---|---:|---|
| A | Hook + cadru etic + activare cunoștințe | 4 min | interactiv |
| B | Model mental al laboratorului (Compose + topologie) | 4 min | demo + predicție |
| C | Pornire infrastructură + verificări minimale | 7 min | demo + observație |
| D | Scanning cu `nmap` (descoperire + scan țintit) | 9 min | demo + predicție |
| E | Scanner TCP minimal în Python | 7 min | demo + întrebări |
| F | Enumerare: evidențe → risc → control | 6 min | demo + micro-exercițiu |
| G | Recap + temă + preview S14 | 3 min | interactiv |
| **Total** | | **40 min** | |

---

## Bloc A — Hook + cadru etic + activare (0:00–0:04)

### Hook (situat, afectiv)

> *▸ „Deschid un terminal și scriu o singură comandă: `nc -v 127.0.0.1 2121`. Apare un banner: `220 (vsFTPd 2.3.4)`. Cine poate spune, doar din aceste 5 cuvinte, dacă mașina e vulnerabilă sau nu? Și dacă da — la ce anume?"*

Lași 5–10 secunde de gândire. Nu dai răspunsul.

> *▸ „Păstrați răspunsul vostru — revenim la el la final. Poate vă surprinde ce aflăm."*

### Cadru etic (30 secunde, ferm)

> *▸ „Tot ce facem astăzi se întâmplă strict în containere Docker locale. Aceleași tehnici, aplicate pe un sistem fără consimțământ, sunt infracțiune. Nu simplific — e Codul Penal, art. 360."*

Proiectezi 10 secunde din paragraful de avertizare din `S13_Part01_Explanation_Pentest_Intro.md`.

### Activare cunoștințe (legătura cu S12)

> *▸ „La S12 am lucrat cu RPC — am expus servicii pe porturi. Astăzi inversăm perspectiva: cum descoperi ce porturi sunt deschise, ce servicii rulează și ce versiuni au — din postura cuiva care nu știe nimic despre rețea."*

**Fișiere din kit referite:** `S13_Part01_Explanation_Pentest_Intro.md`

---

## Bloc B — Model mental al laboratorului (0:04–0:08)

### Ce faci (🔵 Terminal A)

Deschizi Compose-ul și îl parcurgi ca pe o schemă de rețea:

```bash
cat S13_Part02_Config_Docker_Compose_Pentest.yml
```

> Fișierul are 48 de linii — se vede integral.

### Ce subliniezi (pe tablă sau slide, spus rar)

- Subnet: `172.20.0.0/24`
- Ținte:
  - `172.20.0.10` — DVWA (HTTP intern pe port 80, mapat la host 8888)
  - `172.20.0.11` — WebGoat (HTTP intern pe port 8080, mapat la host 8080)
  - `172.20.0.12` — vsftpd 2.3.4 (FTP intern pe port 21, mapat la host 2121; port 6200 mapat la host 6200)

### 🎯 Predicție (tipar POE)

> *▸ „Fără să scanați — doar din ce vedeți în Compose: câte porturi vă așteptați să fie deschise pe `172.20.0.12`? Care anume?"*

Răspunsuri așteptate: 21 și 6200. Unii pot spune „doar 21" — notezi ambele pe tablă, revii după scan.

> **Epifanie urmărită:** Porturile nu sunt accidentale; sunt *interfețe ale funcțiilor expuse* — fiecare port e o decizie de design (sau o greșeală).

**Fișiere din kit referite:** `S13_Part02_Config_Docker_Compose_Pentest.yml`

---

## Bloc C — Pornire infrastructură + verificare minimă (0:08–0:15)

### Ce spui

> *▸ „Într-un audit, primul artefact e un log: ce ai pornit, ce versiuni, ce ai observat. Verificarea minimă precedă orice scan."*

### Ce faci (🔵 Terminal A)

1. Pornești serviciile:

```bash
docker compose -p s13pentest -f S13_Part02_Config_Docker_Compose_Pentest.yml up -d
```

2. Verifici containerele:

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

> Arăți studenților mapping-ul de porturi: `0.0.0.0:8888->80/tcp`, `0.0.0.0:2121->21/tcp`, `0.0.0.0:6200->6200/tcp`.

### Verificări benigne (🟢 Terminal B)

3. Headers HTTP (fără login, fără payload):

```bash
curl -I http://localhost:8888/ | head
curl -I http://localhost:8080/ | head
```

4. Banner FTP (doar conectare, citire banner, `Ctrl+C`):

```bash
nc -v 127.0.0.1 2121
```

> Apare: `220 (vsFTPd 2.3.4)`. Revii la hook-ul de la Bloc A: „Iată bannerul din hook."

### Întrebări de ghidaj

> *▸ „Ce informație de securitate obținem din banner? [versiune, tehnologie, indiciu de vechime] De ce e relevant că serviciile sunt mapate și pe host?"*

**Fișiere din kit referite:** `S13_Part02_Config_Docker_Compose_Pentest.yml`, `S13_Part02_Tasks_Pentest.md` (metodă replicată în temă)

---

## Bloc D — Scanning cu `nmap` (0:15–0:24)

### Ce spui

> *▸ „Scopul scanning-ului: răspundem la întrebarea «ce servicii sunt expuse și cu ce indicii de versiune». Nu bifăm comenzi."*

### 🎯 Predicție înainte de execuție (tipar POE)

> *▸ „Vom scana `172.20.0.0/24`. Câte gazde active vă așteptați? Gândiți-vă: trei containere — dar sunt doar trei?"*

### Ce faci (🟢 Terminal B)

1. Descoperire de gazde:

```bash
nmap -sn 172.20.0.0/24
```

> Apar mai mult de 3 gazde: .1 (gateway), .10, .11, .12 — posibil și .2 (Docker DNS). „Surpriză — gateway-ul Docker e și el o gazdă activă."

2. Scan țintit cu version detection (pentru timp — **nu** `-p-`):

```bash
nmap -sV -p 21,80,8080,6200 172.20.0.10
nmap -sV -p 21,80,8080,6200 172.20.0.11
nmap -sV -p 21,80,8080,6200 172.20.0.12
```

### Ce subliniezi la output

> *▸ „Observați triada: IP → port → serviciu/versiune. Într-un raport, asta devine «attack surface inventory»."*

### 🎯 Capcana de concepție greșită (tipar B)

> *▸ „Port 80 pe `.10` e deschis. Asta înseamnă că e vulnerabil?"*

Răspuns intuitiv: da. Răspuns corect: nu — un port deschis înseamnă „un serviciu ascultă". Vulnerabilitatea depinde de **versiune + configurare + context de expunere**.

> **Epifanie urmărită:** „Deschis ≠ vulnerabil. Vulnerabilitatea e o funcție de trei variabile, nu de una."

### Mini-activitate (60 secunde)

> *▸ „Alegeți o linie din output. Formulați o frază de raport: «Host X expune serviciul Y pe portul Z; versiunea indică …; risc potențial …»."*

**Fișiere din kit referite:** `S13_Part03_Explanation_Scanning.md` (teorie), `S13_Part04_Tasks_Scanning.md` (temă)

---

## Bloc E — Scanner TCP minimal în Python (0:24–0:31)

### Ce spui

> *▸ „`nmap` ascunde mecanismul. Ca să înțelegeți cu adevărat ce înseamnă «open», «closed», «filtered» — construiți un scanner minimal."*

### Ce faci (🟢 Terminal B)

1. Arăți scheletul scriptului:

```bash
cat S13_Part04_Script_Simple_Scanner.py
```

> Fișierul are 55 de linii. Subliniezi: `connect_ex()` returnează 0 dacă portul e deschis; `settimeout(0.2)` limitează așteptarea.

2. Rulezi pe o singură țintă, dar cu **range redus** (pentru timp):

```bash
python3 -c "
import socket, sys
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

> Alternativ, dacă preferi scriptul complet: `python3 S13_Part04_Script_Simple_Scanner.py`. Avertisment: pe 1024 porturi cu timeout 0.2s, durează ~200 secunde. Oprești cu `Ctrl+C` după câteva porturi descoperite, sau modifici `PORT_END = 100` direct în fișier.

### 🎯 „Ce s-ar fi întâmplat dacă…?" (tipar D)

> *▸ „Ce se întâmplă dacă pun timeout-ul la 0.01 secunde? Dar la 5 secunde?"*

Răspuns: timeout mic → false negatives (porturi raportate ca „closed" înainte ca serverul să răspundă). Timeout mare → scan lent.

### Întrebări (închid bucla)

> *▸ „De ce scannerul nostru nu poate identifica versiunile? [nu trimite probe de fingerprinting, nu analizează banner-ul] De ce nu funcționează pentru UDP? [`connect_ex()` e specific TCP — UDP e connectionless]"*

> **Epifanie urmărită:** Scannerele sunt *politici de măsurare*: ce trimiți, cât aștepți, cum clasifici răspunsul.

**Fișiere din kit referite:** `S13_Part04_Script_Simple_Scanner.py`, `S13_Part03_Explanation_Scanning.md`, `_HTMLsupport/S13/S13_Part04_Page_S13_A_Simple_Scanner.html` (resurse suplimentare pentru studiu individual)

---

## Bloc F — Enumerare: evidențe → risc → control (0:31–0:37)

### Ce spui

> *▸ „Enumerarea înseamnă colectare de evidențe. Nu raportezi «am găsit vulnerabilități» — raportezi ce ai observat, cât de credibil e semnalul și ce control recomanzi."*

### Ce faci (🟢 Terminal B)

1. Fingerprinting HTTP — headers:

```bash
curl -I http://localhost:8888/ | egrep -i 'HTTP/|Server|X-Powered-By' || true
```

> Arăți: `Server: Apache/...`, `X-Powered-By: PHP/...`. Versiuni vechi = indiciu, nu verdict.

2. Enumerare automată cu Nmap Scripting Engine (NSE) pe o singură țintă:

```bash
nmap -sV --script vuln -p 80,8080,21 172.20.0.10
```

> NSE = Nmap Scripting Engine — prima expansiune a acronimului. Rulează scripturi de verificare a vulnerabilităților cunoscute (http-enum, ftp-vsftpd-backdoor etc.).

### Micro-exercițiu (90 secunde, pe tablă)

Scrii trei coloane:

| Observație | Risc | Control |
|---|---|---|
| Port 21 deschis, vsftpd 2.3.4 | Backdoor CVE-2011-2523 | Actualizare versiune / închidere port |
| Header `X-Powered-By: PHP/5.x` | Vulnerabilități cunoscute PHP vechi | Patching PHP / eliminare header |
| *(studentul completează)* | | |

> *▸ „Cine completează a treia linie? Orice observație din scan-ul de adineauri."*

### Ce spui la output NSE

> *▸ „Un output de tip «vuln» nu e sentință — e semnal. Regula: tool output → triere → confirmare → recomandare."*

**Fișiere din kit referite:** `S13_Part05_Explanation_Vuln_Enumeration.md`, `S13_Part06_Tasks_Vuln_Enumeration.md` (temă)

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
- **Stage 2:** `S13_Part04_Tasks_Scanning.md` — nmap complet (-p-), scanner Python, comparație cu nmap, reflecție open/closed/filtered.
- **Stage 3:** `S13_Part06_Tasks_Vuln_Enumeration.md` — NSE scan complet, fingerprinting cu curl, banner FTP, identificare CVE.

> **Notă:** Task-ul de Stage 3 cere și `nikto`. Dacă `nikto` nu e instalat pe VM, studenții pot: (a) instala cu `sudo apt install -y nikto`, (b) folosi `docker run --rm -it frapsoft/nikto -h http://172.20.0.10`, sau (c) se limita la nmap NSE + curl manual (rezultate echivalente pentru scopul exercițiului).

> **Etapele 4–5** (exploitation, script Python de exploit) sunt disponibile ca lectură ghidată și exercițiu opțional, cu respectarea cadrului etic discutat.

### Preview S14

> *▸ „La S14 avem evaluarea proiectelor de echipă. Pregătiți-vă demonstrațiile."*

---

## Cheat-sheet

| Acțiune | Comandă |
|---|---|
| Pornire lab | `docker compose -p s13pentest -f S13_Part02_Config_Docker_Compose_Pentest.yml up -d` |
| Verificare containere | `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'` |
| Oprire lab | `docker compose -p s13pentest -f S13_Part02_Config_Docker_Compose_Pentest.yml down -v` |
| Headers HTTP | `curl -I http://localhost:8888/ \| head` |
| Banner FTP | `nc -v 127.0.0.1 2121` |
| Descoperire gazde | `nmap -sn 172.20.0.0/24` |
| Scan țintit + versiuni | `nmap -sV -p 21,80,8080,6200 172.20.0.X` |
| Enumerare NSE | `nmap -sV --script vuln -p 80,8080,21 172.20.0.X` |
| Scanner Python | `python3 S13_Part04_Script_Simple_Scanner.py` |
| Fingerprinting HTTP | `curl -I http://localhost:8888/ \| egrep -i 'Server\|X-Powered-By'` |

---

## Plan de contingență

| # | Problemă | Remediu rapid |
|---|---|---|
| 1 | **Portul 8080 sau 8888 ocupat pe VM** | `sudo ss -lntp \| egrep ':8080\|:8888'` → identifici procesul → oprești sau schimbi mapping-ul în Compose. |
| 2 | **Containere rămase din rulări anterioare** | `docker compose -p s13pentest -f S13_Part02_Config_Docker_Compose_Pentest.yml down -v` și repornești. |
| 3 | **`nmap` nu e instalat** | `sudo apt update && sudo apt install -y nmap` — o singură dată. |
| 4 | **Scanarea completă (`-p-`) durează în clasă** | Folosești scan țintit: `-p 21,80,8080,6200`. Scan complet rămâne temă. |
| 5 | **Scanner Python durează mult (~200s pe 1024 porturi)** | Reduci range-ul: `PORT_END = 100` sau folosești one-liner-ul cu porturi explicite din Bloc E. |
| 6 | **DVWA cere inițializare la prima pornire** | Deschizi `http://localhost:8888/setup.php` în browser, dai click pe „Create / Reset Database". Durează 10 secunde. |
| 7 | **WebGoat pornește lent (Java, ~30s)** | Pornești Compose cu 2–3 minute înainte de seminar. Verifici cu `docker logs webgoat --tail 5` — aștepți „Started WebGoat". |

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
- POE (Predicție-Observație-Explicație): Bloc B (câte porturi pe `.12`?), Bloc D (câte gazde active?).
- Capcana de concepție greșită: Bloc D (port deschis = vulnerabil? — nu).
- „Ce s-ar fi întâmplat dacă…?": Bloc E (timeout 0.01 vs. 5 secunde).

**Concepții greșite vizate:**
- „Port deschis = vulnerabil" — Bloc D.
- „nmap arată totul" — Bloc E (scannerul Python ilustrează limitările; nmap le are pe ale lui).
- „Un banner spune adevărul" — Bloc F implicit (banner-ul poate fi falsificat; e indiciu, nu verdict).

**Momente de epifanie:**
- Bloc B: Porturile sunt interfețe ale funcțiilor expuse.
- Bloc D: Deschis ≠ vulnerabil.
- Bloc E: Scannerele sunt politici de măsurare.

**Cross-referințe:**
- De la S12: RPC — servicii expuse pe porturi → acum inversăm perspectiva.
- De la S07: Captură de pachete, filtrare TCP → acum capturile pot arăta „semnătura" unui scan.
- Spre S14: Evaluarea proiectelor de echipă.

# Seminar S11 — Reverse proxy și load balancing cu Docker Compose

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (claudev11) — `04_SEMINARS/S11/` |
| **Infra** | Windows nativ + Docker Desktop + Wireshark |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un load balancer nu „pasează" conexiunea — el o termină și deschide alta; observăm asta concret, cu Nginx (declarativ) și cu Python (procedural). |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. **Explica** diferența dintre *forward proxy* și *reverse proxy*, indicând direcția fluxului și cine e „reprezentat" de fiecare.
2. **Rula** un stack Docker Compose cu Nginx ca reverse proxy în fața a 3 backend-uri HTTP și **observa** distribuția round-robin a cererilor.
3. **Localiza** în configurația Nginx blocurile `upstream` și `proxy_pass` și **anticipa** ce trebuie modificat la adăugarea unui backend.
4. **Descrie** funcționarea internă a unui load balancer scris în Python (socket accept → select backend → connect → forward → relay) și **identifica** limitele sale față de Nginx.
5. **Demonstra** într-un pcap că load balancer-ul creează o a doua conexiune TCP (Transmission Control Protocol), separată de cea a clientului.
6. **Compara** comportamentul celor două soluții când un backend cade — cu și fără health checks.

---

## Structura seminarului

| Minute | Bloc | Ce se întâmplă | Tipar |
|---:|---|---|---|
| 0–3 | **A** — Hook + predicții | Scenariu: serverul nu mai face față; studenții prezic ce face un LB | POE |
| 3–8 | **B** — Micro-teorie | Reverse proxy, upstream, round robin — desen + întrebare SPOF | expozitiv + întrebare |
| 8–20 | **C** — Demo 1: Nginx Compose | Pornire stack, test rotație, citire config, failure test | POE × 2 |
| 20–22 | **C′** — Curățare Part01 | Oprire stack Nginx | procedural |
| 22–33 | **D** — Demo 2: custom LB (Python) | Naming/DNS, pornire stack, test rotație, failure test | conflict cognitiv + POE |
| 33–37 | **E** — Captură pcap + Wireshark | tcpdump din container, deschidere în Wireshark GUI | epifanie vizuală |
| 37–40 | **F** — Recap + teme | 3 idei fixate, hook reluat, task-uri | sinteză |

**Total:** 40 min.

---

## Pregătire înainte de seminar (instructor)

### Checklist software (Windows)

1. Docker Desktop — **Running** (icon verde în system tray).
2. Verificare rapidă (PowerShell):
   ```powershell
   docker --version
   docker compose version
   ```
3. Wireshark instalat (Npcap prezent).
4. Repo disponibil local; exemplu:
   ```powershell
   cd D:\COMPNET\compnet-2025-redo\04_SEMINARS\S11
   dir
   ```
   *(Adaptează calea la locația reală a kit-ului extras pe stația de lucru.)*

5. Pre-pull imagini (evită așteptare la clasă):
   ```powershell
   docker pull nginx:latest
   docker pull python:3.11-alpine
   docker pull nicolaka/netshoot:latest
   ```

### Notă PowerShell: `curl` vs. `curl.exe`

În PowerShell, `curl` e alias pentru `Invoke-WebRequest`. Pe tot parcursul seminarului, folosim **`curl.exe`** (clientul clasic). Menționează asta studenților o singură dată; nu reveni.

### Decizie pre-seminar: naming mismatch

Scriptul `S11_Part02_Script_Simple_Lb.py` are `BACKENDS = [("web1", 8000), ...]`, dar compose-ul din Part02 definește serviciile ca `web1-lb`, `web2-lb`, `web3-lb`. Discrepanța e deliberată — didactică. Dacă vrei să eviți debugging live, editează `BACKENDS` înainte de seminar.

---

## Bloc A (0–3 min) — Hook: „Serverul nu mai face față"

> *▸ „Aveți o aplicație web. Într-o luni dimineață, traficul se triplează. Serverul răspunde cu 5 secunde latență, apoi cade. Întrebarea: cum păstrați aceeași adresă publică, dar puneți mai multe servere în spate?"*

**Ce faci:**
- 30 sec tăcere reală — fiecare notează o predicție.
- 2–3 răspunsuri scurte. Notezi pe tablă: *distribuie*, *ascunde*, *reziliență*.

> *▸ „Țineți minte predicțiile voastre — revin la ele la final."*

---

## Bloc B (3–8 min) — Micro-teorie: reverse proxy, upstream, round robin

> *▸ „Reverse proxy = un server care primește cereri în locul backend-urilor. Clientul vede o singură adresă; proxy-ul decide cui trimite cererea."*

> *▸ „Upstream = grupul de backend-uri din spatele proxy-ului."*

> *▸ „Load balancing = regula de selecție. Azi vedem round robin — cea mai simplă: fiecare cerere merge la următorul backend, ciclic."*

> *▸ „Comparăm două abordări: Nginx (produs matur) și un script Python (didactic, minimal)."*

**Desen rapid:**
```
curl.exe / Browser  ──►  [ Reverse proxy ]  ──►  web1 :8000
                                             ──►  web2 :8000
                                             ──►  web3 :8000
```

**Întrebare (10 sec):**
> *▸ „Unde e acum punctul unic de eșec?"*

Răspuns așteptat: reverse proxy-ul. Confirmi scurt: „în producție se replică și pe el — dincolo de seminarul de azi."

**Legătură cu S10:** „La S10 ați orchestrat containere cu Docker Compose și ați văzut cum serviciile se găsesc prin DNS intern. Azi construim pe baza aceluiași mecanism."

---

## Bloc C (8–20 min) — Demo 1: Nginx reverse proxy + 3 backend-uri

### C.1 Pornire stack (2 min)

> *▸ „Pornim stack-ul. Un singur port expus către exterior: 8080. Backend-urile ascultă pe 8000, dar doar în rețeaua Docker internă."*

🔵 **PowerShell — Terminal 1 (STACK):**
```powershell
cd D:\COMPNET\compnet-2025-redo\04_SEMINARS\S11\1_nginx-compose
dir

docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml up --build
```

Urmărești în loguri: `nginx-proxy`, `web1`, `web2`, `web3`.

**Predicție privind concepția greșită #5 (porturi auto-expuse):**
> *▸ „Putem accesa direct web1 pe portul 8000 din browser? De ce nu?"*

Răspuns: nu — `expose` nu mapează pe host. Doar Nginx, cu `ports: 8080:80`, e accesibil din exterior.

### C.2 Test round robin (4–5 min)

> *▸ „Trimitem 6 cereri. Predicție: răspund toate trei backend-urile, sau doar unul?"*

Cere ridicare de mână.

🟢 **PowerShell — Terminal 2 (CLIENT):**
```powershell
for ($i=1; $i -le 6; $i++) {
  "---- cerere $i ----"
  curl.exe -s http://localhost:8080 | Select-Object -First 5
}
```

**Output așteptat (din HTML-urile din kit):**
```
<h1>Seminar 11 — Backend server WEB1</h1>
...
<h1>Seminar 11 — Backend server WEB2</h1>
...
<h1>Seminar 11 — Backend server WEB3</h1>
```

**☀️ Epifanie:**
> *▸ „Load balancing-ul nu e abstract — îl observați direct în conținutul răspunsului."*

### C.3 Citire ghidată: unde sunt backend-urile? (4–5 min)

> *▸ „Deschideți configurația și găsiți două lucruri: unde se definesc backend-urile și unde are loc forwarding-ul."*

🔵 **Pe proiector:**
```powershell
Get-Content .\S11_Part01_Config_Nginx.conf
```

**Ce punctezi:**
- `upstream backend_pool { server web1:8000; ... }` — lista de backend-uri
- `proxy_pass http://backend_pool;` — directiva care trimite cererea către upstream
- `proxy_set_header X-Real-IP $remote_addr;` — proxy-ul transmite IP-ul clientului original

**Întrebare (10 sec):**
> *▸ „Dacă adaug al patrulea backend, ce modific?"*

Răspuns: upstream + compose.

**Referință kit:** detalii în `S11_Part01A_Explanation_Reverse_Proxy_Intro.md` și `S11_Part01B_Explanation_Nginx_Compose_Setup.md`.

### C.4 Failure test (3–4 min)

**Predicție (POE):**
> *▸ „Oprim web2. Trei variante: (a) erori 502, (b) Nginx evită automat, (c) totul cade. Ce credeți?"*

🟢 **Terminal 2:**
```powershell
docker stop web2

for ($i=1; $i -le 8; $i++) {
  "---- cerere $i ----"
  curl.exe -s -i http://localhost:8080 | Select-Object -First 8
}
```

**Rezultat posibil:** Nginx detectează backend-ul mort. Studenții văd fie numai web1/web3, fie un 502 urmat de răspunsuri corecte.

> *▸ „Observația voastră e cea care contează. Nginx are mecanisme de retry și marcare a serverelor ca down. Scriptul Python, pe care îl vedem imediat, nu are nimic din astea."*

```powershell
docker start web2
```

---

## Bloc C′ (20–22 min) — Curățare Part01

> *▸ „Oprim stack-ul Nginx — avem nevoie de portul 8080 pentru al doilea demo."*

🔵 **Terminal 1:** `Ctrl+C`, apoi:
```powershell
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml down
```

---

## Bloc D (22–33 min) — Demo 2: custom load balancer (Python)

### D.1 Setarea scenei (1 min)

> *▸ „Nginx e un produs matur. Acum facem același lucru cu un script de ~100 de linii. Scopul: să vedeți mecanic ce face un LB — primește cererea, alege un backend, deschide o conexiune nouă, transmite, returnează."*

```powershell
cd ..\2_custom-load-balancer
dir
```

### D.2 Conflict cognitiv: DNS / naming în Compose (3–4 min)

> *▸ „În Docker Compose, numele serviciului devine DNS intern. Dacă în cod scriu `web1`, dar serviciul se cheamă `web1-lb`, nu se rezolvă."*

🔵 **Pe proiector:**
```powershell
Get-Content .\S11_Part02_Config_Docker_Compose_Lb_Custom.yml
"---"
Get-Content .\S11_Part02_Script_Simple_Lb.py | Select-Object -First 20
```

**Ce arăți:** compose: `web1-lb`, `web2-lb`, `web3-lb`; script: `("web1", 8000)`.

**Mini-exercițiu (30 sec):**
> *▸ „Fixul corect: (a) redenumesc serviciile în compose, sau (b) corectez lista BACKENDS din script. Care e mai rapidă?"*

Răspuns: (b). Deschizi editorul:
```powershell
notepad .\S11_Part02_Script_Simple_Lb.py
```

Modifici:
```python
BACKENDS = [("web1-lb", 8000), ("web2-lb", 8000), ("web3-lb", 8000)]
```
Salvezi.

> *▸ „Lecția: într-un sistem distribuit, dacă un nume nu se rezolvă, nu ai conectivitate."*

**Referință kit:** `S11_Part02A_Explanation_Custom_Lb.md` detaliază ce face și ce lipsește din script.

### D.3 Pornire stack custom LB (2 min)

> *▸ „Pornim. Urmăriți logurile: LB-ul afișează explicit către ce backend trimite."*

🔵 **Terminal 1:**
```powershell
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml up --build
```

**Predicție scurtă:**
> *▸ „Vedem în loguri backend-ul ales?"*

### D.4 Test round robin (3–4 min)

🟢 **Terminal 2:**
```powershell
for ($i=1; $i -le 6; $i++) {
  "---- cerere $i ----"
  curl.exe -s http://localhost:8080 | Select-Object -First 5
}
```

**Output așteptat:**
```
<h1>Seminar 11 — Custom LB backend WEB1</h1>
...
<h1>Seminar 11 — Custom LB backend WEB2</h1>
...
```

**Loguri lb-custom (terminal 1):**
```
[INFO] ('172.18.0.1', 49566) -> web1-lb:8000
[INFO] ('172.18.0.1', 49570) -> web2-lb:8000
```

**☀️ Epifanie:**
> *▸ „În Nginx, politica e declarativă: `upstream { ... }` în config. În Python, politica e procedurală: `backend_index`, modulo, o variabilă globală. Aceeași idee, două paradigme."*

### D.5 Failure test (2–3 min)

**Predicție (POE):**
> *▸ „Oprim web2-lb. La Nginx am văzut [ce ați observat]. Acum? Scriptul Python are health checks?"*

🟢 **Terminal 2:**
```powershell
docker stop web2-lb

for ($i=1; $i -le 6; $i++) {
  "---- cerere $i ----"
  curl.exe -s -i http://localhost:8080 | Select-Object -First 12
}
```

**Rezultat:** fiecare a treia cerere eșuează — `ConnectionRefused` în loguri.

> *▸ „Scriptul trimite orbește. Asta e diferența între un prototip și un produs."*

**Referință kit:** tabelul comparativ în `S11_Part02C_Explanation_Lb_Comparison.md`.

---

## Bloc E (33–37 min) — Captură pcap + Wireshark

### E.1 Generare pcap cu netshoot (2–3 min)

> *▸ „Nu capturăm de pe interfața Windows — loopback-ul poate fi problematic. Capturăm din interiorul containerului, apoi deschidem fișierul în Wireshark."*

🟠 **PowerShell — Terminal 3 (CAPTURĂ):**
```powershell
New-Item -ItemType Directory -Force captures | Out-Null

docker run --rm --net=container:lb-custom `
  -v "${PWD}\captures:/captures" `
  nicolaka/netshoot `
  tcpdump -i eth0 -w /captures/lb_upstream.pcap port 8000
```

🟢 **Terminal 2 (în paralel):**
```powershell
for ($i=1; $i -le 5; $i++) { curl.exe -s http://localhost:8080 > $null }
```

Oprești tcpdump cu `Ctrl+C` (terminal 3).

### E.2 Deschidere în Wireshark (1–2 min)

Wireshark → *File → Open* → `captures\lb_upstream.pcap`.

**Ghidaj în 3 pași:**

> *▸ „Pas 1: Filtru `tcp.port == 8000`. Pas 2: Selectați un pachet HTTP GET — uitați-vă la Request URI. Pas 3: Observați IP-urile sursă și destinație: sunt adrese interne Docker."*

**☀️ Epifanie (fraza centrală):**
> *▸ „Load balancer-ul nu «pasează» conexiunea clientului. El termină conexiunea cu clientul și deschide una nouă către backend. E un intermediar activ — exact ce spune RFC 7230 §2.3 despre intermediaries."*

---

## Bloc F (37–40 min) — Recap + teme

### Recap: 3 idei fixate

> *▸ „Trei lucruri de reținut:"*
> 1. *„Reverse proxy = ascunde backend-urile; clientul vede o singură adresă."*
> 2. *„Nginx e declarativ și are health checks; scriptul Python e procedural și orb."*
> 3. *„LB-ul nu pasează conexiunea — o rupe în două. Ați văzut asta în pcap."*

### Reluare hook

> *▸ „La început v-am întrebat: cum păstrați aceeași adresă și puneți servere în spate? Acum aveți răspunsul: un reverse proxy cu upstream. Și ați văzut ce se întâmplă când prototipul nu are reziliență."*

### Teme

> *▸ „Nu vreau eseuri. Comenzi rulate, output relevant, concluzii scurte."*

**Task-uri din kit:**
- `1_nginx-compose\S11_Part01C_Tasks_Nginx.md`
- `2_custom-load-balancer\S11_Part02B_Tasks_Custom_Lb.md`
- `2_custom-load-balancer\S11_Part02D_Tasks_Lb_Compose.md`

**Fișiere livrabile:**

| Fișier | Ce conține |
|---|---|
| `reverse_proxy_intro_findings.txt` | Diferența forward/reverse proxy, diagramă ASCII, avantaje LB |
| `nginx_round_robin_log.txt` | Output curl cu 3 backend-uri + output cu web2 oprit + reflecții |
| `lb_custom_output.txt` | Output curl custom LB + failure test + reflecții |
| `lb_compose_comparison.txt` | Comenzi, output-uri, 1 similaritate, 2 diferențe, 1 limitare |

**Material suplimentar de studiu (din kit):**
- `S11_Part01A_Explanation_Reverse_Proxy_Intro.md` — teorie reverse proxy
- `S11_Part02C_Explanation_Lb_Comparison.md` — tabel comparativ detaliat
- `_HTMLsupport\S11\` — simulatoare interactive (Nginx și custom LB)

**Legătură S12:**
> *▸ „La S12 trecem de la HTTP la RPC (Remote Procedure Call) — un alt mod de comunicare între servicii distribuite."*

---

## Curățare (post-seminar)

🔵 **Terminal 1:** `Ctrl+C`, apoi:
```powershell
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml down

docker ps   # trebuie gol
```

---

## Cheat-sheet

### Comenzi Docker Compose (PowerShell)

| Acțiune | Comandă |
|---|---|
| Pornire stack (cu rebuild) | `docker compose -f <fișier>.yml up --build` |
| Oprire stack + ștergere containere | `docker compose -f <fișier>.yml down` |
| Oprire un container | `docker stop <nume>` |
| Repornire container | `docker start <nume>` |
| Loguri container | `docker logs <nume>` |
| Listare containere | `docker ps` |

### Testare (PowerShell)

| Acțiune | Comandă |
|---|---|
| Cerere HTTP (scurt) | `curl.exe -s http://localhost:8080` |
| Cerere HTTP (cu headere) | `curl.exe -s -i http://localhost:8080` |
| Buclă 6 cereri | `for ($i=1; $i -le 6; $i++) { curl.exe -s http://localhost:8080 }` |

### Captură și analiză (PowerShell)

| Acțiune | Comandă |
|---|---|
| Captură din container | ``docker run --rm --net=container:<c> -v "${PWD}\captures:/captures" nicolaka/netshoot tcpdump -i eth0 -w /captures/f.pcap port 8000`` |
| Wireshark | Deschide `captures\lb_upstream.pcap` → filtru `tcp.port == 8000` |

### Fișiere cheie S11

| Fișier | Rol |
|---|---|
| `S11_Part01_Config_Nginx.conf` | Configurare Nginx: upstream + proxy_pass |
| `S11_Part01_Config_Docker_Compose_Nginx.yml` | Stack: nginx-proxy + web1/web2/web3 pe `lbnet` |
| `S11_Part02_Script_Simple_Lb.py` | LB custom Python: socket, round robin, forwarding |
| `S11_Part02_Config_Docker_Compose_Lb_Custom.yml` | Stack: lb-custom + web1-lb/web2-lb/web3-lb pe `lbnet` |
| `S11_Part02_Config_Dockerfile_Lb.lb` | Dockerfile pentru containerul LB custom |

---

## Plan de contingență

| # | Problemă | Simptom | Soluție |
|---|---|---|---|
| 1 | Portul 8080 ocupat | `bind: address already in use` | Schimbă mapping-ul în compose la `8081:80` / `8081:8080`; folosește `http://localhost:8081` |
| 2 | Pull de imagini lent | Stack-ul blochează la download | Folosește timpul pentru micro-teorie (Bloc B) sau citire config; imaginile se descarcă în fundal |
| 3 | Naming mismatch (web1 vs. web1-lb) necorectat | `ConnectionRefused` în logurile lb-custom | Editează `BACKENDS` în script: `("web1-lb", 8000)` etc. |
| 4 | PowerShell `curl` vs. `curl.exe` | Output HTML în loc de text simplu / eroare `Invoke-WebRequest` | Folosește `curl.exe` explicit, nu `curl` |
| 5 | Containere rămase de la grupa anterioară | `web1 already in use` | `docker rm -f web1 web2 web3 nginx-proxy lb-custom web1-lb web2-lb web3-lb` |
| 6 | Docker Desktop nu e pornit | `error during connect` | Pornește Docker Desktop; așteaptă icon verde în tray |
| 7 | Pcap gol sau tcpdump nu captează nimic | Fișierul are 0 pachete | Verifică: (a) tcpdump rulează când trimiți cererile; (b) `port 8000` e corect; (c) `--net=container:lb-custom` — numele containerului e exact |
| 8 | Volume path greșit pe Windows | Container nu pornește / nu găsește fișierele | Verifică: calea completă, ghilimele în jurul `${PWD}\captures`, Docker Desktop are acces la drive-ul respectiv |

---

## Referințe (APA 7th)

Aweya, J., Ouellette, M., Montuno, D. Y., Doray, B., & Felske, K. (2002). An adaptive load balancing scheme for web servers. *International Journal of Network Management, 12*(1), 3–39. https://doi.org/10.1002/nem.421

Dymora, P., Mazurek, M., & Sudek, B. (2021). Comparative analysis of selected open-source solutions for traffic balancing in server infrastructures providing WWW service. *Energies, 14*(22), 7719. https://doi.org/10.3390/en14227719

Fielding, R. & Reschke, J. (Eds.). (2014). *Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing* (RFC 7230). Internet Engineering Task Force. https://doi.org/10.17487/RFC7230

Karger, D., Lehman, E., Leighton, T., Panigrahy, R., Levine, M., & Lewin, D. (1997). Consistent hashing and random trees: Distributed caching protocols for relieving hot spots on the World Wide Web. In *Proceedings of the Twenty-Ninth Annual ACM Symposium on Theory of Computing (STOC '97)* (pp. 654–663). Association for Computing Machinery. https://doi.org/10.1145/258533.258660

Al Nuaimi, K., Mohamed, N., Al Nuaimi, M., & Al-Jaroodi, J. (2012). A survey of load balancing in cloud computing: Challenges and algorithms. In *2012 Second Symposium on Network Cloud Computing and Applications (NCCA)* (pp. 137–142). IEEE. https://doi.org/10.1109/NCCA.2012.29

Zhang, Z., & Fan, W. (2008). Web server load balancing: A queueing analysis. *European Journal of Operational Research, 186*(2), 681–693. https://doi.org/10.1016/j.ejor.2007.02.011

Valeur, F., Vigna, G., Kruegel, C., & Kirda, E. (2006). An anomaly-driven reverse proxy for web applications. In *Proceedings of the 2006 ACM Symposium on Applied Computing (SAC '06)* (pp. 361–368). Association for Computing Machinery. https://doi.org/10.1145/1141277.1141361

---

## Note pedagogice

**Arcul cognitiv al seminarului:** Hook (server suprasolicitat) → Activare (DNS intern din S10) → Conflict cognitiv (naming mismatch + failure fără health checks) → Explorare ghidată (demo 1 + demo 2) → Formalizare (tabel comparativ din kit) → Aplicare (task-uri) → Recap (3 idei + hook reluat).

**Tipare socratice folosite:**
1. POE în C.2 (predicție rotație → observare → explicare)
2. POE în C.4 (predicție failure Nginx → observare)
3. POE în D.5 (predicție failure custom LB → contrast cu Nginx)
4. Conflict cognitiv deliberat în D.2 (naming mismatch DNS)
5. „Ce s-ar fi întâmplat dacă…?" — implicit în C.4 și D.5

**Concepție greșită vizată explicit:** #5 (porturile containerelor sunt automat accesibile) — adresată în C.1 prin întrebarea „putem accesa direct web1 pe 8000?"

**Epifanii marcate:** 3 — (1) rotația vizibilă în output, (2) declarativ vs. procedural, (3) două conexiuni TCP în pcap.

**Specificități Windows:**
- `curl.exe` în loc de `curl` (alias PowerShell)
- Captura pcap: din interiorul containerului cu netshoot, deschisă apoi în Wireshark GUI (nu pe loopback Windows)
- Căi cu backslash; volume Docker cu `${PWD}\`
- Docker Desktop necesar (nu Docker nativ pe Linux)

Această variantă este complet autonomă — zero referințe la varianta VM.

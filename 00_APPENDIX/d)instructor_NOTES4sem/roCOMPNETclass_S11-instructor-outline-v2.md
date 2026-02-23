# Seminar S11 — Reverse proxy și load balancing cu Docker Compose

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` (claudev11) — `04_SEMINARS/S11/` |
| **Infra** | MININET-SDN (VM Ubuntu 24.04 / VirtualBox) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | Un load balancer nu „pasează" conexiunea — el o termină și deschide alta; observăm asta concret, cu Nginx (declarativ) și cu Python (procedural). |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. **Explica** diferența dintre *forward proxy* și *reverse proxy*, indicând direcția fluxului și cine e „reprezentat" de fiecare.
2. **Rula** un stack Docker Compose cu Nginx ca reverse proxy în fața a 3 backend-uri HTTP și **observa** distribuția round-robin a cererilor.
3. **Localiza** în configurația Nginx blocurile `upstream` și `proxy_pass` și **anticipa** ce trebuie modificat la adăugarea unui backend.
4. **Descrie** funcționarea internă a unui load balancer scris în Python (socket accept → select backend → connect → forward → relay) și **identifica** limitele sale față de Nginx.
5. **Demonstra** într-un pcap că load balancer-ul creează o a doua conexiune TCP, separată de cea a clientului.
6. **Compara** comportamentul celor două soluții când un backend cade — cu și fără health checks.

---

## Structura seminarului

| Minute | Bloc | Ce se întâmplă | Tipar |
|---:|---|---|---|
| 0–3 | **A** — Hook + predicții | Scenariu: serverul nu mai face față; studenții prezic ce face un LB | POE |
| 3–8 | **B** — Micro-teorie | Reverse proxy, upstream, round robin — desen + întrebare SPOF | expozitiv + întrebare |
| 8–20 | **C** — Demo 1: Nginx Compose | Pornire stack, test rotație, citire config, failure test | POE × 2 |
| 20–22 | **C′** — Curățare Part01 | Oprire stack Nginx | procedural |
| 22–34 | **D** — Demo 2: custom LB (Python) | Naming/DNS, pornire stack, test rotație, failure test | conflict cognitiv + POE |
| 34–38 | **E** — Captură pcap + interpretare | tcpdump din container, tshark rapid | epifanie vizuală |
| 38–40 | **F** — Recap + teme | 3 idei fixate, hook reluat, task-uri | sinteză |

**Total:** 40 min.

---

## Pregătire înainte de seminar (instructor)

### Checklist tehnic

1. VM MININET-SDN pornit, user `stud`.
2. Docker funcțional:
   ```bash
   docker --version
   docker compose version
   ```
3. Repo disponibil (adaptează calea):
   ```bash
   cd ~/compnet/04_SEMINARS/S11
   ls
   ```
4. Pre-pull imagini (evită așteptare la clasă):
   ```bash
   docker pull nginx:latest
   docker pull python:3.11-alpine
   docker pull nicolaka/netshoot:latest
   ```
5. Verifică că portul 8080 e liber:
   ```bash
   ss -tlnp | grep 8080
   ```

### Decizie pre-seminar: naming mismatch

Scriptul `S11_Part02_Script_Simple_Lb.py` are `BACKENDS = [("web1", 8000), ...]`, dar compose-ul din Part02 definește serviciile ca `web1-lb`, `web2-lb`, `web3-lb`. Aceasta e o discrepanță **deliberată** — momentul de debugging e didactic valoros. Dacă preferi să eviți debugging live, editează `BACKENDS` înainte de seminar. Dacă îl lași, el devine un conflict cognitiv explicit.

---

## Bloc A (0–3 min) — Hook: „Serverul nu mai face față"

> *▸ „Aveți o aplicație web. Într-o luni dimineață, traficul se triplează. Serverul răspunde cu 5 secunde latență, apoi cade. Întrebarea: cum păstrați aceeași adresă publică, dar puneți mai multe servere în spate?"*

**Ce faci:**
- 30 sec tăcere reală — fiecare notează o predicție.
- 2–3 răspunsuri scurte. Notezi pe tablă: *distribuie*, *ascunde*, *reziliență*.

> *▸ „Țineti minte predicțiile voastre — revin la ele la final."*

**De ce contează:** hook-ul creează tensiune cognitivă (o problemă reală, nu o definiție) și ancorează discuția ulterioară. Îl reluăm explicit la Bloc F.

---

## Bloc B (3–8 min) — Micro-teorie: reverse proxy, upstream, round robin

> *▸ „Reverse proxy = un server care primește cereri în locul backend-urilor. Clientul vede o singură adresă; proxy-ul decide cui trimite cererea."*

> *▸ „Upstream = grupul de backend-uri din spatele proxy-ului."*

> *▸ „Load balancing = regula de selecție. Azi vedem round robin — cea mai simplă: fiecare cerere merge la următorul backend, ciclic."*

> *▸ „Comparăm două abordări: Nginx (produs matur) și un script Python (didactic, minimal)."*

**Desen rapid (tablă/proiector):**
```
curl / Browser  ──►  [ Reverse proxy ]  ──►  web1 :8000
                                         ──►  web2 :8000
                                         ──►  web3 :8000
```

**Întrebare (10 sec):**
> *▸ „Unde e acum punctul unic de eșec?"*

Răspuns așteptat: reverse proxy-ul. Confirmi: „da — în producție se replică și pe el, dar asta depășește seminarul de azi."

**Legătură cu S10:** „La S10 ați văzut cum containerele comunică prin DNS intern în Docker. Azi construim pe baza aceluiași mecanism — proxy-ul găsește backend-urile prin nume de serviciu."

---

## Bloc C (8–20 min) — Demo 1: Nginx reverse proxy + 3 backend-uri

### C.1 Pornire stack (2 min)

> *▸ „Pornim stack-ul. Un singur port expus către exterior: 8080. Backend-urile ascultă pe 8000, dar doar în rețeaua Docker internă."*

🔵 **Terminal 1 (SERVER / stack):**
```bash
cd ~/compnet/04_SEMINARS/S11/1_nginx-compose
ls
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml up --build
```

Urmărești în loguri: containerele `nginx-proxy`, `web1`, `web2`, `web3`.

**Predicție privind concepția greșită #5 (porturi auto-expuse):**
> *▸ „Putem accesa direct web1 pe portul 8000 din browser? De ce nu?"*

Răspuns: nu — `expose` nu mapează pe host; doar Nginx, cu `ports: 8080:80`, e accesibil din exterior.

### C.2 Test round robin (4–5 min)

> *▸ „Trimitem 6 cereri. Predicție: răspund toate trei backend-urile, sau doar unul?"*

Cere ridicare de mână: „cine crede că toate trei?" / „cine crede că doar web1?"

🟢 **Terminal 2 (CLIENT):**
```bash
for i in {1..6}; do
  echo "---- cerere $i ----"
  curl -s http://localhost:8080 | head -n 5
done
```

**Output așteptat (real, din HTML-urile din kit):**
```html
<h1>Seminar 11 — Backend server WEB1</h1>
...
<h1>Seminar 11 — Backend server WEB2</h1>
...
<h1>Seminar 11 — Backend server WEB3</h1>
...
<h1>Seminar 11 — Backend server WEB1</h1>
```

**☀️ Epifanie:**
> *▸ „Load balancing-ul nu e abstract — îl observați direct în conținutul răspunsului. Fiecare backend spune cine e."*

### C.3 Citire ghidată: unde sunt backend-urile? (4–5 min)

> *▸ „Nu rămâne cutie neagră. Deschideți configurația și găsiți două lucruri: unde se definesc backend-urile și unde are loc forwarding-ul."*

🔵 **Terminal 1 (sau pe proiector):**
```bash
cat S11_Part01_Config_Nginx.conf
```

**Ce punctezi:**
- `upstream backend_pool { server web1:8000; server web2:8000; server web3:8000; }` — lista de backend-uri
- `proxy_pass http://backend_pool;` — directiva care trimite cererea către upstream
- `proxy_set_header X-Real-IP $remote_addr;` — proxy-ul adaugă informație despre clientul original

**Întrebare (10 sec):**
> *▸ „Dacă adaug al patrulea backend, ce modific?"*

Răspuns așteptat: (a) adaug `server web4:8000;` în upstream; (b) adaug serviciul `web4` în compose.

**Referință kit:** detalii în `S11_Part01A_Explanation_Reverse_Proxy_Intro.md` și `S11_Part01B_Explanation_Nginx_Compose_Setup.md`.

### C.4 Failure test — ce se întâmplă când pică un backend? (3–4 min)

**Predicție (POE):**
> *▸ „Oprim web2. Trei variante posibile: (a) erori 502 la fiecare cerere care ar fi mers la web2, (b) Nginx evită automat backend-ul mort, (c) totul cade. Ce credeți?"*

🟢 **Terminal 2:**
```bash
docker stop web2

for i in {1..8}; do
  echo "---- cerere $i ----"
  curl -s -i http://localhost:8080 | head -n 8
done
```

**Rezultat posibil:** Nginx detectează backend-ul mort (timeout) și, după prima eroare, îl marchează ca indisponibil temporar. Studenții vor vedea fie numai web1/web3 (ideal), fie un 502 urmat de răspunsuri corecte.

> *▸ „Observația voastră e cea care contează. Nginx are mecanisme interne de retry și de marcare a serverelor ca down. Scriptul nostru Python, pe care îl vedem imediat, nu are nimic din astea."*

**Repornire web2 (pentru curățenie):**
```bash
docker start web2
```

---

## Bloc C′ (20–22 min) — Curățare Part01

> *▸ „Oprim stack-ul Nginx ca să eliberăm portul 8080 pentru al doilea demo."*

🔵 **Terminal 1:** `Ctrl+C` (oprire), apoi:
```bash
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml down
```

Verifică rapid:
```bash
ss -tlnp | grep 8080
```
— trebuie să fie gol.

---

## Bloc D (22–34 min) — Demo 2: custom load balancer (Python)

### D.1 Setarea scenei (1 min)

> *▸ „Nginx e un produs matur cu mii de linii de cod. Acum facem același lucru cu un script de ~100 de linii. Scopul: să vedeți ce face un LB mecanic — primește cererea, alege un backend, deschide o conexiune nouă, transmite, returnează."*

```bash
cd ~/compnet/04_SEMINARS/S11/2_custom-load-balancer
ls
```

### D.2 Conflict cognitiv: DNS / naming în Compose (3–4 min)

> *▸ „În Docker Compose, numele serviciului devine automat nume DNS în rețeaua internă. Dacă în cod scriu `web1`, dar serviciul se cheamă `web1-lb`, nu se rezolvă."*

🔵 **Proiector:**
```bash
head -40 S11_Part02_Config_Docker_Compose_Lb_Custom.yml
echo "---"
head -20 S11_Part02_Script_Simple_Lb.py
```

**Ce arăți:** compose definește `web1-lb`, `web2-lb`, `web3-lb`; scriptul are `("web1", 8000)`.

**Mini-exercițiu (30 sec):**
> *▸ „Două opțiuni: (a) redenumim serviciile în compose, sau (b) corectăm lista BACKENDS din script. Care e mai rapidă?"*

Răspuns: (b). Editezi:
```bash
nano S11_Part02_Script_Simple_Lb.py
```

Modifici:
```python
BACKENDS = [("web1-lb", 8000), ("web2-lb", 8000), ("web3-lb", 8000)]
```
Salvezi (`Ctrl+O`, `Enter`, `Ctrl+X`).

> *▸ „Rețineți lecția: într-un sistem distribuit, dacă un nume nu se rezolvă, nu ai conectivitate. La S10 ați văzut DNS-ul în containere — acum vedeți consecința practică."*

**Referință kit:** `S11_Part02A_Explanation_Custom_Lb.md` detaliază ce face scriptul și ce lipsește intenționat.

### D.3 Pornire stack custom LB (2 min)

> *▸ „Pornim. Urmăriți logurile: LB-ul afișează explicit către ce backend trimite fiecare cerere."*

🔵 **Terminal 1:**
```bash
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml up --build
```

**Predicție scurtă:**
> *▸ „Cine crede că logurile ne vor arăta backend-ul ales? Unde altundeva am putea vedea asta?"*

Urmărești: `lb-custom`, `web1-lb`, `web2-lb`, `web3-lb` pornite.

### D.4 Test round robin (3–4 min)

🟢 **Terminal 2:**
```bash
for i in {1..6}; do
  echo "---- cerere $i ----"
  curl -s http://localhost:8080 | head -n 5
done
```

**Output așteptat:**
```html
<h1>Seminar 11 — Custom LB backend WEB1</h1>
...
<h1>Seminar 11 — Custom LB backend WEB2</h1>
...
```

**Ce arăți în logurile lb-custom (terminal 1):**
```
[INFO] ('172.18.0.1', 49566) -> web1-lb:8000
[INFO] ('172.18.0.1', 49570) -> web2-lb:8000
[INFO] ('172.18.0.1', 49574) -> web3-lb:8000
```

**☀️ Epifanie:**
> *▸ „În Nginx, politica e declarativă: `upstream { ... }` în config. În Python, politica e procedurală: `backend_index`, modulo, o variabilă globală. Aceeași idee, două paradigme."*

### D.5 Failure test (3 min)

**Predicție (POE):**
> *▸ „Oprim web2-lb. La Nginx am văzut [ce ați observat]. Acum ce credeți că se întâmplă? Scriptul Python are health checks?"*

🟢 **Terminal 2:**
```bash
docker stop web2-lb

for i in {1..6}; do
  echo "---- cerere $i ----"
  curl -s -i http://localhost:8080 | head -n 10
done
```

**Rezultat:** fiecare a treia cerere (cea care nimereşte web2-lb) va eşua — eroare `ConnectionRefused` în loguri, răspuns gol sau eroare la client.

> *▸ „Scriptul Python nu are niciun mecanism de evitare a unui backend mort. Trimite orbește. Asta e diferența practică între un prototip și un produs."*

**Referință kit:** tabelul comparativ complet se găsește în `S11_Part02C_Explanation_Lb_Comparison.md`.

---

## Bloc E (34–38 min) — Captură pcap: dovada celor două conexiuni TCP

### E.1 Generare pcap cu netshoot (2–3 min)

> *▸ „Facem dovada vizuală: LB-ul nu «pasează» conexiunea clientului — el creează o a doua conexiune. Capturăm traficul intern."*

🟠 **Terminal 3 (CAPTURĂ):**
```bash
mkdir -p captures

docker run --rm --net=container:lb-custom \
  -v "$(pwd)/captures:/captures" \
  nicolaka/netshoot \
  tcpdump -i eth0 -w /captures/lb_upstream.pcap port 8000
```

🟢 **Terminal 2 (în paralel):**
```bash
for i in {1..5}; do curl -s http://localhost:8080 >/dev/null; done
```

Oprești tcpdump cu `Ctrl+C` (terminal 3).

### E.2 Interpretare rapidă (1–2 min)

Cu `tshark` (disponibil în VM):
```bash
tshark -r captures/lb_upstream.pcap -Y "http.request" \
  -T fields -e ip.src -e ip.dst -e http.request.method -e http.request.uri | head
```

Sau, dacă ai Wireshark GUI: `wireshark captures/lb_upstream.pcap &` → filtru `tcp.port == 8000`.

**Ce arăți:**
- IP-urile sunt interne Docker (172.x.x.x)
- LB-ul are un IP; backend-urile au IP-uri diferite
- Fiecare cerere HTTP GET apare ca o conexiune inițiată de LB, nu de clientul original

**☀️ Epifanie (fraza centrală):**
> *▸ „Un load balancer termină conexiunea cu clientul și deschide una nouă către backend. Nu e un fir care trece prin el — e un intermediar activ. Reveniți la definiția de la RFC 7230 §2.3: un intermediary care face „inbound" și „outbound" connections."*

---

## Bloc F (38–40 min) — Recap + teme

### Recap: 3 idei fixate

> *▸ „Trei lucruri de reținut:"*
> 1. *„Reverse proxy = ascunde backend-urile; clientul vede o singură adresă."*
> 2. *„Diferența practică: Nginx e declarativ și are health checks; scriptul Python e procedural și orb — trimite și la backend-uri moarte."*
> 3. *„LB-ul nu pasează conexiunea — o rupe în două. Asta ați văzut în pcap."*

### Reluare hook

> *▸ „La început v-am întrebat: cum păstrăm aceeași adresă și punem mai multe servere în spate? Acum aveți răspunsul concret: un reverse proxy cu upstream. Și ați văzut ce se întâmplă când prototipul nu are reziliență — cererea cade."*

### Teme

> *▸ „Nu vreau eseuri. Comenzi rulate, output relevant, concluzii scurte."*

**Task-uri din kit:**
- `1_nginx-compose/S11_Part01C_Tasks_Nginx.md`
- `2_custom-load-balancer/S11_Part02B_Tasks_Custom_Lb.md`
- `2_custom-load-balancer/S11_Part02D_Tasks_Lb_Compose.md`

**Fișiere livrabile (conform task-urilor):**

| Fișier | Ce conține |
|---|---|
| `reverse_proxy_intro_findings.txt` | Diferența forward/reverse proxy, diagramă ASCII, avantaje LB |
| `nginx_round_robin_log.txt` | Output curl cu 3 backend-uri + output cu web2 oprit + reflecții |
| `lb_custom_output.txt` | Output curl custom LB + failure test + reflecții |
| `lb_compose_comparison.txt` | Comenzi, output-uri, 1 similaritate, 2 diferențe, 1 limitare |

**Material suplimentar de studiu (din kit):**
- `S11_Part01A_Explanation_Reverse_Proxy_Intro.md` — teorie reverse proxy
- `S11_Part02C_Explanation_Lb_Comparison.md` — tabel comparativ detaliat
- `_HTMLsupport/S11/` — simulatoare interactive (Nginx și custom LB)

**Legătură S12:**
> *▸ „La S12 trecem de la HTTP la RPC — un alt mod de comunicare între servicii distribuite. Dacă azi ați văzut proxy-ul ca intermediar HTTP, data viitoare vedeți intermediarul la nivel de funcții."*

---

## Curățare (post-seminar)

```bash
cd ~/compnet/04_SEMINARS/S11/2_custom-load-balancer
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml down

# Verificare finală
docker ps   # trebuie gol (sau doar containere nerelaționate)
```

---

## Cheat-sheet

### Comenzi Docker Compose

| Acțiune | Comandă |
|---|---|
| Pornire stack (cu rebuild) | `docker compose -f <fișier>.yml up --build` |
| Oprire stack + ștergere containere | `docker compose -f <fișier>.yml down` |
| Oprire un container | `docker stop <nume_container>` |
| Repornire container | `docker start <nume_container>` |
| Loguri container | `docker logs <nume_container>` |
| Listare containere | `docker ps` |

### Testare

| Acțiune | Comandă |
|---|---|
| Cerere HTTP (scurt) | `curl -s http://localhost:8080` |
| Cerere HTTP (cu headere) | `curl -s -i http://localhost:8080` |
| Buclă 6 cereri | `for i in {1..6}; do curl -s http://localhost:8080 \| head -n 5; done` |
| Port liber? | `ss -tlnp \| grep 8080` |

### Captură și analiză

| Acțiune | Comandă |
|---|---|
| Captură din namespace container | `docker run --rm --net=container:<c> -v ... nicolaka/netshoot tcpdump -i eth0 -w /captures/f.pcap port 8000` |
| Analiză rapidă | `tshark -r f.pcap -Y "http.request" -T fields -e ip.src -e ip.dst` |
| Wireshark GUI | `wireshark f.pcap &` |

### Fișiere cheie S11

| Fișier | Rol |
|---|---|
| `S11_Part01_Config_Nginx.conf` | Configurare Nginx: upstream + proxy_pass |
| `S11_Part01_Config_Docker_Compose_Nginx.yml` | Stack: nginx-proxy + web1/web2/web3 pe rețeaua `lbnet` |
| `S11_Part02_Script_Simple_Lb.py` | LB custom Python: socket, round robin, forwarding |
| `S11_Part02_Config_Docker_Compose_Lb_Custom.yml` | Stack: lb-custom + web1-lb/web2-lb/web3-lb pe `lbnet` |
| `S11_Part02_Config_Dockerfile_Lb.lb` | Dockerfile pentru containerul LB custom |

---

## Plan de contingență

| # | Problemă | Simptom | Soluție |
|---|---|---|---|
| 1 | Portul 8080 ocupat | `bind: address already in use` | `ss -tlnp \| grep 8080` → oprește procesul sau schimbă mapping-ul în compose la `8081:80` / `8081:8080` |
| 2 | Pull de imagini lent (fără pre-pull) | Stack-ul blochează la download | Folosești timpul pentru micro-teorie (Bloc B) sau citire config (C.3); imaginile se descarcă în fundal |
| 3 | Naming mismatch (web1 vs. web1-lb) nu e corectat | `ConnectionRefused` în logurile lb-custom | Editează `BACKENDS` în script sau redenumește serviciile în compose |
| 4 | `tshark` indisponibil sau pcap gol | Nu apare output la `tshark -r ...` | Verifică: (a) tcpdump a fost oprit cu Ctrl+C (nu kill -9); (b) cererile curl au fost trimise în timp ce tcpdump rula; (c) alternativă: `tcpdump -r captures/lb_upstream.pcap -n \| head` |
| 5 | Containere rămase de la grupa anterioară | Conflict de nume (`web1 already in use`) | `docker rm -f web1 web2 web3 nginx-proxy lb-custom web1-lb web2-lb web3-lb` |
| 6 | Nginx nu distribuie round-robin (răspunde mereu web1) | Output identic la toate cererile | Verifică: (a) cache browser (folosește `curl -s`, nu browser); (b) conexiuni keep-alive — adaugă `proxy_http_version 1.1;` și `proxy_set_header Connection "";` |
| 7 | Eroare `permission denied` pe volume Docker | Container nu pornește | Verifică permisiunile pe directoarele `web1/`, `web2/`, `web3/`: `chmod -R 755 .` |

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

**Arcul cognitiv al seminarului:** Hook (server suprasolicitat) → Activare (DNS intern din S10) → Conflict cognitiv (naming mismatch + failure fără health checks) → Explorare ghidată (demo 1 + demo 2) → Formalizare (tabel comparativ din kit: `S11_Part02C`) → Aplicare (task-uri + temă) → Recap (3 idei + hook reluat).

**Tipare socratice folosite:**
1. POE în C.2 (predicție rotație → observare → explicare)
2. POE în C.4 (predicție failure Nginx → observare)
3. POE în D.5 (predicție failure custom LB → contrast cu Nginx)
4. Conflict cognitiv deliberat în D.2 (naming mismatch)
5. „Ce s-ar fi întâmplat dacă…?" — implicit în C.4 și D.5

**Concepție greșită vizată explicit:** #5 (porturile containerelor sunt automat accesibile) — adresată în C.1 prin întrebarea „putem accesa direct web1 pe 8000?".

**Epifanii marcate:** 3 — (1) rotația vizibilă în output, (2) declarativ vs. procedural, (3) două conexiuni TCP în pcap.

**Progresia temelor S01→S14:** S11 presupune competențe de socket (S02–S04), HTTP (S08), Docker Compose (S10). Temele S11 cer observații concrete cu output-uri, nu cod nou — nivel Apply/Analyse.

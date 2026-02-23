# Seminar S08 — HTTP „pe fir", fără MININET-SDN: Windows + Docker Desktop + Wireshark

**`curl.exe` pe Windows, server HTTP Python în container Docker, server HTTP manual (socket) în container, nginx reverse proxy în Docker Compose, captură în Wireshark**

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` → `04_SEMINARS/S08/` |
| **Infra** | Windows 10/11 + Docker Desktop (Linux containers) + Wireshark (Npcap) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | HTTP e text peste TCP; un server HTTP minimal se reduce la parsarea primei linii + construirea unui răspuns valid cu status, headere și body. |

---

## Obiective operaționale

La finalul seminarului, studentul:

1. Citește un output `curl.exe -v` și identifică fără ezitare: request line, status line, headere relevante, delimitarea header/body.
2. Explică rolul `Content-Type` și `Content-Length` — și descrie ce se întâmplă când lipsesc.
3. Pornește și testează un server HTTP (builtin Python) în container Docker, adăugând un endpoint JSON (`/student`).
4. Distinge între un server care „ascunde" protocolul (builtin) și unul care îl „face vizibil" (socket manual).
5. Justifică de ce un reverse proxy (nginx) apare în fața unui backend în producție.
6. Compară headerele unui răspuns direct (port 8000) cu cele ale aceluiași răspuns prin proxy (port 8080).

---

## Principiul de lucru (spus în primele 30 sec)

> *▸ „Pe Windows, nu ne batem cu instalări locale de Python. Rulăm serverele în containere Docker. Clientul rămâne pe host (`curl.exe`), iar observabilitatea vine din `curl.exe -v` și, opțional, din Wireshark."*

---

## Structura seminarului (35–40 min)

| Bloc | Ce se întâmplă | Durată |
|:---:|---|---:|
| **A** | Hook + activare: „când clientul cere `/hello`, cum știe că răspunsul s-a terminat?" | 3 min |
| **B** | HTTP + `curl.exe -v`: request/response ca text | 7–8 min |
| **C** | Server builtin Python în container Docker — 3 endpoint-uri, Content-Length prezent vs absent | 8–9 min |
| **D** | Server HTTP manual (socket) în container — același răspuns, construit de noi | 8–9 min |
| **E** | nginx reverse proxy în Docker Compose — aceeași pagină, alte headere | 6–7 min |
| **F** | Recap + temă: fixare 3 idei, returnare la hook | 2–3 min |
| | **Total estimat** | **34–39 min** |

> **Regulă pragmatică:** dacă Wireshark devine greu (interfață Npcap, adapter loopback), păstrezi observabilitatea pe `curl.exe -v`. Comanda `curl.exe -v` rămâne o formă validă de inspecție HTTP — Wireshark devine bonus, nu condiție.

---

## Pregătire înainte de seminar (checklist pentru instructor)

### Ce trebuie instalat

- Docker Desktop pornit (Linux containers mode).
- Wireshark instalat **cu Npcap** (ideal cu suport loopback capture).
- Imaginile Docker pre-pulled (recomandare: faceți asta din timp):
  ```powershell
  docker pull python:3.12-slim
  docker pull nginx:1.27-alpine
  ```

### Ce pregătești în sală

1. Deschizi **două** ferestre PowerShell:
   - 🔵 **SERVER**: va rula containerele cu serverele
   - 🟢 **CLIENT**: va rula `curl.exe` și comenzi scurte

2. Deschizi Wireshark (dar nu pornești captura încă).

3. În ambele PowerShell-uri, mergi în root-ul kitului:
   ```powershell
   cd C:\...\compnet-2025-redo-main
   dir 04_SEMINARS\S08
   ```

### Pregătire fișiere nginx Windows

Fișierele din kit (`S08_Part04_Config_Docker_Compose.yml` și `S08_Part04_Config_Nginx.conf`) folosesc `network_mode: host`, care funcționează doar pe Linux. Pentru Windows, **creezi înainte de seminar** două fișiere adaptate în `04_SEMINARS\S08\4_nginx\`:

**Fișier 1: `S08_Part04_Config_Nginx.win.conf`**

```nginx
# nginx (Windows/Docker Desktop) — reverse proxy către serviciul "backend"

events {}

http {
    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    server {
        listen 8080;
        server_name localhost;

        location / {
            proxy_pass http://backend:8000;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            add_header X-Student-Lab "Seminar8";
        }
    }
}
```

**Fișier 2: `S08_Part04_Config_Docker_Compose.win.yml`**

```yaml
services:
  backend:
    image: python:3.12-slim
    working_dir: /app
    volumes:
      - ../2_simple-http:/app
    command: ["python", "S08_Part02B_Example_Simple_HTTP_Builtin.py", "8000"]
    ports:
      - "8000:8000"

  nginx:
    image: nginx:1.27-alpine
    depends_on:
      - backend
    ports:
      - "8080:8080"
    volumes:
      - ./S08_Part04_Config_Nginx.win.conf:/etc/nginx/nginx.conf:ro
```

> Aceste fișiere **nu sunt în kit** — sunt necesare doar pentru varianta Windows. Pe Linux (VM), kit-ul folosește `network_mode: host` direct.

### Avertisment PowerShell

În PowerShell, `curl` e adesea alias pentru `Invoke-WebRequest`. Folosești explicit `curl.exe`:

```powershell
curl.exe -V
```

Spui asta și studenților la început (altfel văd un output complet diferit).

---

## Bloc A — Hook + activare (3 min)

### Scenariu de deschidere

> *▸ „Pornesc un server pe portul 8000. Trimit `GET /hello`. Serverul răspunde cu textul «Hello». Întrebare: de unde știe clientul că răspunsul s-a terminat? Sunt doar 5 caractere — dar clientul nu știe dinainte câte caractere vin. Cum se descurcă?"*

Lași 10 secunde de gândire. Notezi 2–3 răspunsuri pe tablă. Nu corectezi — le fixezi în Blocul C.

### Activare (legătura cu S07)

> *▸ „La S07 am capturat segmente TCP. Azi urcăm un strat: înăuntrul acelui payload TCP e protocolul HTTP. Și o să-l facem vizibil."*

---

## Bloc B — HTTP + `curl.exe`: anatomia request/response (7–8 min)

### B.1. Predicții

Întrebări scurte:

- „Când scriu `GET /`, ce trimite clientul pe lângă această linie?"
- „De ce ar vrea serverul să specifice tipul conținutului?"

### B.2. Demo cu site public (doar dacă merge internetul)

În 🟢 CLIENT:

```powershell
curl.exe -I http://example.com
curl.exe -v http://example.com
```

Ce arăți cu cursorul:
- `>` = request headers (ce trimite clientul)
- `<` = response headers (ce trimite serverul)
- linia goală separă headerele de body

> Dacă site-ul face redirect HTTPS: *▸ „Redirect-ul e tot HTTP: 301 + header `Location`. Urmărirea o facem cu `-L`, dar azi ne interesează structura."*

### B.3. Epifanie: HTTP e text

> *▸ „Tot ce vedeți aici e text ASCII. HTTP, în forma clasică, e literalmente text peste TCP. De asta `curl.exe -v` e instrumentul de laborator implicit."*

Le spui că asta documentează în `curl_basics_log.txt` și `curl_questions.txt`.

---

## Bloc C — Server builtin Python în Docker (8–9 min)

**Fișier kit:** `04_SEMINARS/S08/2_simple-http/S08_Part02B_Example_Simple_HTTP_Builtin.py`

### C.1. Pornire server în container

În 🔵 SERVER (din root-ul kitului):

```powershell
docker run --rm -it -p 8000:8000 `
  -v ${PWD}:/work `
  -w /work/04_SEMINARS/S08/2_simple-http `
  python:3.12-slim `
  python S08_Part02B_Example_Simple_HTTP_Builtin.py 8000
```

> *▸ „Nu instalăm nimic pe Windows. Containerul are Python. Noi doar montăm folderul cu fișierul și expunem portul."*

### C.2. Testare 3 endpoint-uri

În 🟢 CLIENT:

```powershell
curl.exe -v http://localhost:8000/
curl.exe -v http://localhost:8000/hello
curl.exe -v http://localhost:8000/api/time
```

**Observații ghidate:**

1. La `/hello`:
   - `Content-Type: text/plain; charset=utf-8` — prezent
   - `Content-Length` — **absent** (serverul nu l-a trimis explicit pe acest endpoint)
2. La `/api/time`:
   - `Content-Type: application/json` — prezent
   - `Content-Length: <valoare>` — prezent (trimis explicit în cod)

### C.3. Conflict cognitiv: returnare la hook

> *▸ „Acum avem răspunsul la întrebarea de la început. La `/hello`, serverul NU a trimis Content-Length. Clientul se descurcă pentru că protocolul e HTTP/1.0 — serverul închide conexiunea, iar clientul citește până la EOF."*
>
> *▸ „La `/api/time`, serverul a trimis explicit `Content-Length`. Clientul știe exact câți octeți să aștepte. Asta e mecanismul robust — și obligatoriu pentru HTTP/1.1 cu conexiuni persistente."*

### C.4. Temă

> *▸ „Modificați handler-ul: adăugați `/student`, returnați JSON cu numele vostru și `lab: 8`. Salvați output-ul `curl` în `builtin_http_log.txt`."*

---

## Bloc D — Server HTTP manual (socket) în Docker (8–9 min)

**Fișiere kit:**
- `04_SEMINARS/S08/3_socket-http/S08_Part03B_Example_Socket_HTTP_Server.py`
- `04_SEMINARS/S08/3_socket-http/static/` (pagina HTML)

### D.1. Oprire builtin, pornire server manual

În 🔵 SERVER: `Ctrl+C` (oprești containerul). Apoi:

```powershell
docker run --rm -it -p 8000:8000 `
  -v ${PWD}:/work `
  -w /work/04_SEMINARS/S08/3_socket-http `
  python:3.12-slim `
  python S08_Part03B_Example_Socket_HTTP_Server.py 8000
```

### D.2. Testare + observații

În 🟢 CLIENT:

```powershell
curl.exe -v http://localhost:8000/
curl.exe -v http://localhost:8000/index.html
curl.exe -v http://localhost:8000/doesnotexist
```

**Observații verbalizate:**

1. `/` e mapat la `S08_Part03_Page_Index.html` din `static/`.
2. 404 e un răspuns HTTP valid: status line + headere + body HTML minimal.
3. `Content-Length` e prezent mereu în serverul manual — contrastul cu builtin-ul pe `/hello`.

> *▸ „Concepția greșită obișnuită: 404 e «eroare de server». Nu. 404 e un răspuns HTTP perfect valid — cu status line, headere, body."*

### D.3. Punct pedagogic

> *▸ „Serverul builtin ascunde protocolul. Serverul manual îl face vizibil: fiecare header e o decizie explicită."*

Temă: în `socket_http_log.txt` descriu parsarea, decizia de fișier, rolul `Content-Length`.

---

## Bloc E — nginx reverse proxy în Docker Compose (6–7 min)

### E.1. Oprire container anterior

În 🔵 SERVER: `Ctrl+C`.

### E.2. Pornire compose (backend + nginx)

```powershell
cd 04_SEMINARS\S08\4_nginx
docker compose -f S08_Part04_Config_Docker_Compose.win.yml up
```

> *▸ „Pe Windows nu avem `network_mode: host`. Compose-ul pune backend-ul și nginx în aceeași rețea Docker. nginx accesează backend-ul prin numele serviciului: `http://backend:8000`."*

### E.3. Test comparativ: direct vs proxy

Întrebi înainte: *▸ „Ce diferențe vă așteptați între portul 8000 și 8080?"*

În 🟢 CLIENT:

```powershell
curl.exe -I http://localhost:8000/
curl.exe -I http://localhost:8080/
```

Ce observă:
- pe 8080: `Server: nginx`
- apare `X-Student-Lab: Seminar8`
- body-ul e (aproape) identic

### E.4. Micro-modificare (1 min)

Într-un editor (Notepad / VS Code), modifici `S08_Part04_Config_Nginx.win.conf`:

```nginx
add_header X-Student-Lab "Seminar8-ReverseProxy";
```

Oprești compose (`Ctrl+C`), repornești:

```powershell
docker compose -f S08_Part04_Config_Docker_Compose.win.yml up
```

Testezi:

```powershell
curl.exe -I http://localhost:8080/
```

**Concluzie:** *▸ „Reverse proxy-ul adaugă politici fără să atingă backend-ul."*

### E.5. Wireshark bonus (doar dacă timpul și adapter-ul permit — 2 min max)

1. În Wireshark, alegi **Npcap Loopback Adapter**. Start capture.
2. În 🟢 CLIENT: `curl.exe -v http://localhost:8080/hello`
3. Oprești captura.
4. Display filter: `tcp.port == 8080` → **Follow → TCP Stream**.

> *▸ „Request-ul de aici e exact cel din `curl -v`. Diferența: aici îl vedeți ca flux TCP, cu sequence numbers, ACK-uri. Observabilitatea începe cu `curl`, dar se termină pe fir."*

> **Dacă Wireshark nu vede traficul loopback:** nu insista. Spui: *▸ „Pe unele configurații, Npcap nu capturează loopback. `curl.exe -v` rămâne instrumentul vostru principal."*

---

## Bloc F — Recap + temă (2–3 min)

### F.1. Cele 3 idei de fixat

> *▸ „Trei lucruri din azi:*
> *1. HTTP e text. `curl -v` vi-l arată integral.*
> *2. `Content-Length` e mecanismul prin care clientul știe când s-a terminat răspunsul.*
> *3. Reverse proxy-ul separă clientul de backend. Adaugă politici, nu logică."*

### F.2. Returnare la hook

> *▸ „La început am întrebat: «de unde știe clientul că răspunsul s-a terminat?» Acum știți: Content-Length (robust) și Connection: close (simplu, dar fragil). Decizia asta se ia la fiecare răspuns HTTP."*

### F.3. Livrabile

| Fișier | Ce conține |
|---|---|
| `curl_basics_log.txt` | Output `curl.exe -v` + identificare headere |
| `curl_questions.txt` | De ce curl > browser pentru debugging |
| `builtin_http_log.txt` | Output pe `/`, `/hello`, `/api/time`, `/student` |
| Endpoint `/student` | JSON `{"name": "...", "lab": 8}` |
| `socket_http_log.txt` | Output curl + explicație parsing + Content-Length |
| `reverse_proxy_log.txt` | Comparare direct vs proxy + config nginx modificat |

### F.4. Motivare (fără morală)

- „Un inginer bun nu ghicește: reproduce, capturează, compară headere."
- „Reverse proxy-ul e primul pas spre arhitecturi reale: TLS, caching, rate limiting, load balancing."

---

## Cheat-sheet

### Comenzi `curl.exe` (Windows)

| Comandă | Ce face |
|---|---|
| `curl.exe -v URL` | Request + response verbose |
| `curl.exe -I URL` | Doar response headers |
| `curl.exe -X POST -d "key=val" URL` | POST cu body URL-encoded |
| `curl.exe -V` | Verificare versiune (NU aliasul PowerShell) |

### Docker run (servere S08)

| Server | Comandă |
|---|---|
| Builtin Python | `docker run --rm -it -p 8000:8000 -v ${PWD}:/work -w /work/04_SEMINARS/S08/2_simple-http python:3.12-slim python S08_Part02B_Example_Simple_HTTP_Builtin.py 8000` |
| Socket manual | `docker run --rm -it -p 8000:8000 -v ${PWD}:/work -w /work/04_SEMINARS/S08/3_socket-http python:3.12-slim python S08_Part03B_Example_Socket_HTTP_Server.py 8000` |
| nginx Compose | `docker compose -f S08_Part04_Config_Docker_Compose.win.yml up` (din directorul `4_nginx`) |

### Wireshark (loopback)

| Pas | Ce faci |
|---|---|
| Adapter | Npcap Loopback Adapter |
| Display filter (HTTP) | `http && tcp.port == 8080` |
| Display filter (fallback) | `tcp.port == 8080` |
| Decodare stream | Click dreapta → Follow → TCP Stream |

---

## Plan de contingență

| # | Problemă | Simptom | Soluție |
|---|---|---|---|
| 1 | `curl` e alias PowerShell | Output HTML-encoded, nu text | Folosește explicit `curl.exe` (cu extensia) |
| 2 | Port 8000 ocupat | `Ports are not available` | `netstat -ano | findstr :8000` → identifică PID → oprește procesul |
| 3 | Docker pull lent | Container nu pornește rapid | Pre-pull: `docker pull python:3.12-slim` și `docker pull nginx:1.27-alpine` |
| 4 | Docker Desktop nu rulează | `error during connect` | Pornește Docker Desktop → așteaptă „Docker is running" |
| 5 | Wireshark nu vede loopback | Npcap Loopback Adapter absent | Reinstalează Npcap cu opțiunea „Support loopback traffic". Alternativ: sari peste Wireshark, `curl.exe -v` e suficient |
| 6 | Volume mount eșuează | Container nu vede fișierele | Verifică: ești în root-ul kitului? `${PWD}` funcționează? Alternativ: calea absolută `C:\...\compnet-2025-redo-main:/work` |
| 7 | nginx nu se conectează la backend | 502 Bad Gateway | Verifică: serviciul `backend` rulează? `docker compose logs backend`. Frecvent: eroare de cale în compose (volumes) |

**Regulă de sacrificare:**
1. Primul sacrificat: Wireshark (Bloc E.5) — `curl.exe -v` acoperă observabilitatea
2. Al doilea: demo pe site public (Bloc B.2)
3. Al treilea: micro-modificare nginx (Bloc E.4) — studenții fac la temă
4. Nu se sacrifică: hook-ul, compararea Content-Length, testul direct vs proxy

---

## Referințe (APA 7th ed.)

Buchanan, W. J., Helme, S., & Woodward, A. (2018). Analysis of the adoption of security headers in HTTP. *IET Information Security, 12*(2), 118–126. https://doi.org/10.1049/iet-ifs.2016.0621

Cohen, E., Kaplan, H., & Oldham, J. (1999). Managing TCP connections under persistent HTTP. *Computer Networks, 31*(11–16), 1709–1723. https://doi.org/10.1016/S1389-1286(99)00018-3

Curipallo Martínez, M., Guevara-Vega, A., Reyes Narváez, A., Raura, G., & Barba Molina, H. (2025). Web application protection optimization through Coraza WAF: Performance assessment against OWASP risks in reverse proxy configurations. *Engineering Proceedings, 115*(1), 17. https://doi.org/10.3390/engproc2025115017

Fielding, R. T., Nottingham, M., & Reschke, J. (2022). HTTP Semantics (RFC 9110). Internet Engineering Task Force. https://doi.org/10.17487/RFC9110

Karopoulos, G., Geneiatakis, D., & Kambourakis, G. (2021). Neither good nor bad: A large-scale empirical analysis of HTTP security response headers. In *Trust, Privacy and Security in Digital Business* (pp. 83–95). Springer. https://doi.org/10.1007/978-3-030-86586-3_6

Mogul, J. C. (1995). The case for persistent-connection HTTP. *ACM SIGCOMM Computer Communication Review, 25*(4), 299–313. https://doi.org/10.1145/217391.217465

Nielsen, H. F., Gettys, J., Baird-Smith, A., Prud'hommeaux, E., Lie, H. W., & Lilley, C. (1997). Network performance effects of HTTP/1.1, CSS1, and PNG. *ACM SIGCOMM Computer Communication Review, 27*(4), 155–166. https://doi.org/10.1145/263109.263157

Reese, W. (2008). Nginx: The high-performance web server and reverse proxy. *Linux Journal, 2008*(173). https://doi.org/10.5555/1412202.1412204

---

## Note pedagogice

**Arc cognitiv:** identic cu varianta MININET-SDN. Hook (Content-Length?) → Activare → Conflict (endpoint fără/cu CL) → Explorare → Formalizare → Aplicare → Recap.

**Diferențe structurale față de varianta VM:**
- Serverele rulează în containere Docker, nu nativ pe host. Asta adaugă un strat de complexitate (volume mount, port mapping) dar elimină dependința de Python local.
- nginx folosește Docker networking intern (serviciu `backend`) în loc de `network_mode: host`. Diferența se explică verbal (30 sec) ca motivație pentru Docker Compose.
- Wireshark pe loopback e opțional și degradabil: dacă nu funcționează, `curl.exe -v` oferă aceeași informație la nivel HTTP.

**Tipare socratice:** POE (hook → C.3), capcană 404 (D.2), predicție comparativă (E.3).

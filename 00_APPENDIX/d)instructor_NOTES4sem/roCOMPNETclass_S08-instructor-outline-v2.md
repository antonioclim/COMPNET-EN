# Seminar S08 — HTTP „pe fir": de la `curl` la server minimal și reverse proxy

**Instrumentare HTTP cu `curl`, server Python (`http.server`), server manual cu socket, nginx reverse proxy în Docker**

| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` → `04_SEMINARS/S08/` |
| **Infra** | MININET-SDN (Ubuntu 24.04, utilizator `stud`) + Docker Engine/Compose |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | HTTP e text peste TCP; un server HTTP minimal se reduce la parsarea primei linii + construirea unui răspuns valid cu status, headere și body. |

---

## Obiective operaționale

La finalul seminarului, studentul:

1. Citește un output `curl -v` și identifică fără ezitare: request line, status line, headere relevante, delimitarea header/body (`\r\n\r\n`).
2. Explică rolul `Content-Type` și `Content-Length` — și descrie ce se întâmplă când lipsesc.
3. Pornește, testează și modifică un server HTTP (builtin Python) adăugând un endpoint JSON (`/student`).
4. Distinge între un server care „ascunde" protocolul (builtin) și unul care îl „face vizibil" (socket manual).
5. Justifică de ce un reverse proxy (nginx) apare în fața unui backend în producție.
6. Compară headerele unui răspuns direct (port 8000) cu cele ale aceluiași răspuns prin proxy (port 8080).

---

## Structura seminarului (35–40 min)

| Bloc | Ce se întâmplă | Durată |
|:---:|---|---:|
| **A** | Hook + activare: „când clientul cere `/hello`, cum știe că răspunsul s-a terminat?" | 3 min |
| **B** | HTTP + `curl -v`: request/response ca text, headere vizibile | 7–8 min |
| **C** | Server builtin Python (`http.server`) — 3 endpoint-uri, Content-Length prezent vs absent | 8–9 min |
| **D** | Server HTTP manual (socket) — același răspuns, construit de noi | 8–9 min |
| **E** | nginx reverse proxy (Docker) — aceeași pagină, alte headere | 6–7 min |
| **F** | Recap + temă: fixare 3 idei, returnare la hook | 2–3 min |
| | **Total estimat** | **34–39 min** |

> **Regulă de ritm:** dacă apare fricțiune (port ocupat, Docker trage imagini, internet slab), sari la `localhost` și mergi mai departe. Scopul e modelul mental, nu perfecțiunea demo-ului.

---

## Pregătire înainte să intre studenții (checklist 3 min)

1. Intră în VM, mergi în kit:
   ```bash
   cd ~/compnet-2025-redo/04_SEMINARS/S08
   ls
   ```
   Trebuie să vezi: `1_testing-tools/`, `2_simple-http/`, `3_socket-http/`, `4_nginx/`.

2. Verifică porturile (ideal libere):
   ```bash
   ss -tuln | grep -E ':8000|:8080' || echo "Porturile sunt libere"
   ```

3. Verifică `curl`:
   ```bash
   curl --version | head -1
   ```

4. Pregătește **trei** ferestre de terminal, vizibile simultan pe proiector:
   - 🔵 **SERVER** — va rula serverele
   - 🟢 **CLIENT** — va rula `curl`
   - 🟠 **CAPTURĂ** (opțional) — `tshark` dacă timpul permite

5. (Opțional) Pre-pull imaginea Docker:
   ```bash
   docker pull nginx:alpine
   ```

---

## Bloc A — Hook + activare (3 min)

### Scenariu de deschidere

> *▸ „Pornesc un server pe portul 8000. Trimit `GET /hello`. Serverul răspunde cu textul «Hello». Întrebare: de unde știe clientul că răspunsul s-a terminat? Sunt doar 5 caractere — dar clientul nu știe dinainte câte caractere vin. Cum se descurcă?"*

Lași 10 secunde de gândire. Notezi 2–3 răspunsuri pe tablă (tipic: „serverul închide conexiunea", „trimite lungimea", „un caracter special"). Nu corectezi — le fixezi în Blocul C.

### Activare (legătura cu S07)

> *▸ „La S07 am capturat segmente TCP, am văzut SYN-ACK, payload, FIN. Azi urcăm un strat: înăuntrul acelui payload TCP e protocolul HTTP. Și o să-l facem vizibil."*

**Tipar socratic: POE pregătit.** Predicția de la hook se va verifica concret la Blocul C (endpoint `/hello` fără `Content-Length` vs `/api/time` cu `Content-Length`).

---

## Bloc B — HTTP + `curl -v`: anatomia unui request/response (7–8 min)

### B.1. Predicții (constructivist)

Întrebări scurte, cu mâna sus:

- „Când scriu `GET /`, ce trimite clientul *pe lângă* această linie?"
- „De ce ar vrea serverul să specifice tipul conținutului (`Content-Type`)?"

Nu corectezi imediat. Le notezi pe tablă.

### B.2. Demo cu site public (doar dacă merge internetul)

În 🟢 CLIENT:

```bash
curl -I http://example.com
```

Ce arăți cu cursorul:
- linia de status: `HTTP/1.1 200 OK`
- 2–3 headere: `Content-Type`, `Content-Length`, `Date`

Apoi verbose:

```bash
curl -v http://example.com
```

Ce explici **în timp ce curge textul**:
- liniile cu `>` = request headers (ce trimite clientul)
- liniile cu `<` = response headers (ce trimite serverul)
- linia goală (`\r\n\r\n`) separă headerele de body

> Dacă site-ul face redirect HTTPS (301 + `Location`), spui scurt: *▸ „Redirect-ul e tot HTTP: status 301 + header `Location`. Urmărirea o facem cu `-L`, dar azi ne interesează structura, nu lanțul de redirect-uri."*

> **Dacă internetul nu merge:** sari direct la B.3.

### B.3. Epifanie: HTTP e text

> *▸ „Tot ce vedeți aici e text ASCII. HTTP, în forma clasică (fără TLS), e literalmente text peste TCP. De asta debugging-ul e atât de direct — și de asta `curl -v` e instrumentul de laborator implicit."*

Le spui că exact asta documentează în `curl_basics_log.txt` și `curl_questions.txt` (din `1_testing-tools/`).

**Material suport:** pagina interactivă `_HTMLsupport/S08/1_testing-tools/S08_Part01_Page_Testing_Tools.html` (de arătat studenților pentru studiu individual).

---

## Bloc C — Server builtin Python: „serverul face multă muncă invizibilă" (8–9 min)

**Fișiere kit:**
- `2_simple-http/S08_Part02A_Explanation_Http_server_Builtin.md` (lectură pre/post-seminar)
- `2_simple-http/S08_Part02B_Example_Simple_HTTP_Builtin.py` (codul pe care îl rulăm)

### C.1. Pornire server

În 🔵 SERVER:

```bash
cd 2_simple-http
python3 S08_Part02B_Example_Simple_HTTP_Builtin.py 8000
```

> *▸ „Server HTTP complet funcțional, construit pe `http.server` din biblioteca standard Python. Nu e framework — e standard library. Routing, headere, status codes — în câteva zeci de linii."*

### C.2. Testare 3 endpoint-uri

În 🟢 CLIENT:

```bash
curl -v http://localhost:8000/
curl -v http://localhost:8000/hello
curl -v http://localhost:8000/api/time
```

**Ce spui și arăți cu cursorul, pas cu pas:**

1. La `/`: serverul listează sau servește conținut din directorul curent (comportament `SimpleHTTPRequestHandler`).
2. La `/hello`:
   - identifici `Content-Type: text/plain; charset=utf-8`
   - **observație cheie:** NU apare `Content-Length` — serverul nu l-a trimis explicit
3. La `/api/time`:
   - identifici `Content-Type: application/json`
   - identifici `Content-Length: <valoare>` — de data asta e explicit

### C.3. Conflict cognitiv: returnare la hook (POE — Observație + Explicație)

> *▸ „Acum avem răspunsul la întrebarea de la început. La `/hello`, serverul NU a trimis Content-Length. Cum se descurcă clientul? Răspuns: protocolul e HTTP/1.0, iar serverul închide conexiunea (`Connection: close`). Clientul citește până la EOF."*
>
> *▸ „La `/api/time`, serverul a trimis explicit `Content-Length`. Clientul știe exact câți octeți să aștepte. Asta e mecanismul robust — și e motivul pentru care în HTTP/1.1 cu conexiuni persistente, `Content-Length` devine obligatoriu (sau se folosește `Transfer-Encoding: chunked`)."*

**Tipar socratic: POE complet.** Predicție (hook) → Observație (`curl -v` pe două endpoint-uri) → Explicație (mecanismul de terminare).

### C.4. Temă (foarte concret)

> *▸ „Modificați handler-ul: adăugați `/student`, returnați JSON cu numele vostru și `lab: 8`. Testați cu `curl -v`. Salvați output-ul în `builtin_http_log.txt`."*

Menționezi: în tasks apare uneori `simple_http_builtin.py`, dar în kit fișierul este `S08_Part02B_Example_Simple_HTTP_Builtin.py` — același lucru.

**Material suport:** `_HTMLsupport/S08/2_simple-http/S08_Part02_Page_Simple_HTTP.html`.

---

## Bloc D — Server HTTP manual cu socket: „protocolul devine concret" (8–9 min)

**Fișiere kit:**
- `3_socket-http/S08_Part03A_Explanation_HTTP_Socket.md`
- `3_socket-http/S08_Part03B_Example_Socket_HTTP_Server.py`
- `3_socket-http/static/S08_Part03_Page_Index.html`

### D.1. Oprire builtin, pornire server manual

În 🔵 SERVER: `Ctrl+C` (oprești builtin). Apoi:

```bash
cd ../3_socket-http
python3 S08_Part03B_Example_Socket_HTTP_Server.py 8000
```

Output așteptat:
```text
Manual HTTP server started on port 8000
```

### D.2. Testare + observații (tipar „capcană de concepție greșită")

În 🟢 CLIENT:

```bash
curl -v http://localhost:8000/
curl -v http://localhost:8000/index.html
curl -v http://localhost:8000/doesnotexist
```

**Observații verbalizate explicit:**

1. **Routing minimal:** `/` e mapat la `S08_Part03_Page_Index.html` din `static/`. Maparea e o decizie a programatorului, nu a protocolului.
2. **404 nu e magie:** e doar o linie de status + headere + body HTML minimal. Serverul manual construiește fiecare octet.
3. **Content-Length e prezent mereu** în serverul manual (funcția `build_http_response` îl include). Comparați cu serverul builtin care „uita" să-l trimită pe `/hello`.

> *▸ „Concepția greșită obișnuită: 404 e «eroare de server». Nu. 404 e un răspuns HTTP perfect valid — cu status line, headere, body. Eroarea e doar semantică: fișierul nu există."*

**Tipar socratic: capcană de concepție greșită** — 404 ca „eroare" vs 404 ca răspuns valid.

### D.3. Demo opțional (dacă ai 2 min): request scris de mână cu `nc`

```bash
printf 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n' | nc -q 1 127.0.0.1 8000
```

> *▸ „Asta e, la propriu, HTTP. Browserul face automat exact acest text. Acum vedeți de ce un bug în `\r\n\r\n` sau în `Content-Length` vă strică tot."*

### D.4. Punct pedagogic (închidere bloc)

> *▸ „Serverul builtin ascunde protocolul în bibliotecă. Serverul manual îl face vizibil: fiecare header e o decizie explicită a programatorului."*

Temă: în `socket_http_log.txt` descriu parsarea requestului, decizia de fișier și rolul `Content-Length`. Fișierul `S08_Part03X_Tasks_HTTP_Socket.md` cere și test în browser + explicație 5-6 propoziții.

**Material suport:** `_HTMLsupport/S08/3_socket-http/S08_Part03_Page_Socket_HTTP.html`.

---

## Bloc E — nginx reverse proxy în Docker: „aceeași aplicație, altă arhitectură" (6–7 min)

**Fișiere kit:**
- `4_nginx/S08_Part04A_Explanation_Nginx_Reverse_Proxy.md`
- `4_nginx/S08_Part04_Config_Docker_Compose.yml` (folosește `network_mode: host`)
- `4_nginx/S08_Part04_Config_Nginx.conf` (`proxy_pass http://127.0.0.1:8000`)

### E.1. Pornire backend pe 8000

În 🔵 SERVER (un tab nou, sau după `Ctrl+C` pe serverul manual):

```bash
cd ../2_simple-http
python3 S08_Part02B_Example_Simple_HTTP_Builtin.py 8000
```

Verificare rapidă în 🟢 CLIENT:

```bash
curl -I http://localhost:8000/
```

### E.2. Pornire nginx (Docker Compose)

Într-un al doilea tab al 🔵 SERVER, în `4_nginx/`:

```bash
cd ../4_nginx
docker compose -f S08_Part04_Config_Docker_Compose.yml up
```

> *▸ „Docker Compose-ul din kit folosește `network_mode: host` — containerul nginx vede 127.0.0.1:8000 ca și cum ar fi pe aceeași mașină. Simplu, dar funcționează doar pe Linux."*

### E.3. Test comparativ: direct vs proxy (predicție)

Înainte de a rula, întrebi:

> *▸ „Ce diferențe vă așteptați să vedeți între răspunsul de pe portul 8000 și cel de pe 8080?"*

În 🟢 CLIENT:

```bash
curl -I http://localhost:8000/
curl -I http://localhost:8080/
```

**Ce îi obligi să observe:**

- pe 8080 apare `Server: nginx/...`
- apare headerul custom: `X-Student-Lab: Seminar8`
- body-ul e (aproape) identic cu cel de pe 8000

### E.4. Micro-modificare (1–2 min)

În 🔵 SERVER, editează config-ul:

```bash
nano S08_Part04_Config_Nginx.conf
```

Modifică:
```nginx
add_header X-Student-Lab "Seminar8-ReverseProxy";
```

Oprești compose (`Ctrl+C`), repornești:
```bash
docker compose -f S08_Part04_Config_Docker_Compose.yml up
```

În 🟢 CLIENT:
```bash
curl -I http://localhost:8080/
```

**Concluzie de efect:**

> *▸ „Reverse proxy-ul poate adăuga politici — headere de securitate, rate limiting, caching — fără să atingă o linie din backend."*

**Material suport:** `_HTMLsupport/S08/4_nginx/S08_Part04_Page_Nginx.html`.

---

## Bloc F — Recap + temă (2–3 min)

### F.1. Cele 3 idei de fixat

> *▸ „Trei lucruri din azi:*
> *1. HTTP e text. `curl -v` vi-l arată integral.*
> *2. `Content-Length` e mecanismul prin care clientul știe când s-a terminat răspunsul. Fără el, se bazează pe închiderea conexiunii — fragil.*
> *3. Reverse proxy-ul e stratul care separă clientul de backend. Adaugă politici, nu logică."*

### F.2. Returnare la hook

> *▸ „La început am întrebat: «de unde știe clientul că răspunsul s-a terminat?» Acum știți două mecanisme: Content-Length (robust, explicit) și Connection: close (simplu, dar incompatibil cu conexiuni persistente). Asta e una din deciziile pe care un server HTTP real le ia la fiecare răspuns."*

### F.3. Livrabile (dictat sau pe ecran)

| Fișier | Sursă din kit | Ce conține |
|---|---|---|
| `curl_basics_log.txt` | `1_testing-tools/` | Output `curl -v` pe `example.com` + identificare headere |
| `curl_questions.txt` | `1_testing-tools/` | De ce curl > browser pentru debugging (2–3 propoziții) |
| `builtin_http_log.txt` | `2_simple-http/` | Output curl pe `/`, `/hello`, `/api/time`, `/student` |
| Endpoint `/student` | `2_simple-http/S08_Part02B_...py` | JSON `{"name": "...", "lab": 8}` |
| `socket_http_log.txt` | `3_socket-http/` | Output curl + explicație parsing + Content-Length |
| `reverse_proxy_log.txt` | `4_nginx/` | Comparare direct vs proxy + config nginx modificat |

### F.4. Preview S09

> *▸ „La S09: protocoale de fișiere. Server FTP custom, transfer minimal, multi-client cu containere. Logica de la S08 se extinde: alt protocol, dar aceleași principii — request, response, headere, status."*

---

## Cheat-sheet

### Comenzi `curl`

| Comandă | Ce face |
|---|---|
| `curl -v URL` | Request + response verbose (headere complete) |
| `curl -I URL` | Doar response headers (HEAD request) |
| `curl -X POST -d "key=val" URL` | POST cu body URL-encoded |
| `curl -o fisier.html URL` | Salvează body-ul într-un fișier |
| `curl -w "%{http_code}" URL` | Afișează doar status code |

### Servere S08

| Server | Pornire | Port | Oprire |
|---|---|---|---|
| Builtin Python | `python3 S08_Part02B_Example_Simple_HTTP_Builtin.py 8000` | 8000 | `Ctrl+C` |
| Socket manual | `python3 S08_Part03B_Example_Socket_HTTP_Server.py 8000` | 8000 | `Ctrl+C` |
| nginx (Docker) | `docker compose -f S08_Part04_Config_Docker_Compose.yml up` | 8080 | `Ctrl+C` |

### Headere HTTP relevante

| Header | Rol |
|---|---|
| `Content-Type` | Tipul conținutului (ex: `text/html`, `application/json`) |
| `Content-Length` | Lungimea body-ului în octeți |
| `Connection` | `close` (oprește conexiunea) sau `keep-alive` (conexiune persistentă) |
| `Server` | Identifică software-ul server (ex: `nginx/1.27`) |
| `X-Student-Lab` | Header custom adăugat de nginx (din config) |

### Verificare porturi

```bash
ss -tuln | grep -E ':8000|:8080'
```

---

## Plan de contingență

| # | Problemă | Simptom | Soluție |
|---|---|---|---|
| 1 | Port 8000 ocupat | `Address already in use` | `ss -tuln | grep :8000` → identifică PID → `kill <PID>` sau folosește port 9000 |
| 2 | Internet indisponibil | `curl http://example.com` timeout | Sari la Bloc C (server local). Demo-ul pe site public e doar bonus |
| 3 | Docker pull lent (nginx:alpine) | compose blochează la pull | Pre-pull: `docker pull nginx:alpine`. Alternativ: sari la Bloc F, tema include nginx |
| 4 | `curl` returnează erori de conexiune | `Connection refused` | Verifică: serverul rulează? Portul e corect? Firewall? `ss -tuln` |
| 5 | Serverul manual returnează 500 | Eroare Python în terminal 🔵 | Citește traceback-ul. Cele mai frecvente: fișier lipsă în `static/`, eroare de parsare request |
| 6 | nginx nu pornește | Eroare config în loguri | `docker compose logs nginx` — de obicei linia de eroare indică exact unde e problema în `.conf` |
| 7 | Serverul builtin nu răspunde la `/api/time` | Eroare 404 sau timeout | Verifică că rulezi `S08_Part02B_Example_Simple_HTTP_Builtin.py`, nu `python3 -m http.server` |

**Regulă de sacrificare (dacă timpul se comprimă):**
1. Primul sacrificat: demo-ul pe site public (Bloc B.2) — sari direct la server local
2. Al doilea: demo-ul opțional cu `nc` (Bloc D.3)
3. Al treilea: micro-modificarea nginx (Bloc E.4) — menționezi verbal, studenții fac singuri la temă
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

**Arc cognitiv al seminarului:**

```
Hook (Content-Length?) → Activare (S07 → HTTP) → Conflict (endpoint fără CL vs cu CL)
  → Explorare ghidată (curl → builtin → socket → nginx) → Formalizare (mecanismele de terminare)
    → Aplicare (temă: endpoint /student, log-uri) → Recap (3 idei + hook reluat)
```

**Tipare socratice folosite:**
1. **POE complet** (Bloc A → C.3): predicție la hook → observație pe `/hello` vs `/api/time` → explicație despre Content-Length și Connection: close.
2. **Capcană de concepție greșită** (Bloc D.2): 404 = „eroare de server" vs 404 = răspuns HTTP valid.
3. **„Ce s-ar fi întâmplat dacă…?"** (Bloc D.3, opțional): request HTTP scris manual — un `\r\n` greșit strică totul.
4. **Predicție înainte de comparație** (Bloc E.3): „ce diferențe vă așteptați?" → verificare cu curl.

**Epifanii vizate:**
- Bloc B.3: „HTTP e text" — studenții îl văd decodat, caracter cu caracter.
- Bloc C.3: absența Content-Length pe `/hello` vs prezența pe `/api/time` — mecanismele de terminare devin concrete.
- Bloc D.4: „fiecare header e o decizie" — serverul manual elimină toată magia bibliotecii.

**Legătură cu concepțiile greșite documentate:**
- Misconception #12 (recv() returnează mesajul complet): Content-Length este exact mecanismul care rezolvă problema recv() parțial — fără el, clientul nu știe când s-a terminat body-ul.
- Misconception #5 (porturile se expun automat): nginx în Docker cu `network_mode: host` ocolește mapping-ul explicit, dar conceptul e reforțat prin contrastul cu varianta Windows.

**Cross-referințe:**
- S07: „am capturat segmente TCP" → acum vedem payload-ul HTTP din acele segmente.
- S09: „alt protocol (FTP), aceeași logică de request-response."
- S11: „nginx ca load balancer" → la S08 e primul contact cu nginx, doar reverse proxy simplu.

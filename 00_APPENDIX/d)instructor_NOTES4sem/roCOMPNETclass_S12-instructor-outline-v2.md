# Seminar S12 — RPC în practică: de la JSON lizibil la contract binar
| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` · `04_SEMINARS/S12/` |
| **Infra** | MININET-SDN (VM Ubuntu 24.04, VirtualBox, headless) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | RPC transformă un apel de funcție într-un schimb de mesaje pe rețea; contractul `.proto` mută efortul de la „parsăm manual" la „generăm cod". |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. Formula cel puțin trei diferențe concrete între modelul RPC (Remote Procedure Call) și REST, în termeni de model mental și implicații de rețea.
2. Identifica câmpurile unui mesaj JSON-RPC 2.0 (`jsonrpc`, `method`, `params`, `id`) și interpreta răspunsul (`result` / `error`).
3. Completa un fișier `.proto` minimal (mesaje + serviciu) și genera codul Python cu `grpc_tools.protoc`.
4. Rula un server gRPC și un client gRPC pe două host-uri Mininet diferite (h1, h2), folosind IP-ul corect ca target.
5. Observa în captură de trafic (tcpdump/tshark) contrastul dintre payload JSON lizibil și cadre HTTP/2 + protobuf binar.
6. Diagnostica eroarea produsă când clientul gRPC apelează un server oprit — diferențiind comportamentul de un apel local.

---

## Structura seminarului

| Bloc | Minute | Titlu | Rezultat vizibil |
|---|---:|---|---|
| A | 0–3 | Hook: „Funcție locală sau la distanță?" | Studenții formulează predicții |
| B | 3–8 | Mini-teorie: RPC vs REST | Trei contraste fixate |
| C | 8–18 | Demo 1: JSON-RPC (h2 → h1) + captură | Payload JSON lizibil în tshark |
| D | 18–25 | Protobuf: completăm `.proto` + codegen | Fișierele `*_pb2*.py` generate |
| E | 25–35 | Demo 2: gRPC (h2 → h1) + experiment eșec | Rezultate Add/Multiply/Power + eroare fără server |
| F | 35–40 | Captură gRPC + recap cu reluare hook | „De ce nu mai pot citi payload-ul?" |

---

## Pregătire înainte de seminar (instructor, 5–10 min)

### Verificare mediu

```bash
cd ~/compnet-2025-redo-main       # sau calea efectivă din VM
source ~/venvs/compnet/bin/activate 2>/dev/null || true
python3 -c "import requests, grpc; import grpc_tools; print('OK')"
```

Dacă importurile eșuează:

```bash
python3 -m pip install -U pip
python3 -m pip install requests grpcio grpcio-tools
```

### Pre-creare server JSON-RPC

Serverul JSON-RPC minimal nu există în kit — trebuie creat o singură dată. Recomandare: creează-l *înainte* de seminar, nu în fața studenților (evită 2 minute de lipire în `nano`).

```bash
cd 04_SEMINARS/S12/1_jsonrpc
cat > jsonrpc_server_minimal.py << 'PYEOF'
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ast, operator

BIN_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}
UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

def safe_eval(expr: str):
    node = ast.parse(expr, mode="eval").body
    def _eval(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in BIN_OPS:
            return BIN_OPS[type(n.op)](_eval(n.left), _eval(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in UNARY_OPS:
            return UNARY_OPS[type(n.op)](_eval(n.operand))
        raise ValueError("Unsupported expression.")
    return _eval(node)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            req = json.loads(body)
            method, params = req.get("method"), req.get("params", [])
            req_id = req.get("id")
            if method != "evaluate":
                raise ValueError(f"Unknown method: {method}")
            expr = params[0] if params else ""
            result = safe_eval(expr)
            resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
            print(f"[JSONRPC-SERVER] evaluate({expr}) -> {result}")
        except Exception as e:
            resp = {"jsonrpc": "2.0", "id": None,
                    "error": {"code": -32602, "message": str(e)}}
            print("[JSONRPC-SERVER] error:", e)
        data = json.dumps(resp).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def main():
    host, port = "0.0.0.0", 8080
    print(f"[JSONRPC-SERVER] listening on http://{host}:{port}")
    HTTPServer((host, port), Handler).serve_forever()

if __name__ == "__main__":
    main()
PYEOF
```

### Repetiție codegen (opțional)

```bash
cd ../3_grpc
python3 -m grpc_tools.protoc -I../2_protobuf \
    --python_out=. --grpc_python_out=. \
    ../2_protobuf/S12_Part02_Config_Calculator.proto
python3 -c "import S12_Part02_Config_Calculator_pb2 as pb2; print('OK pb2')"
```

### Pre-editare URL-uri

Dacă nu vrei să editezi în fața studenților:

1. În `1_jsonrpc/S12_Part01_Script_JSONRPC_Client.py`, schimbă `URL = "https://api.mathjs.org/v4/"` în `URL = "http://10.0.0.1:8080/"`.
2. În `3_grpc/S12_Part03_Script_g_RPC_Client.py`, schimbă `GRPC_TARGET = "localhost:50051"` în `GRPC_TARGET = "10.0.0.1:50051"`.

---

## Bloc A (0–3 min) — Hook: „Funcție locală sau la distanță?"

> *▸ „Până acum am lucrat mult cu HTTP — request pe o resursă, response cu date. Astăzi schimbăm o singură propoziție în cap: nu mai cerem o resursă, ci chemăm o funcție la distanță. Uite, ceva concret:"*

**Fă (pe tablă sau ecran partajat):** scrie două linii de cod:

```python
# local
result = add(2, 3)

# remote (RPC)
result = server.Add(AddRequest(a=2, b=3))
```

> *▸ „Arată aproape la fel. Dar întrebarea-capcană: ce se întâmplă dacă serverul nu răspunde? La varianta locală — nu avem cum să avem problema asta. La varianta remote — e o altă poveste."*

**Predicție (ridică mâini, 20–30 sec):**

- „Dacă rețeaua are latență de 500 ms, apelul remote durează 500 ms mai mult. Cine crede că *doar* latența e problema?" (Majoritatea ridică mâna. Răspunsul corect: și timeout, și erori de conexiune, și versiuni incompatibile.)

> *▸ „Păstrați întrebarea în cap. La final, vă arăt ce se întâmplă concret."*

**De ce funcționează ca hook:** scenariu concret (două linii de cod), provoacă surpriză (problema nu e doar latența), tematic (RPC = tema zilei), concis (sub 3 min), returnabil (revenim la final cu experimentul server oprit).

---

## Bloc B (3–8 min) — Mini-teorie: RPC vs REST

> *▸ „De la S08 și S10 știm cum funcționează HTTP și REST. Acum le punem pe masă lângă RPC și vedem diferențele."*

**Fixează 3 contraste (spuse concis, scrise pe tablă/slide):**

1. **Model mental:** REST = resurse (URI-uri + verbe HTTP); RPC = metode/proceduri (apelezi o funcție).
2. **Contract:** REST adesea fără contract formal (documentație OpenAPI opțională); gRPC = contract `.proto` strict → cod generat automat.
3. **Observabilitate:** REST + JSON = lizibil direct în pcap; gRPC = eficient, dar binar — necesită tooling (logging, interceptors, `grpcurl`).

> *▸ „RPC îți dă iluzia de local. Asta e sursa clasică de bug-uri — tratezi apelul ca și cum nu ar putea eșua."*

**Legătură cu kit-ul:** studenții pot citi `1_jsonrpc/S12_Part01A_Explanation_RPC_Intro.md` pentru tabelul complet RPC vs REST, tipuri de RPC (unary, streaming), și contexte de utilizare.

---

## Bloc C (8–18 min) — Demo 1: JSON-RPC în Mininet (h2 → h1)

### C.1 Pornești Mininet

**Fă (din directorul `04_SEMINARS/S12`):**

```bash
cd ~/compnet-2025-redo-main/04_SEMINARS/S12
sudo mn --topo single,2 --mac --switch ovsk --controller none
```

**Fă (verificare IP, 15 sec):**

```
mininet> h1 ip -4 addr show h1-eth0
mininet> h2 ip -4 addr show h2-eth0
```

> *▸ „Mininet ne dă două host-uri cu namespace-uri de rețea separate — IP-uri diferite. RPC-ul e cu adevărat remote."*

### C.2 Pornești serverul JSON-RPC pe h1 🔵

```
mininet> h1 python3 1_jsonrpc/jsonrpc_server_minimal.py &
```

Ar trebui să apară:

```text
[JSONRPC-SERVER] listening on http://0.0.0.0:8080
```

> *▸ „Serverul ascultă pe portul 8080. Evaluarea expresiei e deliberat restricționată — scopul e să vedem protocolul, nu să facem un calculator de producție."*

### C.3 Rulezi clientul pe h2 🟢

**Predicție (POE — Predicție-Observație-Explicație):**

> *▸ „Clientul trimite un JSON cu `method: evaluate` și `params: ["2+3"]`. Ce formă are răspunsul — credeți că serverul returnează un string, un număr, sau altceva?"*

**Fă:**

```
mininet> h2 python3 1_jsonrpc/S12_Part01_Script_JSONRPC_Client.py
```

**Observație:** clientul afișează payload-ul JSON (lizibil) și rezultatul `evaluate(2+3) = 5`. Serverul raportează `[JSONRPC-SERVER] evaluate(2+3) -> 5`.

**Explicație:**

> *▸ „Rezultatul e un număr — câmpul `result` din răspunsul JSON-RPC. Observați: tot schimbul e text clar. Asta e confortabil pentru debug, dar plătim cu overhead de serializare."*

**Fixare (15 sec):**

> *▸ „În request, care câmp decide ce funcție se execută pe server? — `method`."*

### C.4 Captură pcap JSON-RPC 🟠

```
mininet> h1 tcpdump -i h1-eth0 -w /tmp/jsonrpc.pcap tcp port 8080 -c 50 &
mininet> h2 python3 1_jsonrpc/S12_Part01_Script_JSONRPC_Client.py
```

Apoi, în VM (alt terminal):

```bash
tshark -r /tmp/jsonrpc.pcap -q -z follow,tcp,ascii,0 | head -n 80
```

> *▸ „Aici e motivul pentru care REST cu JSON e popular: când ai o problemă, poți citi direct conversația din trafic."*

---

## Bloc D (18–25 min) — Protobuf: contract + codegen

**Tranziție:**

> *▸ „Am văzut JSON-RPC: simplu, lizibil, fără contract formal. Acum trecem la cealaltă extremă: definim un contract explicit, iar codul se generează automat. Când contractul e explicit, nu mai construim payload manual."*

### D.1 Completezi `.proto` (2–3 min)

**Fă (în alt terminal al VM, nu în Mininet):**

```bash
cd ~/compnet-2025-redo-main/04_SEMINARS/S12/2_protobuf
nano S12_Part02_Config_Calculator.proto
```

**Completează în locurile TODO:**

```proto
message PowerRequest {
  int32 base = 1;
  int32 exponent = 2;
}

message PowerResponse {
  int32 result = 1;
}
```

Și în `service Calculator`:

```proto
rpc Power (PowerRequest) returns (PowerResponse);
```

**Micro-epifanie:**

> *▸ „Numerele câmpurilor — `= 1`, `= 2` — nu sunt decor. Intră în formatul binar; asta permite adăugarea de câmpuri noi fără a sparge clienții existenți. De aici vine ideea de compatibilitate în timp."*

### D.2 Generezi pb2-urile în `3_grpc/` (3–4 min)

```bash
cd ../3_grpc
python3 -m grpc_tools.protoc -I../2_protobuf \
    --python_out=. --grpc_python_out=. \
    ../2_protobuf/S12_Part02_Config_Calculator.proto
ls -1 S12_Part02_Config_Calculator_pb2*.py
```

Trebuie să vezi:

- `S12_Part02_Config_Calculator_pb2.py` — definițiile de mesaje
- `S12_Part02_Config_Calculator_pb2_grpc.py` — stub-urile server/client

**Gotcha:**

> *▸ „Scripturile server și client importă pb2-urile din același folder — `3_grpc/`. Dacă generați în altă parte, ori copiați fișierele, ori ajustați `PYTHONPATH`."*

Dacă nu apar ambele fișiere, nu mergi mai departe.

**Referință pentru studenți:** detalii despre structura `.proto` în `2_protobuf/S12_Part02A_Explanation_Protobuf.md`.

---

## Bloc E (25–35 min) — Demo 2: gRPC în Mininet (h2 → h1)

### E.1 Pornești serverul gRPC pe h1 🔵

Oprește serverul JSON-RPC (dacă rulează încă):

```
mininet> h1 kill %1
```

Pornește serverul gRPC:

```
mininet> h1 python3 3_grpc/S12_Part03_Script_g_RPC_Server.py &
```

Ar trebui să apară:

```text
[SERVER] gRPC Calculator server started on port 50051
```

### E.2 Rulezi clientul gRPC pe h2 🟢

```
mininet> h2 python3 3_grpc/S12_Part03_Script_g_RPC_Client.py
```

Dictează valori predictibile:

- Add: `7` și `5` → 12
- Multiply: `4` și `6` → 24
- Power: `2` și `10` → 1024

> *▸ „Observați experiența de programare: `stub.Add(request)` arată ca un apel local. Dar în spate e o conexiune TCP, cadre HTTP/2 și mesaje binare serializate cu protobuf."*

**Ce se vede:**
- 🟢 CLIENT: `Add(7, 5) = 12`, `Multiply(4, 6) = 24`, `Power(2, 10) = 1024` + crează `grpc_client_log.txt`
- 🔵 SERVER: trei linii de log cu valorile primite

### E.3 Experiment: server oprit 🔵→❌ (30 sec)

**Tipar socratic: „Ce s-ar fi întâmplat dacă…?"**

> *▸ „Acum oprim serverul și rulăm clientul din nou."*

```
mininet> h1 kill %1
mininet> h2 python3 3_grpc/S12_Part03_Script_g_RPC_Client.py
```

**Predicție:**

> *▸ „Ce tip de eroare primiți?"*

**Observație:** eroare `grpc._channel._InactiveRpcError: ... UNAVAILABLE`.

**Explicație:**

> *▸ „La un apel local, nu ai cum să primești UNAVAILABLE. Asta e diferența fundamentală: apelul arată local, dar comportamentul e de rețea. Concepția greșită clasică din sistemele distribuite — presupui că rețeaua e fiabilă."*

**Legătură cu hook-ul:** exact întrebarea de la început — „ce se întâmplă când serverul nu răspunde?"

---

## Bloc F (35–40 min) — Captură gRPC + recap

### F.1 Captură pcap gRPC 🟠 (dacă ai timp — 2 min)

Repornește serverul:

```
mininet> h1 python3 3_grpc/S12_Part03_Script_g_RPC_Server.py &
```

Captură:

```
mininet> h1 tcpdump -i h1-eth0 -w /tmp/grpc.pcap tcp port 50051 -c 80 &
mininet> h2 python3 3_grpc/S12_Part03_Script_g_RPC_Client.py
```

Apoi, în VM:

```bash
tshark -r /tmp/grpc.pcap -q -z follow,tcp,ascii,0 | head -n 80
```

**Epifanie:**

> *▸ „Traficul e acolo, dar nu mai e prietenos pentru ochiul uman. Vedeți prefața HTTP/2 și payload binar. Asta nu e un defect — e o alegere: eficiență + contract + tooling în loc de lizibilitate directă."*

### F.2 Recap cu reluare hook (2 min)

> *▸ „Trei lucruri de reținut din seminarul de azi:"*

1. **RPC = apel de funcție peste rețea.** Arată local, dar suportă toate riscurile rețelei (latenţă, eșec, versiuni incompatibile) — ați văzut eroarea UNAVAILABLE.
2. **Contract `.proto` → cod generat.** Nu mai scriem manual payload-uri JSON; definim o interfață, generăm stub-uri, iar server și client vorbesc aceeași „limbă" binar.
3. **Observabilitate:** JSON e lizibil direct în trafic; gRPC necesită tooling — dar câștigă eficiență și tipizare.

> *▸ „La S13 trecem la securitate: scanare de porturi și testare de vulnerabilități. Ce ați lucrat azi — porturi deschise, servicii care ascultă — devine suprafața de atac pe care o vom analiza."*

### F.3 Teme — ce livrează studenții

| Task (.md din kit) | Livrabil | Ce se cere |
|---|---|---|
| `S12_Part01B_Tasks_RPC.md` | `stage1_rpc_intro_answers.txt` | 3 diferențe RPC/REST, avantaje/dezavantaje, rolul protobuf |
| `S12_Part01D_Tasks_JSONRPC.md` | `stage2_jsonrpc_output.txt` | Expresie + request JSON + response |
| `S12_Part02B_Tasks_Protobuf.md` | `stage3_protobuf_output.txt` | `.proto` completat + listing pb2-uri |
| `S12_Part03B_Tasks_g_RPC_Server.md` | `stage4_grpc_server_log.txt` | Log server (Add/Multiply/Power) + reflecție `.proto` |
| `S12_Part03D_Tasks_g_RPC_Client.md` | `stage5_grpc_client_results.txt` | Log client + comparație gRPC vs REST (3–5 propoziții) |

**Materiale de referință pentru studenți:** fișierele `.md` explicative din fiecare subfolder + paginile HTML interactive din `_HTMLsupport/S12/`.

> *▸ „Dacă terminați S12 complet, ați trecut pragul de la «știu HTTP» la «știu un mecanism modern de comunicare inter-servicii cu contract, stub-uri și testare minimală»."*

---

## Cheat-sheet

### Comenzi cheie

| Ce | Comandă |
|---|---|
| Pornire Mininet | `sudo mn --topo single,2 --mac --switch ovsk --controller none` |
| IP h1 | `10.0.0.1` (default Mininet `single,2`) |
| IP h2 | `10.0.0.2` |
| Server JSON-RPC | `h1 python3 1_jsonrpc/jsonrpc_server_minimal.py &` |
| Client JSON-RPC | `h2 python3 1_jsonrpc/S12_Part01_Script_JSONRPC_Client.py` |
| Codegen protobuf | `python3 -m grpc_tools.protoc -I../2_protobuf --python_out=. --grpc_python_out=. ../2_protobuf/S12_Part02_Config_Calculator.proto` |
| Server gRPC | `h1 python3 3_grpc/S12_Part03_Script_g_RPC_Server.py &` |
| Client gRPC | `h2 python3 3_grpc/S12_Part03_Script_g_RPC_Client.py` |
| Captură JSON-RPC | `h1 tcpdump -i h1-eth0 -w /tmp/jsonrpc.pcap tcp port 8080 -c 50 &` |
| Captură gRPC | `h1 tcpdump -i h1-eth0 -w /tmp/grpc.pcap tcp port 50051 -c 80 &` |
| Inspecție pcap | `tshark -r /tmp/<fisier>.pcap -q -z follow,tcp,ascii,0 \| head -n 80` |
| Oprire proces background | `h1 kill %1` sau `pkill -f <script>` |

### Porturi

| Serviciu | Port |
|---|---|
| JSON-RPC server | 8080 (TCP) |
| gRPC server | 50051 (TCP) |

### Fișiere generate de codegen

| Fișier | Conținut |
|---|---|
| `S12_Part02_Config_Calculator_pb2.py` | Clasele de mesaje (AddRequest, AddResponse, …) |
| `S12_Part02_Config_Calculator_pb2_grpc.py` | Stub-uri și Servicer (CalculatorStub, CalculatorServicer) |

---

## Plan de contingență

| # | Problemă | Simptom | Soluție | Timp pierdut |
|---|---|---|---|---|
| 1 | `ModuleNotFoundError: grpc_tools` | Import eșuat la server/codegen | `python3 -m pip install grpcio grpcio-tools` | 30–60 sec |
| 2 | pb2-urile nu se găsesc la import | `ModuleNotFoundError: S12_Part02_Config_Calculator_pb2` | Verifică: `ls 3_grpc/S12_Part02_Config_Calculator_pb2*.py`. Dacă lipsesc, rulează codegen din `3_grpc/`. | 30 sec |
| 3 | Clientul gRPC se conectează la `localhost` | `UNAVAILABLE` deși serverul rulează pe h1 | Verifică `GRPC_TARGET` — trebuie să fie `10.0.0.1:50051`, nu `localhost:50051`. | 15 sec |
| 4 | Port 8080/50051 ocupat | `OSError: [Errno 98] Address already in use` | `pkill -f jsonrpc_server_minimal.py` sau `pkill -f S12_Part03_Script_g_RPC_Server.py` | 10 sec |
| 5 | `requests` lipsește | `ModuleNotFoundError: No module named 'requests'` la clientul JSON-RPC | `python3 -m pip install requests` | 20 sec |
| 6 | Mininet nu pornește | `mn: command not found` sau eroare Mininet | Verifică instalarea Mininet: `which mn`. Dacă VM-ul nu are Mininet, revino la varianta locală (fără topologie). | 2–3 min |
| 7 | tcpdump nu capturează nimic | `pcap` gol | Asigură-te că tcpdump rulează *înainte* de client. Verifică interfața: `h1-eth0`, nu `eth0`. | 30 sec |

**Dacă timpul se comprimă:** sacrifică blocul F.1 (captura gRPC) — epifania despre traficul binar se poate transmite verbal. Păstrează neapărat E.3 (experimentul server oprit) — fixează conceptul central.

---

## Referințe

Birrell, A. D., & Nelson, B. J. (1984). Implementing remote procedure calls. *ACM Transactions on Computer Systems, 2*(1), 39–59. https://doi.org/10.1145/2080.357392

Fielding, R. T., & Taylor, R. N. (2002). Principled design of the modern Web architecture. *ACM Transactions on Internet Technology, 2*(2), 115–150. https://doi.org/10.1145/514183.514185

Currier, C. (2022). Protocol Buffers. In C. Hummert & D. Pawlaszczyk (Eds.), *Mobile Forensics – The File Format Handbook* (pp. 223–260). Springer. https://doi.org/10.1007/978-3-030-98467-0_9

Chamas, C. L., Cordeiro, D., & Eler, M. M. (2017). Comparing REST, SOAP, Socket and gRPC in computation offloading of mobile applications: An energy cost analysis. In *2017 IEEE 9th Latin-American Conference on Communications (LATINCOM)* (pp. 1–6). IEEE. https://doi.org/10.1109/LATINCOM.2017.8240185

JSON-RPC Working Group. (2013). *JSON-RPC 2.0 Specification*. https://www.jsonrpc.org/specification

---

## Note pedagogice

### Concepții greșite vizate

1. **„RPC e ca un apel local."** → Experimentul E.3 (server oprit) demonstrează vizibil diferența: `UNAVAILABLE` nu există în apelurile locale.
2. **„Tot traficul de rețea e lizibil."** → Contrastul JSON (C.4) vs. gRPC binar (F.1) arată că lizibilitatea e o alegere de design, nu o proprietate universală.
3. **„Server și client pot evolua independent."** → Micro-epifania din D.1 (numerele câmpurilor) + reflecția din stage4 pregătesc ideea de compatibilitate a contractului.

### Tipare socratice folosite

| Tipar | Unde | Ce vizează |
|---|---|---|
| POE (Predicție-Observație-Explicație) | C.3: „Ce formă are răspunsul?" | Structura mesajului JSON-RPC |
| „Ce s-ar fi întâmplat dacă…?" | E.3: server oprit → eroare client | Diferența apel local vs. remote |
| Capcană de concepție greșită | A: „Cine crede că *doar* latența e problema?" | RPC ≠ apel local |

### Conexiuni cross-seminar

- **S08/S10** (HTTP/REST) → baza de comparație pentru RPC
- **S11** (Docker Compose) → studenții sunt familiari cu containere și rețele Docker
- **S13** (securitate) → porturile deschise azi devin suprafața de atac de mâine

---

*Outline instructor — S12 (MININET-SDN) | Rețele de Calculatoare — COMPNET*
*Kit: `compnet-2025-redo` | Februarie 2026*

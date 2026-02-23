# Seminar S12 — RPC în practică: de la JSON lizibil la contract binar
| | |
|---|---|
| **Curs** | Rețele de Calculatoare — COMPNET |
| **Kit / repo** | `compnet-2025-redo` · `04_SEMINARS/S12/` |
| **Infra** | Windows 10/11 + Docker Desktop + Wireshark (fără MININET-SDN) |
| **Durată țintă** | 35–40 min |
| **Ideea-cheie** | RPC transformă un apel de funcție într-un schimb de mesaje pe rețea; contractul `.proto` mută efortul de la „parsăm manual" la „generăm cod". |

---

## Obiective operaționale

La finalul seminarului, studentul poate:

1. Formula cel puțin trei diferențe concrete între modelul RPC (Remote Procedure Call) și REST, în termeni de model mental și implicații de rețea.
2. Identifica câmpurile unui mesaj JSON-RPC 2.0 (`jsonrpc`, `method`, `params`, `id`) și interpreta răspunsul (`result` / `error`).
3. Completa un fișier `.proto` minimal (mesaje + serviciu) și genera codul Python cu `grpc_tools.protoc`.
4. Rula un server gRPC și un client gRPC în containere Docker separate, folosind un target de tip `nume_container:port`.
5. Compara în Wireshark: payload JSON (lizibil în *Follow TCP Stream*) vs. gRPC/HTTP2 (cadre + payload binar).
6. Diagnostica eroarea produsă când clientul gRPC apelează un server oprit — diferențiind comportamentul de un apel local.

---

## Structura seminarului

| Bloc | Minute | Titlu | Rezultat vizibil |
|---|---:|---|---|
| A | 0–3 | Hook: „Funcție locală sau la distanță?" | Studenții formulează predicții |
| B | 3–8 | Mini-teorie: RPC vs REST + setup Docker | Trei contraste fixate + rețea Docker creată |
| C | 8–18 | Demo 1: JSON-RPC (2 containere) + pcap | *Follow TCP Stream* arată JSON |
| D | 18–25 | Protobuf: completăm `.proto` + codegen | Fișierele `*_pb2*.py` generate |
| E | 25–35 | Demo 2: gRPC (2 containere) + experiment eșec | Rezultate Add/Multiply/Power + eroare fără server |
| F | 35–40 | Captură gRPC + recap cu reluare hook | Wireshark: HTTP/2 binar vs. JSON lizibil |

---

## Pregătire înainte de seminar (instructor, 5–10 min)

### Pre-pull imagini (evită așteptări în clasă)

```powershell
docker pull python:3.12-slim
docker pull nicolaka/netshoot
```

### Pre-creare server JSON-RPC

Serverul JSON-RPC minimal nu există în kit — trebuie creat o singură dată. Cel mai simplu: creează-l direct pe host (fișierul e montat în container prin `-v`).

Într-un PowerShell, în directorul kitului:

```powershell
cd .\04_SEMINARS\S12\1_jsonrpc
```

Creează fișierul `jsonrpc_server_minimal.py` cu editorul preferat (VS Code, Notepad++, etc.) — conținutul complet:

```python
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
```

### Pre-editare URL-uri (opțional)

1. În `1_jsonrpc/S12_Part01_Script_JSONRPC_Client.py`, schimbă `URL = "https://api.mathjs.org/v4/"` în `URL = "http://s12-server:8080/"`.
2. În `3_grpc/S12_Part03_Script_g_RPC_Client.py`, schimbă `GRPC_TARGET = "localhost:50051"` în `GRPC_TARGET = "s12-server:50051"`.

Dacă preferi să editezi în fața studenților (ca moment pedagogic), fă-o de pe host — fișierele sunt montate cu `-v`.

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

---

## Bloc B (3–8 min) — Mini-teorie: RPC vs REST + setup Docker

### B.1 Trei contraste (3 min)

> *▸ „De la S08 și S10 știm cum funcționează HTTP și REST. Acum le punem pe masă lângă RPC și vedem diferențele."*

1. **Model mental:** REST = resurse (URI-uri + verbe HTTP); RPC = metode/proceduri.
2. **Contract:** REST adesea fără contract formal; gRPC = contract `.proto` strict → cod generat.
3. **Observabilitate:** REST + JSON = lizibil direct în Wireshark; gRPC = eficient, dar binar.

> *▸ „RPC îți dă iluzia de local. Asta e sursa clasică de bug-uri."*

### B.2 Setup Docker (2 min)

**Fă (într-o fereastră PowerShell):**

```powershell
cd cale\catre\compnet-2025-redo\04_SEMINARS\S12
docker network create compnet-s12 2>$null
```

> *▸ „Rețeaua Docker `compnet-s12` e echivalentul unui switch virtual: containerele noastre comunică între ele, iar Docker le rezolvă numele automat prin DNS intern."*

Ai nevoie de **două ferestre PowerShell**: una pentru containerul server, una pentru containerul client. Ambele deschise în `04_SEMINARS\S12`.

---

## Bloc C (8–18 min) — Demo 1: JSON-RPC (2 containere) + pcap

### C.1 Pornești containerul server 🔵 (PowerShell #1)

```powershell
docker run --rm -it --name s12-server --network compnet-s12 `
    -v ${PWD}:/work -w /work python:3.12-slim bash
```

În container:

```bash
pip install --no-cache-dir requests 2>/dev/null
cd 1_jsonrpc
python jsonrpc_server_minimal.py
```

Ar trebui să apară:

```text
[JSONRPC-SERVER] listening on http://0.0.0.0:8080
```

> *▸ „Evaluarea expresiei e deliberat restricționată — scopul e să vedem protocolul, nu să facem un calculator de producție."*

### C.2 Pornești containerul client 🟢 (PowerShell #2)

```powershell
docker run --rm -it --name s12-client --network compnet-s12 `
    -v ${PWD}:/work -w /work python:3.12-slim bash
```

În container:

```bash
pip install --no-cache-dir requests 2>/dev/null
cd 1_jsonrpc
```

**Editare URL (dacă n-ai făcut-o dinainte):** pe host, în editorul preferat, în fișierul `1_jsonrpc/S12_Part01_Script_JSONRPC_Client.py`, schimbă:

```python
URL = "https://api.mathjs.org/v4/"
```

în:

```python
URL = "http://s12-server:8080/"
```

Fișierul e montat — modificarea e vizibilă imediat în container.

### C.3 Rulezi clientul 🟢

**Predicție (POE):**

> *▸ „Clientul trimite un JSON cu `method: evaluate` și `params: ["2+3"]`. Ce formă are răspunsul — credeți că serverul returnează un string, un număr, sau altceva?"*

```bash
python S12_Part01_Script_JSONRPC_Client.py
```

**Observație:**
- 🟢 CLIENT: payload JSON vizibil + `evaluate(2+3) = 5`
- 🔵 SERVER: `[JSONRPC-SERVER] evaluate(2+3) -> 5`

**Explicație:**

> *▸ „Rezultatul e un număr — câmpul `result` din răspunsul JSON-RPC. Tot schimbul e text clar. Confortabil pentru debug, dar plătim cu overhead de serializare."*

**Fixare:**

> *▸ „Care câmp din request decide ce funcție se execută pe server? — `method`."*

### C.4 Captură pcap (opțional — recomandat) 🟠

Într-o a treia fereastră PowerShell:

```powershell
docker run --rm --net=container:s12-server `
    --cap-add NET_ADMIN --cap-add NET_RAW `
    -v ${PWD}:/work -w /work nicolaka/netshoot `
    tcpdump -i any -w s12_jsonrpc.pcap tcp port 8080 -c 60
```

Rulează clientul încă o dată (din 🟢) în timp ce tcpdump capturează. Apoi deschide `s12_jsonrpc.pcap` în Wireshark (de pe host — fișierul e în directorul montat):

- Display filter: `tcp.port == 8080`
- Right click pe un pachet → **Follow → TCP Stream**

**Epifanie:**

> *▸ „Asta e confortul JSON-ului: îl poți citi direct din trafic. Țineți minte senzația asta — o comparăm imediat cu gRPC."*

---

## Bloc D (18–25 min) — Protobuf: contract + codegen

**Tranziție:**

> *▸ „Am văzut JSON-RPC: simplu, lizibil, fără contract formal. Acum definim un contract explicit — iar codul se generează automat."*

### D.1 Completezi `.proto` (2–3 min)

Pe host, în editorul preferat, deschide `2_protobuf/S12_Part02_Config_Calculator.proto` și completează în locurile TODO:

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

> *▸ „Numerele câmpurilor — `= 1`, `= 2` — nu sunt decor. Intră în formatul binar; de aici vine compatibilitatea în timp. Poți adăuga câmpuri noi fără a sparge clienții existenți."*

### D.2 Generezi pb2-urile în `3_grpc/` (3–4 min)

În containerul 🟢 (`s12-client`):

```bash
pip install --no-cache-dir grpcio grpcio-tools 2>/dev/null
cd /work/3_grpc
python -m grpc_tools.protoc -I../2_protobuf \
    --python_out=. --grpc_python_out=. \
    ../2_protobuf/S12_Part02_Config_Calculator.proto
ls -1 S12_Part02_Config_Calculator_pb2*.py
```

Trebuie să vezi:

- `S12_Part02_Config_Calculator_pb2.py`
- `S12_Part02_Config_Calculator_pb2_grpc.py`

**Gotcha:**

> *▸ „Scripturile importă pb2-urile din același folder. Dacă generați în altă parte, mutați fișierele în `3_grpc/`."*

**Referință:** detalii în `2_protobuf/S12_Part02A_Explanation_Protobuf.md`.

---

## Bloc E (25–35 min) — Demo 2: gRPC (2 containere) + experiment eșec

### E.1 Pornești serverul gRPC 🔵

Revii în fereastra containerului `s12-server` (🔵). Oprești serverul JSON-RPC cu `Ctrl+C`, apoi:

```bash
pip install --no-cache-dir grpcio grpcio-tools 2>/dev/null
cd /work/3_grpc
python S12_Part03_Script_g_RPC_Server.py
```

Ar trebui să apară:

```text
[SERVER] gRPC Calculator server started on port 50051
```

### E.2 Configurezi clientul

Pe host, editează `3_grpc/S12_Part03_Script_g_RPC_Client.py` — schimbă:

```python
GRPC_TARGET = "localhost:50051"
```

în:

```python
GRPC_TARGET = "s12-server:50051"
```

### E.3 Rulezi clientul gRPC 🟢

În containerul `s12-client`:

```bash
cd /work/3_grpc
python S12_Part03_Script_g_RPC_Client.py
```

Dictează valori predictibile:

- Add: `7` și `5` → 12
- Multiply: `4` și `6` → 24
- Power: `2` și `10` → 1024

> *▸ „Programatic, `stub.Add(request)` pare apel local. Operațional, e o conexiune TCP + HTTP/2 + mesaje binare serializate cu protobuf."*

### E.4 Experiment: server oprit 🔵→❌ (30 sec)

**Tipar socratic: „Ce s-ar fi întâmplat dacă…?"**

> *▸ „Oprim serverul și rulăm clientul din nou."*

Oprește serverul în 🔵 cu `Ctrl+C`, apoi rulează clientul în 🟢:

```bash
python S12_Part03_Script_g_RPC_Client.py
```

**Predicție:**

> *▸ „Ce tip de eroare primiți?"*

**Observație:** `grpc._channel._InactiveRpcError: ... UNAVAILABLE`

**Explicație:**

> *▸ „La un apel local, UNAVAILABLE nu există. Asta e diferența fundamentală — apelul arată local, dar comportamentul e de rețea. Exact ce am discutat la început."*

---

## Bloc F (35–40 min) — Captură gRPC + recap

### F.1 Captură pcap gRPC în Wireshark 🟠 (dacă ai timp — 2 min)

Repornește serverul (🔵): `python S12_Part03_Script_g_RPC_Server.py`

Într-a treia fereastră PowerShell:

```powershell
docker run --rm --net=container:s12-server `
    --cap-add NET_ADMIN --cap-add NET_RAW `
    -v ${PWD}:/work -w /work nicolaka/netshoot `
    tcpdump -i any -w s12_grpc.pcap tcp port 50051 -c 120
```

Rulează clientul din 🟢, apoi deschide `s12_grpc.pcap` în Wireshark:

- Display filter: `tcp.port == 50051` (și, dacă apare disecat, `http2`)
- **Follow → TCP Stream** — prefață HTTP/2 + payload predominant binar

**Epifanie:**

> *▸ „Cu gRPC, nu mai debug-uim citind JSON din pcap. Debug-uim cu tooling: logging, interceptors, `grpcurl`, tracing. Contractul `.proto` e ancora."*

### F.2 Recap cu reluare hook (2 min)

> *▸ „Trei lucruri de reținut:"*

1. **RPC = apel de funcție peste rețea.** Arată local, dar riscurile sunt ale rețelei — ați văzut eroarea UNAVAILABLE.
2. **Contract `.proto` → cod generat.** Nu mai construim payload-uri manual; definim interfața, generăm stub-uri.
3. **Observabilitate:** JSON e lizibil direct; gRPC necesită tooling — dar câștigă eficiență și tipizare.

> *▸ „La S13 trecem la securitate: scanare de porturi și testare de vulnerabilități. Porturile deschise azi devin suprafața de atac de mâine."*

### F.3 Teme — ce livrează studenții

| Task (.md din kit) | Livrabil | Ce se cere |
|---|---|---|
| `S12_Part01B_Tasks_RPC.md` | `stage1_rpc_intro_answers.txt` | 3 diferențe RPC/REST, avantaje/dezavantaje, rolul protobuf |
| `S12_Part01D_Tasks_JSONRPC.md` | `stage2_jsonrpc_output.txt` | Expresie + request JSON + response |
| `S12_Part02B_Tasks_Protobuf.md` | `stage3_protobuf_output.txt` | `.proto` completat + listing pb2-uri |
| `S12_Part03B_Tasks_g_RPC_Server.md` | `stage4_grpc_server_log.txt` | Log server (Add/Multiply/Power) + reflecție `.proto` |
| `S12_Part03D_Tasks_g_RPC_Client.md` | `stage5_grpc_client_results.txt` | Log client + comparație gRPC vs REST (3–5 propoziții) |

**Materiale de referință:** fișierele `.md` explicative din fiecare subfolder + paginile HTML interactive din `_HTMLsupport/S12/`.

> *▸ „Dacă terminați S12 complet, ați trecut pragul de la «știu HTTP» la «știu un mecanism modern de comunicare inter-servicii cu contract, stub-uri și testare minimală»."*

---

## Cheat-sheet

### Comenzi cheie

| Ce | Comandă (PowerShell) |
|---|---|
| Creare rețea Docker | `docker network create compnet-s12` |
| Container server 🔵 | `docker run --rm -it --name s12-server --network compnet-s12 -v ${PWD}:/work -w /work python:3.12-slim bash` |
| Container client 🟢 | `docker run --rm -it --name s12-client --network compnet-s12 -v ${PWD}:/work -w /work python:3.12-slim bash` |
| Install dependențe (în container) | `pip install --no-cache-dir requests grpcio grpcio-tools` |
| Server JSON-RPC | `python jsonrpc_server_minimal.py` (din `1_jsonrpc/`) |
| Client JSON-RPC | `python S12_Part01_Script_JSONRPC_Client.py` (din `1_jsonrpc/`) |
| Codegen protobuf | `python -m grpc_tools.protoc -I../2_protobuf --python_out=. --grpc_python_out=. ../2_protobuf/S12_Part02_Config_Calculator.proto` (din `3_grpc/`) |
| Server gRPC | `python S12_Part03_Script_g_RPC_Server.py` (din `3_grpc/`) |
| Client gRPC | `python S12_Part03_Script_g_RPC_Client.py` (din `3_grpc/`) |
| Captură pcap | `docker run --rm --net=container:s12-server --cap-add NET_ADMIN --cap-add NET_RAW -v ${PWD}:/work -w /work nicolaka/netshoot tcpdump -i any -w <fisier>.pcap tcp port <port> -c <n>` |

### Porturi

| Serviciu | Port |
|---|---|
| JSON-RPC server | 8080 (TCP) |
| gRPC server | 50051 (TCP) |

### URL-uri modificate (Docker DNS)

| Fișier | Valoare originală | Valoare Docker |
|---|---|---|
| `S12_Part01_Script_JSONRPC_Client.py` → `URL` | `https://api.mathjs.org/v4/` | `http://s12-server:8080/` |
| `S12_Part03_Script_g_RPC_Client.py` → `GRPC_TARGET` | `localhost:50051` | `s12-server:50051` |

### Fișiere generate de codegen

| Fișier | Conținut |
|---|---|
| `S12_Part02_Config_Calculator_pb2.py` | Clasele de mesaje |
| `S12_Part02_Config_Calculator_pb2_grpc.py` | Stub-uri și Servicer |

---

## Plan de contingență

| # | Problemă | Simptom | Soluție | Timp pierdut |
|---|---|---|---|---|
| 1 | `pip install` lent în container | Așteptare >60 sec | Pre-pull `python:3.12-slim`; ideal, construiește o imagine locală cu dependențele pre-instalate (`docker build`). | 30–90 sec |
| 2 | pb2-urile nu se găsesc | `ModuleNotFoundError: S12_Part02_Config_Calculator_pb2` | `ls 3_grpc/S12_Part02_Config_Calculator_pb2*.py`. Dacă lipsesc, rulează codegen din `3_grpc/`. | 30 sec |
| 3 | `GRPC_TARGET` greșit | `UNAVAILABLE` deși serverul rulează | Verifică: trebuie `s12-server:50051`, nu `localhost:50051`. | 15 sec |
| 4 | Containerul nu vede rețeaua | `Temporary failure in name resolution` | Verifică: `--network compnet-s12` la `docker run`. Dacă rețeaua nu există: `docker network create compnet-s12`. | 20 sec |
| 5 | tcpdump nu rulează | `nicolaka/netshoot` lipsă sau eroare capabilities | `docker pull nicolaka/netshoot`. Verifică `--cap-add NET_ADMIN --cap-add NET_RAW`. | 30 sec |
| 6 | Wireshark nu deschide pcap | Fișier gol | Asigură-te că tcpdump rulează *înainte* de client. Verifică: `tcpdump -c 60` (limita de pachete). | 15 sec |
| 7 | Port 8080/50051 ocupat pe host | N/A — porturile sunt în containere, nu pe host. Dacă totuși: eroare `Address already in use` în container. | `docker rm -f s12-server` și repornește. | 15 sec |

**Dacă timpul se comprimă:** sacrifică blocul F.1 (captura gRPC) — transmite epifania verbal. Păstrează E.4 (experimentul server oprit). Dacă și E.4 nu încape, menționează-l verbal și indică tema ca exercițiu individual.

---

## Referințe

Birrell, A. D., & Nelson, B. J. (1984). Implementing remote procedure calls. *ACM Transactions on Computer Systems, 2*(1), 39–59. https://doi.org/10.1145/2080.357392

Fielding, R. T., & Taylor, R. N. (2002). Principled design of the modern Web architecture. *ACM Transactions on Internet Technology, 2*(2), 115–150. https://doi.org/10.1145/514183.514185

Currier, C. (2022). Protocol Buffers. In C. Hummert & D. Pawlaszczyk (Eds.), *Mobile Forensics – The File Format Handbook* (pp. 223–260). Springer. https://doi.org/10.1007/978-3-030-98467-0_9

Ain, M. Z., Ardiansyah, R., Pratama, S. A., Akbar, M., & Lapatta, N. T. (2025). Comparative performance analysis of gRPC and REST API under various traffic conditions and data sizes using a quantitative approach. *Journal of Applied Informatics and Computing, 9*(2), 450–457. https://doi.org/10.30871/jaic.v9i2.9276

JSON-RPC Working Group. (2013). *JSON-RPC 2.0 Specification*. https://www.jsonrpc.org/specification

---

## Note pedagogice

### Concepții greșite vizate

1. **„RPC e ca un apel local."** → Experimentul E.4 (server oprit) demonstrează vizibil diferența.
2. **„Tot traficul de rețea e lizibil."** → Contrastul JSON (C.4) vs. gRPC binar (F.1) în Wireshark.
3. **„Server și client pot evolua independent."** → Micro-epifania din D.1 + reflecția din stage4.

### Tipare socratice folosite

| Tipar | Unde | Ce vizează |
|---|---|---|
| POE (Predicție-Observație-Explicație) | C.3: „Ce formă are răspunsul?" | Structura mesajului JSON-RPC |
| „Ce s-ar fi întâmplat dacă…?" | E.4: server oprit → eroare client | Diferența apel local vs. remote |
| Capcană de concepție greșită | A: „Cine crede că *doar* latența e problema?" | RPC ≠ apel local |

### Diferențe față de varianta MININET-SDN

| Aspect | MININET-SDN | Docker pe Windows |
|---|---|---|
| Izolare | Namespace-uri Mininet (h1, h2) | Containere Docker pe rețea `compnet-s12` |
| Adresare | IP fix (`10.0.0.1`) | DNS Docker (`s12-server`) |
| Captură trafic | tcpdump pe h1-eth0 + tshark | tcpdump în `nicolaka/netshoot` + Wireshark pe host |
| Editare fișiere | `nano` în VM | Editor pe host (fișiere montate cu `-v`) |
| Avantaj principal | Izolare realistă la nivel L2/L3 | Captură pcap deschisă direct în Wireshark GUI |

### Conexiuni cross-seminar

- **S08/S10** (HTTP/REST) → baza de comparație
- **S11** (Docker Compose) → studenții sunt familiari cu containere
- **S13** (securitate) → porturile deschise devin suprafața de atac

---

*Outline instructor — S12 (fără MININET-SDN) | Rețele de Calculatoare — COMPNET*
*Kit: `compnet-2025-redo` | Februarie 2026*

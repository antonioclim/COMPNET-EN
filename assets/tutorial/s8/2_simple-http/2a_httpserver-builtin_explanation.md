Perfect — trecem la **Stage 2: Server HTTP de bază cu `http.server` (Python)**.

În această etapă oferim:

1. **Fișier de explicații** – `index_httpserver_builtin_explanation.md`
2. **Cod complet comentat** – `simple_http_builtin.py`
3. **Fișier cu sarcini** – `index_httpserver_builtin_tasks.md`

Totul în română.

---

## **index_httpserver_builtin_explanation.md**

```markdown
### Server HTTP folosind biblioteca standard Python (http.server)

În această etapă pornim un server HTTP funcțional folosind doar biblioteca
standard Python. Scopul este să înțelegem:

- cum arată un server HTTP minimal
- cum se pot servi fișiere statice
- cum se poate suprascrie comportamentul pentru a răspunde la anumite endpoint-uri

Python oferă două clase utile pentru un server rapid:

- `http.server.SimpleHTTPRequestHandler`  
  – servește automat fișiere din directorul curent  

- `http.server.BaseHTTPRequestHandler`  
  – bază pentru definirea unui server HTTP personalizat

Vom porni un server care:
- servește fișiere din directorul curent
- răspunde la `/hello`
- răspunde la `/api/time` cu JSON

Ulterior, serverul va fi testat cu `curl`.

---

### Cum se pornește serverul

Rulați:

```

python3 simple_http_builtin.py 8000

```

Apoi testați:

```

curl -v [http://localhost:8000/](http://localhost:8000/)
curl -v [http://localhost:8000/hello](http://localhost:8000/hello)
curl -v [http://localhost:8000/api/time](http://localhost:8000/api/time)

```

---

### Ce limitări are acest server?

- nu gestionează conexiuni concurente eficiente
- nu folosește MIME-type-uri avansate (doar cele implicite)
- nu parsează request-uri complexe
- nu este potrivit pentru producție

Este însă excelent ca server de laborator și pentru a înțelege cum funcționează
HTTP înainte de a implementa un server „from scratch” cu socket-uri.

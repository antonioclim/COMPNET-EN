
#### Sarcini Stage 4 – Server gRPC

Creați fișierul:

`stage4_grpc_server_log.txt`

Și parcurgeți pașii:

---

### 1. Completați TODO-urile din `grpc_server.py`

* în metoda `Multiply`
* în metoda `Power`

(Pentru a simplifica, în varianta de mai sus sunt deja completate; în varianta pentru studenți poți lăsa doar comentariile și linii goale.)

---

### 2. Porniți serverul

Într-un terminal:

```bash
python grpc_server.py
```

Ar trebui să vedeți:

```text
[SERVER] gRPC Calculator server started on port 50051
```

Lăsați serverul să ruleze (nu închideți terminalul).

---

### 3. Documentați output-ul

După ce veți avea și clientul (Stage 5), serverul va afișa linii de tip:

```text
[SERVER] Add called with a=2, b=3, result=5
[SERVER] Multiply called with a=4, b=5, result=20
[SERVER] Power called with base=2, exponent=10, result=1024
```

Copiați în `stage4_grpc_server_log.txt` cel puțin 3 linii de log de la server (pentru Add, Multiply, Power) după ce rulați și clientul.

Până atunci, puteți nota:

* mesajul la pornirea serverului
* eventuale erori dacă există

---

### 4. Mică reflecție (2–3 fraze)

La finalul fișierului `stage4_grpc_server_log.txt`, răspundeți:

1. Ce avantaje vedeți în faptul că serverul și clientul folosesc **același .proto**?
2. Ce s-ar întâmpla dacă ați schimba structura mesajelor doar pe server și nu ați regenera codul clientului?


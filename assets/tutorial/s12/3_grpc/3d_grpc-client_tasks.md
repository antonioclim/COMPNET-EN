
#### Sarcini Stage 5 – Client gRPC

Creați fișierul:

`stage5_grpc_client_results.txt`

Și efectuați următorii pași:

---

### 1. Porniți serverul gRPC

Într-un terminal:

```bash
python grpc_server.py
```

Lăsați serverul să ruleze.

---

### 2. Rulați clientul

În alt terminal:

```bash
python grpc_client.py
```

Introduceți la prompt:

* valori pentru `a`, `b` (Add)
* valori pentru `a`, `b` (Multiply)
* valori pentru `base`, `exponent` (Power)

---

### 3. Conținutul fișierului `stage5_grpc_client_results.txt`

Includeți:

1. Copie a conținutului din `grpc_client_log.txt`
   (output-ul salvat de client).

2. 3–4 linii de log de la server (din consola unde rulează `grpc_server.py`):

   * una pentru Add
   * una pentru Multiply
   * una pentru Power

3. Un scurt răspuns (3–5 fraze) la întrebarea:

   „Cum diferă experiența de programare cu gRPC față de a scrie manual un client HTTP (REST) cu `requests`? Ce avantaje aduce contractul `.proto`?”


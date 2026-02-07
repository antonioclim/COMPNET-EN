
### Seminar 12 – Stage 2

## JSON-RPC: un client simplu către un serviciu RPC

În această etapă vom implementa un client JSON-RPC simplu folosind Python.

JSON-RPC este un protocol extrem de simplu, de forma:

```json
{
  "jsonrpc": "2.0",
  "method": "add",
  "params": [1, 2],
  "id": 1
}
```

La care serverul răspunde cu:

```json
{
  "jsonrpc": "2.0",
  "result": 3,
  "id": 1
}
```

---

## 1. Endpoint JSON-RPC folosit

Vom folosi un endpoint de test JSON-RPC (public sau local).
Pentru seminariu, folosim exemplul clasic:

```
https://api.mathjs.org/v4/
```

Acesta acceptă cereri JSON-RPC de forma:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "evaluate",
  "params": ["2+3"]
}
```

---

## 2. Client Python JSON-RPC

Fișier: `jsonrpc_client.py`

Programul:

* construiește JSON-ul RPC
* trimite request prin `requests.post`
* afișează rezultatul
* include TODO-uri pentru studenți

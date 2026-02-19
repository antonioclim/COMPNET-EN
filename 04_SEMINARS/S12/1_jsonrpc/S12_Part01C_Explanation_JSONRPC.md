### Seminar 12 – Part 2

## JSON-RPC: a minimal client to an RPC service

The task here is to implement a simple JSON-RPC client using Python.

JSON-RPC is an intentionally minimal protocol. A typical request looks like:

```json
{
  "jsonrpc": "2.0",
  "method": "add",
  "params": [1, 2],
  "id": 1
}
```

The server responds with:

```json
{
  "jsonrpc": "2.0",
  "result": 3,
  "id": 1
}
```

---

## 1. JSON-RPC endpoint used

The exercises target a JSON-RPC test endpoint (public or local). For this seminar the commonly used example is:

```text
https://api.mathjs.org/v4/
```

It accepts JSON-RPC requests of the form:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "evaluate",
  "params": ["2+3"]
}
```

---

## 2. Python JSON-RPC client

File: `S12_Part01_Script_JSONRPC_Client.py`

The programme:

- builds the JSON-RPC payload
- sends the request via `requests.post`
- prints the result
- includes TODO sections for students

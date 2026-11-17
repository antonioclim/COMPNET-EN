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

The exercises use the supplied local JSON-RPC 2.0 server. From this directory, start it in terminal A:

```bash
python3 S12_Part01_Script_JSONRPC_Server.py
```

Run the client in terminal B:

```bash
python3 S12_Part01_Script_JSONRPC_Client.py
```

The endpoint is:

```text
http://127.0.0.1:8000/
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

### Local contract and error evidence

`evaluate` accepts `["2+3"]` or `{"expr":"2+3"}`; the bounded expression language
contains numbers, parentheses and `+ - * /`. `add` accepts `[2,3]` or `{"a":2,"b":3}`.
Request ids are echoed unchanged. Errors use -32700 (invalid JSON), -32600 (invalid
request), -32601 (unknown method) and -32602 (invalid method parameters).
A notification omits `id` and receives no JSON-RPC response. For this HTTP binding,
responses use HTTP 200 and notifications use HTTP 204 with an empty body. JSON-RPC
itself does not mandate these HTTP statuses. Batches are supported, up to 100 requests.

Capture one successful call, one unknown method and one notification. Check the id
and the exclusive `result`/`error` fields. The public mathjs API is a separate REST
API using `expr`; do not send JSON-RPC envelopes to it.

Specification: <https://www.jsonrpc.org/specification>.

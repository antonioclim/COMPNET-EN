#### Tasks – Part 5 (gRPC client)

Create the file:

`stage5_grpc_client_results.txt`

and complete the following steps.

---

### 1. Start the gRPC server

In a terminal:

```bash
python S12_Part03_Script_g_RPC_Server.py
```

Keep the server running.

---

### 2. Run the client

In another terminal:

```bash
python S12_Part03_Script_g_RPC_Client.py
```

At the prompts, enter:

- values for `a`, `b` (Add)
- values for `a`, `b` (Multiply)
- values for `base`, `exponent` (Power)

---

### 3. Content of `stage5_grpc_client_results.txt`

Include:

1. a copy of the content of `grpc_client_log.txt` (the output saved by the client)

2. 3–4 log lines from the server (from the terminal where `S12_Part03_Script_g_RPC_Server.py` runs):

   - at least one for Add
   - at least one for Multiply
   - at least one for Power

3. a short answer (3–5 sentences) to:

   "How does the programming experience with gRPC differ from manually writing an HTTP (REST) client with `requests`? What advantages does the `.proto` contract provide?"

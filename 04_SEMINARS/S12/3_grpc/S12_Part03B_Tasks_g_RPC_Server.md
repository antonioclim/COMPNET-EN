#### Tasks – Part 4 (gRPC server)

Create the file:

`stage4_grpc_server_log.txt`

and follow the steps below.

---

### 1. Complete the TODOs in `S12_Part03_Script_g_RPC_Server.py`

Complete the TODO sections:

- in the `Multiply` method
- in the `Power` method

(For simplicity, the version provided to you may already be complete. In the student version, these sections can be left as comments with empty lines.)

---

### 2. Start the server

In a terminal:

```bash
python S12_Part03_Script_g_RPC_Server.py
```

You should see:

```text
[SERVER] gRPC Calculator server started on port 50051
```

Keep the server running (do not close the terminal).

---

### 3. Document the server output

After you also have the client (Part 5), the server will print lines such as:

```text
[SERVER] Add called with a=2, b=3, result=5
[SERVER] Multiply called with a=4, b=5, result=20
[SERVER] Power called with base=2, exponent=10, result=1024
```

Copy into `stage4_grpc_server_log.txt` at least three server log lines (Add, Multiply and Power) after you run the client.

Until then, you can record:

- the server start-up message
- any errors, if they appear

---

### 4. Short reflection (2–3 sentences)

At the end of `stage4_grpc_server_log.txt`, answer:

1. What advantages do you see in the fact that both server and client use the **same .proto** file?
2. What would happen if you changed the message structure only on the server and did not regenerate the client code?

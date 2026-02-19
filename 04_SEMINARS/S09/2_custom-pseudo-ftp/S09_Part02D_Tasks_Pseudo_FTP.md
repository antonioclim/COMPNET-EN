### Stage 3 — Tasks for Pseudo-FTP (Active/Passive)

Objective: to understand in practice how an FTP-style protocol works with:
- a control connection
- data connections in active and passive mode

The result of this stage will be a log file:

```

pseudoftp_log.txt

````

and the server/client code, possibly slightly modified by you.

---

## 1. Preparing the directories

Make sure you have two directories:

```bash
mkdir -p temp
mkdir -p client-temp
````

In `temp` place at least 2 text files (e.g. `server1.txt`, `server2.txt`).

In `client-temp` place at least 1 file (e.g. `client1.txt`).

---

## 2. Start the server

In a terminal:

```bash
python3 S09_Part02B_Script_Pseudo_FTP_Server.py
```

You should see:

```
[SERVER] Pseudo-FTP server listening on 127.0.0.1:3333
```

---

## 3. Start the client

In another terminal:

```bash
python3 S09_Part02C_Script_Pseudo_FTP_Client.py
```

You should see:

```text
[CLIENT] Connected to pseudo-FTP server at 127.0.0.1:3333
Commands: list, help, active_get/put, passive_get/put, Ctrl+C to exit
-> 
```

---

## 4. Test control commands (list, help)

1. In the client, run:

```text
-> help
-> list
```

2. Copy the output (both from `help` and from `list`) into the file:

```
pseudoftp_log.txt
```

---

## 5. Active mode test (active_get / active_put)

### active_get

1. From the client:

```text
-> active_get server1.txt
```

2. Verify that the file `server1.txt` appears in the `client-temp` directory.

### active_put

1. From the client:

```text
-> active_put client1.txt
```

2. Verify that the file `client1.txt` appears in the `temp` directory.

Note in `pseudoftp_log.txt` which commands you issued and whether the transfers succeeded.

---

## 6. Passive mode test (passive_get / passive_put)

### passive_get

1. From the client:

```text
-> passive_get server2.txt
```

2. Verify that the file `server2.txt` appears in `client-temp`.

### passive_put

1. From the client:

```text
-> passive_put client1.txt
```

2. Verify that the file appears in `temp` (it may overwrite or create a copy).

Add the relevant output from the client to `pseudoftp_log.txt` ([CLIENT] messages and any [SERVER] messages you see).

---

## 7. Small extension (mandatory, but very simple)

In `S09_Part02B_Script_Pseudo_FTP_Server.py`, the function:

```python
def process_help(client, command_items):
    ...
```

contains a simple help text.

TASK:

* modify the text so that it includes a short description (1 sentence) for each command.
* for example:

```text
active_get <filename>  - downloads a file from the server using active mode
```

Run again:

```text
-> help
```

and copy the new output into `pseudoftp_log.txt` (under a separate heading such as `--- MODIFIED HELP ---`).

---

## 8. Reflection questions (write at the end of pseudoftp_log.txt)

Answer in 1–3 sentences each:

1. What is the practical difference between `active_get` and `passive_get` in this protocol?
2. What happens if you run the server and client on different machines in a network with firewall/NAT?

   * which mode is more likely to work (active/passive) and why?
3. In what way does this protocol resemble real FTP?
4. What obvious limitations does it have (file size, security, robustness)?

---

### Stage 3 Deliverables

Submit:

* `S09_Part02B_Script_Pseudo_FTP_Server.py` (may contain only the help modification)
* `S09_Part02C_Script_Pseudo_FTP_Client.py` (unmodified or with minor display improvements)
* `pseudoftp_log.txt` with:

  * output from `help` (initial and modified)
  * output from `list`
  * at least one `active_get` and one `active_put` transfer
  * at least one `passive_get` and one `passive_put` transfer
  * answers to the reflection questions

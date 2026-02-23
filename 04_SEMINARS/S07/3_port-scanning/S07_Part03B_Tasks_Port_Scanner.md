### Tasks — Mini TCP Port Scanner (Stage 4)

In this stage you will implement and test a simple port scanner
based on TCP connections (connect scan).

---

### 1. Complete the scan_port and scan_range functions

In `port_scanner.py`:

1. In `scan_port`:
   - use `socket.socket(AF_INET, SOCK_STREAM)`
   - set a short timeout (e.g. 0.5s)
   - attempt `connect((host, port))`
   - handle exceptions:
     - `ConnectionRefusedError` -> `"CLOSED"`
     - `socket.timeout` -> `"FILTERED"`
     - any other `Exception` -> you may treat it as `"CLOSED"` or `"FILTERED"`, but document your decision in a comment

2. In `scan_range`:
   - iterate from `start_port` to `end_port` (inclusive)
   - for each port:
     - call `scan_port(host, port)`
     - print the line `PORT <port> <STATE>` on screen
     - store the same line in the `results` list

At the end, `scan_range` returns the `results` list.

---

### 2. Run a basic local test

On the local machine or in a Mininet host, run:

```bash
python3 port_scanner.py 127.0.0.1 1 1024
```

Observations:

- you should see a few `OPEN` ports (e.g. 22, 80, 443, depending on what services are running)
- most ports will be `CLOSED` or `FILTERED`
- the results will be saved to `S07_Part03_Output_Scan_Results.txt`

If the scan takes too long, try a smaller range (e.g. 1–200).

---

### 3. Test in the laboratory environment (Mininet)

If you are using Mininet with topologies from previous seminars, you can test the scanner between hosts:

1. In the Mininet CLI, on h2, start a TCP server (for example `S06_Part03_Script_TCP_Server.py`):

```bash
h2 python3 S06_Part03_Script_TCP_Server.py 5000
```

2. On h1, run the scanner:

```bash
h1 python3 port_scanner.py 10.0.10.2 4900 5100
```

3. Verify that port 5000 appears as `OPEN` and that surrounding ports are `CLOSED` or `FILTERED`.

---

### 4. Analyse the results

Open the file `S07_Part03_Output_Scan_Results.txt`. Observe:

- how many ports are `OPEN`?
- do they match the services you know are running?
- do you see `FILTERED` ports? Why might they appear as filtered (hint: firewall, missing SYN response and so on)?

---

### 5. Optional extension (for faster students)

If you have time, try:

- adding an optional `--fast` argument that scans only a set of common ports (e.g. 22, 80, 443, 8080, 3306 and so on)
- displaying a brief summary at the end:
  - `N` ports OPEN
  - `M` ports CLOSED
  - `K` ports FILTERED

You can achieve this by counting the states in `scan_range`.

---

### 6. Reflection questions (to be written in S07_Part03_Output_Scan_Results.txt or in a separate file scan_log.txt)

Answer briefly:

1. What is the difference between a TCP connect scan and a SYN scan (at a conceptual level, without implementing one)?
2. Why is a UDP scan generally harder to interpret than a TCP scan?
3. Why can a firewall make ports appear as `FILTERED` instead of `CLOSED`?

---

### Deliverable Stage 4

Submit:

- `port_scanner.py` complete (with `scan_port` and `scan_range` implemented)
- `S07_Part03_Output_Scan_Results.txt` or `scan_log.txt` containing:
  - the scan output (at least 50 ports scanned)
  - the answers to the reflection questions

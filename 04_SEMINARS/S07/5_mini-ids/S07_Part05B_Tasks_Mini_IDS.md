### Stage 6 — mini IDS (integrated assignment for Seminar 7)

In this stage you will finalise a mini IDS (Intrusion Detection System)
built on the ideas from the preceding stages:

- RAW sniffer
- TCP/UDP filtering
- port scan detection
- UDP spray detection
- flood detection towards a port

The final deliverables are the script `S07_Part05A_Script_Mini_IDS.py`, the log file `ids_alerts.log`
and a short report.

---

### 1. Complete the log_alert function

In `S07_Part05A_Script_Mini_IDS.py`, the function:

```python
def log_alert(message: str):
    ...
````

must:

1. build a message with a timestamp:

   * suggested format: `[YYYY-MM-DD HH:MM:SS] <message>`
2. display the message on screen (print)
3. write the same message to a file `ids_alerts.log`, one alert per line

The basic steps are already in the code, but verify:

* that the file is opened in append mode (`"a"`)
* that you use `full_msg + "\n"`

---

### 2. TCP port-scan detection

In the function:

```python
def handle_tcp_packet(src_ip, dst_ip, dst_port, flags, now):
    ...
```

the proposed logic already exists, similar to `detect_scan.py`.

Task:

1. Understanding:

   * for each `src_ip`, `ids_state["tcp_scan"][src_ip]` is a dictionary:

     * key: `dst_port`, value: `timestamp`
   * `cleanup_old_entries` removes ports older than `WINDOW_SECONDS` seconds
   * if the number of distinct ports >= `TCP_SYN_THRESHOLD`, `log_alert` is called

2. Adjust (if needed) the logic as you see fit, but preserve the core idea:

   * count only SYN without ACK (`is_syn and not is_ack`)
   * handle only the relevant TCP packets (the rest may be ignored)

3. Test:

   * run `S07_Part05A_Script_Mini_IDS.py` on a host (e.g. h2)
   * run `port_scanner.py` from another host (e.g. h1) with a port range of at least 20–30:

     ```bash
     h1 python3 port_scanner.py 10.0.10.2 1 200
     ```
   * verify that an alert of the form appears:

     ```text
     [....] Possible TCP PORT SCAN from 10.0.10.1: 10 SYN ports ...
     ```

---

### 3. UDP "spray" detection

In the function:

```python
def handle_udp_packet(src_ip, dst_ip, dst_port, now):
    ...
```

you must use `ids_state["udp_spray"]` to detect multi-port UDP
from the same source.

Task:

1. Structure:

   * `ids_state["udp_spray"][src_ip]` is a dictionary:

     * key: `dst_port`, value: `timestamp`

2. Logic:

   * remove old entries with `cleanup_old_entries`
   * record `dst_port` with its timestamp
   * if the number of distinct ports >= `UDP_PORT_THRESHOLD` within `WINDOW_SECONDS` seconds:

     * call `log_alert` with a message of the form:

       ```text
       Possible UDP SPRAY from <src_ip>: <N> UDP ports in the last <WINDOW_SECONDS>s
       ```

3. Test:

   * on the "attacker" (h1), write or adapt a script that sends UDP to multiple ports
     (you may even modify `S06_Part03_Script_UDP_Client.py` or write a small custom script).
   * run `S07_Part05A_Script_Mini_IDS.py` on h2
   * verify that the UDP alert appears after you have sent to enough ports.

---

### 4. Flood detection towards a port

Also in `handle_tcp_packet`, you have logic for `ids_state["flood"]`:

* the key is a tuple `(dst_ip, dst_port)`
* the value is a dictionary `{ timestamp: timestamp }` (or another simple way of counting packets)

Task:

1. Verify and understand the existing logic:

   * old entries (older than `WINDOW_SECONDS` seconds) are removed
   * a new timestamp is added for each packet
   * if the dictionary length >= `FLOOD_THRESHOLD`:

     * `log_alert` is called with the flood message

2. Optionally, adapt or simplify:

   * you may use only the packet count rather than storing all timestamps
   * but the current implementation is simple enough for the laboratory

3. Test:

   * run a script that sends many TCP packets to the same port in a short time
     (you may modify `port_scanner.py` to scan the same port many times
     or write a small script that makes many rapid connect() calls).
   * verify that the flood alert appears.

---

### 5. Integrated run and log collection

Run `S07_Part05A_Script_Mini_IDS.py` on the "victim" machine/host (e.g. h2) for at least 2–3 scenarios:

1. Scenario 1 — TCP port scan (with `port_scanner.py`)
2. Scenario 2 — multi-port UDP (with a UDP script or a modified `S06_Part03_Script_UDP_Client.py`)
3. Scenario 3 — optionally a flood towards a port (dedicated script or adaptation)

After running these tests:

* stop `S07_Part05A_Script_Mini_IDS.py` with Ctrl-C
* open the file `ids_alerts.log`
* verify that the alerts corresponding to the above scenarios are recorded

---

### 6. Short report

Create a file:

```text
explanation.md
```

In which you write 10–15 sentences (or 3–5 short paragraphs) about:

1. What types of attacks / behaviours your mini IDS detects:

   * TCP port scan
   * UDP spray
   * flood towards a port
2. What parameters control sensitivity:

   * WINDOW_SECONDS
   * TCP_SYN_THRESHOLD
   * UDP_PORT_THRESHOLD
   * FLOOD_THRESHOLD
3. Concrete examples of false positives and false negatives:

   * when you could have an alert yet there is no real attack
   * when a real attack could go unnoticed
4. At least 2 improvement ideas:

   * other patterns (e.g. slow scan with many minutes between packets)
   * packet content analysis (signatures)
   * integration with a central log or a real alerting system

---

### 7. Final deliverable for Seminar 7

At the end of the seminar (or as homework), the student must submit a package
containing at least:

* `packet_sniffer.py` (Stage 2, completed)
* `packet_filter.py` (Stage 3, completed)
* `port_scanner.py` (Stage 4, completed)
* `detect_scan.py` (Stage 5)
* `S07_Part05A_Script_Mini_IDS.py` (Stage 6, completed)
* `sniffer_log.txt`
* `filter_results.txt`
* `S07_Part03_Output_Scan_Results.txt` or `scan_log.txt`
* `scan_detection.txt`
* `ids_alerts.log`
* `explanation.md`

This represents the integrated project for Seminar 7:
from sniffer to filter, to port scanner, to scan/flood detection and mini IDS.

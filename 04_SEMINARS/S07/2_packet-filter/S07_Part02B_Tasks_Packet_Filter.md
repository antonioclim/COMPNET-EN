### Tasks — TCP/UDP Packet Filter (Stage 3)

In this stage you will adapt the sniffer so that it displays ONLY packets of interest,
by implementing the `passes_filter` function in `packet_filter.py`.

---

### 1. Copy the parse_ipv4_header implementation

If `packet_filter.py` does not already have a complete version of the function:

```python
def parse_ipv4_header(data: bytes):
    ...
````

then copy the correct implementation you wrote in `packet_sniffer.py`.

Make sure that:

* it returns `(src_ip_str, dst_ip_str, proto, ihl)`
* it uses `struct.unpack('! 8x B B 2x 4s 4s', data[:20])`

---

### 2. Implement the filter — Step 1 (TCP only)

In `passes_filter`, start by implementing a simple rule:

* display ONLY TCP packets (proto == 6)
* ignore all other packets

Pseudo-code:

```python
if proto == 6:
    return True
else:
    return False
```

Run:

```bash
sudo python3 packet_filter.py <INTERFACE>
```

Generate traffic (e.g. `curl`, `ssh`, `nc` and so on) and verify that you see only lines with `proto=TCP`.

---

### 3. Implement the filter — Step 2 (UDP port 53)

Extend the filter with the following logic:

1. If the packet is UDP and `dst_port == 53`, display it (DNS).
2. If the packet is TCP, display it only if `dst_port > 1024`.
3. All other packets are ignored.

Suggestion:

```python
# UDP packet destined for port 53
if proto == 17 and dst_port == 53:
    return True

# TCP packet destined for an unprivileged port
if proto == 6 and dst_port is not None and dst_port > 1024:
    return True

return False
```

Run the script again and:

* execute a `dig google.com` or `nslookup` (to generate DNS traffic)
* execute a `curl http://example.com` (TCP traffic to port 80, which may or may not pass the filter depending on the rule)
* observe which packets pass the filter

---

### 4. Implement the filter — Step 3 (source IP filter)

Add an additional criterion:

* display ONLY packets (that already satisfy the rules above) whose source address belongs to a specific network
* for example, only source addresses from `10.x.x.x` (the source string starts with `"10."`)

Pseudo-code:

```python
if not src_ip.startswith("10."):
    return False
```

Your final filter may look like a combination:

```python
# only sources from 10.0.0.0/8
if not src_ip.startswith("10."):
    return False

# UDP destined for 53
if proto == 17 and dst_port == 53:
    return True

# TCP destined for port > 1024
if proto == 6 and dst_port is not None and dst_port > 1024:
    return True

return False
```

Adapt to your environment (you may use `192.168.` or other relevant prefixes).

---

### 5. Run and collect results

Run:

```bash
sudo python3 packet_filter.py <INTERFACE>
```

While the filter is running:

* generate DNS traffic (dig / nslookup)
* generate HTTP traffic (curl)
* generate SSH or other TCP traffic (if relevant)
* verify that the filter genuinely discards unwanted packets

Copy the relevant output (at least 20 lines) to a file:

```text
filter_results.txt
```

---

### 6. Reflection questions (to be written in filter_results.txt)

Below the log, answer:

1. Which type of traffic were you able to filter most easily (TCP/UDP)?
2. Why can filtering by destination port be misleading in practice (hint: port reuse, tunnelling, non-standard services)?
3. What would you change in your filter if you were interested only in detecting DNS traffic to a single server (for example 8.8.8.8)?

---

### Deliverable Stage 3

Submit:

* `packet_filter.py` complete (with `passes_filter` implemented)
* `filter_results.txt` containing:

  * at least 20 lines of filter output
  * the answers to the reflection questions

### Tasks — Simple IPv4 Packet Sniffer (Stage 2)

In this stage you will:

- complete the `parse_ipv4_header` function in `packet_sniffer.py`
- run the sniffer on an interface
- generate some traffic (ping, curl and so on)
- collect a log with the first 20 IPv4 packets

---

### 1. Complete parse_ipv4_header

In the file `packet_sniffer.py` you will find the function:

```python
def parse_ipv4_header(data: bytes):
    ...
    # >>> STUDENT TODO
    ...
    raise NotImplementedError("Complete the parse_ipv4_header function")
````

Task:

1. Implement the following steps in place of the TODO:

   * extract `version_ihl = data[0]`
   * calculate:

     * `version = version_ihl >> 4`
     * `ihl = (version_ihl & 0x0F) * 4`
   * use `struct.unpack` to obtain:

     * `ttl`, `proto`, `src`, `dst`
   * convert `src` and `dst` to strings with `ipv4_addr`
   * return `(src_ip_str, dst_ip_str, proto, ihl)`

2. After implementing, delete or comment out the line:

```python
raise NotImplementedError("Complete the parse_ipv4_header function")
```

Suggested `struct.unpack`:

```python
ttl, proto, src, dst = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
```

---

### 2. Start the sniffer

Run:

```bash
sudo python3 packet_sniffer.py <INTERFACE>
```

Examples:

* on the local machine: `eth0`, `wlan0`, `lo`
* in Mininet (on a host): `h1-eth0`

Example in Mininet (after entering the Mininet CLI):

```bash
h1 sudo python3 packet_sniffer.py h1-eth0
```

---

### 3. Generate traffic

While the sniffer is running:

* in a separate terminal, execute a `ping` to some address:

  * `ping 8.8.8.8` (on the local machine)
  * or `h1 ping 10.0.1.1` in Mininet
* or run `curl http://example.com`
* or any other command that generates IPv4 traffic

Observe lines of the form:

```text
[1] 192.168.0.10 -> 8.8.8.8  proto=ICMP
[2] 8.8.8.8 -> 192.168.0.10  proto=ICMP
[3] ...
```

---

### 4. Stop the sniffer and save the log

Stop the sniffer with `Ctrl-C` after at least 20 packets have been displayed (or after `MAX_PACKETS` is reached).

Copy the relevant output to a file:

```text
sniffer_log.txt
```

This file must contain:

* at least 20 lines of the form:

  * `[N] SRC_IP -> DST_IP  proto=...`
* a few ICMP packets (from ping)
* if possible, a few TCP or UDP packets (from curl or other commands)

---

### 5. Reflection questions (to be written in sniffer_log.txt)

Below the log, answer briefly (1–2 sentences each):

1. Which protocol did you observe most frequently in the capture (ICMP, TCP, UDP)?
2. Which IP addresses appear most often as destination? Why?
3. What happens to the sniffer if you are not root (without sudo)?

---

### Deliverable Stage 2

* the completed `packet_sniffer.py` file (with `parse_ipv4_header` implemented)
* the `sniffer_log.txt` file containing:

  * the packet log
  * the answers to the reflection questions

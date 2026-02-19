### Tasks: SDN Topology with Os-Ken and an OpenFlow Switch

---

### 1. Starting the Os-Ken Controller

In a separate terminal (NOT inside Mininet), run:

```bash
osken-manager index_sdn_os-keb_controller.py
````

You should see Os-Ken log messages and, eventually, a notification when the switch connects.

---

### 2. Starting the Mininet SDN Topology

In another terminal:

```bash
sudo python3 index_sdn_topo_switch.py
```

After startup you will enter the Mininet CLI (`mininet>`).

Verify the hosts:

```bash
h1 ip a
h2 ip a
h3 ip a
```

---

### 3. Testing Connectivity with Ping

#### a) h1 to h2 (should succeed)

```bash
h1 ping -c 3 10.0.10.2
```

You should see replies and new flows appearing in s1.

#### b) h1 to h3 (should be blocked)

```bash
h1 ping -c 3 10.0.10.3
```

You should see a timeout (no reply). The controller installs a drop flow.

---

### 4. Inspecting the Flow Table

In the Mininet CLI:

```bash
s1 ovs-ofctl dump-flows s1
```

Analyse:

* Is the table-miss flow (priority 0) present?
* Are there flows for traffic between 10.0.10.1 ↔ 10.0.10.2?
* Are there drop flows for destination 10.0.10.3?

---

### 5. *Optional*: Traffic Capture

Start a capture on s1:

```bash
s1 tcpdump -i s1-eth1 -n
```

In parallel:

```bash
h1 ping -c 3 10.0.10.2
```

Observe the ICMP packets. Stop tcpdump with Ctrl-C.

---

### Partial Deliverable

Create the file:

```
sdn_stage2_output.txt
```

It must contain:

* output from:

  * `h1 ping 10.0.10.2`
  * `h1 ping 10.0.10.3`
* an `ovs-ofctl dump-flows s1` dump (complete or partial)
* 5–7 sentences explaining:

  * how the flow table shows that h1 ↔ h2 traffic is permitted
  * how the flow table shows that traffic towards h3 is blocked
  * the role of the table-miss rule

This file will be completed in Stage 3 with Python server/client tests.

### Tasks: TCP and UDP Traffic through the SDN Switch

These tasks build upon Stage 2 (Os-Ken controller + SDN topology).

Assumptions:
- the Os-Ken controller is running with `index_sdn_os-ken_controller.py`
- the Mininet SDN topology is running with `index_sdn_topo_switch.py`

---

### 1. Test TCP — Permitted between h1 and h2

1. In the Mininet CLI, start the TCP server on h2:

```bash
h2 python3 S06_Part03_Script_TCP_Server.py 5000
````

2. In another Mininet terminal (or after opening a new CLI with `xterm h1`, if used), start the TCP client on h1:

```bash
h1 python3 S06_Part03_Script_TCP_Client.py 10.0.10.2 5000
```

3. Send a few messages (e.g. `hello`, `test`) and verify that:

* the server displays them
* the client receives the echo

4. Stop the client with `exit`, then stop the server with Ctrl-C.

---

### 2. Test TCP — Blocked between h1 and h3

1. From h1, attempt to connect to h3 (without running a server there — SDN blocks the traffic regardless):

```bash
h1 python3 S06_Part03_Script_TCP_Client.py 10.0.10.3 5000
```

2. Observe:

* you should see `Connection failed` or a time-out
* in the Os-Ken log, drop messages for traffic towards 10.0.10.3 should appear
* `ovs-ofctl dump-flows s1` should show the previously installed drop flow

Save the client output in the deliverable file.

---

### 3. Test UDP with h3 (Initially Blocked at IP Level)

1. Start the UDP server on h3:

```bash
h3 python3 S06_Part03_Script_UDP_Server.py 6000
```

2. From h1, start the UDP client:

```bash
h1 python3 S06_Part03_Script_UDP_Client.py 10.0.10.3 6000
```

3. Attempt to send a few messages. Depending on the controller implementation:

* if a general drop flow on `dst_ip == 10.0.10.3` exists, nothing may arrive
* if no drop flow has been installed for this case yet, messages may pass through

In the next step the controller will be modified explicitly to handle TCP and UDP separately.

---

### 4. Modifying the Os-Ken Controller: Permit UDP, Block TCP towards h3

In the file `index_sdn_os-ken_controller.py`, within the `packet_in_handler`, modify the logic so that:

* for TCP traffic (ip_proto = 6) towards `10.0.10.3`:

  * install a drop flow (as before)
* for UDP traffic (ip_proto = 17) towards `10.0.10.3`:

  * install a flow that **permits** forwarding to the h3 port

Hints:

* obtain the protocol from `ipv4_pkt.proto`
* `parser.OFPMatch` can be used as follows:

```python
match = parser.OFPMatch(
    eth_type=0x0800,
    ip_proto=17,         # UDP
    ipv4_dst="10.0.10.3"
)
```

* for actions, use the port to which h3 is connected (typically 3):

```python
actions = [parser.OFPActionOutput(3)]
```

* for TCP, use `ip_proto=6` and an empty action list (`actions = []`) for drop.

After modifying the file, restart the controller:

```bash
# stop the old Os-Ken instance
# then:
osken-manager index_sdn_os-ken_controller.py
```

Restart the Mininet network as well if it was stopped.

---

### 5. Re-testing UDP and TCP

1. With the UDP server on h3:

```bash
h3 python3 S06_Part03_Script_UDP_Server.py 6000
```

2. With the UDP client on h1:

```bash
h1 python3 S06_Part03_Script_UDP_Client.py 10.0.10.3 6000
```

3. Send a few messages:

* the server should now display the messages and the client should receive echo replies
* UDP should be permitted

4. Retry the TCP client:

```bash
h1 python3 S06_Part03_Script_TCP_Client.py 10.0.10.3 5000
```

* this should still be blocked (SDN-level drop)

---

### 6. Inspecting Flows after Modification

Run:

```bash
s1 ovs-ofctl dump-flows s1
```

Look for:

* a flow for UDP with ip_proto=17, dst=10.0.10.3 and action output towards the h3 port
* a flow for TCP with ip_proto=6, dst=10.0.10.3 and empty actions (drop)

---

### Final SDN Deliverable

Combine all results from Stages 2 and 3 into a single file:

```
sdn_lab_output.txt
```

It must contain:

1. Relevant output from Stage 2:

   * ping h1 -> h2 (successful)
   * ping h1 -> h3 (failed)
   * a flow table dump

2. Output from Stage 3:

   * TCP client h1 -> h2 (messages successful)
   * TCP client h1 -> h3 (failed)
   * UDP client h1 -> h3 (successful after controller modification)
   * a flow table dump after modification

3. An explanation of 8–10 sentences describing:

   * the difference between classical routing (triangle) and SDN
   * how the Os-Ken controller influences TCP and UDP traffic
   * how the security policy is visible in the flow table (TCP blocked, UDP permitted)
   * what advantages SDN offers for such fine-grained (application-aware) policies

This file is the deliverable to be submitted for Seminar 6.

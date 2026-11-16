### Tasks: TCP and UDP traffic through the SDN switch

Continue from Part 2 with the baseline Os-Ken controller and the Mininet topology running. The topology was started from `04_SEMINARS/S06/2_sdn`, so the supplied application scripts are reached through `../3_sdn-app-traffic/`.

Commands prefixed with `h1`, `h2`, `h3` or `s1` run at the **Mininet CLI**. Keep the separate controller terminal open. Server processes run in the background so the Mininet CLI remains available.

### 1. TCP permitted between h1 and h2

At the **Mininet CLI**, start the h2 server and record its process identifier:

```text
h2 sh -c 'python3 -u ../3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 > /tmp/compnet-s06-tcp-h2.log 2>&1 & echo $! > /tmp/compnet-s06-tcp-h2.pid'
h2 ss -ltn '( sport = :5000 )'
```

Wait until h2 shows a listener on port 5000, then run a bounded client exchange:

```text
h1 sh -c 'printf "hello\nexit\n" | timeout 8s python3 -u ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.2 5000'
h2 cat /tmp/compnet-s06-tcp-h2.log
```

The client should connect and receive an echo of `hello`. You can also run the client interactively and type `exit` when finished. Save both client and server evidence.

### 2. TCP blocked between h1 and h3

A failed connection to an absent server does not demonstrate an SDN policy. Start a real h3 listener first:

```text
h3 sh -c 'python3 -u ../3_sdn-app-traffic/S06_Part03_Script_TCP_Server.py 5000 > /tmp/compnet-s06-tcp-h3.log 2>&1 & echo $! > /tmp/compnet-s06-tcp-h3.pid'
h3 ss -ltn '( sport = :5000 )'
s1 ovs-ofctl -O OpenFlow13 dump-flows s1
```

After confirming the listener, attempt the blocked connection:

```text
h1 sh -c 'timeout 8s python3 -u ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.3 5000; printf "Client exit status: %s\n" "$?"'
s1 ovs-ofctl -O OpenFlow13 dump-flows s1
```

The deadline bounds the blocked demonstration; exit status 124 means `timeout` ended the client. A client-side connection error may end earlier. Retain the server-listener evidence and the matching drop-flow counters to distinguish the policy result from a setup failure.

### 3. UDP initially blocked towards h3

Start the UDP echo server on h3:

```text
h3 sh -c 'python3 -u ../3_sdn-app-traffic/S06_Part03_Script_UDP_Server.py 6000 > /tmp/compnet-s06-udp-h3.log 2>&1 & echo $! > /tmp/compnet-s06-udp-h3.pid'
h3 ss -lun '( sport = :6000 )'
```

Confirm the listener, then send a message through the baseline policy:

```text
h1 sh -c 'printf "hello\nexit\n" | timeout 8s python3 -u ../3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py 10.0.10.3 6000; printf "Client exit status: %s\n" "$?"'
s1 ovs-ofctl -O OpenFlow13 dump-flows s1
```

The baseline policy drops IPv4 traffic to h3, including the first UDP packet before a drop flow has been installed. Expect no echo. The deadline prevents the client from waiting indefinitely for a blocked reply.

### 4. Extend the baseline policy: permit UDP, retain the TCP block

Edit `S06_Part02C_Script_SDNOS_Ken_Controller.py` in `2_sdn/`. Implement a UDP exception for **both directions** between h1 and h3. An echo requires a request path and a reply path.

Requirements for your change:

- Match IPv4 UDP using `eth_type=0x0800` and `ip_proto=17`.
- Permit `10.0.10.1 → 10.0.10.3` on switch port 3.
- Permit `10.0.10.3 → 10.0.10.1` on switch port 1.
- Give the exception a priority greater than the baseline generic h3 drop rule, whose priority is 20.
- Handle the current packet as well as installing the future flow, following the baseline controller's buffer/packet-out logic.
- Keep TCP towards h3 blocked and retain ARP handling.

A directional match has this form:

```python
match = parser.OFPMatch(
    eth_type=0x0800,
    ip_proto=17,
    ipv4_src="10.0.10.1",
    ipv4_dst="10.0.10.3",
)
actions = [parser.OFPActionOutput(3)]
```

Add the corresponding reply direction, with source/destination exchanged and output port 1. Evaluate the exception before the generic h3-drop branch. Save your edited controller as part of the deliverable.

**Restart cleanly after changing the policy:** stop the application servers using Section 6 below, enter `exit` at the Mininet CLI and stop the old controller with `Ctrl+C`. In the controller terminal, run:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S06/2_sdn"
osken-manager --ofp-listen-host 127.0.0.1 --ofp-tcp-listen-port 6633 S06_Part02C_Script_SDNOS_Ken_Controller.py
```

In a second guest terminal, start a fresh topology:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S06/2_sdn"
sudo python3 S06_Part02B_Script_SDN_Topo_Switch.py
```

A new topology prevents old drop flows from obscuring the changed policy. Restart the h3 TCP and UDP servers from Sections 2–3 and verify their listeners.

### 5. Re-test the exception and inspect flows

At the new **Mininet CLI**:

```text
h1 sh -c 'printf "hello\nexit\n" | timeout 8s python3 -u ../3_sdn-app-traffic/S06_Part03_Script_UDP_Client.py 10.0.10.3 6000'
h3 cat /tmp/compnet-s06-udp-h3.log
h1 sh -c 'timeout 8s python3 -u ../3_sdn-app-traffic/S06_Part03_Script_TCP_Client.py 10.0.10.3 5000; printf "Client exit status: %s\n" "$?"'
s1 ovs-ofctl -O OpenFlow13 dump-flows s1
```

Expected results: UDP produces an echo, TCP remains blocked and the flow table contains the UDP request/reply directions at a priority above the general drop. Check counters as well as rule presence.

The optional advanced controller provides a separate comparison using `ALLOW_UDP_TO_H3=1`. It does not replace the required explanation of your own baseline-policy change. Restart the topology when switching controllers.

### 6. Stop the processes you started

For each server started in the current topology, use its recorded PID at the **Mininet CLI**:

```text
h2 sh -c 'test ! -f /tmp/compnet-s06-tcp-h2.pid || kill "$(cat /tmp/compnet-s06-tcp-h2.pid)"'
h3 sh -c 'test ! -f /tmp/compnet-s06-tcp-h3.pid || kill "$(cat /tmp/compnet-s06-tcp-h3.pid)"'
h3 sh -c 'test ! -f /tmp/compnet-s06-udp-h3.pid || kill "$(cat /tmp/compnet-s06-udp-h3.pid)"'
```

Run only the lines corresponding to servers you started in this topology; a PID file from an older run is not a current process identifier. Then enter `exit` at `mininet>` and stop the controller with `Ctrl+C`.

### Final SDN deliverable

Create `sdn_lab_output.txt` containing:

- The controller-policy modification and why each match, action and priority is needed
- The successful h1–h2 TCP exchange
- Listener and drop-counter evidence for the blocked h1–h3 TCP test
- The blocked baseline UDP test and the successful UDP request/reply exchange after modification
- Flow dumps produced with `-O OpenFlow13`
- Eight to ten sentences comparing static routing with SDN, explaining the policy's effect on TCP/UDP and relating the observations to the actual match/action rules

Submit the modified controller alongside the log. Retain unexpected results and explain their causes instead of treating any timeout as proof that the policy worked.

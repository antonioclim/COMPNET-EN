### Tasks: SDN topology with Os-Ken and an OpenFlow switch

All commands run inside the MININET-SDN guest. Commands labelled **Mininet CLI** are entered at `mininet>`; the controller and packet capture use separate Ubuntu terminals.

### 1. Start the Os-Ken controller

In **SSH Terminal 1**:

```bash
test -f "$HOME/venvs/compnet/bin/activate" && source "$HOME/venvs/compnet/bin/activate"
cd "$HOME/COMPNET-EN/04_SEMINARS/S06/2_sdn"
command -v osken-manager
osken-manager --ofp-listen-host 127.0.0.1 --ofp-tcp-listen-port 6633 S06_Part02C_Script_SDNOS_Ken_Controller.py
```

Keep this terminal open. The controller will report the switch connection after the topology starts. Both endpoints explicitly use port 6633.

Use the manager from the supplied course environment. The application imports `os_ken`, so `ryu-manager` is not a drop-in replacement. OS-Ken 4.x removed the manager CLI ([release notes](https://docs.openstack.org/releasenotes/os-ken/2026.1.html)); do not replace a working course installation with an unpinned upgrade.

**Optional advanced controller:** after stopping the baseline controller and exiting its topology, choose one of these commands in Terminal 1. Start a fresh topology afterwards so old flows do not carry over.

```bash
osken-manager --ofp-listen-host 127.0.0.1 --ofp-tcp-listen-port 6633 S06_Part02C_Script_SDNOS_Ken_Controller_AdvancedPolicy.py
```

Or, to enable its UDP exception to/from h3:

```bash
ALLOW_UDP_TO_H3=1 osken-manager --ofp-listen-host 127.0.0.1 --ofp-tcp-listen-port 6633 S06_Part02C_Script_SDNOS_Ken_Controller_AdvancedPolicy.py
```

The advanced controller is an extension exercise. Complete the baseline observations first.

### 2. Start the Mininet topology

In **SSH Terminal 2**:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S06/2_sdn"
sudo python3 S06_Part02B_Script_SDN_Topo_Switch.py
```

After startup, enter these commands at the **Mininet CLI**:

```text
h1 ip -brief addr
h2 ip -brief addr
h3 ip -brief addr
```

The hosts use `10.0.10.1/24`, `10.0.10.2/24` and `10.0.10.3/24`. The switch uses OpenFlow 1.3.

### 3. Test connectivity

**Mininet CLI — h1 to h2, permitted:**

```text
h1 ping -c 3 -W 1 10.0.10.2
```

Expect replies and forwarding flows. Then test the blocked destination:

```text
h1 ping -c 3 -W 1 10.0.10.3
```

Expect no replies. Correlate that result with the controller log and the drop flow. Packet loss alone is insufficient evidence of a policy rule.

### 4. Inspect the flow table

**Mininet CLI:**

```text
s1 ovs-ofctl -O OpenFlow13 dump-flows s1
```

Identify the table-miss rule, the permitted h1–h2 traffic and the drop rule for destination `10.0.10.3`. Compare packet counters before and after the blocked ping. Use the explicit `-O OpenFlow13` option consistently.

### 5. Optional bounded traffic capture

Open **SSH Terminal 3 inside the guest** and run:

```bash
sudo tshark -i s1-eth1 -a duration:15 -f icmp
```

While the capture is active, run at the existing **Mininet CLI in Terminal 2**:

```text
h1 ping -c 3 -W 1 10.0.10.2
```

The capture stops after 15 seconds. This leaves the Mininet CLI available for traffic generation and avoids an indefinitely blocking capture command in that CLI.

### 6. Continue or stop

Continue directly with Part 3 while retaining the controller and topology. To stop, enter `exit` at the Mininet CLI and press `Ctrl+C` in the controller terminal. Use `sudo mn -c` only if a failed run left resources behind and no other Mininet exercise is active.

### Partial deliverable

Create `sdn_stage2_output.txt` containing:

- Both bounded ping outputs
- A flow dump with `-O OpenFlow13`
- Relevant controller messages and packet counters
- Five to seven sentences explaining the permitted h1–h2 path, the drop towards h3 and the role of the table-miss rule

This file will be extended with the TCP and UDP results from Part 3.

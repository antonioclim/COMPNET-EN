### Mininet Tasks: Address Configuration, Routing and Testing

These exercises must be carried out inside the Mininet CLI after starting the topology:

```

sudo python3 index_mininet-topology.py

```

---

### 1. Verifying the Interfaces

Run:

```

h1 ip a
h2 ip a
r1 ip a

```

Confirm that the IPv4 addresses have been assigned correctly.

---

### 2. Testing Local Connectivity

Test host-to-router connectivity:

```

h1 ping -c 3 10.0.1.1
h2 ping -c 3 10.0.2.1

```

If it does not work, note the error.

---

### 3. Enabling Routing (if not already active)

Check:

```

r1 sysctl net.ipv4.ip_forward

```

If the value is 0, enable it with:

```

r1 sysctl -w net.ipv4.ip_forward=1

```

---

### 4. Adding Default Routes on h1 and h2

On h1:

```

h1 ip route add default via 10.0.1.1

```

On h2:

```

h2 ip route add default via 10.0.2.1

```

---

### 5. Testing End-to-End Connectivity

```

h1 ping -c 4 10.0.2.10

```

If this succeeds, r1 has routed the packets correctly.

---

### 6. Tracing the Path with traceroute

```

h1 traceroute 10.0.2.10

```

You should observe the packet passing through r1.

---

### 7. Capturing Traffic

Start a capture on r1:

```

r1 tcpdump -i r1-eth0 -n

```

Then, in another Mininet console:

```

h1 ping 10.0.2.10

```

Observe the ICMP packets.

Stop tcpdump with Ctrl-C.

---

### 8. Optional: IPv6 Test (if you enabled the addresses)

Verify:

```

h1 ping6 2001:db8:10:2::10

```

---

### Deliverable

Create the file:

```

mininet_lab_output.txt

```

It must contain:
- the commands used  
- the output of `ping`, `traceroute` and `tcpdump` (partial capture)  
- an explanation of 5–7 sentences describing:
  - how the subnets from the subnetting section were used
  - the role of the default route
  - why r1 is necessary for the communication

This file will be uploaded as proof of lab completion.

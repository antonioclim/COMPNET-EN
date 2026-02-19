### Tasks: Static Routing in the Triangle Topology

---

### 1. Verifying IP Addresses

Run the following in the Mininet CLI:

```

r1 ip a
r2 ip a
r3 ip a
h1 ip a
h3 ip a

```

Confirm that every interface has the correct address.

---

### 2. Configuring Static Routes

### On r1:

```

r1 ip route add 10.0.3.0/30 via 10.0.12.2

```

or the alternative route:

```

r1 ip route add 10.0.3.0/30 via 10.0.13.2

```

### On r2:

```

r2 ip route add 10.0.1.0/30 via 10.0.12.1
r2 ip route add 10.0.3.0/30 via 10.0.23.2

```

### On r3:

```

r3 ip route add 10.0.1.0/30 via 10.0.13.1
r3 ip route add 10.0.12.0/30 via 10.0.23.1

```

---

### 3. Testing Connectivity

```

h1 ping -c 4 10.0.3.2

```

If replies arrive, routing is functional.

---

### 4. Observing the Route in Use

```

h1 traceroute 10.0.3.2

```

Notes:
- If the output shows r1 → r2 → r3, the route on r1 is set via r2.
- If the output shows r1 → r3, traffic takes the direct path.

---

### 5. Exercise: Manually Changing the Route

1. Delete the current route:

```

r1 ip route del 10.0.3.0/30

```

2. Add the alternative route through r3:

```

r1 ip route add 10.0.3.0/30 via 10.0.13.2

```

3. Compare:

```

h1 traceroute 10.0.3.2

```

---

### 6. *Optional*: Packet Capture on Routers

Example:

```

r2 tcpdump -i r2-eth1 -n

```

---

### Deliverable

Create the file:

```

triangle_routing_output.txt

```

It must include:

- `ip route` output from each router  
- `ping` and `traceroute` output  
- A short `tcpdump` capture fragment  
- A paragraph of 6–8 sentences explaining:  
  - how static routing works  
  - how you determined the path taken by traffic  
  - what happens when routes are changed  
  - why traceroute displays the path in the observed order

This file will be uploaded as proof of exercise completion.

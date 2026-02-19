### Scenario: ping and traceroute (latency vs route)

#### Objective
- Observe latency (ping) and the route (hops) to a destination.
- Briefly discuss latency, jitter, loss and hop count.

#### Recommendation
Prefer a real network connection (Wi‑Fi or Ethernet). Terminal access is required.

#### Step 1: Identify the local gateway
Linux/macOS:
- ip route | grep default

Windows:
- ipconfig

Note the gateway IP (typically 192.168.x.1 or 10.x.x.1).

#### Step 2: Ping the gateway (local)
Linux/macOS:
- ping -c 20 <GATEWAY_IP>

Windows:
- ping -n 20 <GATEWAY_IP>

Observe:
- min/avg/max (or approximations)
- packet loss

#### Step 3: Ping an external destination
Examples:
- 1.1.1.1
- 8.8.8.8

Linux/macOS:
- ping -c 20 1.1.1.1

Windows:
- ping -n 20 1.1.1.1

Discussion:
- Why does latency increase?
- What does jitter mean?

#### Step 4: traceroute (route)
Linux:
- traceroute 1.1.1.1

macOS:
- traceroute 1.1.1.1

Windows:
- tracert 1.1.1.1

Observe:
- How many hops?
- Where do timeouts appear?
- Difference between local (ISP) hops and more distant hops

#### Quick questions (2–3 minutes)
- Why does ping use ICMP rather than TCP?
- Why do some routers not respond to traceroute?

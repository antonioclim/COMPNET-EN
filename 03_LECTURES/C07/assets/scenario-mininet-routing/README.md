### Scenario: Mininet (router triangle) — failures and asymmetric routing

#### Requirements
- Linux
- Mininet installed
- run as root (sudo)

#### Topology
- 3 routers: r1, r2, r3 (fully connected triangle: r1-r2, r2-r3, r1-r3)
- 3 LANs:
  - h1 behind r1 (10.1.0.0/24)
  - h2 behind r2 (10.2.0.0/24)
  - h3 behind r3 (10.3.0.0/24)

Inter-router links:
- r1-r2: 10.12.0.0/24
- r1-r3: 10.13.0.0/24
- r2-r3: 10.23.0.0/24

#### Scenario 1: link-down (traffic uses an alternative route)
Running:
- sudo python3 tringle-net.py link-down

What happens:
- static routes are configured so that traffic between LANs can bypass a failed link
- the r1-r2 link is then brought down
- ping h1 -> h2 should still succeed via r3

#### Scenario 2: asymmetric routing (route in one direction only)
Running:
- sudo python3 tringle-net.py asymmetric

What happens:
- r1 has a route towards 10.2.0.0/24 via r2
- r2 does not have a return route towards 10.1.0.0/24
- h1 -> h2 can reach the destination (request), but the reply is lost (no route back)

#### Using the Mininet CLI
The script enters the Mininet CLI after it configures the selected scenario.
Useful commands:
- r1 ip route
- r2 ip route
- r3 ip route
- r1 ip link
- h1 ping -c 2 10.2.0.2
- h1 traceroute -n 10.2.0.2  (if traceroute is available)

#### Important observation
Routing can be asymmetric. A common symptom is that traffic appears to work in one direction only because the return route is missing.

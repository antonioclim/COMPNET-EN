### Introduction to Network Simulation with Mininet

In this section we use Mininet to create a basic topology consisting of two hosts and an intermediary node that acts as a router. The goal is to manually configure IP addresses and routes, then verify network operation using commands such as `ping`, `traceroute` and `tcpdump`.

---

### Why Mininet

Mininet is a lightweight network simulator that runs on a single machine and emulates:
- virtual hosts
- switches
- routers
- virtual links

It is well suited for rapid lab work because:
- it requires neither containers nor multiple virtual machines
- all hosts can execute real Linux commands
- it allows traffic inspection via tcpdump, Wireshark or built-in Mininet commands

---

### Topology Used

We create a simple topology:

```

h1 ----- r1 ----- h2

```

Hosts:
- h1 and h2 will each have their own IPv4 and IPv6 addresses
- r1 will have two interfaces, one for each subnet

---

### Addressing Schemes

We use two IPv4 subnets:

- Subnet A (h1 – r1): `10.0.1.0/24`
- Subnet B (h2 – r1): `10.0.2.0/24`

Assigned addresses:

| Host | Interface | Address |
|------|-----------|---------|
| h1 | h1-eth0 | 10.0.1.10 |
| r1 | r1-eth0 | 10.0.1.1 |
| h2 | h2-eth0 | 10.0.2.10 |
| r1 | r1-eth1 | 10.0.2.1 |

Optionally, you may also configure IPv6:

- `2001:db8:10:1::/64` for the h1–r1 link  
- `2001:db8:10:2::/64` for the h2–r1 link

---

### Student Objectives

- launch the Mininet topology  
- verify the IP configurations  
- enable IP forwarding on r1  
- configure default routes on h1 and h2  
- verify connectivity with ping  
- observe the path with traceroute  
- capture packets with tcpdump  

Complete all tasks in the file `index_mininet-config_tasks.md`.

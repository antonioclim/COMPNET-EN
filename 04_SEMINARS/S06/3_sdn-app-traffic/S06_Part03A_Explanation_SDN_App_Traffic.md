### Application Traffic through SDN: Python Servers and Clients

In earlier stages we:

- built a simple SDN topology (h1, h2 and h3 connected to s1)
- used an Os-Ken controller that permits traffic between h1 and h2 while blocking traffic towards h3
- tested the behaviour with `ping`

This stage moves on to **application-level traffic**:

- a Python TCP server running on h2
- a Python TCP client running on h1
- a Python UDP server running on h3
- a Python UDP client running on h1

Expected observations:

- successful TCP connection between h1 and h2 (permitted by the controller)
- failed TCP connection between h1 and h3 (blocked by the controller)
- after modifying the controller:
  - UDP traffic permitted between h1 and h3
  - TCP traffic towards h3 still blocked

---

### Ports and Addresses

For clarity the following assignments are used:

- TCP server on h2: port 5000
- TCP client on h1: connects to `10.0.10.2:5000`
- UDP server on h3: port 6000
- UDP client on h1: sends to `10.0.10.3:6000`

The topology is the same as in Stage 2:

```

h1 ---- s1 ---- h2
            |
            +---- h3

```

IP addresses:

- h1: 10.0.10.1/24
- h2: 10.0.10.2/24
- h3: 10.0.10.3/24

---

### Objectives

The student must:

- start the TCP server on h2 and test the TCP client from h1 (succeeds)
- attempt a TCP connection from h1 to h3 (fails)
- start the UDP server on h3
- modify the Os-Ken controller so that UDP from h1 to h3 is permitted
- test the UDP client and confirm the different behaviour of TCP versus UDP
- save command output in a log file

Concrete commands and steps are in `index_sdn_app-traffic_tasks.md`.

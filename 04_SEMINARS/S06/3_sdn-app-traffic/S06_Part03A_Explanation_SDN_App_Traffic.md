### Application Traffic through SDN: Python Servers and Clients

In earlier stages we:

- built a simple SDN topology (h1, h2 and h3 connected to s1)
- used an Os-Ken controller that permits traffic between h1 and h2 while blocking traffic towards h3
- tested the behaviour with `ping`

This stage moves on to **application-level traffic**:

- a Python TCP server running on h2
- a Python TCP server on h3, so the blocked test has a confirmed listener
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
- TCP server on h3: port 5000 (blocked-path comparison)
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
- confirm the h3 TCP listener, then attempt a connection from h1 to h3 and correlate the failure with the drop-flow counters
- start the UDP server on h3
- modify the Os-Ken controller so that UDP requests from h1 to h3 and replies from h3 to h1 are permitted
- test the UDP client and confirm the different behaviour of TCP versus UDP
- save command output in a log file

Concrete commands and steps are in [S06_Part03B_Tasks_SDN_App_Traffic.md](S06_Part03B_Tasks_SDN_App_Traffic.md).

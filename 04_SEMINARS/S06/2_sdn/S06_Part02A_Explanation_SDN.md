### SDN Introduction and the OpenFlow Switch Topology

This section uses a Mininet topology built around an OpenFlow switch (s1) controlled by an external Os-Ken controller. The aim is to observe how the controller decides which traffic is permitted and which is blocked by installing flows in the switch.

---

### Core SDN Concept

Software Defined Networking (SDN) separates:

- **control plane** – the decision logic (the controller)
- **data plane** – the devices that merely enforce rules (switches and routers)

Within an SDN architecture:

- the controller communicates with switches through a control protocol (e.g. OpenFlow)
- switches forward unknown packets to the controller (packet_in)
- the controller replies with instructions (packet_out, flow_mod) that install match–action rules

---

### SDN Topology Used

The Mininet topology:

```

h1 ---- s1 ---- h2
            |
            +---- h3

```

- s1 is an Open vSwitch configured to use OpenFlow
- h1, h2 and h3 are Mininet hosts
- an external Os-Ken controller connects to s1

Addressing scheme (all hosts share the same subnet):

| Host | Interface  | IPv4 Address   |
|------|------------|----------------|
| h1   | h1-eth0    | 10.0.10.1/24   |
| h2   | h2-eth0    | 10.0.10.2/24   |
| h3   | h3-eth0    | 10.0.10.3/24   |

---

### Desired Behaviour (SDN Logic)

The Os-Ken controller must enforce the following policy:

- traffic between h1 and h2 is permitted (h1 ↔ h2)  
- traffic from h1 towards h3 is blocked  
- optionally:
  - traffic from h3 towards h1 may be permitted or blocked, depending on the implementation

The implementation works as follows:

- upon the first packet (packet_in) between h1 and h2:
  - bidirectional flows are installed in s1 (h1 → h2 and h2 → h1)
- upon a packet destined for h3:
  - a drop flow (no actions) is installed to block the traffic

---

### What You Will Do in This Stage

- start the Os-Ken controller with the provided application
- start the Mininet topology containing switch s1
- test connectivity:
  - `h1 ping h2` should succeed
  - `h1 ping h3` should be blocked
- inspect the flow table in s1 with `ovs-ofctl dump-flows`

Python servers and clients will be added in the next stage to generate more interesting traffic than ping.

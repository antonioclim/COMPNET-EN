### The physical layer and the data link layer

---

### Learning objectives
By the end of the lecture, students should be able to:
- Describe the role of the physical layer and its limitations
- List transmission media types and relevant properties
- Briefly explain line coding (NRZ, NRZI and Manchester) and why it exists
- Understand the idea of modulation (ASK, FSK, PSK and QAM) at a conceptual level
- Explain the role of LLC and MAC and the structure of a frame
- Understand Ethernet: MAC addresses, frame format, collisions and CSMA/CD
- Understand Wi‑Fi at Layer 2: channels, frame types, CSMA/CA and interface modes
- Understand the role of a switch: CAM learning, flooding and ageing
- Explain VLANs and why they reduce the broadcast domain

---

### Where we are in the stack
- Physical layer: signals and bits
- Data link layer: frames, MAC and medium access

[FIG] assets/images/fig-l1-l2-context.png

---

### Physical layer: role
- Physical transfer of bits over a medium
- Defines the signal type: electrical, optical or radio
- Defines parameters: rate, synchronisation, connectors and distances

---

### Transmission media (high level)
- Guided:
  - copper: coaxial, twisted pair (UTP/STP)
  - optical fibre: single-mode, multi-mode
- Unguided:
  - radio: Wi‑Fi, LTE and similar technologies

[FIG] assets/images/fig-transfer-media.png

---

### Relevant medium properties
- attenuation (signal amplitude decreases)
- noise (interference)
- bandwidth (Hz) vs bitrate (bits/s)
- crosstalk (copper), reflections (impedance)
- practical maximum distance

---

### Line coding: why?
- we want synchronisation and transitions
- we want to avoid prolonged DC components
- we sometimes want simple error detection
- examples: NRZ, NRZI and Manchester

[FIG] assets/images/fig-line-coding-overview.png

[SCENARIO] assets/scenario-line-coding/

---

### NRZ (concept)
- 1 and 0 are represented as constant levels
- problem: long sequences without transitions make synchronisation difficult

---

### NRZI (concept)
- 1 produces a transition and 0 does not (or the inverse, depending on convention)
- improves synchronisation for certain data patterns

---

### Manchester (concept)
- a transition in the middle of the bit period
- good synchronisation, but the signal rate increases (bandwidth cost)

---

### Modulation (concept)
- we vary a carrier:
  - ASK: amplitude
  - FSK: frequency
  - PSK: phase
  - QAM: a combination of amplitude and phase

[FIG] assets/images/fig-modulation.png

---

### From signal to frame
- Layer 1 delivers a bit stream
- Layer 2 builds frames: delimitation, addressing and CRC

---

### Physical layer limitations (transition to Layer 2)
- The physical layer cannot communicate directly with software
- The physical layer does not support addressing
- It handles simple bit streams
- The data link layer:
  - enables addressing
  - provides a structured unit: the frame
  - offers medium access services to upper layers

---

### Data link layer structure
- Two sublayers:
  - LLC (Logical Link Control): interface towards software
  - MAC (Media Access Control): interface towards hardware

[FIG] assets/images/fig-llc-mac.png

---

### LLC
- IEEE 802.2
- independent of the physical medium
- flow control (where applicable)
- multiplexing for upper-layer protocols

---

### MAC
- medium access control
- builds the actual frames
- technology dependent (Ethernet vs Wi‑Fi)

---

### MAC functions
- frame delimitation
- source and destination addressing (MAC)
- transparent transfer of LLC PDUs
- error detection (CRC)
- medium access control

---

### Layer 2 encapsulation
- wrapping data into a frame
- the format depends on the technology, but fields are similar

[FIG] assets/images/fig-l2-encapsulation.png

---

### Typical frame fields
- start of frame (preamble/delimiter)
- source and destination MAC addresses
- type/length
- data (payload)
- CRC/FCS

---

### Ethernet
- The most widespread Layer 2 technology (IEEE 802.3)
- media: copper (historically coaxial, then twisted pair) and fibre in many scenarios
- variants: 10BaseT, 100BaseT, 1000BaseT and others

---

### Ethernet frame format
[FIG] assets/images/fig-ethernet-frame.png

---

### MAC addresses (48 bits)
- OUI (24 bits) + interface identifier (24 bits)
- local broadcast: FF:FF:FF:FF:FF:FF
- locally administered addresses: a specific bit set in the first octet

[SCENARIO] assets/scenario-mac-arp-ethernet/

---

### Ethernet collisions (historical context and concept)
- occur when two nodes transmit simultaneously on the same shared medium
- CSMA/CD: listen, detect collisions, back off
- in full duplex with switches, collisions practically disappear

[FIG] assets/images/fig-csma-cd.png

---

### Other Layer 2 issues (Ethernet)
- switching loops → broadcast storms (there is no TTL at Layer 2)
- jabber (frames that are too large)
- runt frames (frames that are too small)

---

### Wi‑Fi (IEEE 802.11)
- medium: air (radio waves)
- common bands: 2.4 GHz and 5 GHz
- channels: overlapping or non-overlapping

[FIG] assets/images/fig-wifi-channels-24ghz.png

---

### Wi‑Fi frames (types)
- control
- management
- data

---

### Wi‑Fi frame structure (concept)
- control: version, type, subtype
- ToDS/FromDS
- 4 addresses (depending on the scenario)
- FCS at the end

[FIG] assets/images/fig-wifi-frame-concept.png

---

### Wi‑Fi collisions and CSMA/CA
- collisions occur frequently (the medium is shared)
- CSMA/CA: listen, wait randomly, optionally use RTS/CTS, then wait for acknowledgement

[FIG] assets/images/fig-csma-ca.png

---

### Wi‑Fi interface modes
- managed (client)
- AP (access point)
- AP with VLAN tagging (AP-tag)
- Wi‑Fi P2P
- monitor (Layer 2 sniffing)

---

### Wi‑Fi authentication (high level)
- WEP (obsolete)
- WPA (obsolete)
- WPA2 (very widespread)
- WPA3 (in adoption)

---

### Switches: repeater vs bridge vs switch
- repeater: amplifies the signal
- bridge: minimal filtering, simple decisions
- switch: forwarding based on MAC (virtual circuits)

---

### CAM (MAC learning)
- table: MAC → port
- learns from the source address of frames
- if the destination is unknown: floods on all ports

[FIG] assets/images/fig-switch-cam-learning.png

---

### CAM ageing
- entries expire if they are not used
- prevents incorrect associations after a host moves

---

### VLAN
- splits a physical network into logical networks
- each VLAN = a distinct broadcast domain
- tagging (802.1Q) on a trunk

[FIG] assets/images/fig-vlan.png

---

### Summary
- L1: medium, signal, coding and modulation
- L2: frames, MAC/LLC, CRC and medium access
- Ethernet vs Wi‑Fi: CSMA/CD vs CSMA/CA
- switch: CAM learning, flooding and ageing
- VLAN: segmentation and broadcast domains

---

### Preparation for Lecture 5
- Network layer: IP, addressing and subnetting
- Difference: MAC (flat) vs IP (hierarchical)

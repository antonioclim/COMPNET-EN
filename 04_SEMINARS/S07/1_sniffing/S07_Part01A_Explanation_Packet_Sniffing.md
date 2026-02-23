### Seminar 7 — Intercepting TCP and UDP Packets

In this seminar we shall work with:
- RAW sockets to intercept packets at the IP layer
- packet filters implemented in Python
- a mini port-scanner
- a simple port-scan detection script

The goal is to understand what TCP/UDP packets look like at a low level and how to build basic tools comparable, in principle, to tcpdump or Wireshark.

---

### What packet interception means

When you run a packet sniffer on your machine:

- you open a special (RAW) socket capable of receiving raw IP packets
- the operating system delivers copies of packets traversing the network interface to your application
- you can inspect IP, TCP, UDP, ICMP headers and so on

The difference from ordinary sockets (TCP/UDP):

- a TCP socket sees only the data stream belonging to its own connection
- a UDP socket sees only the datagrams destined for its own port
- a RAW socket sees raw packets for multiple connections — potentially all of them

Normally, RAW sockets require elevated privileges (root).

---

### Promiscuous mode and network-level captures

Under normal conditions a network interface accepts only packets addressed to it.

In promiscuous mode:

- the network card accepts every packet traversing the medium
- the network driver forwards them to the kernel's network stack
- a sniffer (tcpdump, Wireshark) can observe all of them

In our laboratory:

- we focus on local captures, on the lab machine or on Mininet hosts
- we do not attempt to intercept other people's traffic in production
- all exercises are strictly educational

---

### How tcpdump and Wireshark perform captures

tcpdump and Wireshark:

- typically use libpcap for efficient kernel-level captures
- can apply BPF (Berkeley Packet Filter) rules directly inside the kernel for performance
- decode complex protocols (HTTP, DNS, TLS and so on)

In this seminar:

- we shall implement simplified variants in Python
- we shall work directly with RAW sockets and decode the basic headers manually:
  - IP (IPv4)
  - TCP
  - UDP

We shall not reach Wireshark's level of detail, but we shall understand the fundamental structure of packets.

---

### Why this knowledge matters

These skills are useful for:

- low-level network debugging (when ping and traceroute are not sufficient)
- understanding how firewalls and IDS/IPS systems operate
- traffic analysis for security (detecting port scans)
- practical understanding of headers and fields within network protocols

In the remainder of this seminar you will:
- write a simple sniffer (from a provided template)
- add a packet filter
- implement a mini port-scanner
- implement a mini scan detector

The next file contains the first code template for a simple sniffer.

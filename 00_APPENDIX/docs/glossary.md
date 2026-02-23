# 📖 Glossary of Terms — Computer Networks
> **Quick reference** for terminology used in the lab
> **Convention:** Technical terms are kept in English per industry standards
> **Version:** 2.3 — January 2026 (extended with WSL and Linux terms)

---

## A-B
**ACK (Acknowledgment)** — Packet or flag confirming successful data receipt. In TCP, each segment sent must be confirmed with ACK.

**apt / apt-get** — Package manager for Debian/Ubuntu distributions. `apt` is the modern version with a friendlier interface. Usage: `sudo apt install <package>`.

**Backlog** — The queue of pending connections waiting to be accepted by a server socket. Set via `listen(backlog)`.

**Bash** — Default shell in most Linux distributions. Configuration files: `~/.bashrc`, `~/.profile`.

**Bind** — Operation of associating a socket with a specific IP address and port. Required for servers before `listen()`.

**Bridge Network** — Default Docker network that enables communication between containers on the same host. Containers receive IPs from the 172.17.0.0/16 range.

**Bytes** — Python data type for raw binary data. Prefixed with `b` (e.g., `b"Hello"`). Required for network operations.

---

## C-D
**CIDR (Classless Inter-Domain Routing)** — Notation for specifying IP address ranges. Format: `IP/prefix` (e.g., `192.168.1.0/24`).

**Container** — Isolated instance of a Docker image, running one or more processes. Shares the kernel with the host.

**Context Manager** — Python construct (`with`) that guarantees resource release (files, sockets) even if an exception occurs.

**Daemon** — Process running in the background. Docker daemon (`dockerd`) manages containers. In WSL2, started with `sudo service docker start`.

**Dataclass** — Python decorator (`@dataclass`) that auto-generates `__init__`, `__repr__`, `__eq__` for data classes.

**DNS (Domain Name System)** — System for translating domain names to IP addresses. Standard port: 53 (UDP/TCP).

---

## E-H
**Encoding** — Process of converting text (str) to bytes. In Python: `"text".encode('utf-8')`.

**Endpoint** — Access point for a network service, specified as IP address + port.

**Exit Code** — Numeric value returned by a programme on termination. 0 = success, != 0 = error. Checked with `echo $?` in Bash.

**Handshake** — Initial exchange establishing a connection. TCP uses a three-way handshake: SYN → SYN-ACK → ACK.

**host.docker.internal** — Special DNS name in Docker that resolves to the host's IP address. Used to access host services from a container.

**HTTP (Hypertext Transfer Protocol)** — Application layer protocol for transferring web resources. Standard ports: 80 (HTTP), 443 (HTTPS).

---

## I-L
**Image (Docker)** — Read-only template for creating containers. Built from layers.

**Kernel** — Core of the operating system that manages hardware resources. WSL2 runs a real Linux kernel.

**Localhost** — Loopback address referring to the local machine: 127.0.0.1 (IPv4) or ::1 (IPv6).

**Logging** — Recording events for debugging and monitoring. Python module: `logging`.

**Loopback** — Network interface that routes traffic back to the same host. Address: 127.0.0.1 (IPv4) or ::1 (IPv6).

---

## M-P
**NAT (Network Address Translation)** — Technique of translating private IP addresses to public addresses, allowing multiple devices to share a single public address.

**Network Byte Order** — Big-endian, the standard order for transmitting data in networks. In Python: `struct.pack('!H', port)`.

**PATH** — Environment variable listing directories where the system searches for executables. Modified in `~/.bashrc`.

**Port** — 16-bit number (0-65535) identifying a service or application. Well-known ports: 0-1023.

**Portainer** — Web interface for managing Docker containers. Default port: 9000.

---

## S-T
**Shebang (#!)** — First line of a script indicating the interpreter. E.g., `#!/usr/bin/env python3`.

**Socket** — Endpoint for network communication, defined by IP + port + protocol. API for network programming.

**stdin / stdout / stderr** — Standard input, output and error streams. stdin = keyboard, stdout/stderr = terminal.

**struct** — Python module for conversion between bytes and native types. Essential for parsing binary protocols.

**sudo** — Command for executing with administrator (root) privileges. "Superuser do".

**systemd** — Modern init system for Linux. Manages services with `systemctl`. WSL2 by default does not use systemd.

**TCP (Transmission Control Protocol)** — Connection-oriented transport protocol with guaranteed ordered delivery without loss. HTTP, HTTPS and SSH use TCP.

**TTL (Time To Live)** — Field in IP header limiting packet lifetime (number of hops). Decremented by each router.

**Type Hints** — Optional annotations in Python for specifying types: `def func(x: int) -> str:`.

---

## U-W
**UDP (User Datagram Protocol)** — Connectionless transport protocol with no delivery guarantees. Used for DNS, streaming and gaming.

**UTF-8** — Standard encoding for Unicode text, compatible with ASCII. Recommendation: always use UTF-8.

**vEthernet (WSL)** — Virtual network interface in Windows connecting WSL2 to the host system. Visible in Wireshark.

**Volume** — Docker mechanism for data persistence outside the container lifecycle.

**Wireshark** — Network protocol analyser. Captures and displays packets in real time or from `.pcap` files.

**WSL / WSL2 (Windows Subsystem for Linux)** — Subsystem enabling a Linux kernel to run in Windows. WSL2 uses a real Linux kernel in a lightweight VM.

---

## Symbols and Notation

| Symbol | Meaning |
|--------|---------|
| `0.0.0.0` | All interfaces (bind) |
| `127.0.0.1` | Localhost |
| `/24` | Subnet mask 255.255.255.0 |
| `:8080` | Port 8080 |
| `→` | Data flow direction |
| `$` | Normal user prompt |
| `#` | Root prompt / comment |
| `~` | User's home directory |

---

## Common Confusions

| Term A | Term B | Difference |
|--------|--------|------------|
| **Container** | **Image** | Image is read-only template, container is runnable instance |
| **WSL1** | **WSL2** | WSL1 translates syscalls, WSL2 runs real Linux kernel |
| **send()** | **sendall()** | send() may send partially, sendall() sends everything |
| **localhost** | **0.0.0.0** | localhost = local only, 0.0.0.0 = all interfaces |
| **TCP** | **UDP** | TCP = guaranteed delivery, UDP = best-effort |
| **str** | **bytes** | str = Unicode text, bytes = binary data |
| **apt** | **apt-get** | apt = modern interface, apt-get = classic |
| **docker stop** | **docker rm** | stop preserves container, rm deletes it |
| **-p 8080:80** | **EXPOSE 80** | -p publishes port, EXPOSE only documents |
| **bridge** | **host** | bridge = isolated network, host = shares host's network |

---

## See Also

- [docs/misconceptions.md](misconceptions.md) — Detailed common errors
- [docs/concept_analogies.md](concept_analogies.md) — Concept analogies
- [LIVE_CODING_INSTRUCTOR_GUIDE.md](../LIVE_CODING_INSTRUCTOR_GUIDE.md) — Instructor guide

---

*Glossary for Computer Networks course*
*ASE Bucharest — CSIE*
*Version: 2.3 | January 2026*

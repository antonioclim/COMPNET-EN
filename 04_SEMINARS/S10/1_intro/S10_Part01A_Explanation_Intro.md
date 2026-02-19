### Seminar 10 – Network services: DNS and SSH (introduction)

This seminar covers two fundamental network services:

- **DNS (Domain Name System)** — for resolving names to IP addresses
- **SSH (Secure Shell)** — for remote administration, command execution and file transfer

The exercises use Docker containers in scenarios that resemble real deployments.

---

### 1. DNS refresher

DNS is a distributed system that maps names such as:

```text
www.example.com -> 93.184.216.34
```

A few important record types:

| Type | Description |
|-----|-------------|
| **A** | name → IPv4 |
| **AAAA** | name → IPv6 |
| **CNAME** | alias to another name |
| **MX** | mail exchanger |
| **NS** | authoritative nameserver for a zone |

Common tools:

- **nslookup** — simple and interactive
- **dig** — more detailed and usually preferred

Examples:

```bash
dig example.com
dig A example.com
dig @8.8.8.8 example.com
```

DNS normally uses UDP (port 53) and sometimes TCP (large responses or zone transfers).

---

### 2. SSH refresher

SSH is a secure protocol for:

- remote login
- remote command execution
- file transfer (typically via SFTP)
- traffic tunnelling (port forwarding)

Simple connection:

```bash
ssh user@host
```

Remote command:

```bash
ssh user@host "uname -a"
```

Local port forwarding (conceptual):

```bash
ssh -L local_port:dest_host:dest_port user@host
```

These ideas reappear later in container-based scenarios.

---

### 3. Seminar objectives

1. DNS resolution inside a Docker container network
2. implementing a minimal DNS server that answers a single query type
3. configuring an SSH server in a container
4. a Python script using **Paramiko** for remote command execution and SFTP
5. SSH port forwarding to an HTTP service running in another container

All exercises are accompanied by templates and concrete tasks.

---

### 4. Required tools

- **nslookup** and **dig** for DNS testing
- **ssh** and **scp** for basic interaction
- **docker** and **docker compose**
- Python with:
  - `paramiko`
  - optional: `dnslib` for the minimal DNS server

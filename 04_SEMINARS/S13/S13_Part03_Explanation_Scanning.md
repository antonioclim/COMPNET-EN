#### Seminar 13 – Stage 2

## Network Scanning: nmap and Implementing a Simple Scanner in Python

Two fundamental reconnaissance techniques are covered here:

1. **Scanning the network with dedicated tools (nmap)**
2. **Manual scanning via a Python script** (to understand the underlying mechanisms)

The goal is *not only* to discover open ports but to understand **the behaviour of an application at the socket level**.

---

## 1. Scanning with nmap

`nmap` is the standard tool for:

* host discovery
* open-port identification
* version detection
* vulnerability detection (via NSE scripts)

### 1.1. Scanning the lab network

The Docker network is:

```
172.20.0.0/24
```

To discover active hosts:

```bash
sudo nmap -sn 172.20.0.0/24
```

To discover open ports on each host:

```bash
nmap -sV -p- 172.20.0.10
nmap -sV -p- 172.20.0.11
nmap -sV -p- 172.20.0.12
```

Explanation:

* `-sV` identifies the software version
* `-p-` scans **all ports (1–65535)**
* `-T4` or `-T5` accelerates the scan (risk: false negatives)

---

## 2. Why Write Our Own Scanner?

`nmap` is excellent but complex, and it conceals many details.
To understand:

* how a TCP connection works
* what *open*, *closed* and *filtered* mean
* why timeouts matter

we write a minimal Python scanner that:

* attempts `connect()` on each port
* marks open ports
* uses configurable timeouts
* can rapidly scan a range of ports

---

## 3. Anatomy of a Simple Port Scanner

Required steps:

1. create a TCP socket
2. set a timeout (0.1 – 0.5 sec)
3. attempt the connection with `connect_ex()`
4. if the return value is `0` → port open
5. if it is any other error code → closed / filtered
6. close the socket
7. repeat for a set of ports

We provide a Python template where students fill in the core logic.

---

## 4. Why Can't a Simple Scanner See Everything?

Aspects our scanner **cannot** detect:

* UDP services (a different approach is needed for UDP)
* firewall-protected services
* filtered ports that respond only to certain packets
* version fingerprinting
* stealth scans (SYN scan, FIN scan, etc.)

However, it is perfectly suited for:

* grasping the concepts
* identifying TCP ports in the "open" state
* analysing the behaviour of applications in the vulnerable environment

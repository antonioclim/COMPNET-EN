## Lecture 11 – Application layer: FTP, DNS and SSH

### FTP, DNS and SSH: classic application protocols and their operational role

---

### Learning objectives

By the end of the lecture, students should be able to:

* Explain the difference between file-oriented, name-oriented and control-oriented application protocols
* Describe how FTP works (control vs data, active vs passive)
* Explain the role of DNS and the resolution process
* Understand the role of TTL and caching in DNS
* Explain the role of SSH as a secure control protocol
* Use SSH for remote execution, file transfer and tunnelling

---

### Application layer – recap

* The application layer defines:

  * semantics (what the data means)
  * message structure
  * protocol behaviour
* Application protocols:

  * use TCP or UDP
  * are independent of the underlying network and transport details
* Classic examples:

  * FTP – file transfer
  * DNS – name resolution
  * SSH – remote access and control

---

## FTP – File Transfer Protocol

---

### What is FTP?

* An application-layer protocol for file transfer
* An older specification (RFC 959), still conceptually relevant
* Runs over TCP
* Separates:

  * the control channel
  * the data channel

---

### FTP: control vs data

* Control connection:

  * TCP port 21
  * persistent
  * text commands and responses
* Data connection:

  * separate
  * used only for the actual transfer
  * opened and closed frequently

[FIG] assets/images/fig-ftp-control-data.png

---

### FTP: active mode vs passive mode

* Active mode:

  * the server initiates the data connection towards the client
  * problematic in the presence of NAT and firewalls
* Passive mode:

  * the client initiates the data connection
  * more reliable in modern networks

[FIG] assets/images/fig-ftp-active-vs-passive.png

---

### FTP in practice

* Classic FTP is fragile because of:

  * NAT
  * firewalls
  * multiple dynamic ports
* In practice:

  * FTPS (FTP over TLS)
  * SFTP (over SSH)
* FTP remains didactically relevant for:

  * the separation of control/data
  * the limitations of older protocols

---

## DNS – Domain Name System

---

### The role of DNS

* Translates symbolic names into IP addresses
* Distributed, hierarchical system
* Essential for the Internet to function
* Most applications depend on DNS implicitly

---

### DNS actors

* Stub resolver:

  * in the OS or the browser
* Recursive resolver:

  * ISP, enterprise or public (e.g., 8.8.8.8)
* Authoritative servers:

  * hold the final information for a zone

[FIG] assets/images/fig-dns-actors.png

---

### DNS resolution (conceptual)

1. The client queries the recursive resolver
2. The resolver queries:

   * root
   * TLD
   * authoritative
3. The response is cached according to TTL

[FIG] assets/images/fig-dns-resolution-overview.png

---

### TTL and caching

* Each DNS answer has a TTL
* Resolvers cache answers
* Changes are not visible instantly
* Low TTL:

  * flexibility
  * more traffic
* High TTL:

  * performance
  * slower propagation

---

### DNSSEC (brief mention)

* A security extension for DNS
* Provides:

  * data integrity
  * answer authenticity
* Based on a cryptographic chain of trust

[FIG] assets/images/fig-dnssec-chain-of-trust.png

---

## SSH – Secure Shell

---

### What is SSH?

* A secure remote access protocol
* Runs over TCP (port 22)
* Provides:

  * authentication
  * encryption
  * integrity
* Replaces telnet, rsh and insecure FTP

---

### SSH: connection and channels

* A single TCP connection
* Logical multiplexing into channels:

  * interactive shell
  * command execution
  * SFTP
  * port forwarding

[FIG] assets/images/fig-ssh-channels.png

---

### SSH port forwarding

* local forwarding
* remote forwarding
* dynamic forwarding (SOCKS proxy)
* SSH can function as:

  * a secure tunnel
  * a bastion host
  * an ad hoc proxy

[FIG] assets/images/fig-ssh-port-forwarding.png

---

### SSH as a 'control plane'

* Used extensively in:

  * system administration
  * DevOps
  * infrastructure operations
* Many modern tools are effectively 'orchestrated SSH':

  * Ansible
  * Fabric
  * older Terraform patterns (remote exec)
* SSH + JSON often becomes a general-purpose control protocol

---

## Practical scenarios

---

### Scenario 1 – Real FTP: control vs data

* A real FTP server (pyftpdlib)
* A Python FTP client
* Observing connections:

  * control
  * data
* Comparing active vs passive

[SCENARIO] assets/scenario-ftp-baseline/

---

### Scenario 2 – FTP with NAT/firewall

* A topology with an intermediate NAT
* A client 'behind the firewall'
* We demonstrate:

  * why active mode is problematic
  * why passive mode works

[SCENARIO] assets/scenario-ftp-nat-firewall/

---

### Scenario 3 – DNS: TTL and caching

* Authoritative DNS + recursive resolver
* Modifying a DNS zone
* Observing propagation as a function of TTL

[SCENARIO] assets/scenario-dns-ttl-caching/

---

### Scenario 4 – SSH as a provisioning mechanism

* Infrastructure description in JSON
* Remote command execution
* File transfer
* Python implementation with paramiko

[SCENARIO] assets/scenario-ssh-provision/

---

### Summary

* FTP:

  * control/data separation
  * limitations in modern networks
* DNS:

  * distributed system
  * caching and TTL
* SSH:

  * secure protocol
  * a general control mechanism

---

### Conclusion

Classic application protocols are:

* semantically simpler
* operationally extremely important
* the foundation for many modern systems

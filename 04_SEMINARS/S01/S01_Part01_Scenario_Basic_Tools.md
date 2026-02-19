### Introduction

This stage covers three basic utilities available on almost any operating system: `ping`, `netstat` and `nslookup`. Their purpose is to provide visibility into connectivity, the state of connections and the DNS resolution process. These tools are fundamental for any network analysis activity.

---

### Exploring the commands

#### 1. Checking connectivity with `ping`

```
ping -c 4 google.com
```

#### 2. Listing connections and listening ports with `netstat`

```
netstat -tulnp
```

```
netstat --tcp --udp --listening --program --numeric
```

#### 3. Querying DNS with `nslookup`

```
nslookup google.com
```

---

### Notes

Note that:

* `ping` checks whether a host responds and provides latency values. If DNS resolution works, the name is automatically translated into an IP address. If it does not, `ping` can fail even before sending ICMP.
* `netstat` shows which ports are listening and which connections are open. The `-tulnp` option combines TCP, UDP, listening sockets and the process names that use them.
* `nslookup` helps diagnose DNS issues: you can see the DNS server used, the IP addresses of the domain and possible resolution errors.

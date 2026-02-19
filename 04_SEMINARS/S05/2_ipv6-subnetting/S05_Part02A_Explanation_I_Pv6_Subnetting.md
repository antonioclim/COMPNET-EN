### Introduction to IPv6 and IPv6 Subnetting

This section outlines the essential IPv6 concepts: address structure, notation, subnetting and simple design examples.

The goal is to understand why IPv6 subnetting is simpler than in IPv4 and why, in practice, nearly all networks use /64 prefixes.

---

### Structure of an IPv6 Address

An IPv6 address is 128 bits long. Example:

```

2001:db8:abcd:0012:0000:0000:0000:0001

```

Hexadecimal notation is used, and groups of zeroes can be shortened:

- remove leading zeroes from each group
- replace a single contiguous run of all-zero groups with "::"

Shortened example:

```

2001:db8:abcd:12::1

```

---

### General Structure of an IPv6 Prefix

An IPv6 address is logically divided into three parts:

- global prefix (identifies the organisation)  
- subnet ID (identifies the subnet within the organisation)  
- interface ID (identifies a device within the subnet)

Common model:
```

[ 48-bit prefix ] [ 16-bit subnet ] [ 64-bit interface ID ]

```

This structure explains why most subnets are /64.

---

### Why /64 for LANs

General rule:  
**Every IPv6 LAN uses a /64 prefix.**

Rationale:
- the SLAAC protocol works only with /64  
- maximum interoperability  
- simplified network configuration  
- standardised equipment support

---

### Simple IPv6 Subnetting Example

Given the prefix:
```

2001:db8:10::/48

```

A /48 means 16 bits (2^16 = 65 536 subnets) are available for the Subnet ID.

Possible subnets:

- Subnet 1: `2001:db8:10:1::/64`  
- Subnet 2: `2001:db8:10:2::/64`  
- Subnet 3: `2001:db8:10:3::/64`  
- Subnet 4: `2001:db8:10:ff::/64` (e.g. for inter-router transit)

Each subnet has its own host address space:
```

2001:db8:10:X::1 ... 2001:db8:10:X:ffff:ffff:ffff:ffff

```

---

### Subnetting Example with Prefix Subdivision

Starting from:
```

2001:db8:abcd::/48

```

We want 4 large subnets.

Use 2 additional bits for the Subnet ID → prefix /50:

- `2001:db8:abcd:0::/50`  
- `2001:db8:abcd:4::/50`  
- `2001:db8:abcd:8::/50`  
- `2001:db8:abcd:c::/50`  

However, for most exercises and practical applications we use only /64.

---

### Quick Comparison: IPv4 vs IPv6

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address size | 32 bits | 128 bits |
| Subnetting | complex, dependent on host requirements | simple (typically /64) |
| Broadcast | Yes | No |
| Auto-configuration | Limited | Extensive (SLAAC) |
| Scalability | Low | Very high |

---

### What You Need to Know for This Seminar

- How an IPv6 address looks and how it is shortened.  
- How to identify the prefix and subnets.  
- How to create several /64 prefixes from a /48.  
- How to choose addresses for hosts.

Then proceed to the exercises.

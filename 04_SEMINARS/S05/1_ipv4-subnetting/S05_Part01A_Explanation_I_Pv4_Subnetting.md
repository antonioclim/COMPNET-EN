### IPv4 Addressing, Special Addresses, Subnetting and VLSM

This section revisits IPv4 addressing concepts and lays the groundwork for the subnetting and VLSM exercises. Read it carefully before moving on to the practical part.

---

### Structure of an IPv4 Address

An IPv4 address is 32 bits long and written in dotted decimal notation, for example:

```

192.168.10.25

```

Every address consists of:
- a network portion
- a host portion

The prefix length (CIDR notation) indicates how many bits are used for the network part:

- /24 means 24 bits for the network  
- /26 means 26 bits for the network  
- /30 means only 2 bits remain for hosts  

---

### Special IPv4 Ranges

Certain IPv4 ranges are reserved for specific purposes. The most important ones:

| Range | Purpose |
|---------|---------|
| 0.0.0.0/8 | "This host", default routes |
| 127.0.0.0/8 | Loopback (localhost) |
| 169.254.0.0/16 | Link-local APIPA, used when DHCP fails |
| 192.168.0.0/16 | Private |
| 10.0.0.0/8 | Private |
| 172.16.0.0/12 | Private |
| 224.0.0.0/4 | Multicast |
| 255.255.255.255 | Limited broadcast address |

Private ranges are the most commonly used in local networks.

---

### Network Address, Broadcast Address, Host Range

Every subnet has:
- **network address**: all host bits set to 0  
- **broadcast address**: all host bits set to 1  
- **host range**: from network address + 1 to broadcast − 1  

Example:

Subnet:
```

192.168.50.0/26

```

Details:
- /26 leaves 6 bits for hosts  
- total number of addresses = 64  
- network address = 192.168.50.0  
- broadcast address = 192.168.50.63  
- usable hosts = 192.168.50.1 … 192.168.50.62  

---

### Fixed Subnetting (Equal-Size Subnetting)

To subnet into equal-sized blocks, borrow bits from the host portion.

Example: divide 192.168.10.0/24 into 4 equal subnets.

1. 4 subnets require 2 borrowed bits (2^2 = 4)  
2. New prefix = /26  
3. Subnet increment = 64  

Subnets:
- 192.168.10.0/26  
- 192.168.10.64/26  
- 192.168.10.128/26  
- 192.168.10.192/26  

---

### VLSM (Variable Length Subnet Masking)

VLSM allows subnets of different sizes. The essential rule:

**always allocate the largest subnets first**

Example:

Requirements:
- 100 hosts  
- 50 hosts  
- 10 hosts  
- 2 hosts (point-to-point link)

Starting block:
```

10.0.0.0/24

```

1. 100 hosts → /25 (126 hosts)  
   subnet: 10.0.0.0/25  

2. 50 hosts → /26 (62 hosts)  
   subnet: 10.0.0.128/26  

3. 10 hosts → /28 (14 hosts)  
   subnet: 10.0.0.192/28  

4. 2 hosts → /30 (2 hosts)  
   subnet: 10.0.0.208/30  

This ordering prevents subnet overlap.

---

### Verification with an Online Calculator

After computing a subnet, verify:
- the prefix
- the network address
- the broadcast address
- the number of hosts

You may use any IPv4 subnet calculator.


### IPv6 Subnetting Exercises

Solve the exercises and write your answers in:
`index_ipv6-subnetting_solutions-template.md`

---

### Exercise 1: Understanding the Notation

Convert the following addresses to shortened form:

1. `2001:0db8:0000:0000:abcd:0000:0000:0001`  
2. `fe80:0000:0000:0000:00ff:0000:0000:1234`  

---

### Exercise 2: /64 Prefixes from a /48

You have:
```

2001:db8:1234::/48

```

Create the following /64 subnets:

- subnet for servers  
- subnet for LAN clients  
- subnet for IoT  
- subnet for a router-to-router link

Write down the chosen /64 prefixes.

---

### Exercise 3: Subnetting into Multiple /64s

From the same /48 prefix:
```

2001:db8:abcd::/48

```

Allocate 4 consecutive /64 subnets.  
Write down the prefixes.

---

### Exercise 4: Host Addresses

For each /64 subnet from Exercise 2, choose a valid host address.

Example format:
```

IoT Subnet: 2001:db8:1234:3::10

```

---

### Exercise 5: Prefix Identification

For the addresses below, identify the /64 prefix they belong to:

1. `2001:db8:10:5::abcd`  
2. `2001:db8:10:ff::20`  
3. `2001:db8:abcd:12::1`  

---

### Exercise 6: Extra

Explain in 2–3 sentences why most IPv6 networks use /64 and not smaller prefix lengths.

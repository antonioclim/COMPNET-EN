
### Exercitii de subnetare IPv6

Rezolvati exercitiile si scrieti raspunsurile in:
`index_ipv6-subnetting_solutions-template.md`

---

### Exercitiul 1: Intelegerea notatiei

Transformati adresele urmatoare in forma scurtata:

1. `2001:0db8:0000:0000:abcd:0000:0000:0001`  
2. `fe80:0000:0000:0000:00ff:0000:0000:1234`  

---

### Exercitiul 2: Prefixe /64 dintr-un /48

Aveti:
```

2001:db8:1234::/48

```

Creati urmatoarele subretele /64:

- subnet pentru servere  
- subnet pentru clientii LAN  
- subnet pentru IoT  
- subnet pentru o legatura router-router

Scrieti prefixele /64 alese.

---

### Exercitiul 3: Subnetare in mai multe /64

Din acelasi prefix /48:
```

2001:db8:abcd::/48

```

Alocati 4 subretele /64 consecutive.  
Scrieti prefixele.

---

### Exercitiul 4: Adrese de host

Alegeti pentru fiecare subnet /64 din exercitiul 2 cate o adresa valida pentru un host.

Exemplu format:
```

Subnet IoT: 2001:db8:1234:3::10

```

---

### Exercitiul 5: Identificarea prefixului

Pentru adresele de mai jos, indicati prefixul /64 caruia ii apartin:

1. `2001:db8:10:5::abcd`  
2. `2001:db8:10:ff::20`  
3. `2001:db8:abcd:12::1`  

---

### Exercitiul 6: Extra

Explicati in 2-3 propozitii de ce majoritatea retelelor IPv6 folosesc /64 si nu dimensiuni mai mici.


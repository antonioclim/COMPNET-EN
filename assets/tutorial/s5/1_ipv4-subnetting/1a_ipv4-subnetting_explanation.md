### Adresare IPv4, adrese speciale, subnetare si VLSM

Aceasta sectiune revede conceptele de adresare IPv4 si pregateste terenul pentru exercitiile de subnetare si VLSM. Cititi cu atentie, apoi treceti la partea practica.

---

### Structura unei adrese IPv4

O adresa IPv4 are 32 de biti si este scrisa in notatie zecimala cu punct, de exemplu:

```

192.168.10.25

```

Baza unei adrese consta in:
- portiunea de retea
- portiunea de host

Lungimea prefixului (notatia CIDR) indica numarul de biti folositi pentru partea de retea:

- /24 inseamna 24 de biti pentru retea  
- /26 inseamna 26 de biti pentru retea  
- /30 inseamna ca mai raman doar 2 biti pentru hosturi  

---

### Intervalele speciale IPv4

Unele intervale IPv4 sunt rezervate pentru utilizari specifice. Cele mai importante:

| Interval | Scop |
|---------|------|
| 0.0.0.0/8 | "Acest host", rute implicite |
| 127.0.0.0/8 | Loopback (localhost) |
| 169.254.0.0/16 | Link-local APIPA, folosit cand DHCP esueaza |
| 192.168.0.0/16 | Privat |
| 10.0.0.0/8 | Privat |
| 172.16.0.0/12 | Privat |
| 224.0.0.0/4 | Multicast |
| 255.255.255.255 | Adresa broadcast limitat |

Intervalele private sunt cele mai utilizate in retele locale.

---

### Adresa de retea, adresa de broadcast, intervalul de hosturi

Orice subnet are:
- **adresa de retea**: toti bitii de host sunt 0  
- **adresa de broadcast**: toti bitii de host sunt 1  
- **intervalul de hosturi**: intre adresa de retea + 1 si broadcast - 1  

Exemplu:

Subnet:
```

192.168.50.0/26

```

Detalii:
- /26 lasa 6 biti pentru hosturi  
- numar total adrese = 64  
- adresa de retea = 192.168.50.0  
- adresa de broadcast = 192.168.50.63  
- hosturi utilizabile = 192.168.50.1 ... 192.168.50.62  

---

### Subnetare fixa (subnetare egala)

Pentru subnetare in bucati egale se imprumuta biti din partea de host.

Exemplu: impartiti 192.168.10.0/24 in 4 subretele egale.

1. 4 subretele necesita 2 biti imprumutati (2^2 = 4)  
2. Prefix nou = /26  
3. Increment subnet = 64  

Subretele:
- 192.168.10.0/26  
- 192.168.10.64/26  
- 192.168.10.128/26  
- 192.168.10.192/26  

---

### VLSM (Variable Length Subnet Masking)

VLSM permite utilizarea unor subretele de dimensiuni diferite. Regula esentiala:

**se aloca intotdeauna subretelele mari primele**

Exemplu:

Cerinte:
- 100 hosturi  
- 50 hosturi  
- 10 hosturi  
- 2 hosturi (link point-to-point)

Bloc de plecare:
```

10.0.0.0/24

```

1. 100 hosturi -> /25 (126 hosturi)  
   subnet: 10.0.0.0/25  

2. 50 hosturi -> /26 (62 hosturi)  
   subnet: 10.0.0.128/26  

3. 10 hosturi -> /28 (14 hosturi)  
   subnet: 10.0.0.192/28  

4. 2 hosturi -> /30 (2 hosturi)  
   subnet: 10.0.0.208/30  

Ordinea evita suprapunerea subretelelor.

---

### Verificare cu un calculator online

Dupa ce calculati o subretea, verificati:
- prefixul
- adresa de retea
- adresa de broadcast
- numarul de hosturi

Puteti folosi orice calculator de subnetare IPv4.
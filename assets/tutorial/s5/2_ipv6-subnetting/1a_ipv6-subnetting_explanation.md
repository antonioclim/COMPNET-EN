### Introducere in IPv6 si subnetare IPv6

Aceasta sectiune prezinta pe scurt conceptele esentiale din IPv6: structura unei adrese, notatia, subnetarea si exemple simple de proiectare.

Scopul este sa intelegeti de ce subnetarea IPv6 este mai simpla decat in IPv4 si de ce, in practica, aproape toate retelele folosesc prefixe /64.

---

### Structura unei adrese IPv6

O adresa IPv6 are 128 de biti. Exemplu:

```

2001:db8:abcd:0012:0000:0000:0000:0001

```

Se foloseste notatia hexazecimala, iar grupurile de zerouri pot fi scurtate:

- eliminarea zerourilor din stanga din fiecare grup
- inlocuirea unui singur sir de grupuri zero cu "::"

Exemplu scurtat:

```

2001:db8:abcd:12::1

```

---

### Structura generala a unui prefix IPv6

O adresa IPv6 este impartita logic in trei parti:

- prefix global (identifica organizatia)  
- subnet ID (identifica subretea din interiorul organizatiei)  
- interface ID (identifica un dispozitiv din subretea)

Model comun:
```

[ 48 biti prefix ] [ 16 biti subnet ] [ 64 biti interface ID ]

```

Aceasta structura sugereaza de ce majoritatea subretelelor sunt /64.

---

### De ce prefix /64 pentru LAN

Regula generala:  
**Fiecare LAN IPv6 foloseste un prefix /64.**

Motivatie:
- protocolul SLAAC functioneaza doar cu /64  
- interoperabilitate maxima  
- simplificarea configuratiei de retea  
- standardizarea suportului pentru echipamente

---

### Exemplu simplu de subnetare IPv6

Avem prefixul:
```

2001:db8:10::/48

```

Un /48 inseamna ca avem 16 biti (2^16 = 65536 subretele) pentru Subnet ID.

Putem crea:

- Subnet 1: `2001:db8:10:1::/64`  
- Subnet 2: `2001:db8:10:2::/64`  
- Subnet 3: `2001:db8:10:3::/64`  
- Subnet 4: `2001:db8:10:ff::/64` (ex. pentru tranzit intre routere)

Fiecare are propriul spatiu de adrese pentru hosturi:
```

2001:db8:10:X::1 ... 2001:db8:10:X:ffff:ffff:ffff:ffff

```

---

### Exemplu de subnetare cu impartirea prefixului

Pornind de la:
```

2001:db8:abcd::/48

```

Dorim 4 subretele mari.

Se pot folosi 2 biti suplimentari pentru Subnet ID -> prefix /50:

- `2001:db8:abcd:0::/50`  
- `2001:db8:abcd:4::/50`  
- `2001:db8:abcd:8::/50`  
- `2001:db8:abcd:c::/50`  

Totusi, pentru majoritatea exercitiilor si aplicatiilor practice vom folosi doar /64.

---

### Comparatie rapida IPv4 vs IPv6

| Caracteristica | IPv4 | IPv6 |
|----------------|------|------|
| Marime adresa | 32 biti | 128 biti |
| Subnetare | complexa, dependenta de cerintele hosturilor | simpla (de obicei /64) |
| Broadcast | Da | Nu |
| Autoconfigurare | Limitata | Extinsa (SLAAC) |
| Scalabilitate | Redusa | Foarte mare |

---

### Ce trebuie sa stiti pentru acest seminar

- Cum arata o adresa IPv6 si cum se scurteaza.  
- Cum se identifica prefixul si subretelele.  
- Cum se creeaza cateva prefixe /64 dintr-un /48.  
- Cum sa alegeti adrese pentru hosturi.

Apoi treceti la exercitii.

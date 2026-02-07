### Introducere in simularea de retea cu Mininet

In aceasta sectiune vom folosi Mininet pentru a crea o topologie de baza formata din doua hosturi si un nod intermediar care se comporta ca un router. Scopul este sa configurati manual adrese IP, rute si sa verificati functionarea retelei folosind comenzi precum `ping`, `traceroute` si `tcpdump`.

---

### De ce Mininet

Mininet este un simulator de retele usor de utilizat, care ruleaza pe un singur calculator si emuleaza:
- hosturi virtuale
- switch-uri
- routere
- legaturi virtuale

Este excelent pentru laboratoare rapide deoarece:
- nu necesita containere sau masini virtuale multiple
- toate hosturile pot rula comenzi reale Linux
- permite vizualizarea traficului prin tcpdump, Wireshark sau comenzi Mininet

---

### Topologia utilizata

Vom crea o topologie simpla:

```

h1 ----- r1 ----- h2

```

Hosturile:
- h1 si h2 vor avea adrese IPv4 si IPv6 proprii
- r1 va avea doua interfete, cate una pentru fiecare subnet

---

### Schemele de adresare

Vom folosi doua subretele IPv4:

- Subnet A (h1 - r1): `10.0.1.0/24`
- Subnet B (h2 - r1): `10.0.2.0/24`

Adresele asignate:

| Host | Interfata | Adresa |
|------|-----------|--------|
| h1 | h1-eth0 | 10.0.1.10 |
| r1 | r1-eth0 | 10.0.1.1 |
| h2 | h2-eth0 | 10.0.2.10 |
| r1 | r1-eth1 | 10.0.2.1 |

Optional, puteti configura si IPv6:

- `2001:db8:10:1::/64` pentru legatura h1–r1  
- `2001:db8:10:2::/64` pentru legatura h2–r1

---

### Obiectivele studentului

- sa lanseze topologia Mininet  
- sa verifice configuratiile IP  
- sa activeze forwardarea IP pe r1  
- sa configureze rute implicite pe h1 si h2  
- sa verifice conectivitatea cu ping  
- sa observe traseul cu traceroute  
- sa captureze pachete cu tcpdump  

Completati toate sarcinile din fisierul `index_mininet-config_tasks.md`.

### Sarcini Mininet: configurare adrese, rute si testare

Aceste exercitii trebuie facute in interiorul CLI-ului Mininet, dupa ce porniti topologia:

```

sudo python3 index_mininet-topology.py

```

---

### 1. Verificarea interfetelor

Rulati:

```

h1 ip a
h2 ip a
r1 ip a

```

Verificati ca adresele IPv4 au fost asignate corect.

---

### 2. Testarea conectivitatii locale

Testati conectivitatea host-router:

```

h1 ping -c 3 10.0.1.1
h2 ping -c 3 10.0.2.1

```

Daca nu functioneaza, notati eroarea.

---

### 3. Activarea rutarii (daca nu este activa)

Verificare:

```

r1 sysctl net.ipv4.ip_forward

```

Daca este 0, activati cu:

```

r1 sysctl -w net.ipv4.ip_forward=1

```

---

### 4. Adaugarea rutelor implicite pe h1 si h2

Pe h1:

```

h1 ip route add default via 10.0.1.1

```

Pe h2:

```

h2 ip route add default via 10.0.2.1

```

---

### 5. Testarea conectivitatii end-to-end

```

h1 ping -c 4 10.0.2.10

```

Daca functioneaza, r1 a rutat pachetele corect.

---

### 6. Testarea traseului cu traceroute

```

h1 traceroute 10.0.2.10

```

Ar trebui sa observati trecerea prin r1.

---

### 7. Capturarea traficului

Porniti o captura pe r1:

```

r1 tcpdump -i r1-eth0 -n

```

Apoi intr-o alta consola Mininet:

```

h1 ping 10.0.2.10

```

Observati pachetele ICMP.

Opriti tcpdump cu Ctrl-C.

---

### 8. Optional: test IPv6 (daca ati activat adresele)

Verificati:

```

h1 ping6 2001:db8:10:2::10

```

---

### Deliverabil

Creati fisierul:

```

mininet_lab_output.txt

```

Acesta trebuie sa contina:
- comenzile folosite  
- output-ul la `ping`, `traceroute` si `tcpdump` (captura partiala)  
- o explicatie de 5-7 propozitii in care descrieti:
  - cum au fost folosite subretelele din partea de subnetare
  - rolul rutei implicite
  - de ce r1 este necesar pentru comunicatie

Acest fisier va fi incarcat ca dovada a finalizarii laboratorului.

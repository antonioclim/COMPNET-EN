### Sarcini: Rutare statică în topologia triunghiului

---

### 1. Verificarea adreselor IP

Rulați în CLI Mininet:

```

r1 ip a
r2 ip a
r3 ip a
h1 ip a
h3 ip a

```

Confirmați că toate interfețele au adresele corecte.

---

### 2. Configurarea rutelor statice

### Pe r1:

```

r1 ip route add 10.0.3.0/30 via 10.0.12.2

```

sau ruta alternativă:

```

r1 ip route add 10.0.3.0/30 via 10.0.13.2

```

### Pe r2:

```

r2 ip route add 10.0.1.0/30 via 10.0.12.1
r2 ip route add 10.0.3.0/30 via 10.0.23.2

```

### Pe r3:

```

r3 ip route add 10.0.1.0/30 via 10.0.13.1
r3 ip route add 10.0.12.0/30 via 10.0.23.1

```

---

### 3. Testarea conectivității

```

h1 ping -c 4 10.0.3.2

```

Dacă merge, rutarea este funcțională.

---

### 4. Observarea rutei folosite

```

h1 traceroute 10.0.3.2

```

Note:
- Dacă vedeți r1 → r2 → r3, rutele sunt setate pe r1 via r2.
- Dacă vedeți r1 → r3, traficul merge direct.

---

### 5. Exercițiu: Schimbați manual ruta

1. Ștergeți ruta curentă:

```

r1 ip route del 10.0.3.0/30

```

2. Adăugați ruta alternativă prin r3:

```

r1 ip route add 10.0.3.0/30 via 10.0.13.2

```

3. Comparați:

```

h1 traceroute 10.0.3.2

```

---

### 6. *Optional*: Captură pachete pe routere

Exemplu:

```

r2 tcpdump -i r2-eth1 -n

```

---

### Deliverable

Creați un fișier:

```

triangle_routing_output.txt

```

Acesta trebuie să includă:

- Output `ip route` de pe fiecare router  
- Output `ping` și `traceroute`  
- Un fragment scurt de captură `tcpdump`  
- Un paragraf de 6–8 propoziții în care explicați:  
  - cum funcționează rutarea statică  
  - cum ați determinat calea traficului  
  - ce se întâmplă când modificați rutele  
  - de ce traceroute arată traseul în ordinea observată

Acest fișier va fi încărcat ca dovadă a finalizării exercițiilor.


### Trafic de aplicatie prin SDN: servere si clienti Python

In stage-urile anterioare am:

- construit o topologie SDN simpla (h1, h2, h3 conectate la s1)
- folosit un controller Os-ken care permite traficul intre h1 si h2 si blocheaza traficul catre h3
- testat comportamentul cu `ping`

In acest stage vom trece la **trafic de aplicatie**:

- un server TCP Python rulat pe h2
- un client TCP Python rulat pe h1
- un server UDP Python rulat pe h3
- un client UDP Python rulat pe h1

Vom observa:

- conexiune TCP reusita intre h1 si h2 (permisa de controller)
- conexiune TCP esuata intre h1 si h3 (blocata de controller)
- dupa modificarea controllerului:
  - trafic UDP permisa intre h1 si h3
  - trafic TCP spre h3 in continuare blocat

---

### Porturi si adrese

Pentru claritate vom folosi:

- server TCP pe h2: port 5000
- client TCP pe h1: conecteaza la `10.0.10.2:5000`
- server UDP pe h3: port 6000
- client UDP pe h1: trimite catre `10.0.10.3:6000`

Topologia este aceeasi ca in stage 2:

```

h1 ---- s1 ---- h2
|
+---- h3

```

Adrese IP:

- h1: 10.0.10.1/24
- h2: 10.0.10.2/24
- h3: 10.0.10.3/24

---

### Obiective

Studentul trebuie sa:

- porneasca serverul TCP pe h2 si sa testeze clientul TCP de pe h1 (merge)
- incerce conexiune TCP de la h1 la h3 (nu merge)
- porneasca serverul UDP pe h3
- modifice controllerul Os-ken astfel incat UDP de la h1 la h3 sa fie permis
- testeze clientul UDP si sa confirme comportamentul diferit TCP vs UDP
- salveze output-ul comenzilor intr-un fisier de tip log

Comenzile si pasii concreti sunt in `index_sdn_app-traffic_tasks.md`.

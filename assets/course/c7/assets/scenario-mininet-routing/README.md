### Scenariu: Mininet (triunghi de rutere) + defecte si rutare asimetrica

#### Cerinte
- Linux
- Mininet instalat
- rulare ca root (sudo)

#### Topologie
- 3 rutere: r1, r2, r3 (triunghi complet: r1-r2, r2-r3, r1-r3)
- 3 LAN-uri:
  - h1 in spatele lui r1 (10.1.0.0/24)
  - h2 in spatele lui r2 (10.2.0.0/24)
  - h3 in spatele lui r3 (10.3.0.0/24)

Link-uri intre rutere:
- r1-r2: 10.12.0.0/24
- r1-r3: 10.13.0.0/24
- r2-r3: 10.23.0.0/24

#### Scenariul 1: link-down (merge prin ruta alternativa)
Rulare:
- sudo bash run-link-down.sh

Ce se intampla:
- setam rute statice astfel incat traficul intre LAN-uri sa poata ocoli un link
- apoi coboram link-ul r1-r2
- ping h1 -> h2 ar trebui sa mearga in continuare prin r3

Comenzi utile in Mininet CLI:
- r1 ip route
- r2 ip route
- r3 ip route
- r1 ip link
- h1 ping -c 2 10.2.0.2
- h1 traceroute -n 10.2.0.2  (daca traceroute exista)

#### Scenariul 2: rutare asimetrica (ruta doar intr-un sens)
Rulare:
- sudo bash run-asymmetric.sh

Ce se intampla:
- r1 are ruta catre 10.2.0.0/24 via r2
- r2 NU are ruta de intoarcere catre 10.1.0.0/24
- h1 -> h2 poate ajunge (request), dar raspunsul se pierde (no route back)

Comenzi utile:
- h1 ping -c 2 10.2.0.2
- r2 ip route
- r2 ip route get 10.1.0.2

#### Observatie importanta
Asta e fix motivul pentru care rutarea poate fi asimetrica si de ce “merge intr-un sens” e un simptom clasic de rute lipsa pe retur.

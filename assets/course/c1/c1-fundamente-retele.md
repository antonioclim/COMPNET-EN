### Rețele de calculatoare
### Fundamente: concepte, componente, clasificări

---

### Descriere generală
- Utilitate
- Obiective
- Structura cursului
- Cerințe și punctaj
- Resurse și instrumente

---

### Obiective
La finalul cursului, studentul poate:
- Defini o rețea de calculatoare
- Clasifica rețelele după dimensiune și topologie
- Explica rolul mediilor de transmisie și al dispozitivelor de rețea
- Înțelege noțiunile de protocol, stivă de protocoale și încapsulare
- Urmări conceptual traseul unui mesaj în rețea

---

### Ce este o rețea de calculatoare?
- Set de sisteme de calcul interconectate
- Comunicare între sisteme:
  - fizic: dispozitive + medii
  - logic: protocoale

[FIG] c1-assets/fig-rețea-vs-sistem.png

---

### De ce sunt utile rețelele?
- Partajarea resurselor
- Acces la resurse la distanță
- Comunicarea la distanță
- Coordonarea acțiunilor
- Scalarea capacității de procesare și stocare

---

### Standarde în rețele
- IEEE (ex: 802.3, 802.11)
- RFC-uri (IETF)
- Standarde de programare (Berkeley Sockets)

---

### Dimensiunea unei rețele
- LAN (Local Area Network)
  - cameră, clădire, campus
- WAN (Wide Area Network)
  - regiune, țară, continent
- Internet
  - interconectare globală de rețele WAN și LAN

[FIG] c1-assets/fig-lan-wan-internet.png

---

### LAN: caracteristici
- Dimensiuni reduse
- Întârzieri mici
- Erori puține
- Tehnologii uzuale: Ethernet, Wi-Fi

---

### WAN: caracteristici
- Interconectează mai multe LAN-uri
- Nodurile finale sunt în subrețele distincte
- Transmiterea se face prin rutarea pachetelor

---

### Topologia unei rețele
- Modalitatea de conectare a nodurilor
- Topologie fizică vs topologie logică
- Punct-la-punct vs multipunct
- Simetrică vs asimetrică

---

### Topologii uzuale
[FIG] c1-assets/fig-topologii.png

---

### Clasificare după topologie
|               | Simetrică                   | Asimetrică                    |
|--------------|-----------------------------|-------------------------------|
| Punct la punct | inel, plasă total conectată | stea, plasă parțial, arbore   |
| Multipunct     | magistrală, inel            | satelit                       |

---

### Medii de transmisie
- Ghidate:
  - cupru (coaxial, torsadat)
  - fibră optică
- Neghidate:
  - wireless (radio)

[FIG] c1-assets/fig-medii.png

---

### Parametri ai transmisiei
- bandwidth: cantitatea de date pe secundă
- latency: întârzierea
- jitter: variația întârzierii
- loss: pierderi de pachete

[SCENARIO] c1-assets/scenario-ping-traceroute/

---

### Mecanisme de transmisie
- Difuzare (broadcast)
- Punct-la-punct

---

### Tipuri de comutare
- Comutare de circuit
- Comutare de pachete

[FIG] c1-assets/fig-circuit-vs-pachete.png

---

### Dispozitive de comunicație
- NIC
- repetor
- hub
- switch
- router

[FIG] c1-assets/fig-dispozitive.png

---

### Hub vs switch vs router
- hub: retransmite către toate nodurile
- switch: transmite selectiv
- router: conectează rețele

[FIG] c1-assets/fig-hub-switch-router.png

---

### Modele logice de comunicație
- Client-server
- Peer-to-peer
Notă: la nivel de programare, comunicarea este întotdeauna client-server

---

### Protocoale de comunicație
- Protocol = reguli + sintaxă + comportament
- Implementare hardware sau software
- Protocoalele se compun

---

### Stive de protocoale
- Separarea pe straturi
- Fiecare strat oferă servicii
- Fiecare strat are unitatea sa de transfer

---

### Încapsulare
- Datele sunt împachetate succesiv
- Fiecare nivel adaugă antet
- Nivelurile inferioare nu interpretează payload-ul

[FIG] c1-assets/fig-încapsulare.png

---

### Mini-analiză de trafic
- Ce este un pachet real
- Ce vedem într-un ping
- Ce vedem într-o interogare DNS

[SCENARIO] c1-assets/scenario-capture-basics/

---

### Recapitulare
- Clasificări (LAN, WAN, Internet)
- Topologii și medii
- Dispozitive de rețea
- Protocol, stivă, încapsulare

---

### Pregătire pentru Curs 2
- Modele arhitecturale: OSI și TCP/IP
- Formalizarea straturilor și responsabilităților

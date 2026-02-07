### Introducere in programarea aplicatiilor cu comunicare in retea

---

### Obiective
La finalul cursului, studentul poate:
- Explica diferentele: aplicatie peste HTTP vs programare pe socket (transport)
- Folosi socket-uri TCP si UDP (client + server)
- Intelege probleme tipice: framing, concurenta, timeouts, sesiuni
- Intelege ce inseamna RAW sockets si cand are sens sa le folosesti

---

### Consideratii generale (design de protocol)
- Unitati de transfer: format, marime, reprezentare (bytes vs text)
- Protocoale de comunicatie: comenzi, raspunsuri, erori
- Unidirectional vs bidirectional
- Cu stare vs fara stare
- Semnalarea erorilor (coduri, mesaje, retry)
- Extensibilitate (versiuni, campuri optionale)
- Securitate (autentificare, criptare, integritate)

---

### Abstractii peste nivelul aplicatie
- Folosim un protocol de aplicatie existent ca “transport”
- Ignoram straturile de sub aplicatie
- Exemplu: HTTP pentru acces la obiecte la distanta (REST), RPC

[FIG] c3-assets/fig-app-over-http.png

---

### Programarea la nivel transport
- Folosim TCP sau UDP ca “canal”
- Implementam servere care respecta un protocol de aplicatie (ex: HTTP minimal)
- Sau definim protocoale custom

La baza: Berkeley sockets

---

### Ce este un socket
- O structura/obiect care reprezinta un capat de comunicatie
- In Unix: seamana cu un fisier (descriptor)
- Identificare prin: IP + port + protocol (TCP/UDP)

---

### Tipuri de socket-uri
- TCP (stream sockets)
- UDP (datagram sockets)
- RAW sockets (sub nivelul transport)

---

### TCP: caracteristici
- Orientat pe conexiune
- Flux de bytes (nu “mesaje”)
- Livrare in ordine (in mod normal)
- Control flux / retransmisii (la nivel TCP)
- Problema aplicatiei: delimitarea mesajelor (framing)

---

### Fluxul unui server TCP (accept loop)
[FIG] c3-assets/fig-tcp-server-flow.png

---

### TCP: problema 1 - framing (stream != message)
- recv(1024) nu garanteaza ca primesti “un mesaj complet”
- Solutii:
  - delimitator (ex: newline)
  - lungime prefixata (length prefix)
  - format de tip TLV

[SCENARIO] c3-assets/scenario-tcp-framing/

---

### TCP: problema 2 - concurenta
- Un server simplu blocheaza pe un client
- Solutii uzuale:
  - thread per client
  - process per client
  - async / event loop (select, epoll)

[FIG] c3-assets/fig-tcp-concurrency.png

[SCENARIO] c3-assets/scenario-tcp-multiclient/

---

### TCP: timeouts si inchideri
- Timeouts pentru connect/recv
- Clientul poate inchide conexiunea (recv -> 0 bytes)
- Tratare robusta a erorilor

---

### UDP: caracteristici
- Fara conexiune
- Un mesaj = o datagrama (limite de marime)
- Nu garanteaza livrare / ordine / unicitate
- Serverul nu “accepta”, doar recvfrom/sendto

---

### Fluxul unui server UDP
[FIG] c3-assets/fig-udp-server-flow.png

---

### UDP: probleme specifice
- “Sesiuni” la nivel aplicatie (identificare client)
- Confirmari (ACK) si retransmisii la nivel aplicatie
- Comenzi multi-pas (stare)

[SCENARIO] c3-assets/scenario-udp-session-ack/

---

### RAW sockets (sub nivel transport)
- Trimiti/primesti pachete “mai jos” decat TCP/UDP
- Necesita privilegii (root/admin)
- Folosit pentru instrumente (diagnostic), cercetare, implementari custom

[FIG] c3-assets/fig-raw-layering.png

---

### Scapy (constructie de pachete)
- Permite construire si trimitere pachete L3/L2
- Bun pentru invatare: IP/ICMP, DNS simplu, etc.

[SCENARIO] c3-assets/scenario-scapy-icmp/

---

### Recapitulare
- HTTP ca abstractie peste aplicatie vs socket direct
- TCP: stream, framing, concurenta
- UDP: datagrame, sesiune/ACK in aplicatie
- RAW/scapy: sub transport, cu privilegii

---

### Pregatire pentru urmatorul curs
- In Curs 4: nivel fizic + legatura de date
- Vom lega: cadre, MAC, switch, coliziuni/CSMA (conceptual)

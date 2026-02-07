### Scenariu: TCP vs UDP si mapare pe straturi (OSI / TCP-IP)

#### Obiectiv
- Generezi trafic TCP si UDP local
- Il observi in Wireshark sau tcpdump
- Il mapezi conceptual pe straturi:
  - Aplicatie: mesajul tau
  - Transport: TCP sau UDP
  - Rețea: IP (observabil in captură)
  - Legătură / Fizic: nu intram in detalii aici

#### Cerinte
- Python 3
- Wireshark sau tcpdump

Porturi folosite:
- TCP: 9000
- UDP: 9001

---

### Pasul 1: porneste serverele

Terminal 1:
- python3 tcp-server.py

Terminal 2:
- python3 udp-server.py

---

### Pasul 2: porneste captura

#### Varianta A: tcpdump (Linux/macOS)
Intr-un alt terminal:
- sudo tcpdump -i any -n '(tcp port 9000 or udp port 9001)'

#### Varianta B: Wireshark (orice OS)
Display filter:
- tcp.port == 9000 or udp.port == 9001

---

### Pasul 3: genereaza trafic

Terminal 3:
- python3 tcp-client.py

Terminal 4:
- python3 udp-client.py

---

### Ce ar trebui sa observi
TCP:
- conexiune (SYN, SYN-ACK, ACK)
- apoi date + ACK-uri

UDP:
- nu exista handshake
- vezi datagrame trimise direct

---

### Intrebari rapide
1) La TCP, cate pachete apar inainte sa trimiti efectiv mesajul?
2) La UDP, ce lipseste fata de TCP?
3) In captură, unde vezi:
   - IP (stratul Rețea)?
   - TCP/UDP (stratul Transport)?
   - payload-ul aplicatiei?

---

### Mapare pe straturi (rezumat)
- Aplicație: string-ul trimis de client
- Transport: TCP sau UDP
- Rețea: IP (header IP in captură)
- Acces la rețea: depinde de adaptor (Ethernet/Wi-Fi), nu insistam aici

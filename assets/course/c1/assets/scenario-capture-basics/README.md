### Scenariu: mini-analiza de trafic (ping + DNS + HTTP local)

#### Obiectiv
- Vezi pachete reale: ICMP (ping), DNS query, un request HTTP simplu.
- Nu intram pe straturi OSI/TCPIP inca, doar observatie.

#### Cerinte
Alege una:
- Wireshark (GUI)
- tcpdump (CLI, Linux/macOS)
- pe Windows: Wireshark recomandat

---

### Varianta A: tcpdump (Linux/macOS)

#### 1) Porneste un server HTTP local
Intr-un terminal, in folderul scenariului:
- python3 start-http-server.py

Serverul porneste pe http://127.0.0.1:8000

#### 2) Captura DNS + ICMP + HTTP
In alt terminal:
- sudo tcpdump -i any -n '(icmp or udp port 53 or tcp port 8000)'

#### 3) Genereaza trafic
- ping -c 4 1.1.1.1
- python3 dns-query.py
- deschide in browser: http://127.0.0.1:8000

Ce ar trebui sa vezi:
- ICMP echo request/reply
- UDP 53 (DNS)
- TCP catre portul 8000 (HTTP local)

---

### Varianta B: Wireshark (orice OS)

#### 1) Start captura pe interfata activa (Wi-Fi/Ethernet)
Filtru de captura sau display filter:
- icmp or dns or tcp.port == 8000

#### 2) Genereaza trafic
- ping catre 1.1.1.1
- ruleaza dns-query.py
- deschide http://127.0.0.1:8000

#### Intrebari rapide
- Cate pachete vezi pentru DNS?
- Ping genereaza cate request/reply?
- De ce pentru HTTP apar mai multe pachete decat "un singur mesaj"?

### Scenariu: ping si traceroute (latency vs traseu)

#### Obiectiv
- Observi latency (ping) si traseul (hop-uri) pana la o destinatie.
- Discuti pe scurt despre: latency, jitter, loss si hop count.

#### Recomandare
Ruleaza in retea reala (Wi-Fi sau cablu). Ai nevoie de access la terminal.

#### Pasul 1: identifica gateway-ul local
Linux/macOS:
- ip route | grep default

Windows:
- ipconfig

Noteaza IP-ul gateway-ului (de obicei 192.168.x.1 sau 10.x.x.1).

#### Pasul 2: ping catre gateway (local)
Linux/macOS:
- ping -c 20 <GATEWAY_IP>

Windows:
- ping -n 20 <GATEWAY_IP>

Observa:
- min/avg/max (sau aproximari)
- pierderi (packet loss)

#### Pasul 3: ping catre o destinatie externa
Exemple:
- 1.1.1.1
- 8.8.8.8

Linux/macOS:
- ping -c 20 1.1.1.1

Windows:
- ping -n 20 1.1.1.1

Discutie:
- de ce creste latency?
- ce inseamna jitter?

#### Pasul 4: traceroute (traseu)
Linux:
- traceroute 1.1.1.1

macOS:
- traceroute 1.1.1.1

Windows:
- tracert 1.1.1.1

Observa:
- cate hop-uri?
- unde apar timeouts?
- diferenta intre hop-uri locale (ISP) si distante

#### Intrebari rapide (2-3 minute)
- De ce ping foloseste ICMP si nu TCP?
- De ce unele routere nu raspund la traceroute?

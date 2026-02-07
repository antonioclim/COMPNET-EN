### Scenario: UDP vs TCP sub pierderi folosind Mininet (TCLink)

### Obiectiv
- UDP: unele mesaje se pierd (best-effort)
- TCP: aplicatia vede stream complet (retransmisii transparente)

### Cerinte
- Linux
- Mininet (sudo)
- python3

### Topologie
h1 --- s1 --- h2
Link-ul h1-s1 si/sau s1-h2 are loss artificial (ex: 20%)

### Cum rulezi
- sudo ./run.sh

Scriptul:
- porneste Mininet cu topologia si loss
- ruleaza UDP receiver pe h2, UDP sender pe h1
- ruleaza TCP receiver pe h2, TCP sender pe h1
- afiseaza rezultatele in terminal

### Ce observi
- UDP: receiver raporteaza mesaje lipsa
- TCP: receiver raporteaza numarul complet de linii

### Parametri utili
In topo.py poti modifica:
- loss (ex: 5, 10, 20)
- delay (optional)

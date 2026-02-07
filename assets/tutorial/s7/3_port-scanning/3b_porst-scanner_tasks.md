### Sarcini – Mini port-scanner TCP (Stage 4)

In acest stage veti implementa si testa un port-scanner simplu,
bazat pe conexiuni TCP (connect scan).

---

### 1. Completati functiile scan_port si scan_range

In `port_scanner.py`:

1. In `scan_port`:
   - folositi `socket.socket(AF_INET, SOCK_STREAM)`
   - setati un timeout scurt (ex: 0.5s)
   - incercati `connect((host, port))`
   - tratati exceptiile:
     - `ConnectionRefusedError` -> `"CLOSED"`
     - `socket.timeout` -> `"FILTERED"`
     - orice alt `Exception` -> puteti considera `"CLOSED"` sau `"FILTERED"`, dar scrieti decizia in comentariu

2. In `scan_range`:
   - iterati de la `start_port` la `end_port` (inclusiv)
   - pentru fiecare port:
     - apelati `scan_port(host, port)`
     - afisati pe ecran linia `PORT <port> <STATE>`
     - salvati aceeasi linie in lista `results`

La final, `scan_range` returneaza lista `results`.

---

### 2. Rulati un test local de baza

Pe masina locala sau intr-un host Mininet, rulati:

```bash
python3 port_scanner.py 127.0.0.1 1 1024
```

Observatii:

- ar trebui sa vedeti cateva porturi `OPEN` (ex: 22, 80, 443, in functie de ce servicii rulati)
- multe porturi vor fi `CLOSED` sau `FILTERED`
- rezultatele vor fi salvate in `scan_results.txt`

Daca scanarea dureaza prea mult, incercati un interval mai mic (ex: 1–200).

---

### 3. Test in mediul de laborator (Mininet)

Daca folositi Mininet cu topologiile din seminariile anterioare, puteti testa scanner-ul intre hosturi:

1. In CLI Mininet, pe h2, porniti un server TCP (de exemplu `tcp_server.py`):

```bash
h2 python3 tcp_server.py 5000
```

2. Pe h1, rulati scanner-ul:

```bash
h1 python3 port_scanner.py 10.0.10.2 4900 5100
```

3. Verificati ca portul 5000 apare ca `OPEN`, iar porturile din jur sunt `CLOSED` sau `FILTERED`.

---

### 4. Analiza rezultatelor

Deschideti fisierul `scan_results.txt`. Observati:

- cate porturi sunt `OPEN`?  
- se potrivesc cu serviciile pe care stiti ca le aveti pornite?  
- vedeti porturi `FILTERED`? De ce ar putea aparea ca filtrate (hint: firewall, lipsa raspunsului la SYN, etc.)?  

---

### 5. Extensie optionala (pentru cei mai rapizi)

Daca mai aveti timp, incercati:

- sa adaugati un argument optional `--fast` care scaneaza doar un set de porturi comune (ex: 22, 80, 443, 8080, 3306, etc.)
- sa afisati la final un mic rezumat:
  - `N` porturi OPEN
  - `M` porturi CLOSED
  - `K` porturi FILTERED

Puteti face asta numarand starile in `scan_range`.

---

### 6. Intrebari de reflexie (de scris in scan_results.txt sau intr-un fisier separat scan_log.txt)

Raspundeti scurt:

1. Care este diferenta dintre un TCP connect scan si un SYN scan (la nivel conceptul, fara implementare)?  
2. De ce un scan UDP este in general mai greu de interpretat decat un scan TCP?  
3. De ce un firewall poate face porturile sa apara ca `FILTERED` in loc de `CLOSED`?  

---

### Deliverable Stage 4

Predati:

- `port_scanner.py` complet (cu `scan_port` si `scan_range` implementate)
- `scan_results.txt` sau `scan_log.txt` care sa contina:
  - output-ul scanarii (cel putin 50 de porturi scanate)
  - raspunsurile la intrebarile de reflexie
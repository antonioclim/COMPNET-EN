### Sarcini – Detectarea unui port scan (Stage 5)

In acest stage veti folosi detect_scan.py pentru a detecta un port scan
generat de port_scanner.py.

Scenariul ideal este in Mininet, dar se poate adapta si pe o singura masina.

---

### 1. Pregatirea mediului (Mininet, recomandat)

1. Porniti o topologie simpla (de exemplu cea cu h1 si h2 din seminariile anterioare).
2. In CLI Mininet, asigurati-va ca:
   - h1 are o adresa IP (ex: 10.0.10.1)
   - h2 are o adresa IP (ex: 10.0.10.2)

Vom considera ca:
- **h1** va rula port_scanner.py (atacator)
- **h2** va rula detect_scan.py (victima / server)

---

### 2. Rulati detect_scan pe h2

In CLI Mininet:

```bash
h2 sudo python3 detect_scan.py h2-eth0
````

Ar trebui sa vedeti mesajele:

* `[INFO] Pornim detect_scan ...`
* configuratia ferestrei si a pragului

Lasati scriptul sa ruleze.

---

### 3. Rulati port_scanner pe h1

Intr-un alt terminal, in CLI Mininet:

```bash
h1 python3 port_scanner.py 10.0.10.2 1 200
```

sau un interval mai mic daca este prea lent, de exemplu:

```bash
h1 python3 port_scanner.py 10.0.10.2 20 120
```

Pe masura ce scannerul incearca sa se conecteze la porturi multiple de pe h2:

* detect_scan ar trebui sa vada multe pachete TCP SYN dinspre IP-ul lui h1
* daca intr-o fereastra de 5 secunde sunt atinse >= 10 porturi diferite,
  scriptul va afisa:

```text
[ALERT] Posibil port scan de la 10.0.10.1: 10 porturi diferite in ultimele 5 secunde
```

(Adresa IP si numarul porturilor pot varia.)

---

### 4. Ajustati sensibilitatea detectorului

In `detect_scan.py` aveti variabile:

```python
WINDOW_SECONDS = 5
PORT_THRESHOLD = 10
```

Task:

1. Modificati `WINDOW_SECONDS` la 2 secunde si `PORT_THRESHOLD` la 5.
2. Rulati din nou:

   * detect_scan pe h2
   * port_scanner pe h1 (pe un interval de porturi similar)

Observati:

* apare alerta mai repede?
* riscati mai multe „false positive”?

Scrieti observatiile in fisierul de log (vezi deliverable).

---

### 5. Optional: test fara port_scanner

Incercati sa generati trafic „normal” (fara port_scanner):

* un ping h1 -> h2
* un client TCP catre un singur port (de ex. `tcp_client.py` la port 5000)
* cateva conexiuni repetate la acelasi port

Intrebari:

* Se declanseaza alerta si in acest caz?
* Care este diferenta ca pattern fata de un port-scan (multi-port) clasic?

---

### 6. Deliverable Stage 5

Creati un fisier:

```text
scan_detection.txt
```

care sa contina:

1. Un fragment de output din `detect_scan.py` in timpul rularii port_scanner-ului,
   incluzand cel putin o linie `[ALERT] ...`.
2. Un fragment de output din `detect_scan.py` in timpul traficului „normal”
   (fara sa ruleze port_scanner-ul).
3. Un mic rezumat (6–8 propozitii) in care explicati:

   * ce conditie foloseste scriptul pentru a decide ca are loc un port scan
   * cum influenteaza `WINDOW_SECONDS` si `PORT_THRESHOLD` sensibilitatea
   * ce tip de fals pozitiv ati putea avea cu un astfel de detector simplu
   * cum ar putea fi imbunatatit (ex: diferentiere dupa tipul de porturi,
     contabilizare separata pentru TCP/UDP, folosirea unui sliding window real etc.)

---

### Legatura cu Stage 6 (mini_ids.py)

In Stage 6 (tema finala) veti:

* extinde ideile de aici intr-un script `mini_ids.py`
* combina filtrarea de pachete cu detectarea de pattern-uri (scan, flood, etc.)
* loga evenimente de tip "ALERT" intr-un fisier dedicat

Pentru moment, asigurati-va ca:

* detect_scan functioneaza
* puteti declansa in mod controlat un port scan folosind port_scanner.py
* ati salvat log-urile in `scan_detection.txt`


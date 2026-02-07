#### Seminar 13 – Stage 2

## Sarcini – Scanare cu Nmap + Implementarea scanner-ului Python

Creați fișierul:
`stage2_scan_results.txt`

---

## 1. Descoperirea hosturilor active

Rulați:

```bash
sudo nmap -sn 172.20.0.0/24
```

În `stage2_scan_results.txt`:

* copiați IP-urile hosturilor active
* notați timpul de execuție

---

## 2. Scanarea porturilor pentru fiecare host

Pentru fiecare IP (10, 11, 12):

```bash
nmap -sV -p- 172.20.0.X
```

În fișier:

* copiați lista porturilor deschise
* identificați serverele găsite la fiecare (Apache/Tomcat/FTP etc.)
* notați versiunile detectate

---

## 3. Rulați scanner-ul Python

Executați:

```bash
python3 simple_scanner.py
```

Apoi:

* comparați rezultatele cu cele din nmap
* explicați diferențele în 3–5 propoziții

---

## 4. Sarcină tehnică (opțional bonus)

Modificați scannerul astfel încât să:

* accepte parametrul IP din linia de comandă:

```
python3 simple_scanner.py 172.20.0.11
```

* accepte un interval diferit de porturi

Exemplu:

```
python3 simple_scanner.py 172.20.0.11 20 200
```

---

## 5. Întrebare de reflecție

Explicați diferența dintre:

* port **closed**
* port **filtered**
* port **open**

și de ce doar primul și ultimul apar corect în scannerul Python simplu.


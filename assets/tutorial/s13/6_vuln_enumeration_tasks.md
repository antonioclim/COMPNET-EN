#### Sarcini – Stage 3: Enumerarea vulnerabilităților

Creați fișierul:
`stage3_vuln_enumeration_report.txt`

---

## 1. Rulează scanarea NSE

Pentru fiecare host:

```bash
nmap -sV --script vuln -p- 172.20.0.X
```

În fișier:

* copiați minim **3 vulnerabilități** detectate
* pentru fiecare indicați:

  * portul
  * numele scriptului NSE
  * descriere scurtă (1–2 propoziții)

---

## 2. Rulează nikto pe DVWA și WebGoat

Ex:

```bash
nikto -h http://172.20.0.10:8888
nikto -h http://172.20.0.11:8080
```

În fișier:

* copiați **5 rezultate relevante** (nu toate, doar cele importante)
* explicați ce înseamnă fiecare

---

## 3. Fingerprinting manual cu curl

Executați:

```bash
curl -I http://172.20.0.10:8888
curl -I http://172.20.0.11:8080
```

În fișier:

* notați versiunile serverelor detectate
* explicați de ce versiuni vechi de PHP/Apache sunt riscante

---

## 4. Banner grabbing pentru FTP vulnerabil

```
nc 172.20.0.12 2121
```

În fișier:

* copiați bannerul complet
* identificați CVE-ul aferent (CVE-2011-2523)

---

## 5. Întrebare de reflecție

**De ce este important să combinăm instrumentele automate (nmap, nikto) cu analiza manuală (curl, nc)?**
Răspuns de 5–10 rânduri.

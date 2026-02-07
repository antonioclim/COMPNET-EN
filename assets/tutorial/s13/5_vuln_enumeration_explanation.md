#### Seminar 13 – Stage 3

## Enumerarea vulnerabilităților: tehnici, unelte, interpretare rezultate

În acest stage vom trece dincolo de „porturi deschise” și vom învăța cum să identificăm vulnerabilități reale folosind:

* **nmap NSE (scripting engine)**
* **nikto** (web vulnerability scanner)
* **fingerprinting manual cu curl**
* examinarea banerelor de la aplicații vulnerabile (FTP, HTTP)

Scopul este să înțelegem *ce tipuri de vulnerabilități sunt prezente* în serviciile descoperite în Stage 2 și *cum le detectăm în mod profesionist*.

---

## 1. Enumerarea vulnerabilităților cu Nmap NSE

### Ce este NSE?

Nmap Scripting Engine (NSE) permite rularea de scripturi gata făcute pentru:

* SSL/TLS checks
* vulnerabilități FTP, SSH, HTTP
* misconfigurations
* brute-force
* INFO disclosure
* CVE-uri specifice

Pentru laborator vom folosi:

```
nmap --script vuln -p- 172.20.0.X
```

Acest script rulează toate scripturile NSE marcate ca *vuln*.

### Exemple de scripturi utile:

* `ftp-vsftpd-backdoor`
* `http-enum`
* `http-sql-injection`
* `http-php-version`
* `http-methods`
* `banner`

### Exemplu concret (pentru vsftpd vulnerabil):

```bash
nmap -sV --script ftp-vsftpd-backdoor -p 2121 172.20.0.12
```

Acest script confirmă existența backdoor-ului celebru din `vsftpd 2.3.4`.

---

## 2. Enumerarea vulnerabilităților web – Nikto

Nikto este un scanner foarte util pentru:

* path-uri vulnerabile
* versiuni învechite
* fișiere periculoase
* configurări nesigure

Rulare minimă:

```bash
nikto -h http://172.20.0.10:8888
```

sau pentru WebGoat:

```bash
nikto -h http://172.20.0.11:8080
```

Notă: WebGoat întotdeauna raportează vulnerabilități (este intenționat construit așa).

---

## 3. Fingerprinting manual cu curl

Unele vulnerabilități se văd doar manual:

### 3.1. Identificarea serverului

```bash
curl -I http://172.20.0.10:8888/
```

Observați:

* `Server: Apache/X.Y.Z`
* `X-Powered-By: PHP/5.x`

VERSIUNILE vechi sunt indicatori de vulnerabilități.

### 3.2. Descoperirea metodelor HTTP

```bash
curl -X OPTIONS -I http://172.20.0.10:8888/
```

Dacă răspunsul include:

```
Allow: GET, POST, PUT, DELETE
```

→ potențiale probleme dacă serverul nu ar trebui să suporte metode periculoase.

---

## 4. Analizarea bannerelor FTP

Conectați-vă:

```bash
nc 172.20.0.12 2121
```

Bannerul:

```
220 (vsFTPd 2.3.4)
```

Identificare problemă:

* `2.3.4` este o versiune cu backdoor intenționat (CVE-2011-2523)
* o simplă căutare online confirmă vulnerabilitatea

---

## 5. Rezultate așteptate în acest stage

După finalizarea enumerării, studenții trebuie să fi identificat clar:

* cel puțin **2 vulnerabilități web** (ex: SQL injection în DVWA, XSS, header leakage, PHP outdated)
* cel puțin **1 vulnerabilitate FTP** (vsftpd backdoor)
* cel puțin **1 vulnerabilitate generală** găsită cu nmap/nse

Aceste rezultate vor fi folosite în Stage 4 pentru **exploatare controlată**.

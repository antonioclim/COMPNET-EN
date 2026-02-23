#### Seminar 13 – Stage 3

## Vulnerability Enumeration: Techniques, Tools and Interpreting Results

This stage moves beyond "open ports" to identify real vulnerabilities using:

* **nmap NSE (Scripting Engine)**
* **nikto** (web vulnerability scanner)
* **manual fingerprinting with curl**
* examining banners from vulnerable applications (FTP, HTTP)

The objective is to determine *what types of vulnerabilities are present* in the services discovered in Stage 2 and *how to detect them professionally*.

---

## 1. Vulnerability Enumeration with Nmap NSE

### What is NSE?

Nmap Scripting Engine (NSE) runs ready-made scripts for:

* SSL/TLS checks
* FTP, SSH and HTTP vulnerabilities
* misconfigurations
* brute-force attacks
* information disclosure
* specific CVEs

For this lab we use:

```
nmap --script vuln -p- 172.20.0.X
```

This command runs every NSE script tagged as *vuln*.

### Useful script examples:

* `ftp-vsftpd-backdoor`
* `http-enum`
* `http-sql-injection`
* `http-php-version`
* `http-methods`
* `banner`

### Concrete example (vulnerable vsftpd):

```bash
nmap -sV --script ftp-vsftpd-backdoor -p 2121 172.20.0.12
```

This script confirms the presence of the notorious backdoor in `vsftpd 2.3.4`.

---

## 2. Web Vulnerability Enumeration – Nikto

Nikto is a highly useful scanner for:

* vulnerable paths
* outdated versions
* dangerous files
* insecure configurations

Minimal execution:

```bash
nikto -h http://172.20.0.10:8888
```

or for WebGoat:

```bash
nikto -h http://172.20.0.11:8080
```

Note: WebGoat always reports vulnerabilities (it is intentionally built that way).

---

## 3. Manual Fingerprinting with curl

Some vulnerabilities are only visible through manual inspection:

### 3.1. Server identification

```bash
curl -I http://172.20.0.10:8888/
```

Observe:

* `Server: Apache/X.Y.Z`
* `X-Powered-By: PHP/5.x`

Outdated VERSIONS are indicators of vulnerabilities.

### 3.2. Discovering HTTP methods

```bash
curl -X OPTIONS -I http://172.20.0.10:8888/
```

If the response includes:

```
Allow: GET, POST, PUT, DELETE
```

→ potential issues if the server is not supposed to support dangerous methods.

---

## 4. Analysing FTP Banners

Connect:

```bash
nc 172.20.0.12 2121
```

Banner:

```
220 (vsFTPd 2.3.4)
```

Problem identification:

* `2.3.4` is a version with an intentional backdoor (CVE-2011-2523)
* a simple online search confirms the vulnerability

---

## 5. Expected Results for This Stage

After completing the enumeration, students should have clearly identified:

* at least **2 web vulnerabilities** (e.g. SQL injection in DVWA, XSS, header leakage, outdated PHP)
* at least **1 FTP vulnerability** (vsftpd backdoor)
* at least **1 general vulnerability** found with nmap/NSE

These results will be used in Stage 4 for **controlled exploitation**.

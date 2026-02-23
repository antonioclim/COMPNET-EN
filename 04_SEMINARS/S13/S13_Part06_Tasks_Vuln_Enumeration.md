#### Tasks – Stage 3: Vulnerability Enumeration

Create the file:
`stage3_vuln_enumeration_report.txt`

---

## 1. Run the NSE scan

For each host:

```bash
nmap -sV --script vuln -p- 172.20.0.X
```

In the file:

* paste a minimum of **3 detected vulnerabilities**
* for each one indicate:

  * the port
  * the NSE script name
  * a short description (1–2 sentences)

---

## 2. Run nikto on DVWA and WebGoat

E.g.:

```bash
nikto -h http://172.20.0.10:8888
nikto -h http://172.20.0.11:8080
```

In the file:

* paste **5 relevant results** (not all — only the important ones)
* explain what each one means

---

## 3. Manual fingerprinting with curl

Execute:

```bash
curl -I http://172.20.0.10:8888
curl -I http://172.20.0.11:8080
```

In the file:

* note the detected server versions
* explain why outdated PHP/Apache versions pose a risk

---

## 4. Banner grabbing for the vulnerable FTP service

```
nc 172.20.0.12 2121
```

In the file:

* paste the complete banner
* identify the associated CVE (CVE-2011-2523)

---

## 5. Reflection question

**Why is it important to combine automated tools (nmap, nikto) with manual analysis (curl, nc)?**
Write a 5–10 line answer.

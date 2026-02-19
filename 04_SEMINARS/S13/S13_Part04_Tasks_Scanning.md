#### Seminar 13 – Stage 2

## Tasks – Scanning with Nmap + Implementing the Python Scanner

Create the file:
`stage2_S07_Part03_Output_Scan_Results.txt`

---

## 1. Discovering active hosts

Run:

```bash
sudo nmap -sn 172.20.0.0/24
```

In `stage2_S07_Part03_Output_Scan_Results.txt`:

* paste the IP addresses of active hosts
* note the execution time

---

## 2. Port scanning for each host

For each IP (10, 11, 12):

```bash
nmap -sV -p- 172.20.0.X
```

In the file:

* paste the list of open ports
* identify the servers found at each address (Apache/Tomcat/FTP, etc.)
* note the detected versions

---

## 3. Run the Python scanner

Execute:

```bash
python3 S13_Part04_Script_Simple_Scanner.py
```

Then:

* compare the results with those from nmap
* explain the differences in 3–5 sentences

---

## 4. Technical task (optional bonus)

Modify the scanner so that it:

* accepts the IP parameter from the command line:

```
python3 S13_Part04_Script_Simple_Scanner.py 172.20.0.11
```

* accepts a different port range

Example:

```
python3 S13_Part04_Script_Simple_Scanner.py 172.20.0.11 20 200
```

---

## 5. Reflection question

Explain the difference between:

* a port that is **closed**
* a port that is **filtered**
* a port that is **open**

and why only the first and the last appear correctly in the simple Python scanner.

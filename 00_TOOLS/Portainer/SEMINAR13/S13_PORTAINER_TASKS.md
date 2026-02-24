# S13 — Portainer Observation Tasks

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

In this seminar you work from two viewpoints at once: the **attacker** (nmap from the scanner container) and the **administrator** (Portainer dashboard). Keep both open side by side.

---

### P1 — Infrastructure Inventory *(administrator perspective)*

After `docker compose up`, open Portainer and fill in this table **without scanning anything**:

| Container | Image | Published Ports (host → container) | Static IP |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

Navigate to **Networks** → **pentestnet** to get the IPs.

As an administrator, you already know every service, every port and every IP. What advantage does an attacker need to overcome?

> `__________________________________________________________`

---

### P2 — Service Readiness Check

Before scanning, verify that each target is healthy:

| Target | What to look for in Portainer Logs | Ready? |
|---|---|:---:|
| DVWA | Apache startup message | Y / N |
| WebGoat | "Started WebGoat" (may take 30–60 s) | Y / N |
| vsftpd | FTP daemon start confirmation | Y / N |

If a service is not ready, wait 30 seconds and check again.

---

### P3 — Scan Detection *(administrator perspective)*

1. Open `dvwa` → **Logs** in Portainer (auto-refresh on).

2. From the scanner container, run a targeted scan:
   ```bash
   nmap -sT -p 80 172.20.0.10
   ```
   Do you see any evidence of the scan in the DVWA logs?  → Yes / No

3. Now run a wider scan:
   ```bash
   nmap -sT -p 1-1000 172.20.0.10
   ```
   Is the wider scan more or less visible in the logs?  → `____`

4. What does this tell you about the trade-off between scan thoroughness and stealth?

> `__________________________________________________________`

---

### P4 — The Backdoor Port

Examine `vsftpd_vuln` in Portainer:

1. List all published port mappings:  → `____`
2. Which port is unusual for an FTP server?  → `____`
3. Can you tell from Portainer alone that this port exists and is open?  → Yes / No
4. If you were the administrator and saw port 6200 published alongside port 21, would that raise a concern? Why?

> `__________________________________________________________`

---

### P5 — Version Disclosure Comparison

Fill in from two sources:

| Target | Version from image tag *(Portainer)* | Version from `nmap -sV` banner |
|---|---|---|
| DVWA | | |
| WebGoat | | |
| vsftpd | | |

1. Do the versions match or differ?  → `____`
2. Why is exposing version information through banners a security risk?

> `__________________________________________________________`

3. Name one hardening measure that would reduce version disclosure:

> `__________________________________________________________`

---

### P6 — Post-Exercise Reflection

After completing the scanning and enumeration exercises:

1. What information did the administrator (Portainer) have from the start that the attacker needed to discover through scanning?

> `__________________________________________________________`

2. What information did the attacker uncover that the administrator might miss without active monitoring?

> `__________________________________________________________`

3. In a production environment, what tools would replace Portainer for continuous security monitoring? *(Name at least two.)*

> `__________________________________________________________`

---

### Clean-Up

```powershell
docker compose -f S13_Part02_Config_Docker_Compose_Pentest.yml down
docker rm -f scanner 2>$null
```

Verify in Portainer: only `portainer` remains.

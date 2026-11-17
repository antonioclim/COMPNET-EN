# S13 — Portainer Observation Tasks

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

These are the course defaults for a new instance. Keep existing personal
credentials. For the OVA, open Portainer through the documented SSH tunnel and
run lab commands in the guest. See [environment routes](../../../00_APPENDIX/docs/environment_routes.md).

In this seminar you work from two viewpoints at once: the **attacker** (nmap from the scanner container) and the **administrator** (Portainer dashboard). Keep both open side by side.

---

### P1 — Infrastructure Inventory *(administrator perspective)*

After `docker compose up`, open Portainer and fill in this table **without scanning anything**:

| Container | Image | Published Ports (host → container) | Static IP |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

Open `dvwa` and follow its actual network link to get the declared IPs. The Compose
key `pentestnet` normally becomes a project-prefixed Docker network name.

As an administrator, you can read the declared images, addresses and mappings.
Which of those claims still needs a runtime service or reachability check?

> `__________________________________________________________`

---

### P2 — Service Readiness Check

Before scanning, compare startup logs with a protocol-level response. A log line
or a running container alone does not establish service readiness:

| Target | Supporting startup log | Required protocol check | Ready? |
|---|---|---|:---:|
| DVWA | Apache startup message | HTTP response from its configured host port | Y / N |
| WebGoat | "Started WebGoat" (startup time varies) | HTTP response from its configured host port | Y / N |
| vsftpd | Available daemon startup/error output | FTP greeting from its configured host port | Y / N |

Use the `.env` overrides if present, rather than assuming the default host ports.
If a service is not ready, inspect the observed error and listener; a longer wait
does not repair a failed startup command or an incorrect mapping.

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
   Is the wider scan more or less visible in the available logs? Record **no application-log entry** if that is what you observe.  → `____`

   Then run `curl -v http://172.20.0.10/` from the scanner. Compare its application log entry with the scan and save a packet capture for transport evidence. A TCP connect scan need not send HTTP, and Docker logs may not include a service’s file-based logs.

4. What does this tell you about the trade-off between scan thoroughness and stealth?

> `__________________________________________________________`

---

### P4 — The Backdoor Port

Examine `vsftpd_vuln` in Portainer:

1. List all published port mappings:  → `____`
2. Which port is unusual for an FTP server?  → `____`
3. Can you tell from Portainer alone that this port exists and is open?  → Yes / No
4. Does the 6200 mapping prove that a process is listening? Record a listener/reachability check before and after the authorised local exercise. If you saw this mapping alongside port 21, what would you investigate and why?

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

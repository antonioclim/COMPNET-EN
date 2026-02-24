# S09 Part 3 — Portainer Quick-Start Tasks

| | |
|---|---|
| **Dashboard** | `http://localhost:9050` |
| **Login** | `stud` / `studstudstud` |

These tasks run alongside the main FTP exercises. Complete them after `docker compose up` has started the stack.

---

### P1 — Container Inventory *(~1 min)*

Open Portainer → **Containers**.

1. How many containers are running?  → `____`
2. What image does `seminar9_ftp_server` use?  → `____`
3. Which container has a published port? What port?  → `____`

---

### P2 — Network Inspection *(~1 min)*

Navigate to **Networks** → click **ftpnet**.

| Container | IP address |
|-----------|------------|
| `seminar9_ftp_server` | |
| `seminar9_client1` | |
| `seminar9_client2` | |

What subnet did Docker assign to `ftpnet`?  → `____`

Which of these IPs do you use as the FTP server address in the client script?  → `____`

---

### P3 — Browser Terminal *(~1 min)*

Go to **Containers** → click `seminar9_client1` → **Console** → **Connect**.

Run this command inside the terminal:

```text
python S09_Part03_Script_Pyftpd_Multi_Client.py --help
```

Did you type `docker exec` at any point?  → `____`

---

### P4 — Live Log Observation *(during FTP transfer)*

Open **Containers** → click `seminar9_ftp_server` → **Logs** → enable auto-refresh.

In a separate PowerShell window, trigger a file upload from client1.

Watch the log stream in Portainer. What FTP command sequence do you see?

```text
____  →  ____  →  ____  →  ____
```

*(Typical sequence: USER → PASS → STOR → 226 Transfer complete)*

---

### Self-Check

After completing these tasks, you should be able to answer two questions:

1. What is the difference between a **published port** (visible from the host) and an **exposed port** (visible only inside the Docker network)?

2. Why can `client1` reach the FTP server by its **container name** (`ftp-server`) without specifying an IP address?

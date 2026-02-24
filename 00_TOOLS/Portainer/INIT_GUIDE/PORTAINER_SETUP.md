# Portainer CE — Installation and Configuration Guide

| | |
|---|---|
| **Course** | Computer Networks — COMPNET (ASE-CSIE) |
| **Port** | `9050` — verified conflict-free across the entire repository |
| **Credentials** | `stud` / `studstudstud` |
| **Image** | `portainer/portainer-ce:2.21-alpine` |

---

## 1  Why port 9050 (not 9000)

Port 9000 is taken by S10 Part 4, where the SSH tunnel command is `ssh -L 9000:web:8000`. That exercise is hardcoded across two dozen references in seminar materials, instructor outlines and task sheets — changing it would be disruptive.

Port 9090 is likewise occupied by the C08 TCP handshake scenario and several socket examples in the Python self-study guide.

Port 9050 returned zero hits when searched against every `.md`, `.yml`, `.py`, `.conf` and `.html` file in the repository. It is safe to claim.

---

## 2  Prerequisites

You need Docker Engine 20.10 or later (Docker Desktop on Windows, or Docker Engine inside the VM), Docker Compose v2 (bundled with Docker Desktop) and a modern browser. Port 9050 must be free on the host — if something else is already bound there, the container will fail to start with a clear error message.

---

## 3  Installation — Recommended: Docker Compose

The cleanest approach. Use the `docker-compose-portainer.yml` provided in this directory.

**Windows (PowerShell):**

```powershell
cd <repo>\00_TOOLS\Portainer\INIT_GUIDE

docker compose -f docker-compose-portainer.yml up -d
```

**Linux / VM (Bash):**

```bash
cd <repo>/00_TOOLS/Portainer/INIT_GUIDE

docker compose -f docker-compose-portainer.yml up -d
```

The Compose file creates a container named `portainer`, a named volume `portainer_data` for persistence, maps `9050 → 9000` (host → container) and sets a restart policy of `unless-stopped` so Portainer survives reboots.

**Quick verification:**

```text
docker ps --filter name=portainer --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

NAMES       STATUS          PORTS
portainer   Up 2 minutes    0.0.0.0:9050->9000/tcp, :::9050->9000/tcp
```

---

## 4  Installation — Alternative: single command

If you prefer not to use the Compose file, a one-liner does the same thing.

**Windows (PowerShell):**

```powershell
docker volume create portainer_data

docker run -d -p 9050:9000          `
  --name portainer                   `
  --restart unless-stopped           `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -v portainer_data:/data            `
  portainer/portainer-ce:2.21-alpine
```

**Linux / VM (Bash):**

```bash
docker volume create portainer_data

docker run -d -p 9050:9000          \
  --name portainer                   \
  --restart unless-stopped           \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data            \
  portainer/portainer-ce:2.21-alpine
```

---

## 5  Installation — Automated scripts

For bulk provisioning (e.g. pre-configuring lab workstations), two scripts are included. They pull the image, create the volume, start the container, wait for the API to become available and create the admin user programmatically.

**Windows:**

```powershell
.\portainer-init.ps1
```

**Linux / VM:**

```bash
chmod +x portainer-init.sh
./portainer-init.sh
```

Both scripts are idempotent — running them a second time detects the existing container and recreates it cleanly.

---

## 6  First-time browser setup

1. Open `http://localhost:9050`.

2. If this is the first launch (no admin user yet), you will see a registration form:
   - **Username:** `stud`
   - **Password:** `studstudstud` (exactly 12 characters — Portainer's minimum)
   - Confirm the password, then click **Create user**.

3. On the next screen, click **Get Started**. Portainer detects the local Docker socket automatically.

4. You should now see the **Home** dashboard with one environment ("local") showing container, image, volume and network counts.

**If you miss the 5-minute window:** Portainer enforces a timeout on admin creation after first boot. If the form disappears and you see a "timed out" message, recreate from scratch:

```bash
docker stop portainer && docker rm portainer
docker volume rm portainer_data
# re-run the install command from Section 3 or 4
```

The automated scripts (Section 5) avoid this problem entirely by creating the user through the API.

---

## 7  What the dashboard shows you

### Containers view

The main table lists every container with its name, state (running / stopped / exited), image, creation timestamp, internal IP and published ports. From here you can start, stop, restart or remove containers, and jump straight to their logs or an interactive console.

### Networks view

Lists all Docker networks with driver, subnet, gateway and connected containers. Click a network to see which containers are attached and what IPs they hold — this is the visual equivalent of `docker network inspect`, minus the JSON.

### Container detail — Logs

Live tail with auto-scroll, timestamp toggle and in-log search. You can also download the full log as a text file.

### Container detail — Console

Opens a browser-based terminal (`/bin/sh` or `/bin/bash`) inside the container. This is exactly `docker exec -it <name> sh`, but without needing to remember the container name or switch to a terminal window.

---

## 8  Day-to-day management

Starting Portainer (after a reboot or manual stop):

```bash
docker start portainer
```

Stopping Portainer to free resources:

```bash
docker stop portainer
```

Removing Portainer entirely:

```bash
docker stop portainer && docker rm portainer
docker volume rm portainer_data
```

Updating the image:

```bash
docker stop portainer && docker rm portainer
docker pull portainer/portainer-ce:2.21-alpine
# re-run the install command — the volume is preserved
```

---

## 9  Troubleshooting

| What you see | Likely cause | What to do |
|---|---|---|
| `localhost:9050` does not load | Container is not running | `docker start portainer` |
| Registration form is gone, no login prompt | Admin-creation timeout (5 min) | Remove container + volume, reinstall |
| "Port 9050 already in use" on start | Something else is bound to 9050 | Windows: `netstat -ano \| findstr :9050` — note the PID, then kill it. Linux: `ss -tlnp \| grep 9050` |
| "Permission denied" on Docker socket | Linux user not in `docker` group | Run with `sudo`, or `sudo usermod -aG docker $USER` then re-login |
| Portainer shows 0 containers | Wrong environment selected | Home → click the "local" environment tile |
| Compose containers not visible | Mismatched Docker context | `docker context ls` — the active context must be "default" |

---

## 10  A note on security

Portainer mounts the Docker socket, which gives it full control over the Docker daemon. In a local lab environment this is perfectly fine — the workstation is not exposed to the internet, the VM is disposable and the credentials are shared lab credentials.

In a production setting, Portainer would sit behind TLS, enforce role-based access control and restrict network exposure. That distinction is worth a brief mention when you introduce the tool at S09 — it plants the seed for S13's discussion of attack surfaces.

---

## 11  Files in this directory

| File | What it does |
|------|-------------|
| `PORTAINER_SETUP.md` | This guide |
| `docker-compose-portainer.yml` | Declarative Portainer deployment |
| `portainer-init.ps1` | Automated setup for Windows (PowerShell) |
| `portainer-init.sh` | Automated setup for Linux / VM (Bash) |

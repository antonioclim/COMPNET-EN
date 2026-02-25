# S10 — Portainer Integration (Instructor Notes)

## Context

Seminar 10 is the most fragmented Docker session in the course: three separate Compose stacks started and torn down one after another (DNS containers → SSH with Paramiko → SSH port forwarding). Each stack has its own network and its own set of containers. The most common problem is not conceptual — it is operational. Students forget to stop the previous stack before starting the next one, leaving orphan containers that silently occupy ports. The resulting errors ("address already in use") derail the exercise and waste time.

Portainer turns this invisible problem into a visible one. A single glance at the Containers view tells you exactly what is running and what should not be.

## Port 9000 — Not a Conflict, but a Teaching Moment

S10 Part 4 uses port 9000 for the SSH local-forwarding tunnel:

```text
ssh -L 9000:web:8000 labuser@localhost -p 2222
```

Portainer runs on port 9050. There is no clash. But the proximity is worth mentioning explicitly when you demonstrate the tunnel:

> *▸ "The tunnel uses port 9000; Portainer uses 9050. These are completely different ports — the same machine can host hundreds of services, each on a different port."*

This reinforces a point that students sometimes struggle with: port numbers are just identifiers, and a machine can have many listeners simultaneously.

## Pedagogical Objectives Augmented

| Objective already in the seminar | What Portainer adds |
|---|---|
| Understand Docker DNS (service name → IP) | Networks view shows the IP alongside the name — students verify resolution results against the dashboard |
| Work with multiple Compose stacks in sequence | Containers view acts as a "clean slate" checkpoint between exercises |
| Distinguish published ports from internal exposure | Part 4's `web` container has **no published ports** — visually obvious in Portainer's empty "Ports" column |
| SSH tunnelling as a bypass for network isolation | Logs view on the `web` container shows HTTP requests arriving through the tunnel, despite no direct host access |

The between-exercise checkpoint alone is worth the Portainer investment here. It catches a class of bug that would otherwise cost five to ten minutes per affected student.

## How to Use It — Instructor Perspective

### Pre-seminar checklist

- [ ] Portainer running on 9050
- [ ] No leftover containers from S09: `docker ps -a` shows only `portainer`
- [ ] S10 images pre-pulled:
  ```powershell
  docker pull python:3
  docker pull busybox
  docker pull python:3.10-slim
  ```

### Part 2 — DNS Containers (minutes 3–17)

**Before starting the stack,** open Portainer and confirm the slate is clean: only `portainer` is running.

> *▸ "Clean starting point. A single container — Portainer itself."*

Start the DNS stack:

```powershell
cd 2_dns-containers
docker compose -f S10_Part02_Config_Docker_Compose.yml up -d
```

Switch to Portainer → refresh. Three containers appear: `web`, `dns-server`, `debug`.

Click **Networks** → observe the auto-created Compose network. All three containers are on the same subnet. Open **Console** on `debug` and run:

```sh
nslookup web 127.0.0.11
```

The IP returned should match what Portainer shows in the network view.

> *▸ "Docker's internal DNS (127.0.0.11) resolves `web` to the container's IP address. Check in Portainer — it is the same IP."*

**Before moving to SSH,** stop the DNS stack and verify:

```powershell
docker compose -f S10_Part02_Config_Docker_Compose.yml down
```

> *▸ "Quick check in Portainer: all DNS containers have disappeared. Now we can start SSH without port conflicts."*

### Part 3 — SSH with Paramiko (minutes 17–25)

Start the SSH stack:

```powershell
cd ..\3_ssh
docker compose -f S10_Part03_Config_Docker_Compose.yml up -d --build
```

In Portainer: `ssh-server` and `ssh-client` appear. Click `ssh-server` — the detail view shows the port mapping `2222:22`.

> *▸ "Internal port 22 is mapped to 2222 on the host. That is why we connect with `-p 2222`."*

Stop the stack before Part 4 and verify the clean slate again.

### Part 4 — SSH Port Forwarding (minutes 25–35)

Start the port-forwarding stack:

```powershell
cd ..\4_ssh-port-forwarding
docker compose -f S10_Part04_Config_Docker_Compose.yml up -d --build
```

In Portainer, two containers appear: `ssh-bastion` (published port `2222:22`) and `web` (**no published ports**).

This is the key observation. Draw attention to the empty "Published Ports" column on `web`:

> *▸ "Notice: `web` has no published ports. You cannot access it directly from the browser — port 8000 is only `expose`d, visible only inside the Docker network. The only route is through the SSH tunnel."*

Establish the tunnel:

```powershell
ssh -o StrictHostKeyChecking=no -p 2222 -L 9000:web:8000 labuser@localhost
```

Access `http://localhost:9000/`. Then switch to Portainer → click `web` → **Logs**. The HTTP request appears in the log, even though the container has no published ports.

> *▸ "The `web` container does not know the traffic arrived through a tunnel. It simply sees a normal HTTP request. Portainer shows us exactly that."*

## How to Use It — Student Perspective

Students receive `S10_PORTAINER_TASKS.md`, which contains six tasks distributed across the three exercise blocks. The tasks are deliberately short (fill-in-the-blank, yes/no) so they do not slow down the main flow. The two "clean transition checkpoints" (Tasks P2 and P4) are the most important — they build a habit of verifying the slate between exercises.

The final self-check table maps each Portainer observation to a networking concept (Docker DNS, port mapping, isolation, tunnelling), making the tool usage explicitly didactic rather than merely convenient.

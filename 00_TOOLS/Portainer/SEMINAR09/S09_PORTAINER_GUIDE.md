# S09 — Portainer Integration (Instructor Notes)

## Context

Seminar 09 Part 3 is the first time the course uses a multi-container Docker Compose stack (FTP server + two clients on an isolated bridge network). Up to this point, every exercise ran as a single Python process on the host. The jump to three containers introduces a new kind of confusion — "is my stack actually up? which container am I supposed to exec into? what IP does the server have?" — that has nothing to do with FTP but can eat five minutes if a student gets stuck.

This is the right moment to show Portainer: a small, optional introduction (two to three minutes, no content displaced) that pays dividends across the remaining Docker-heavy seminars.

## Pedagogical Objectives Augmented

Portainer does not teach new concepts here — it accelerates existing ones. Specifically:

| Objective already in the seminar | What Portainer adds |
|---|---|
| Understand multi-container topologies | Visual confirmation: three containers, one network, at a glance |
| Work with Docker Compose | See the Compose project in context, not just as CLI output |
| Interact with containers (exec, logs) | Browser-based alternative that lowers the entry barrier |
| Identify container networking (IP, bridge) | Networks view shows IPs directly — no JSON parsing needed |

None of these replaces the CLI. Students who prefer the terminal continue using it. Portainer simply gives a second path to the same information.

## How to Use It — Instructor Perspective

### Pre-seminar checklist

- [ ] Portainer running: `docker ps --filter name=portainer` → status "Up"
- [ ] Dashboard loads: `http://localhost:9050` → login with `stud` / `studstudstud`
- [ ] S09 images pulled: `docker pull python:3.12-alpine`

### Timing and placement

Introduce Portainer **after** explaining the Compose topology (server + client1 + client2 on `ftpnet`) and **before** running `docker compose up`. The natural phrasing:

> *▸ „Până acum ați lucrat cu un singur script Python. De azi avem infrastructură — mai multe servicii care rulează simultan pe o rețea izolată. Ca să vedem totul dintr-o privire, deschidem Portainer în browser."*

### Live walkthrough (2–3 minutes)

1. Open `http://localhost:9050` → log in → show the Home screen. Point out: zero running containers (nothing started yet).

2. Switch to PowerShell and start the stack:
   ```powershell
   docker compose -f S09_Part03_Config_Docker_Compose.yml up -d
   ```

3. Switch back to Portainer → refresh. Three containers appear, all green:
   - `seminar9_ftp_server`
   - `seminar9_client1` (running `tail -f /dev/null` — keeps the container alive)
   - `seminar9_client2`

4. Click `seminar9_client1` → **Console** → **Connect**. A shell opens in the browser.
   > *▸ „Echivalentul comenzii `docker exec -it seminar9_client1 sh` — dar fără să tastați comanda."*

5. Click **Networks** in the sidebar → click `ftpnet`. All three containers are listed with their IPs.
   > *▸ „Containerele sunt pe aceeași rețea bridge. Serverul are un IP, clienții au altele. Exact ca un LAN fizic — doar că e virtual."*

6. Transition back to the normal seminar flow:
   > *▸ „Portainer rămâne deschis în browser. Folosiți-l oricând pentru log-uri, terminale sau dacă nu mai știți ce containere rulează. Nu înlocuiește CLI-ul — e un instrument în plus."*

### What changes in the existing exercise

Nothing. The FTP tasks proceed exactly as designed. Portainer runs in the background; students who find it useful will reach for it, others will stick with the terminal. Both paths lead to the same result.

## How to Use It — Student Perspective

Students receive the `S09_PORTAINER_TASKS.md` sheet, which contains four short tasks (container inventory, network inspection, browser terminal, live log observation) totalling roughly five minutes. These tasks are designed to be done **in parallel** with the existing FTP exercises, not as a separate block. The self-check questions at the end tie Portainer observations back to Docker networking concepts — published vs exposed ports, DNS-based service discovery — so the time spent is not wasted on tool familiarity alone.

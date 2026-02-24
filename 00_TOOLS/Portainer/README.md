# Portainer — Optional Docker Visibility Layer for COMPNET Seminars

## What This Is (and What It Is Not)

Portainer Community Edition is a browser-based dashboard that surfaces Docker container state, network topology, logs and interactive terminals in a single browser tab. It is **entirely optional** — every exercise in the course works without it and the CLI remains the primary interface. Think of Portainer as a second monitor on the same information: it does not replace `docker ps` or `docker logs`, but it does make the picture easier to read when three or four containers are running at once.

If you choose to adopt it, the investment is small (one container, ~30 MB RAM, a two-minute introduction at Seminar 09) and the payoff is felt across the remaining five Docker-heavy weeks.

## Why Bother

From Seminar 09 onwards, the exercises shift from single-process Python scripts to multi-container Compose stacks. That shift introduces a new category of problems — orphan containers, silent port conflicts, misidentified networks — that have nothing to do with the topic being taught but eat up lab time nonetheless. Portainer addresses these by giving both instructors and students a fast, visual way to answer "what is actually running right now?"

Beyond housekeeping, Portainer augments three pedagogical and observational objectives that the CLI alone handles clumsily:

1. **Simultaneous log observation.** Tailing three backend logs in parallel (S11 round-robin) requires three terminal windows and three `docker logs -f` commands. Portainer does this in three browser tabs with a click each.
2. **Network topology awareness.** Seeing which containers sit on which Docker network — and what their IPs are — takes a single glance in Portainer's Networks view. The CLI equivalent (`docker network inspect`) returns a wall of JSON that students must parse manually.
3. **Isolation verification.** The distinction between a published port and an exposed-only port is central to S10 (SSH tunnelling) and S13 (pentest lab). In Portainer, a container with no published ports has a visibly empty column — the isolation is obvious without explanation.

## Port Allocation

| Port  | Owner | Status |
|------:|-------|--------|
| 9000  | S10 Part 4 — SSH tunnel (`ssh -L 9000:web:8000`) | ⛔ Reserved |
| 9090  | C08 / self-study — TCP handshake and socket examples | ⛔ Reserved |
| **9050** | **Portainer UI** | ✅ Verified free across all 14 weeks |

Port 9050 was checked against every `.md`, `.yml`, `.py`, `.conf` and `.html` file in the repository. Zero conflicts.

## Access Credentials

| Field    | Value |
|----------|-------|
| URL      | `http://localhost:9050` |
| Username | `stud` |
| Password | `studstudstud` |

Credentials follow the same convention as the MININET-SDN workstation (`stud` / `stud` for SSH; the longer variant for Portainer's 12-character minimum).

## Integration Timeline

| Week | Seminar | Role | Folder |
|:----:|---------|------|--------|
| —    | Pre-semester | Install and configure | `INIT_GUIDE/` |
| 8    | S08 Part 4 — Nginx Reverse Proxy | 30-second teaser — first Docker container | `SEMINAR08/` |
| 9    | S09 Part 3 — Multi-client FTP | First proper encounter — introduce the dashboard | `SEMINAR09/` |
| 10   | S10 Parts 2–4 — DNS / SSH / Port Forwarding | Multi-stack housekeeping | `SEMINAR10/` |
| 11   | S11 Parts 1–2 — Load Balancing | Primary observability tool | `SEMINAR11/` |
| 13   | S13 — Penetration Testing Lab | Administrator vs attacker perspective | `SEMINAR13/` |
| 1–14 | All project work (S01–S15) | E2 debugging and multi-container observation | `PROJECTS/` |

### A Note on Seminars S01–S07 and S12

These seminars use no Docker containers in their exercises (pure socket programming, Wireshark, Mininet). Portainer has nothing to show during these sessions. The benefit to students working on those weeks comes exclusively from their **project work**, where Docker Compose is mandatory — see `PROJECTS/PROJECTS_PORTAINER_MAP.md` for a per-project breakdown.

## Repository Structure

```text
00_TOOLS/Portainer/
├── README.md                              ← you are here
│
├── INIT_GUIDE/
│   ├── PORTAINER_SETUP.md                 ← step-by-step install (Windows + VM)
│   ├── docker-compose-portainer.yml       ← declarative deployment
│   ├── portainer-init.ps1                 ← PowerShell automated setup
│   └── portainer-init.sh                  ← Bash automated setup
│
├── SEMINAR08/
│   └── S08_PORTAINER_TEASER.md            ← 30-second teaser (first Docker container)
│
├── SEMINAR09/
│   ├── S09_PORTAINER_GUIDE.md             ← instructor notes
│   └── S09_PORTAINER_TASKS.md             ← student activity sheet
│
├── SEMINAR10/ … SEMINAR11/ … SEMINAR13/   ← same pattern
│
└── PROJECTS/
    └── PROJECTS_PORTAINER_MAP.md           ← overview map (points to per-project guides)

02_PROJECTS/01_network_applications/assets/PORTAINER/
├── S01/PORTAINER_GUIDE_S01.md             ← per-project student guide
├── S02/PORTAINER_GUIDE_S02.md
├── …
└── S15/PORTAINER_GUIDE_S15.md
```

## Guiding Principles

Each seminar folder contains two files: a **GUIDE** (instructor-facing, with timing and pedagogical notes) and a **TASKS** sheet (student-facing, with fill-in tables and reflection questions). The design follows four rules:

1. **Additive, never mandatory.** Every exercise works from the CLI alone. Portainer is a convenience, not a dependency.
2. **One-time setup, semester-long benefit.** Install once before S09; reuse across all Docker seminars without further configuration.
3. **Port 9050 is reserved.** No other course artefact may claim this port.
4. **Instructor quotes stay in Romanian.** The GUIDE files include suggested phrasing in Romanian (the language of instruction) marked with `▸`. Adapt them freely — they are starting points, not scripts.

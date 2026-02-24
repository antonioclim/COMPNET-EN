# S08 — Portainer Teaser (Instructor Notes)

## Context

S08 Part 4 starts a single Nginx container (`network_mode: host`) as a reverse proxy in front of a host-side Python server. It is the **first Docker container** students encounter in a seminar exercise. Portainer adds little operational value here — one container on host networking, no Docker network to inspect, no inter-container topology — but it serves as a **thirty-second teaser** for the multi-container sessions that begin the following week.

This is not a full Portainer introduction. It is a seed: students see the dashboard once, note that it exists, and the proper walkthrough happens at S09 Part 3 when three containers appear on an isolated bridge.

## Pedagogical Justification

The teaser bridges a gap. Without it, the S09 introduction feels abrupt — students jump from "I have never opened Portainer" to "here are three containers on a custom network." With the teaser, the S09 moment becomes a continuation rather than a cold start.

## What to Do (30 seconds, after `docker compose up`)

After starting the Nginx stack:

```powershell
docker compose -f S08_Part04_Config_Docker_Compose.yml up -d
```

Open `http://localhost:9050` (if students have not seen it before, log in as `stud` / `studstudstud`).

Point at the Containers list:

> *▸ „Vedeți un singur container — nginx. Săptămâna viitoare vom avea trei, apoi patru, apoi mai multe. Portainer rămâne deschis pe 9050 pe tot parcursul semestrului."*

That is all. Close the tab, continue with the curl exercises. The introduction proper is at S09.

## What NOT to Do

Do not spend time on:
- Network view (there is no Docker network — `network_mode: host` bypasses it)
- Console access (students will use this from S09)
- Log tailing (the Nginx exercise already uses `docker logs`)

The point is presence, not depth.

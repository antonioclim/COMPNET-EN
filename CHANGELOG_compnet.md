# CHANGELOG (revizie minimă) – compnet-2025-redo-main
Data: 2026-02-07

## Partea generală
Am făcut o revizie **minimă**: am schimbat doar lucrurile care dau erori evidente în contexte uzuale (IDE lint, `python -m py_compile`, rulare directă a scripturilor shell).
Nu am modificat logica exerciţiilor şi nu am „rescris” conţinutul.

## Acţiuni generale (pe scurt)
- **Compatibilitate Python:** 2 fişiere `.py` conţineau text de scenariu (Markdown), nu cod. Au fost încapsulate într-un **docstring** ca să nu mai apară `SyntaxError` la verificări (lint / `py_compile`).
- **Executabilitate shell:** scripturile `render.sh` au primit un **shebang** ca să fie clar interpretul (bash).
- **Clarificare dependenţe:** am adăugat un fişier cu dependenţe *opţionale* (pentru cazurile în care scripturile sunt rulate/folosite în medii „curate”).
- **Documentare audit:** am inclus un audit sumar al scripturilor/configurilor (inventar + context de rulare).

---

## Anexă – detalii punctuale

### 1) FIXED – scenarii scrise în `.py` (nu erau cod Python)
**Problema:** fişierele de mai jos conţineau liste/formatări Markdown (inclusiv caractere Unicode gen „–”), iar la orice verificare Python apărea `SyntaxError`.
- `assets/tutorial/s2/6_tcp-client_scenario.py`
- `assets/tutorial/s3/4_udp-broadcast/4d_udp-broad_scenario.py`

**Schimbare:** am păstrat conţinutul integral, dar l-am încapsulat ca **docstring de modul**, ca să nu mai fie interpretat ca instrucţiuni Python.
**De ce merită:** elimină erori „false” în IDE / CI şi evită confuzia că fişierele ar fi executabile.

### 2) FIXED – `render.sh` fără shebang
**Problema:** fără shebang, rularea directă (ex. `./render.sh`) e ambiguă; în practică merge doar dacă îl rulezi explicit cu `bash render.sh`.
**Schimbare:** am adăugat `#!/usr/bin/env bash` ca prima linie (fără să schimb comenzile existente).

Fişiere afectate (12):
- `assets/course/c1/assets/render.sh`
- `assets/course/c2/assets/render.sh`
- `assets/course/c4/assets/render.sh`
- `assets/course/c5/assets/render.sh`
- `assets/course/c6/assets/render.sh`
- `assets/course/c7/assets/render.sh`
- `assets/course/c8/assets/render.sh`
- `assets/course/c9/assets/render.sh`
- `assets/course/c10/assets/render.sh`
- `assets/course/c11/assets/render.sh`
- `assets/course/c12/assets/render.sh`
- `assets/course/c13/assets/render.sh`

**Notă:** shebang-ul nu setează automat permisiuni de execuţie. Dacă scriptul nu e marcat executabil, îl poţi rula în continuare ca înainte cu `bash render.sh`.

### 3) ADDED – listă de dependenţe opţionale
Am adăugat: `requirements-optional.txt` (rădăcina proiectului)

**Motiv:** unele scripturi folosesc biblioteci care nu sunt „standard library” (ex.: `scapy`, `flask`, `grpcio`, `dnspython` etc.). Într-un mediu curat, altfel apar `ModuleNotFoundError`.
**Observaţie:** pentru Mininet / SDN, unele dependenţe sunt de sistem (nu doar `pip`).

### 4) ADDED – audit scripturi/configuri
Am adăugat: `AUDIT_SCRIPTS.md` (rădăcina proiectului)

**Motiv:** inventar + context de rulare pentru fiecare script/config (ce face, de ce depinde, ce condiţii de mediu presupune).

---

## Ce NU am schimbat (intenţionat)
- Nu am schimbat structura de directoare.
- Nu am schimbat logica exerciţiilor.
- Nu am rescris materialele (curs/seminar/figuri/diagrame).

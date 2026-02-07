### Scenariu: TCP framing (stream -> mesaje)

#### Obiectiv
Arati ca TCP este un flux de bytes si trebuie sa delimitezi mesajele in aplicatie.

Folosim delimitator: newline (\n)

Port: 9100

#### Rulare
Terminal 1:
- python3 server.py

Terminal 2:
- python3 client.py

#### Observa
- serverul citeste bucati si reconstruieste mesaje pe baza de newline
- daca trimiti mesaje rapide, poti primi "lipite" intr-un singur recv

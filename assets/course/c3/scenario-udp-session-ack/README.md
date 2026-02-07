### Scenariu: UDP cu stare minima (token) + confirmare (ACK)

Idee:
- client trimite "HELLO"
- server raspunde cu "TOKEN:<id>"
- client trimite "MSG:<token>:<text>"
- server raspunde cu "ACK:<token>:<seq>"

Port: 9300

#### Rulare
Terminal 1:
- python3 server.py

Terminal 2:
- python3 client.py

#### Observații
- in UDP trebuie sa introduci tu notiuni de sesiune si confirmare

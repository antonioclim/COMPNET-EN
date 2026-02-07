### Scenariu: server TCP concurent (thread per client)

Port: 9200

#### Rulare
Terminal 1:
- python3 server.py

Terminal 2,3,4 (pornesti de 2-3 ori):
- python3 client.py

#### Observa
- serverul proceseaza clienti in paralel
- fiecare client primeste raspuns propriu

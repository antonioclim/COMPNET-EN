### Reverse proxy cu nginx si Docker

In aceasta etapa vom pune in fata serverului nostru HTTP Python
un reverse proxy nginx rulat intr-un container Docker.

Scopuri:

- sa intelegem ce este un reverse proxy
- sa vedem cum nginx poate sta in fata unui backend Python
- sa exersam folosirea Docker/Docker Compose pentru un serviciu simplu

---

### Ce este un reverse proxy?

Schema simplificata:

```

client (browser / curl) -> nginx -> backend (server Python)

```

nginx:

- accepta conexiuni de la clienti pe un port (ex. 8080)
- trimite mai departe cererile catre un backend (ex. http://127.0.0.1:8000)
- preia raspunsul backend-ului si il retrimite clientului
- poate adauga / modifica antete, poate face cache, load balancing etc.

Avantaje:

- ascunde backend-ul (clientul vede doar nginx)
- permite centralizarea autentificarii, logging-ului, TLS etc.
- permite rularea mai multor backend-uri in spate

---

### De ce Docker?

In loc sa instalam nginx direct pe sistem, folosim un container:

- imagine oficiala `nginx:alpine`
- configuratia noastra este montata in container
- pornim totul cu o singura comanda: `docker compose up`

In laboratorul nostru:

- backend-ul (serverul Python) va rula pe host, pe portul 8000
- nginx va rula in container, dar cu `network_mode: "host"` pentru simplitate
  - astfel, containerul poate vedea backend-ul pe `127.0.0.1:8000`
  - si expune direct portul 8080 catre host

---

### Arhitectura pentru laborator

Backend:

- serverul Python (de exemplu `simple_http_builtin.py`) pornit pe portul 8000

Frontend (reverse proxy):

- nginx in Docker, care asculta pe portul 8080
- toate cererile care ajung la nginx pe 8080 sunt trimise catre `http://127.0.0.1:8000`

Schema:

```

curl [http://localhost:8080/](http://localhost:8080/)  -> nginx (8080) -> [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

```

Vom:

- testa direct backend-ul
- testa accesul prin nginx
- adauga un antet custom din nginx pentru a demonstra ca traficul trece prin proxy.


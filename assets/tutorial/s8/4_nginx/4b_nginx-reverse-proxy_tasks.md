### Sarcini – nginx reverse proxy in Docker

In acest stage vom rula:

- un server HTTP Python pe portul 8000
- un container nginx configurat ca reverse proxy pe portul 8080

La final veti demonstra ca acelasi continut este servit fie direct de backend,
fie prin nginx, si ca nginx adauga un antet custom.

---

### 1. Porniti backend-ul Python

Asigurati-va ca aveti `simple_http_builtin.py` (din stage-ul anterior).

Rulati in primul terminal:

```bash
python3 simple_http_builtin.py 8000
````

Verificati rapid:

```bash
curl -v http://localhost:8000/
```

Trebuie sa vedeti un raspuns 200 si continutul paginii (sau listarea directorului).

---

### 2. Porniti nginx cu Docker Compose

In acelasi director in care aveti `docker-compose.yml` si `nginx.conf`, rulati:

```bash
docker compose up
```

(sau, in functie de instalare:)

```bash
docker-compose up
```

Ar trebui sa vedeti ca nginx porneste fara erori.

---

### 3. Testati accesul prin nginx (port 8080)

Rulati:

```bash
curl -v http://localhost:8080/
```

Observati:

* status code (200, daca totul e OK)
* antetele raspunsului (ar trebui sa includa `Server: nginx`)
* continutul paginii (ar trebui sa fie acelasi ca de la `http://localhost:8000/`)

Adaugati output-ul in fisierul:

```text
reverse_proxy_log.txt
```

---

### 4. Comparati acces direct vs. acces prin proxy

In `reverse_proxy_log.txt` adaugati:

1. Outputul de la:

   ```bash
   curl -I http://localhost:8000/
   ```
2. Outputul de la:

   ```bash
   curl -I http://localhost:8080/
   ```

Raspundeti (in 3–4 propozitii):

* ce antete difera intre cele doua raspunsuri?
* ce server apare in antetul `Server`?
* cum puteti confirma ca traficul trece prin nginx?

---

### 5. Modificati antetul custom

In fisierul `nginx.conf` exista linia:

```nginx
add_header X-Student-Lab "Seminar8";
```

Task:

1. Modificati valoarea header-ului, de exemplu:

```nginx
add_header X-Student-Lab "Seminar8-ReverseProxy";
```

2. Reporniti nginx:

```bash
# In terminalul cu docker compose, opriti cu Ctrl+C
docker compose up   # sau docker-compose up
```

3. Testati din nou:

```bash
curl -I http://localhost:8080/
```

Confirmati ca vedeti noul header `X-Student-Lab` cu noua valoare.

Adaugati acest output in `reverse_proxy_log.txt`.

---

### 6. Intrebari de reflexie (de scris in reverse_proxy_log.txt)

Raspundeti la urmatoarele intrebari (cateva propozitii fiecare):

1. Care este diferenta dintre a accesa direct `http://localhost:8000/` si
   `http://localhost:8080/`, din perspectiva clientului?
2. Ce avantaje aduce un reverse proxy in fata unui server Python simplu?
3. Cum ar fi util sa aveti un reverse proxy intr-o aplicatie reala
   (mentionati cel putin 2 exemple: TLS, load balancing, caching, rate limiting etc.)?

---

### Deliverable Stage 4

Predati:

* `docker-compose.yml` (folosit in laborator)
* `nginx.conf` (configuratia modificata, cu header custom)
* `reverse_proxy_log.txt` cu:

  * output de la curl direct pe 8000
  * output de la curl prin nginx (8080)
  * comparatia dintre cele doua
  * raspunsurile la intrebarile de reflexie

Acesta incheie Seminarul 8:

* ati testat HTTP cu curl
* ati scris un server HTTP cu http.server
* ati implementat un server HTTP manual cu socket-uri
* ati pus nginx ca reverse proxy in fata backend-ului Python.

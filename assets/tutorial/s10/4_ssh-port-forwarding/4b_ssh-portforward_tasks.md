
### Sarcini – SSH port forwarding catre un serviciu HTTP in container

Scop:
- sa accesati un server HTTP din containerul `web`
  folosind un tunel SSH prin containerul `ssh-bastion`.

Rezultate:
- fisier de log: `ssh_forward_log.txt`

---

## 1. Porniti infrastructura

Asigurati-va ca aveti:

- `docker-compose.yml`
- Dockerfile pentru `ssh-bastion` (similar cu cel pentru `ssh-server` din Stage 3)

Rulati:

```bash
docker compose up --build
````

---

## 2. Verificati conectivitatea interna (din container)

Intrati in containerul `ssh-bastion`:

```bash
docker compose exec ssh-bastion bash
```

In interior:

```bash
apt-get update && apt-get install -y curl   # daca e nevoie
curl http://web:8000/
```

Ar trebui sa vedeti continutul paginii servite de `web` (de ex. index-ul directorului).

Copiati output-ul in `ssh_forward_log.txt` sub sectiunea:

```text
--- TEST DIRECT DIN ssh-bastion ---
<output>
```

Iesiti din container (`exit`).

---

## 3. Porniti tunelul SSH de pe host

De pe host, rulati:

```bash
ssh -L 9000:web:8000 labuser@localhost -p 2222
```

Notite:

* `labuser` si `labpass` sunt user/parola definite in containerul `ssh-bastion`
* comanda va tine sesiunea deschisa; lasati-o asa cat timp testati curl

---

## 4. Testati accesul HTTP prin tunel

Intr-un **alt terminal** de pe host:

```bash
curl -v http://localhost:9000/
```

Ar trebui sa vedeti acelasi continut ca la `curl http://web:8000/` din container.

Copiati output-ul in `ssh_forward_log.txt` sub sectiunea:

```text
--- TEST PRIN TUNEL (curl localhost:9000) ---
<output>
```

---

## 5. Intrebari de reflexie

La finalul fisierului `ssh_forward_log.txt`, raspundeti in cateva propozitii:

1. Ce rol are containerul `ssh-bastion` in acest scenariu?
2. De ce putem folosi `web` ca `DEST_HOST` in comanda `ssh -L`?
3. Ce s-ar schimba daca `web` ar rula pe alta masina/alt IP?
4. Ce avantaje are port forwarding-ul fata de expunerea directa a portului 8000 pe host?

---

### Deliverable Stage 4

Predati:

* `docker-compose.yml` (varianta folosita pentru acest stage)
* Dockerfile pentru `ssh-bastion` (daca e separat)
* `ssh_forward_log.txt` cu:

  * testul direct din `ssh-bastion`
  * testul prin tunel (curl localhost:9000)
  * raspunsurile la intrebarile de reflexie


### Stage 4 – SSH port forwarding (tunel local catre un serviciu HTTP in containere)

In aceasta etapa vom vedea cum putem accesa un serviciu HTTP aflat
intr-o retea de containere **prin SSH port forwarding**, ca si cum ar fi local.

Scenariu:

- container `web`:
  - ruleaza un server HTTP (ex. `python -m http.server 8000`)
  - nu expune portul 8000 direct pe host (doar `expose`, nu `ports`)
- container `ssh-bastion`:
  - ruleaza `sshd`
  - este accesibil de pe host pe portul 2222
  - se afla in aceeasi retea Docker cu `web`
- host:
  - se conecteaza la `ssh-bastion` cu `ssh -L`
  - deschide un port local 9000 care este tunelat catre `web:8000` in retea

Schema:

```text
browser/curl (host) -> localhost:9000
                      |
                      | (tunel SSH -L)
                      v
            ssh-bastion container
                      |
                      v
                  web:8000 (HTTP server)
````

---

## 1. Ce este port forwarding local (`ssh -L`)?

Sintaxa generala:

```bash
ssh -L LOCAL_PORT:DEST_HOST:DEST_PORT user@ssh_host
```

Inseamna:

* `ssh` porneste o conexiune catre `ssh_host`
* pe masina **locala** se deschide un port `LOCAL_PORT`
* orice trafic trimis la `localhost:LOCAL_PORT` este tunelat prin SSH
  si redirectionat catre `DEST_HOST:DEST_PORT` din perspectiva `ssh_host`.

In laboratorul nostru:

```bash
ssh -L 9000:web:8000 labuser@localhost -p 2222
```

* `ssh_host` = `localhost` port 2222 (containerul `ssh-bastion`)
* `LOCAL_PORT` = 9000 (pe host)
* `DEST_HOST` = `web` (numele serviciului Docker)
* `DEST_PORT` = 8000 (portul HTTP din containerul `web`)

---

## 2. De ce e util acest mecanism?

Cateva cazuri reale:

* acces la servicii interne care nu sunt expuse public
* debug/testare servicii dintr-un cluster intern
* acces la UI-uri interne (ex. dashboard-uri, baze de date) fara a le publica in Internet
* securitate: expui doar SSH, nu si porturile serviciilor.

---

## 3. Ce vom face concret in acest stage

1. Pornim un `docker-compose.yml` cu:

   * `web` (HTTP server pe 8000, doar in retea interna)
   * `ssh-bastion` (server SSH, port map 2222:22)
2. Verificam din `ssh-bastion` ca `web:8000` este accesibil (ex. cu `curl web:8000`)
3. De pe host, rulam:

   ```bash
   ssh -L 9000:web:8000 labuser@localhost -p 2222
   ```
4. Pe host, testam:

   ```bash
   curl http://localhost:9000/
   ```

   si vedem ca raspunsul vine de la serverul HTTP din containerul `web`.


## Tasks – nginx reverse proxy (round robin)

### 1. Start the Docker Compose setup

From this directory, run:

```bash
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml up --build
```

Open another terminal and test:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

---

### 2. Observe load balancing behaviour

You should see output that alternates between the three backends (web1, web2 and web3).
Save the output in a file named:

```text
nginx_round_robin_log.txt
```

---

### 3. Make the backends distinguishable

Open the following files:

- `web1/S11_Part01_Page_Index.html`
- `web2/S11_Part01_Page_Index.html`
- `web3/S11_Part01_Page_Index.html`

Ensure that each file contains a distinct message (e.g. "Hello from web1", "Hello from web2", "Hello from web3").

Rebuild and restart the containers if needed.

Repeat the curl tests and confirm that you can identify which backend answered each request.
Add the results to `nginx_round_robin_log.txt`.

---

### 4. Test resilience: stop one backend

Stop one backend container:

```bash
docker stop web2
```

Then call curl multiple times again:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Observe whether:

- nginx continues to distribute requests
- errors appear
- only web1 and web3 respond

Record the results in `nginx_round_robin_log.txt`.

---

### 5. Reflection questions (write in nginx_round_robin_log.txt)

Answer in a few sentences:

1. How can you tell that round-robin load balancing is happening?
2. What happens when one backend is down?
3. Why is it useful that only nginx is exposed on the host and the backends are not?

---

### Deliverable (Part A)

Submit:

- `S11_Part01_Config_Docker_Compose_Nginx.yml`
- `S11_Part01_Config_Nginx.conf`
- `nginx_round_robin_log.txt` containing:
  - curl outputs with all three backends running
  - curl outputs after stopping one backend
  - answers to the reflection questions

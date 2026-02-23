## Tasks – custom Python load balancer (round robin)

---

### 1. Complete the TODO sections in `S11_Part02_Script_Simple_Lb.py`

The script is a minimal HTTP reverse proxy. Complete the TODO sections so that it can:

- select a backend using **round robin**
- forward the client's HTTP request to the selected backend
- receive the backend's response and relay it to the client
- handle basic error cases (e.g. backend unavailable)

---

### 2. Start the Docker Compose setup

Run:

```bash
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml up --build
```

This will start:

- `web1`, `web2`, `web3` (simple HTTP servers on port 8000 inside the network)
- `custom-lb` (your Python load balancer, exposed on port 8080)

---

### 3. Test load balancing with curl

On the host, run multiple requests:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

You should observe that responses come from different backends (round robin).

Save the output in:

```text
lb_custom_output.txt
```

For each response, note which backend answered (web1/web2/web3).

---

### 4. Basic failure test (optional but recommended)

Stop one backend container:

```bash
docker stop web2
```

Then run the curl test again. Record:

- what happens for requests that would have been sent to web2
- what error code (if any) your load balancer returns

Add the results to `lb_custom_output.txt`.

---

### 5. Reflection questions (write in lb_custom_output.txt)

Answer in a few sentences:

1. Which parts of the HTTP protocol does your script handle correctly?
2. Which parts does it ignore (e.g. keep-alive, chunked encoding)?
3. What would you improve first if you wanted to make the load balancer more robust?

---

### Deliverable (Part B)

Submit:

- `S11_Part02_Script_Simple_Lb.py` (completed)
- `S11_Part02_Config_Docker_Compose_Lb_Custom.yml`
- `lb_custom_output.txt` containing:
  - curl outputs showing round robin
  - optional failure test output
  - answers to the reflection questions

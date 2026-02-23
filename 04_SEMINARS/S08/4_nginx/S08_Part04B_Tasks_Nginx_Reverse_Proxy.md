### Tasks — nginx Reverse Proxy in Docker

In this stage we will run:

- a Python HTTP server on port 8000
- an nginx container configured as a reverse proxy on port 8080

At the end you will demonstrate that the same content is served either directly
by the back-end or through nginx, and that nginx adds a custom header.

---

### 1. Start the Python back-end

Make sure you have `simple_http_builtin.py` (from the previous stage).

Run in the first terminal:

```bash
python3 simple_http_builtin.py 8000
````

Verify quickly:

```bash
curl -v http://localhost:8000/
```

You should see a 200 response and the page content (or a directory listing).

---

### 2. Start nginx with Docker Compose

In the same directory where you have `S08_Part04_Config_Docker_Compose.yml` and `S08_Part04_Config_Nginx.conf`, run:

```bash
docker compose up
```

(or, depending on your installation:)

```bash
docker-compose up
```

You should see nginx start without errors.

---

### 3. Test access through nginx (port 8080)

Run:

```bash
curl -v http://localhost:8080/
```

Observe:

* the status code (200, if everything is OK)
* the response headers (should include `Server: nginx`)
* the page content (should be the same as from `http://localhost:8000/`)

Append the output to the file:

```text
reverse_proxy_log.txt
```

---

### 4. Compare direct access vs. access through the proxy

In `reverse_proxy_log.txt` add:

1. The output from:

   ```bash
   curl -I http://localhost:8000/
   ```
2. The output from:

   ```bash
   curl -I http://localhost:8080/
   ```

Answer (in 3–4 sentences):

* which headers differ between the two responses?
* which server appears in the `Server` header?
* how can you confirm that traffic passes through nginx?

---

### 5. Modify the custom header

In the file `S08_Part04_Config_Nginx.conf` there is the line:

```nginx
add_header X-Student-Lab "Seminar8";
```

Task:

1. Change the header value, for example:

```nginx
add_header X-Student-Lab "Seminar8-ReverseProxy";
```

2. Restart nginx:

```bash
# In the terminal running docker compose, stop with Ctrl+C
docker compose up   # or docker-compose up
```

3. Test again:

```bash
curl -I http://localhost:8080/
```

Confirm that you see the new `X-Student-Lab` header with the updated value.

Add this output to `reverse_proxy_log.txt`.

---

### 6. Reflection questions (write in reverse_proxy_log.txt)

Answer the following questions (a few sentences each):

1. What is the difference between accessing `http://localhost:8000/` directly and
   `http://localhost:8080/`, from the client's perspective?
2. What advantages does a reverse proxy bring in front of a simple Python server?
3. How would a reverse proxy be useful in a real application
   (mention at least 2 examples: TLS, load balancing, caching, rate limiting etc.)?

---

### Stage 4 Deliverables

Submit:

* `S08_Part04_Config_Docker_Compose.yml` (used in the laboratory)
* `S08_Part04_Config_Nginx.conf` (the modified configuration with custom header)
* `reverse_proxy_log.txt` with:

  * curl output directly on 8000
  * curl output through nginx (8080)
  * comparison between the two
  * answers to the reflection questions

This concludes Seminar 8:

* you tested HTTP with curl
* you wrote an HTTP server with http.server
* you implemented a manual HTTP server with sockets
* you placed nginx as a reverse proxy in front of the Python back-end.

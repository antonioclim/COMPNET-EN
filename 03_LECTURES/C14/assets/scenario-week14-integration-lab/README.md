# Week 14 Integration Lab (DNS → HTTP → TLS → Proxy)

This capstone-style lab integrates multiple topics from the module:

- **DNS**: authoritative server (BIND) + caching resolver (Unbound)
- **HTTP**: reverse proxy routing + path rewriting
- **Transport/security**: optional **TLS termination** at the proxy
- **Observability**: debug headers and a client toolbox container

The goal is to be able to narrate a complete request path:

> *client → DNS resolver → authoritative DNS → reverse proxy → backend service(s) → response*

…and to identify where each protocol lives (L7 vs L4), and where state is maintained (caches, sessions, TLS state).

## Topology (logical)

- `auth` (BIND): authoritative for `week14.local`
- `resolver` (Unbound): caching resolver, forwards `week14.local` to `auth`
- `nginx`: reverse proxy front-door (`www.week14.local` → backends)
- `web1`, `web2`: backend web servers (load-balancing evidence via `X-Web-Instance`)
- `api`: backend JSON API (shows forwarded headers)
- `client`: toolbox container configured to use `resolver` as DNS

Static IPs are used inside the lab network so that DNS can map names to stable addresses.

## Run (HTTP variant)

From this folder:

```bash
docker compose up --build
```

- Proxy exposed on the host at: http://localhost:8088/
- Inside the lab network, the canonical name is: `http://www.week14.local/`

Enter the client container:

```bash
docker compose exec client sh
```

Then:

```bash
# DNS answers (through the resolver, i.e., caching behaviour)
python dns_query.py www.week14.local --server 10.14.0.53 --repeat 2 --sleep 5

# Compare to authoritative answers (direct auth query, no cache)
python dns_query.py www.week14.local --server 10.14.0.10 --repeat 2 --sleep 5

# End-to-end HTTP checks
python smoke_test.py
```

## Run (TLS variant)

1) Generate demo certificates (no keys shipped in the repo):

```bash
bash tls/generate_demo_certs.sh
```

2) Start with the TLS overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.tls.yml up --build
```

3) Verify from inside the client container:

```bash
docker compose exec client sh
python smoke_test.py --tls --cafile /client/certs/ca.crt
python http_probe.py https://www.week14.local/app/ --cafile /client/certs/ca.crt
```

Host note: the proxy is published at https://localhost:8443/ (self-signed demo CA).

## Exercises

1) **DNS caching**
   - Explain why the resolver can return a decreasing TTL (depending on implementation).
   - Show how the authoritative server always publishes the zone TTL.

2) **Reverse proxy rewrite**
   - Explain why the backend can serve at `/`, while users browse `/app/`.
   - Identify which component generates the redirect from `/` → `/app/`.

3) **Forwarded headers**
   - Call `/api/users` and explain `X-Forwarded-For` and `X-Forwarded-Proto`.
   - Explain why the application cannot reliably trust `X-Forwarded-*` unless the proxy is trusted.

4) **TLS termination (variant)**
   - Identify what the client verifies (certificate chain + hostname).
   - Explain where the plaintext HTTP now exists (between proxy and backends).

## Capstone extension ideas

- Add Nginx caching for `/api/users` (see C10 advanced proxy overlay for a reference pattern).
- Add rate limiting to protect `/api/`.
- Capture traffic (pcap) from the client and label:
  - DNS query/response
  - TCP handshake
  - HTTP request/response
  - TLS handshake (variant)

## Optional: run via the Phase C lab runner

From the repository root:

```bash
python 00_TOOLS/lab_runner/lab_runner.py up c14-week14-integration --build
python 00_TOOLS/lab_runner/lab_runner.py up c14-week14-integration --variant tls --build
python 00_TOOLS/lab_runner/lab_runner.py down c14-week14-integration --variant tls
```


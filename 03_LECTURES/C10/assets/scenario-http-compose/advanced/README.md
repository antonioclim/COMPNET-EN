# Advanced Proxy Exercises (optional)

This folder extends the base **C10 HTTP reverse proxy** scenario with additional, *exam-relevant* Nginx patterns.

It is an **optional overlay** (no breaking changes to the default lab).

## What you get

- a second web backend (`web2`) so you can observe **load balancing**
- a separate Nginx config (`nginx.advanced.conf`) enabling:
  - correct `X-Forwarded-For` chaining (`$proxy_add_x_forwarded_for`)
  - `proxy_next_upstream` failover behaviour
  - basic **rate limiting** for `/api/`
  - simple **proxy caching** for `/api/users`

## How to run

From the scenario folder (`03_LECTURES/C10/assets/scenario-http-compose/`):

```bash
# Start the advanced variant
docker compose -f docker-compose.yml -f advanced/docker-compose.advanced.yml up --build

# Stop
docker compose -f docker-compose.yml -f advanced/docker-compose.advanced.yml down
```

Or from repository root (Phase C lab runner):

```bash
python 00_TOOLS/lab_runner/lab_runner.py up c10-http-compose --variant advanced-proxy --build
python 00_TOOLS/lab_runner/lab_runner.py down c10-http-compose --variant advanced-proxy
```

## Exercises (what students should prove)

1. **Load balancing proof**
   - Run multiple requests to `http://localhost:8080/app/`.
   - Show that response header `X-Web-Instance` alternates between backends.

2. **X-Forwarded-For chain**
   - Call `http://localhost:8080/api/users`.
   - Confirm the API returns a JSON field `debug.x_forwarded_for` containing your client IP.
   - Explain why `$proxy_add_x_forwarded_for` is the correct choice for a proxy chain.

3. **Rate limiting**
   - Trigger 429 responses by making many requests quickly to `/api/users`.
   - Explain the difference between `limit_req` (rate limit) and `limit_conn` (connection limit).

4. **Caching**
   - Make repeated calls to `/api/users`.
   - Observe `X-Cache-Status` switching from `MISS` → `HIT`.

5. **Failover**
   - Stop one backend (`docker compose stop web2`).
   - Confirm that requests still succeed due to upstream failover.

## Reference solutions and tests

- `solutions/` contains ready-to-use config files.
- `tests/` contains a small host-side test that can be run after the stack is up.


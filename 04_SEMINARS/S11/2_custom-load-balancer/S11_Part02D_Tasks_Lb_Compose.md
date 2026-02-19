## Tasks – running both load balancer scenarios with Docker Compose

This part is focused on running and comparing two complete setups:

1. nginx as a reverse proxy (Part A)
2. your custom Python load balancer (Part B)

---

## 1. Run the nginx scenario

From `1_nginx-compose/`, run:

```bash
docker compose -f S11_Part01_Config_Docker_Compose_Nginx.yml up --build
```

Test:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Stop the stack (Ctrl+C) and remove containers if needed.

---

## 2. Run the custom LB scenario

From `2_custom-load-balancer/`, run:

```bash
docker compose -f S11_Part02_Config_Docker_Compose_Lb_Custom.yml up --build
```

Test again:

```bash
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Stop the stack afterwards.

---

## 3. Comparison report

Create a file named:

```text
lb_compose_comparison.txt
```

Include:

1. the commands used to start each scenario
2. sample curl output for each scenario (at least three requests)
3. one similarity and two differences between the scenarios
4. one limitation you observed in the custom load balancer
5. one advantage of using nginx in production

---

### Deliverable (Seminar 11)

Submit:

- `reverse_proxy_intro_findings.txt`
- `nginx_round_robin_log.txt`
- `lb_custom_output.txt`
- `lb_compose_comparison.txt`
- any modified scripts or configuration files required by the tasks

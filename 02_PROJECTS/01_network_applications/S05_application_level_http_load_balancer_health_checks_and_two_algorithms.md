# S05 — Application-layer HTTP load balancer with health checks and two algorithms

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C10, C08 | S11, S08, S04
- **Protocol/default ports (E2):** TCP: LB 8080/TCP; backends 8081, 8082, 8083/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S05.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
The topic targets an HTTP load balancer implemented as a reverse proxy: clients send requests to a single endpoint and the load balancer distributes them across multiple backend instances. Distribution is not only round robin; you must also implement a state-dependent algorithm such as least connections which requires tracking active connections.

Periodic health checks are added, separated from business traffic. A backend considered unhealthy is removed from rotation and reintroduced only after a minimum number of successful checks. This gives the system an explicit degradation and recovery model that is testable and demonstrable in Mininet.

In the capture you can follow client requests and responses that include the backend identifier. In logs you track routing decisions and backend state transitions so the demonstration remains auditable.

The load balancer is an exercise in application-layer routing control: the team maintains a list of backends, applies the selected algorithm and keeps minimal metrics (active connections, recent errors, estimated latency). The health check is not merely a ping; in E1 you define an endpoint and an interpretation rule (for example status 200 within X ms) then in E2 you demonstrate temporary removal of a backend and its reintroduction after recovery. For clarity during demo, add a response header (such as `X-Backend`) so you can correlate in the PCAP which instance served each request.

## Learning objectives
- Implement an HTTP reverse proxy with routing to N backends
- Apply two balancing strategies (round robin, least connections)
- Implement health checks and a removal/reintroduction policy
- Expose metrics and state for inspection during demo
- Build an automated test set that verifies distribution and failover

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **traffic generator (load) for the LB** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send concurrent requests and report the distribution across backends**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: LB 8080/TCP; backends 8081, 8082, 8083/TCP.
- The Flex component must work with the default values (without manual reconfiguration) so that it can be integrated into automated tests.

### Deliverables
- `flex/` directory with sources plus build/run instructions (avoid exotic dependencies where possible).
- `docs/FLEX.md` with:
  - build/run commands
  - the minimal scenario that is demonstrated
  - known limitations
- A minimal automated test (pytest or script) that starts the Flex component and validates the minimal scenario.

### Assessment (clear and measurable)
- The Flex component is assessed in E3 (as part of the E3 score). Its absence limits the maximum possible E3 mark.

## Phase 0 — Study / observation (Wireshark)
**Objective:** observe request distribution and the effect of health checks in an existing reverse-proxy configuration.

### Minimum scenario
- Run a known reverse proxy (e.g. Nginx) with two simple backends that return different IDs.
- Send 20–30 repeated requests to the proxy and capture traffic.
- Stop one backend and repeat the requests to observe failover.
- Observe what requests the health check sends and at what interval.

### Recommended Wireshark filters
- `frame contains "X-Backend"` — identify the header indicating the backend instance
- `http.request.uri contains "/health"` — health-check traffic separated from business traffic
- `http.request.uri contains "/work"` — traffic distributed to backends
- `tcp.analysis.ack_rtt` — RTT variation that may influence perceived timings
- `http.response.code == 502` — error responses when a backend fails (in the observation stage)

### Guiding questions
- How does the capture show the difference between health-check requests and business requests
- Under what conditions does a reverse proxy generate a 502 response and how does it correlate with backend unavailability
- How can distribution to backends be deduced from payload or from a dedicated header
- What is the effect of a slower backend on distribution under round robin versus least connections

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The load balancer accepts HTTP requests from clients and forwards them to one backend then returns the complete response to the client.
- Two strategies selectable via configuration: round robin and least connections applied over a configurable backend set.
- Periodic health checks to each backend (dedicated endpoint). Backends that fail are removed from rotation and reintroduced only after consecutive successful checks.
- Local status endpoint (e.g. `/status`) reporting active/inactive backends and counters (requests, errors, active connections).
- Deterministic health check: endpoint `/health`, interval (e.g. 2s), timeout (e.g. 300ms) and number of consecutive failures (e.g. 3) are fixed in E1 and used in E2.
- Deterministic backend selection: implement **at least 2** algorithms (e.g. round robin and least connections) switchable via config.

### SHOULD (recommended)
- Response header (e.g. `X-Backend`) that indicates the selected instance for debugging and for PCAP analysis.
- Upstream limits and timeouts: connect and response with a 504 response or equivalent on timeout.
- Backpressure: limit the number of simultaneous connections to a backend.

### MAY (optional)
- Sticky sessions based on a simple cookie with fallback to the main algorithm.
- Weighted round robin with configurable weights and reporting in `/status`.

## Non-functional requirements
- HTTP parsing sufficient to forward GET/HEAD requests and, if needed, small request bodies without blocking the whole process.
- Timeout and error policy: upstream down, upstream slow, client connection interrupted, all logged deterministically.
- YAML configuration: backend list, algorithm, health-check interval, fail/recover thresholds.
- Observability: routing logs (selected backend) and state-transition logs (healthy/unhealthy).
- Testability: distribution is validated via counters and via responses that include the backend ID.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Algorithm specification: how least connections is computed and which counter is used for active connections.
- Health-check specification: endpoint, interval, fail and recover thresholds, log format.
- Definition of the status endpoint and response structure (JSON recommended).
- Mininet topology with at least three backends and a client traffic generator.
- E2 capture plan: how distribution and a controlled failover are evidenced.
- Test plan: validate round robin over 3 backends and validate removal/reintroduction.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S05 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Two functional backends, load balancer started in Docker and end-to-end routing.
- A working health check that marks a backend unavailable when it is stopped.
- A `/status` endpoint reporting the current state.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes requests to `/work` and requests to `/health` for health checking.
- The analysis shows a distribution example (two responses served by different backends) and a failover example.
- A filter for the `X-Backend` header or an equivalent marker is provided.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S05.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S05.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S05 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==8080 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Client → load balancer handshake. |
| R2 | `tcp.port==8080 && frame contains "GET "` | `>= 1` | HTTP request to the load balancer. |
| R3 | `(tcp.dstport==8081 || tcp.dstport==8082 || tcp.dstport==8083) && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | The load balancer initiates a connection to at least one backend. |
| R4 | `(tcp.port==8081 || tcp.port==8082 || tcp.port==8083) && frame contains "/health"` | `>= 1` | At least one health check (/health) to a backend exists. |
| R5 | `tcp.port==8080 && frame contains "HTTP/1.1 200"` | `>= 1` | Final 200 response to the client. |

### Deliverables
- Docker Compose with `lb` plus at least two backend services plus `tester`.
- Smoke tests (`pytest -m e2`) that verify basic distribution and state change when a backend fails.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented with at least three backends in the demonstration.
- Tests for both algorithms and degradation scenarios (backend down, backend slow).
- Mininet demo with one backend configured slower and evidence of selection differences under least connections.
- Documented refactoring and a mini security audit for connection management and timeouts.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (lb) --- s1 --- h2 (client)
             |
             +--- h3 (backend A)
             +--- h4 (backend B)
             +--- h5 (backend C)
```
One backend may have artificial delay to simulate a slower service.

### Demo steps
- Send a burst of requests from h2 and show distribution via the response header and counters in `/status`.
- Stop h4 and show removal from rotation by the health check and continued responses from other backends.
- In the PCAP show requests to `/health` and `/work` in the same time window.

## Docker scenario (E2)
### Mandatory requirements for `docker-compose.yml` (E2)

For the PCAP to be **complete** (including internal hops, e.g. proxy→origin or gateway→microservice), `tester` must capture traffic from the **network namespace of the evaluated service** (typically server/proxy/gateway). Recommended deterministic approach:

- `tester` uses:
  - `network_mode: "service:<service_under_test>"` (e.g. `service:server`, `service:proxy`, `service:gateway`)
  - `cap_add: ["NET_ADMIN", "NET_RAW"]` (for `tcpdump`)
  - volume: `./artifacts:/artifacts`
  - env: `PROJECT_CODE=<CODE>` and `PCAP_PATH=/artifacts/pcap/traffic_e2.pcap`
- `tester` starts `tcpdump -i any`, runs `pytest -m e2`, stops the capture then runs `tools/validate_pcap.py`.

The catalogue includes a reference template: `00_common/docker/tester_base/`.

### Services
- **lb:** reverse proxy/load balancer implemented in Python
- **backend_a:** backend HTTP service with an instance ID
- **backend_b:** backend HTTP service with an instance ID
- **tester:** generates requests, verifies distribution and captures PCAP

### E2 flow
- Start backends and `lb` in the Docker network.
- Run `tester` which performs a short request set and saves `artifacts/pcap/traffic_e2.pcap` via volume.
- Verify capture and stop the stack.

## Notes
- The load balancer is application-layer; full support for all HTTP methods is not required.
- Least connections must be defined unambiguously: counter based on active connections or in-flight requests, with no ambiguity.
- Avoid side effects in health checks; the endpoint must be idempotent.

### Typical pitfalls
- Health checks without timeouts block the balancer and distort distribution when a backend becomes slow.
- The least-connections algorithm counts requests rather than active connections which makes behaviour unpredictable.
- The `Host` header is not preserved correctly (or is rewritten) and backends serve different content than expected in tests.

### Indicative resources (similar examples)
- [HAProxy (established load balancer)](https://github.com/haproxy/haproxy)
- [Traefik (reverse proxy plus dynamic routing)](https://github.com/traefik/traefik)

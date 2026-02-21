# S11 — REST microservices with a service registry and an API gateway with dynamic routing

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C10, C08 | S11, S08, S07
- **Protocol/default ports (E2):** TCP+UDP: gateway 8080/TCP; microservices 5101, 5102/TCP; registry 8500/TCP; discovery 239.10.11.12:5111/UDP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S11.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will build a microservices system communicating over HTTP, composed of a service registry, an API gateway and at least three microservices. The registry keeps a list of active instances while the gateway routes client requests to the appropriate microservice based on the registry rather than on a hard-coded list.

The project tests two recurrent problems in distributed applications: dynamic service discovery and controlled degradation under failure (instances down, timeouts). The registry must apply an expiry policy based on heartbeat while the gateway must avoid routing to expired instances.

In the demo, a client sends requests to the gateway, the gateway consults the registry and forwards to microservices. The PCAP capture must show at least two HTTP hops for the same request and a routing change when an instance becomes unavailable.

The project aims for a minimal set of mechanisms that appear in real systems: a service registry, health checks and an API gateway that routes based on a dynamic table rather than static configuration. In E2 two controlled situations are required: a service goes down (the gateway responds predictably without blocking) and a service returns (re-registration and restored routing). To keep complexity controlled, the REST contracts remain small but are validated strictly (JSON schema, error codes, timeouts).

## Learning objectives
- Implement a registry with registration and heartbeat endpoints
- Build an API gateway that routes requests based on the registry
- Implement three microservices with simple REST endpoints and an instance identifier
- Apply expiry policy and timeouts at gateway level
- Test routing and failover automatically when an instance becomes unavailable

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **service-discovery agent** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send a UDP multicast announcement and register/heartbeat with the registry**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP+UDP: gateway 8080/TCP; microservices 5101, 5102/TCP; registry 8500/TCP; discovery 239.10.11.12:5111/UDP.
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
**Objective:** observe a client → gateway → backend flow and failover signatures in the capture.

### Minimum scenario
- Run a reverse proxy (gateway) in front of two backends that respond with different IDs.
- Capture traffic and send repeated requests to the gateway.
- Stop one backend and observe how responses continue from the other.
- Note which headers can be used for correlation (for example an `X-Request-ID`).

### Recommended Wireshark filters
- `http.request.uri contains "/register"` — registrations to the registry (control plane)
- `http.request.uri contains "/heartbeat"` — periodic heartbeats
- `http.request.uri contains "/api/"` — client requests to the gateway
- `frame contains "X-Request-ID"` — correlate request/response across multiple hops
- `http.response.code == 503` — degradation responses when no instances are available

### Guiding questions
- How can you demonstrate in PCAP that a request went through two HTTP hops
- What is the difference between control plane (register/heartbeat) and data plane (API requests)
- How is failover observed: the selected backend changes or a 503 appears
- Which parameters should be configurable for expiry and timeouts

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Service registry with HTTP endpoints for registration and instance listing plus heartbeat-based expiry.
- At least three REST microservices, each with simple endpoints and a JSON response that includes `service_name` and `instance_id`.
- API gateway that receives client requests and routes them to the appropriate microservice based on the registry without hard-coding instances.
- Failover: if an instance does not respond or expires, the gateway selects another instance or responds deterministically with 503.
- Propagate a request identifier (e.g. `X-Request-ID`) from gateway to microservices and back, visible in logs.
- Networking-oriented service discovery: microservices announce their presence via **UDP multicast** (fixed address/port in E1) plus optional confirmation to the registry.
- The gateway correlates requests through `X-Request-ID` (generated if absent) and propagates it upstream.

### SHOULD (recommended)
- At least two instances for one microservice, with simple distribution (round robin) in the gateway.
- Controlled retry at the gateway for transient errors with a limit and no infinite loops.
- Health endpoint for each microservice and use it in the expiry decision.

### MAY (optional)
- Aggregated metrics endpoint in the gateway (requests per service, errors, latencies).
- A simple circuit breaker for instances that fail repeatedly.

## Non-functional requirements
- Timeouts for HTTP calls between components, configurable; no blocking on slow instances.
- Documented JSON contracts: mandatory fields, types and examples with input validation.
- Separation between control plane and data plane: distinct endpoints and differentiated logs.
- YAML configuration: registry address, list of services supported by the gateway, heartbeat interval, instance TTL.
- Testability: microservices can be started in Docker with stable names but the gateway must not assume fixed IPs.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- Registry API specification: request/response for register, heartbeat, list.
- Gateway API specification: exposed routes and mapping to services.
- JSON contract specification for microservices and for an aggregated response (if present).
- Architecture diagram with components and flows plus sequence diagram for a complete request.
- Mininet topology: client, gateway, registry, two microservices, with delay parameters on one link.
- E2 capture plan: one request with two hops and one controlled failover.
- Test plan: correct routing, expiry, instance down.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S11 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Registry, gateway and two microservices start in Docker and register themselves.
- A client (tester) sends a request to the gateway and receives a response from a microservice.
- Stopping an instance produces rerouting or 503, according to the chosen policy.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes at least one client→gateway request and one gateway→microservice hop for the same request.
- The analysis highlights `X-Request-ID` and shows how the two HTTP flows are correlated.
- One example of registration or heartbeat message towards the registry is included.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S11.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S11.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S11 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `udp.dstport==5111 && ip.dst==239.10.11.12` | `>= 1` | At least one UDP multicast announcement (service discovery). |
| R2 | `tcp.dstport==8080 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the API Gateway. |
| R3 | `tcp.port==8080 && frame contains "GET "` | `>= 1` | HTTP request to the gateway. |
| R4 | `tcp.port==8080 && frame contains "HTTP/1.1 200"` | `>= 1` | 200 response through the gateway. |
| R5 | `(tcp.port==5101 || tcp.port==5102) && frame contains "HTTP/1.1"` | `>= 1` | The gateway communicates with at least one microservice (HTTP upstream). |

### Deliverables
- Docker Compose with `registry`, `gateway`, at least two microservices and `tester`.
- Smoke tests (`pytest -m e2`) that verify routing and a simple failover scenario.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus two instances for one microservice and verifiable distribution.
- Extended tests for heartbeat-based expiry and for timeouts between components.
- Mininet demo that introduces delay for one microservice and shows the impact on gateway routing.
- Documented refactoring and a mini security audit for JSON input and rate limiting at the gateway.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client) --- s1 --- h2 (gateway)
                 |
                 +--- h3 (registry)
                 +--- h4 (service A)
                 +--- h5 (service B)
```
Delay can be introduced on the link to h5 to simulate a slow service.

### Demo steps
- Send a request to the gateway and show in logs the `X-Request-ID` and the selected instance.
- Stop h4 and show rerouting to an alternative instance or a deterministic 503 response.
- In Wireshark show two HTTP hops for the same request.

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
- **registry:** keeps the list of active instances and expires entries
- **gateway:** routes requests to microservices based on the registry
- **service_a:** REST microservice A
- **service_b:** REST microservice B (possible target for the flexible component)
- **tester:** exercises gateway routes, validates failover, captures PCAP

### E2 flow
- Start `registry`, `gateway` and microservices with registration at startup.
- Run `tester` which sends requests to the gateway and generates `artifacts/pcap/traffic_e2.pcap` via volume.
- Stop the stack and verify the capture.

## Notes
- No external service-discovery system is required. The registry is part of the project with controlled scope.
- The gateway does not hard-code instances; it uses the registry and explicit timeouts.
- Routes and JSON contracts must remain stable after E1 to keep tests valid.

### Typical pitfalls
- The registry keeps registrations without TTL; the gateway routes to dead instances and intermittent timeouts appear.
- JSON contracts are not validated; schema errors become runtime failures and propagate between services.
- Docker port configuration is confused (internal port versus published port) and captures no longer reflect the real flow.

### Indicative resources (similar examples)
- [Consul (service discovery, registry/health-check model)](https://github.com/hashicorp/consul)
- [Microservices Demo (example architecture with many services)](https://github.com/GoogleCloudPlatform/microservices-demo)

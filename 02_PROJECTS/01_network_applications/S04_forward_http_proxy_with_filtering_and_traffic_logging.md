# S04 — Forward HTTP proxy with filtering and traffic logging

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C10, C08 | S11, S08, S04
- **Protocol/default ports (E2):** TCP: proxy 3128/TCP; origin (in `tester`) 8080/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S04.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
This project requires a forward HTTP proxy able to mediate requests from clients to upstream servers and return responses without altering request semantics. The proxy operates over TCP and must parse HTTP requests in the form suitable for a proxy (absolute-form in the request line).

You will introduce explicit filtering policies: blocking selected URLs (blacklist) and filtering by content type. In this way the proxy becomes a control point and its behaviour can be tested automatically through predictable status codes (for example 403 when blocked).

In Mininet, the proxy is placed between clients and an origin server controlled by the team. The PCAP capture must show the two distinct conversations: client–proxy and proxy–origin, including the `Host` header differences and how the response is returned.

A forward proxy has two operating modes: for plain HTTP it can rewrite and retransmit the request towards the origin while for HTTPS it must implement the `CONNECT` method correctly and behave as a bidirectional tunnel (without decryption). A component that can be assessed deterministically is logging: for each request you record timestamp, client, target host, status and size and on blocking you also log the applied rule. In Phase 0 and E2, the PCAP must highlight the difference between a standard proxy request and a CONNECT flow (separate handshake followed by opaque payload).

## Learning objectives
- Implement the full request–response path through a forward proxy
- Parse proxy-style HTTP requests and reconstruct the upstream request
- Apply configurable filtering policies that are testable automatically
- Record application-level traffic and correlate it with PCAP evidence
- Build a reproducible environment with an origin server controlled by the team

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- An **HTTP client via proxy** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send a GET via the proxy and (E3) perform CONNECT to a laboratory HTTPS target**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: proxy 3128/TCP; origin (in `tester`) 8080/TCP.
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
**Objective:** observe the request format used when a client relies on a proxy and identify the two TCP connections.

### Minimum scenario
- Run a simple origin server (e.g. `python -m http.server`) and an existing proxy (e.g. `mitmproxy` for observation only).
- Configure `curl` with the proxy option and request a static resource from the origin server.
- Capture traffic on an interface where both client–proxy and proxy–origin are visible.
- Observe the request line: full URL rather than path only.

### Recommended Wireshark filters
- `http.request.full_uri` — useful fields to see the full URL (if exposed by the dissector)
- `http.response.code == 403` — blocking responses generated by the proxy
- `tcp.stream eq 0` — follow the client–proxy flow
- `tcp.stream eq 1` — follow the proxy–origin flow
- `http.proxy_authenticate` — proxy-specific headers if they appear in the capture

### Guiding questions
- How does the capture show that there are two distinct connections for the same request
- What form does the request line take when a proxy is used and what must be reconstructed for the upstream request
- How do you distinguish a 403 generated by the proxy from a 404 generated by the origin server
- Which headers are propagated and which headers are generated locally by the proxy

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The proxy accepts TCP connections from clients and processes HTTP/1.1 requests for methods `GET` and `HEAD`.
- For allowed requests, the proxy connects to the origin server, forwards the request and returns the full response.
- URL or host blacklist configured in `config/config.yaml`. On match, the proxy responds deterministically with 403 and a reason.
- Content-type filtering (by extension or by `Content-Type` in the response). On block, respond deterministically (415 or 403).
- Logging: for each request log method, URL, status, bytes and duration; logs must be correlatable with PCAP.
- Deterministic logging: stable log format (recommended: Common Log Format or JSON lines) with timestamp, client, method, URL, status and bytes.
- Explicit policy for caching and hop-by-hop headers (e.g. `Connection`, `Proxy-Connection`).

### SHOULD (recommended)
- Concurrency: at least 10 clients can issue requests simultaneously without deadlocks.
- Header management: the proxy adds `Via` and preserves `Host` correctly towards the upstream.
- Simple cache for small static resources with configurable TTL and evidence in logs (hit/miss).
- Support `CONNECT` (tunnel) as an E3 extension; in E2 only HTTP forwarding is required.

### MAY (optional)
- `CONNECT` support for TCP tunnelling only, without TLS decryption.
- Rate limiting per client with 429 on exceedance.

## Non-functional requirements
- Robust request parsing: header/body delimitation and handling of repeated headers and partial lines.
- Upstream connection and read timeouts; on timeout respond with 504 or an equivalent error.
- Input validation: reject URLs with disallowed characters and requests above a size limit.
- YAML configuration: proxy port, rules, cache TTL, timeouts and limits.
- Coherent logs without sensitive data and with a configurable level.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- HTTP support specification: methods, accepted request format, propagated headers and response codes for blocking.
- Exact definition of filtering rules and their priority (blacklist before content filter).
- Sequence diagram for an allowed request and a blocked request.
- Proposed Mininet topology and demo scenario with two clients and an origin server.
- E2 capture plan: filters to see both flows and 200/403 codes.
- Test plan: smoke tests for allow and deny plus edge cases for upstream unavailability.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S04 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- One allowed request through the proxy to the origin server and one request blocked by the blacklist.
- Logging produces one line per request with status and duration.
- The system starts in Docker and `tester` runs both requests.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes two streams: client–proxy and proxy–origin for the allowed request.
- For the blocked request the 403 response is visible without any connection to the origin server.
- The analysis includes the filters used and an example of a full URL in the request.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S04.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S04.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S04 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==3128 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Client → proxy handshake. |
| R2 | `tcp.port==3128 && frame contains "GET "` | `>= 1` | HTTP request to the proxy. |
| R3 | `tcp.dstport==8080 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Proxy initiates a connection to the origin server. |
| R4 | `tcp.port==3128 && frame contains "HTTP/1.1 200"` | `>= 1` | Proxy forwards a 200 response to the client. |

### Deliverables
- Docker Compose with `http_proxy` plus `origin_server` plus `tester`.
- Smoke tests (`pytest -m e2`) that verify 200 for allow and 403 for deny.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented plus demonstrable concurrency in Mininet.
- Additional tests for filters (Content-Type), upstream timeouts and invalid requests.
- Mininet demo with two clients issuing requests simultaneously, one to a blocked URL.
- Documented refactoring and a mini security audit (URL validation, timeouts and limits).

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (origin_server) --- s1 --- h2 (proxy)
                         |
                         +--- h3 (client A)
                         +--- h4 (client B)
```
The proxy is an intermediate hop. The link to h4 may have delay to observe the effect on request duration in logs.

### Demo steps
- From h3 issue an allowed request and show in the PCAP both the client–proxy and proxy–origin flows.
- From h4 issue a blocked request and show the 403 response generated locally by the proxy.
- Correlate the times in the logs with the observed packets.

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
- **http_proxy:** forward proxy implemented in Python over sockets
- **origin_server:** simple HTTP server serving team-controlled resources
- **tester:** sends proxy requests, validates status and captures PCAP

### E2 flow
- Start `origin_server` and `http_proxy` in the Docker network.
- Run `tester` which executes one allowed request and one blocked request and saves `artifacts/pcap/traffic_e2.pcap`.
- Validate the PCAP and stop the stack.

## Notes
- For the mandatory part use plain HTTP only; CONNECT tunnelling is optional.
- Filtering must be deterministic and testable rather than based on subjective interpretation.
- If caching is implemented document the invalidation policy precisely.

### Typical pitfalls
- The proxy attempts to decrypt HTTPS (MITM) although the requirement is tunnelling; this leaves the intended scope and becomes difficult to assess.
- Responses are buffered fully before forwarding which increases memory usage for large files.
- Missing timeouts and header-size limits allow stalls with clients sending slowly (slowloris).

### Indicative resources (similar examples)
- [mitmproxy (proxy/intercept, mature project)](https://github.com/mitmproxy/mitmproxy)
- [tinyproxy (lightweight proxy in C, architectural model)](https://github.com/tinyproxy/tinyproxy)

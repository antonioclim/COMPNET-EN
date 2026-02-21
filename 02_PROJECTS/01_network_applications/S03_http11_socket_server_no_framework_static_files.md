# S03 — HTTP/1.1 server on raw sockets (no framework) for static files

## Metadata
- **Group:** 1
- **Difficulty:** 4/5 (★★★★☆)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C08, C10 | S08, S04, S02
- **Protocol/default ports (E2):** TCP: 8080/TCP.

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S03.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
The application is an HTTP/1.1 server implemented directly over sockets with manual parsing of the request line and headers. Static files are served from a root directory and the response is built explicitly including `Content-Length` and `Content-Type`.

The emphasis is on correct HTTP format handling: separation of headers from body, path normalisation, supported methods and errors. To avoid ambiguity you must define a minimal grammar for requests together with a clear validation policy, particularly for paths and disallowed characters.

In the Mininet demonstration you will show simultaneous requests from multiple hosts together with different responses (200, 404, 405) that are visible in the PCAP. The implementation must be robust enough for a standard `curl` client to receive valid responses.

Because this is a socket-level HTTP server, the team must explicitly handle parsing of the request line, headers and body (where present) as well as the connection close rules. In E1 you must define a coherent policy for `Connection: keep-alive` versus `close` so that tests do not depend on client behaviour. A practical goal is a clear separation between: (1) an HTTP parser tolerant to whitespace and header folding (within reasonable limits), (2) a minimal router for GET/HEAD and (3) a file-serving layer with deterministic MIME types.

## Learning objectives
- Implement HTTP/1.1 parsing at the byte and line level
- Construct HTTP responses with correct headers and status codes
- Manage concurrency for simultaneous requests
- Apply file and path security rules (docroot, traversal)
- Design automated tests for status codes and content types

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **minimal HTTP client / benchmark** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **perform 2 GET requests on the same connection and validate status plus Content-Type**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** TCP: 8080/TCP.
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
**Objective:** identify the structure of an HTTP/1.1 request and the difference between GET and HEAD in a capture.

### Minimum scenario
- Start an existing HTTP server (for example `python -m http.server`) in a Mininet topology with two client hosts.
- Capture traffic and send a `GET /index.html` request then a `HEAD /index.html` request with `curl`.
- Observe header delimitation (`

`) and relevant headers (`Host`, `User-Agent`, `Content-Length`).
- Send a request to a missing file to observe a 404.

### Recommended Wireshark filters
- `http.request.method == "HEAD"` — HEAD requests, useful for seeing a response without body
- `http.response.code == 404` — 404 responses for missing resources
- `http.host` — presence of the Host header and its value
- `tcp.len > 0` — data-bearing segments to observe split between request and response
- `http.content_length` — the `Content-Length` value in the response

### Guiding questions
- How does the capture show the difference between GET and HEAD (the response body is absent for HEAD)
- Which headers are required for minimum compatibility with standard clients and where do they appear in the PCAP
- How is the end of headers delimited correctly and what happens when additional headers are present
- How do you identify in the PCAP the status code and content type for a static file

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- Support `GET` and `HEAD` methods on HTTP/1.1 with parsing of the request line and basic headers.
- Serve static files from a configurable docroot with path-traversal prevention.
- Correct responses for at least: 200, 404, 405, 500 with `Content-Length` and `Content-Type`.
- Concurrency: the server can process simultaneous requests from at least 10 clients without blocking on a single request.
- Server logs for each request: method, path, status, response size and duration.
- Explicitly define supported methods (minimum `GET`, optional `HEAD`). Unsupported methods respond with `405 Method Not Allowed`.
- Persistent connections: support `Connection: keep-alive` (at least 2 requests on the same connection in E2 tests).
- Deterministic `Content-Type` mapping by extension (minimum: html, txt, css, js, png/jpg).

### SHOULD (recommended)
- Persistent connections (keep-alive) for multiple requests per connection with a limit on requests per connection.
- Minimal Cache-Control for static files and coherent headers (Date, Server).
- Static error page for 404 and 500 served from the docroot.

### MAY (optional)
- `Range` support (partial content) for large files with a dedicated test.
- Rate limiting per IP or per connection with a 429 response.

## Non-functional requirements
- HTTP framing: `
` delimitation and robust handling of multi-line or additional headers.
- Read and write timeouts, configurable; inactive connections close gracefully.
- Strict path validation: normalisation, denial of `..`, disallowed characters and excessive lengths.
- Simple MIME detection by extension with fallback `application/octet-stream`.
- Memory management: large files are sent in streaming mode (internal chunking) without loading the full file into RAM.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- HTTP subset specification: supported methods, interpreted headers, error codes and full request/response examples.
- Security policy for docroot and paths (normalisation, traversal denial).
- Sequence diagram for GET 200, GET 404 and HEAD 200.
- Mininet topology and demo scenario with concurrent requests from different hosts.
- E2 capture plan: which requests are sent and which status codes are observed in the PCAP.
- Test plan: suite for status codes, Content-Type and large files.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S03 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- A GET for an existing file (200) and a GET for a missing file (404).
- A HEAD request for an existing file with correct headers and no body.
- The server runs in Docker and is accessed by `tester`.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes at least two requests and two complete responses.
- The analysis highlights the request line, header delimitation and a different status code (200 and 404).
- A filter showing a header (for example `http.content_length`) is provided.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S03.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S03.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S03 --pcap artifacts/pcap/traffic_e2.pcap`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `tcp.dstport==8080 && tcp.flags.syn==1 && tcp.flags.ack==0` | `>= 1` | Handshake to the HTTP server. |
| R2 | `tcp.port==8080 && frame contains "GET "` | `>= 2` | At least 2 GET requests (keep-alive/pipelining test). |
| R3 | `tcp.port==8080 && frame contains "HTTP/1.1 200"` | `>= 1` | 200 OK response for an existing file. |
| R4 | `tcp.port==8080 && frame contains "HTTP/1.1 404"` | `>= 1` | 404 response for a missing resource. |
| R5 | `tcp.port==8080 && frame contains "Content-Type:"` | `>= 1` | Content-Type header present in the response. |

### Deliverables
- Docker Compose with `http_raw_server` and `tester`.
- Smoke tests (`pytest -m e2`) that verify 200, 404 and HEAD.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented and robust under invalid input.
- Extended tests for unsupported methods (405), large files and traversal.
- Mininet demo with concurrent requests and evidence in logs and PCAP of traffic interleaving.
- Documented refactoring and a mini security audit for parsing and file access.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (http_server) --- s1 --- h2 (curl client)
                      |
                      +--- h3 (load client)
```
The link to h3 may have a small delay to generate bursty requests and observe the work queue.

### Demo steps
- From h2 run a set of `GET` and `HEAD` requests and show status codes in responses.
- From h3 generate repeated requests and show in logs that the server processes concurrently.
- In Wireshark highlight `http.response.code` for 200 and 404.

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
- **http_raw_server:** socket-level HTTP/1.1 server with mounted docroot
- **tester:** automated client that sends requests, validates responses and captures PCAP

### E2 flow
- Start `http_raw_server` with docroot available in the container.
- Run `tester` which executes requests and saves `artifacts/pcap/traffic_e2.pcap` via volume.
- Stop the stack and verify the capture automatically.

## Notes
- Full web frameworks are not used. Work with sockets and controlled parsing.
- For simplicity request bodies may be ignored in E2 but E3 must handle headers and errors robustly.
- Persistent connections are recommended but a limit must be enforced to avoid starvation.

### Typical pitfalls
- Headers are parsed incompletely (CRLF, continued lines) and incompatibilities with standard clients appear.
- `Content-Length` is incorrect or missing which causes clients to hang waiting for the end of the response.
- Requests fragmented at TCP level are not reassembled correctly and the server responds unpredictably under load.

### Indicative resources (similar examples)
- [CodeCrafters — HTTP server (Python, from scratch)](https://github.com/EpocDotFr/codecrafters-http-server-python)
- [http_tutorial (didactic HTTP implementation, tutorial repository)](https://github.com/briandorsey/http_tutorial)

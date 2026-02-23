# S07 — DNS resolver over UDP with a local zone, forwarding and TTL cache

## Metadata
- **Group:** 1
- **Difficulty:** 5/5 (★★★★★)
- **Recommended team size:** 3 (2–4 accepted)
- **Competency mapping:** C03, C11, C08 | S10, S07, S04
- **Protocol/default ports (E2):** UDP: resolver 5300/UDP; upstream 53/UDP (DNS).

## E1/E2/E3 scope and assessment (RC2026)

- **E1 (25%) — Specification plus Phase 0:** a complete deterministic specification (formats, timeouts, numeric limits) plus the Phase 0 deliverable (`docs/E1_phase0_observations.md`).
- **E2 (35%) — Prototype plus automation plus PCAP:** reproducible execution (Docker Compose or script), `pytest -m e2`, capture `artifacts/pcap/traffic_e2.pcap` and automatic validation via `tools/validate_pcap.py` using the rules `tools/pcap_rules/S07.json`.
- **E3 (40%) — Final plus demo plus Flex:** complete implementation plus demo (included in E3) plus a **Flex component** that is interoperable (a language other than Python).

> Note: E4 (presentation) is absorbed into E3 for RC2026 in order to retain a clear and automatable E1/E2/E3 scope.

## Description
You will implement a DNS resolver that receives UDP queries, parses messages at the byte level and answers for locally defined A records. For names that are not present in the local zone, the resolver forwards the query to a configured upstream and returns the response to the client.

The difficult part is the DNS wire format: header, question, answer sections, name compression and response codes. For didactic scope the set of mandatory queries is limited but you still must implement a correct parser for the relevant fields and an explicit error policy (invalid format, unsupported opcode, query too large).

A TTL cache is required. After the first upstream response, the resolver may answer locally until TTL expiry and E2 must include a capture that shows the difference between a forwarded query and one served from cache.

A DNS resolver forces work with a binary format: header, question, name compression and resource records even if support remains limited to A/AAAA (and optionally CNAME). In caching, TTL becomes the expiry criterion and must be handled together with negative caching (NXDOMAIN) in a simplified form. In E2, captures must clearly show: a query resolved locally (internal zone), a query forwarded to upstream and a query served from cache (no upstream packet for that third query).

## Learning objectives
- Parse and construct DNS messages (header, question, answer) at the byte level
- Implement a simple local zone and authoritative answers
- Forward recursively to a configured upstream and propagate the response correctly
- Implement a TTL cache with deterministic invalidation
- Analyse UDP traffic in Wireshark and correlate it with cache behaviour

## Flexible component (E3 — mandatory, multi-language interoperability)

**Aim:** demonstrate that the E1 specification is sufficient for interoperability (not “it only works with our client”) and practise integration across different languages and stacks.

### Proposed component
- A **DNS client** implemented in a language **other than Python** (e.g. C/C++, C#, Java/Kotlin, JavaScript/Node.js, Go or Rust).
- The component runs independently of the Python implementation and communicates using the protocol defined in E1.

### Minimum requirement (acceptance threshold)
- The component must run end-to-end: **send a UDP query and parse the response (A record/NXDOMAIN)**.
- Any “shortcut” (hardcoding, protocol bypass, direct access to the server’s internal files) is forbidden.

### Contract (interface) — fixed for assessment
- **Protocol/default ports (E2):** UDP: resolver 5300/UDP; upstream 53/UDP (DNS).
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
**Objective:** observe a UDP DNS query and identify transactional fields and TTL.

### Minimum scenario
- Use `dig` or `nslookup` in a controlled topology and capture traffic towards a resolver.
- Send the same query twice for a known name and observe whether there are differences in the response.
- Filter DNS packets and inspect the question and answer sections.
- Note the TTL value and response code (NOERROR, NXDOMAIN).

### Recommended Wireshark filters
- `udp.port == 53` — isolate standard DNS UDP traffic
- `dns.flags.response == 0` — queries, not responses
- `dns.flags.response == 1` — DNS responses
- `dns.qry.type == 1` — A queries
- `dns.resp.ttl` — TTL field in responses (useful for caching)

### Guiding questions
- Which header field links a response to the original query and how do you verify the match
- How does Wireshark show the difference between NOERROR and NXDOMAIN
- Where is TTL located in the response and how can it be used for cache expiry
- How do you recognise in the capture that a resolver forwarded to an upstream (two query/response pairs)

### Mandatory deliverable (counts towards E1)
- `docs/E1_phase0_observations.md` — answers to the guiding questions plus screenshots (or notes) supporting the observations.
- (optional) `artifacts/pcap/phase0.pcapng` — a short capture (≤ 2 MB) used in the explanation.

## Functional requirements
### MUST (mandatory)
- The resolver listens on UDP and accepts DNS A (IPv4) queries, parsing the header and question section.
- Configurable local zone (e.g. `lab.local`) with at least 5 A records. These names are answered locally.
- Forwarding to a configured upstream for names outside the local zone with correct propagation of transaction ID and response code.
- TTL cache: forwarded responses are stored and served from cache until expiry with TTL decreased according to elapsed time.
- Logs for local queries, forwarded queries, cache hit/miss and parsing errors.
- Explicitly implement: `NOERROR`, `NXDOMAIN` (rcode=3) and `SERVFAIL` (rcode=2) with clear rules.
- Deterministic TTL handling: cache uses the TTL from responses; for tests support TTL min/max override (config) for predictability.

### SHOULD (recommended)
- Support `NXDOMAIN` for names absent from the local zone with the correct response code.
- Simple negative caching (store NXDOMAIN for a short interval) to avoid repeated forwarding.
- `AAAA` support as an extension if the parser is generalised.

### MAY (optional)
- An administrative CLI command that displays cache entries and time remaining to expiry.
- Client IP rate limiting to reduce amplification under high query volume.

## Non-functional requirements
- Packet size limits and explicit rejection of malformed DNS messages.
- Timeout for upstream forwarding and a deterministic client response on timeout (SERVFAIL).
- Concurrency handling: non-blocking UDP processing and synchronisation for cache access.
- YAML configuration: port, local zone, upstream IP/port, cache parameters (max entries, TTL min/max).
- Testability: deterministic local answers and the ability to simulate upstream unavailability.

## E1 — Documentation and planning
- **E1 gate (mandatory):** submit `docs/E1_specification.md` plus `docs/E1_phase0_observations.md`. The specification must set numeric values for timeouts, size limits, encodings and message format (including version/magic where appropriate).

- DNS subset specification: supported fields, supported query types and response codes.
- Local-zone format description and lookup rules (exact match, case-insensitive).
- Cache policy: key (qname, qtype), TTL, expiry and negative caching if present.
- Mininet topology: client, resolver, controlled upstream.
- E2 capture plan: one query served locally, one forwarded query and one cache-served query.
- Test plan: parsing, TTL, NXDOMAIN, upstream timeout.

## E2 — Prototype plus PCAP capture
- **E2 gate (mandatory):** there is a single command (recommended `make e2`) that runs the E2 scenario end-to-end: `pytest -m e2`, generates `artifacts/pcap/traffic_e2.pcap` then validates the capture: `python tools/validate_pcap.py --project S07 --pcap artifacts/pcap/traffic_e2.pcap`.

### Minimum demonstrable outcome
- Local response for a name in the `lab.local` zone.
- Forward to upstream for an external name and return of the response.
- A second identical query that becomes a cache hit.

### PCAP requirements
- The capture `artifacts/pcap/traffic_e2.pcap` includes at least two identical queries, with the second being a cache hit (no forward).
- The analysis highlights TTL and response code and explains the difference between the forwarded flow and the cached flow.
- Filters for queries and responses are provided separately.

### Automatic PCAP criteria (E2)
These criteria are **deterministic** and can be verified automatically with `tshark`.
- Official rules: `tools/pcap_rules/S07.json`
- In the catalogue (template): `00_common/tools/pcap_rules/S07.json` and `00_common/tools/validate_pcap.py` (copy into the student repository).

- Command: `python tools/validate_pcap.py --project S07 --pcap artifacts/pcap/traffic_e2.pcap`
- Decode-as used during validation: `udp.port==5300,dns, udp.port==53,dns`

| ID | tshark filter (`-Y`) | Condition | What it validates |
|---:|---|---:|---|
| R1 | `udp.dstport==5300 && dns.flags.response==0` | `>= 3` | At least 3 client → resolver queries (local zone plus forwarding plus cache). |
| R2 | `udp.srcport==5300 && dns.flags.response==1` | `>= 3` | At least 3 resolver → client responses. |
| R3 | `udp.dstport==53 && dns.flags.response==0` | `>= 1` | At least one query forwarded to upstream (port 53). |
| R4 | `udp.dstport==53 && dns.qry.name` | `<= 2` | A limited number of upstream queries (cache demonstration). |
| R5 | `dns.flags.rcode==3` | `>= 1` | At least one NXDOMAIN response (negative caching). |

### Deliverables
- Docker Compose with `dns_resolver`, `upstream_dns` (or an upstream mock) and `tester`.
- Smoke tests (`pytest -m e2`) that validate local response, forwarding and a cache hit.
- `artifacts/pcap/traffic_e2.pcap` and a completed `docs/E2_pcap_analysis.md`.

## E3 — Completion plus demo plus testing
- All MUST requirements implemented including TTL expiry and behaviour under upstream timeout.
- Extended tests for malformed messages, negative caching and cache capacity.
- Mininet demo showing the difference between local, forwarded and cached answers (logs plus PCAP evidence).
- Documented refactoring and a mini security audit for binary input handling and rate limiting.

## Mininet topology and demo scenario
### Topology (ASCII)
```
h1 (client) --- s1 --- h2 (dns_resolver) --- h3 (upstream_dns)
```
h2 and h3 are on the same switch; delay parameters can be introduced on the link to h3.

### Demo steps
- Send a query to `lab.local` and show local response with no upstream traffic.
- Send a query to an external name and show forwarding to h3.
- Repeat the external query and show cache hit (no forwarding) plus reduced TTL.

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
- **dns_resolver:** UDP resolver with local zone and cache
- **upstream_dns:** team-controlled upstream resolver (container)
- **tester:** sends queries, validates responses and captures PCAP

### E2 flow
- Start `upstream_dns` and `dns_resolver` in the Docker network.
- Run `tester` which executes local, forward and cache-hit sequence and writes `artifacts/pcap/traffic_e2.pcap`.
- Stop the stack and verify the capture.

## Notes
- Full DNS name compression support can be approached incrementally; define clearly what is accepted in E2 and what is completed in E3.
- Upstream should be controllable in Docker for repeatable tests; reliance on the Internet is not recommended.
- For caching, TTL correctness matters more than optimisation.

### Typical pitfalls
- Cache ignores TTL and serves expired entries which becomes obvious when an upstream record changes.
- DNS parser does not handle compression pointers and fails on real upstream responses.
- UDP timeout/retry is missing; an upstream that does not respond causes clients to hang.

### Indicative resources (similar examples)
- [dnslib (encode/decode DNS wire format in Python)](https://github.com/paulc/dnslib)
- [dnspython (DNS toolkit in Python)](https://github.com/rthalley/dnspython)

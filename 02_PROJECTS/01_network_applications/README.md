# Group 1 — Network applications (S01–S15)

These projects focus on application-level protocols, service design and reproducible network experiments. Each project is written for the RC2026 E1/E2/E3 structure:

- **E1:** specification plus Phase 0 observations (Wireshark)
- **E2:** reproducible run plus deterministic PCAP capture and validation
- **E3:** completion plus demo plus **Flex component** (multi-language interoperability)

## Projects
- **S01** — Multi-client TCP chat with a text protocol and presence
- **S02** — File transfer server with a control channel and data channel (FTP passive style)
- **S03** — HTTP/1.1 socket-based server (no framework) for static files
- **S04** — Forward HTTP proxy with filtering and traffic logging
- **S05** — Application-level HTTP load balancer with health checks and two algorithms
- **S06** — TCP pub/sub broker with topics and deterministic routing
- **S07** — DNS resolver over UDP with a local zone, forward and TTL cache
- **S08** — Minimal email system: SMTP server for delivery and POP3 server for reading
- **S09** — TCP tunnel on a single port with session multiplexing and demultiplexing
- **S10** — Network file synchronisation with manifest, hashes and conflict resolution
- **S11** — REST microservices with a service registry and an API gateway with dynamic routing
- **S12** — Client–server messaging with a TLS channel and minimal authentication
- **S13** — gRPC-based RPC service: .proto definition, unary and streaming methods
- **S14** — Didactic distance-vector routing in Mininet with convergence and anti-loop
- **S15** — IoT gateway: UDP telemetry ingestion and an HTTP API for querying and streaming

## Notes
- For all projects, E2 must produce `artifacts/pcap/traffic_e2.pcap` and pass `tools/validate_pcap.py`.
- The Flex component is mandatory in E3 for S projects. Use a language other than Python.
- Keep E1 specifications stable after submission to maintain deterministic testing.

See `../00_common/README_STANDARD_RC2026.md` for repository structure and evidence requirements.

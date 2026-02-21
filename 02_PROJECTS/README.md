# RC2026 — Project catalogue (Computer Networks)

This repository contains a catalogue of laboratory projects for **RC2026**, organised into two groups:

- **Group 1 — Network applications** (`01_network_applications/`)
  - application-layer protocols and services (HTTP, DNS, SMTP/POP3, tunnels, file sync, microservices, TLS, gRPC, IoT)
  - E1/E2/E3 with a mandatory **Flex component** (interoperability across languages)

- **Group 2 — Administration and security** (`02_administration_security/`)
  - SDN/OVS/OpenFlow laboratories, deterministic PCAP analysis, practical security in a controlled environment
  - E1/E2/E3 **without** Flex (multi-language interoperability is not required)

Common assessment and deliverable standards are described in:
- `00_common/README_STANDARD_RC2026.md`

## Contents
- `01_network_applications/` — project briefs S01–S15
- `02_administration_security/` — project briefs A01–A10
- `00_common/` — common templates and tools (PCAP validation rules, reference tester patterns)

## Deterministic PCAP validation (E2)
For all projects, E2 requires:
- a reproducible run (recommended `make e2`)
- generation of `artifacts/pcap/traffic_e2.pcap`
- automatic validation of the capture using:
  - `python tools/validate_pcap.py --project <CODE> --pcap artifacts/pcap/traffic_e2.pcap`

PCAP rules are project-specific and stored under:
- `00_common/tools/pcap_rules/<CODE>.json`

## Mapping course ⇄ seminar competencies
See `COURSE_SEMINAR_MAPPING.md`.

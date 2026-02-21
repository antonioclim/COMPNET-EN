# Group 2 — Administration and security (A01–A10)

These projects focus on network administration, SDN and security in a controlled laboratory setting (Mininet, Docker, OVS). Each project follows the RC2026 E1/E2/E3 structure:

- **E1:** specification plus Phase 0 observations (Wireshark)
- **E2:** reproducible run plus deterministic PCAP capture and validation
- **E3:** completion plus demo plus documentation evidence

> For the A01–A10 series there is **no Flex component** requirement.

## Projects
- **A01** — SDN firewall: filtering policies implemented via OpenFlow rules
- **A02** — IDS with simple rules: scan detection, TCP anomalies and payload patterns
- **A03** — PCAP report generator: flow statistics, top talkers and TCP indicators
- **A04** — ARP spoofing detection and mitigation: alerts, evidence and controlled blocking
- **A05** — Laboratory port scanning: TCP connect scan and minimal service fingerprinting
- **A06** — NAT and DHCP laboratory: dynamic allocation, iptables MASQUERADE and verification via PCAP
- **A07** — SDN learning-switch controller with flow installation and ageing
- **A08** — Encapsulation and tunnelling in Mininet: VXLAN between two sites
- **A09** — SDN IPS: dynamic blocking via OpenFlow triggered by IDS detection
- **A10** — Network hardening for containerised services: segmentation and egress filtering with DOCKER-USER

## Notes
- All projects must generate `artifacts/pcap/traffic_e2.pcap` in E2 and pass `tools/validate_pcap.py`.
- Bash automation is expected for most projects in this group; scripts should be deterministic and idempotent.
- All activities are laboratory-only. Do not use these tools or scripts on real networks.

See `../00_common/README_STANDARD_RC2026.md` for repository structure and evidence requirements.

# 00_common/tools/pcap_rules — Per-Project Validation Rules

Thirty JSON rule files, one per project code, consumed by [`../validate_pcap.py`](../validate_pcap.py). Each file defines a sequence of `tshark` display-filter rules with packet-count thresholds that the E2 capture must satisfy.

## File Index

| File | Project group | Target protocol(s) |
|---|---|---|
| `S01.json` – `S20.json` | Group 1 — Network applications | TCP, UDP, HTTP, DNS, SMTP, POP3, TLS, gRPC and custom coordination protocols |
| `A01.json` – `A10.json` | Group 2 — Administration and security | OpenFlow, ARP, ICMP, DHCP, VXLAN, iptables markers |

Total: 30 JSON rule files plus this README index. Each rule file contains a `rules` array where every entry specifies `id`, `filter`, `condition` and `description`.

## Rule Structure (example)

```json
{
  "id": "R1",
  "filter": "tcp.dstport==5000 && tcp.flags.syn==1 && tcp.flags.ack==0",
  "condition": ">= 1",
  "description": "Connection initiation to the server (SYN)."
}
```

## Cross-References

Rules are referenced by project briefs in [`../../../01_network_applications/`](../../../01_network_applications/) (S-series) and [`../../../02_administration_security/`](../../../02_administration_security/) (A-series). The validator script [`../validate_pcap.py`](../validate_pcap.py) loads these files by project code.

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/tools/pcap_rules
```

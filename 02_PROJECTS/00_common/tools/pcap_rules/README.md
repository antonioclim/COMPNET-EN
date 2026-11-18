# 00_common/tools/pcap_rules — Per-Project Validation Rules

Thirty JSON rule files, one per project code, consumed by [`../validate_pcap.py`](../validate_pcap.py). Each file defines a sequence of `tshark` display-filter rules with explicit measurement thresholds that the E2 capture must satisfy.

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

## Measurement and complementary evidence

The default `measurement` is `frames`, which counts matching captured frames only. `field_occurrences` counts decoded field values and supports `aggregation: "max_per_stream"` for HTTP keep-alive evidence. `distinct_values` counts unique values, such as scanned destination ports. `tcp_commands` reassembles one TCP direction, deduplicates identical retransmissions and counts complete LF/CRLF command tokens from `commands`; gaps, conflicting retransmissions and unfinished lines are errors. Capture the handshake so relative sequence numbering starts at one.

For JSON, binary or another E1 framing choice, supply and test the corresponding decoder in the student validator. Do not equate TCP segments with application messages. Each manifest also lists `manual_checks`: correlate actual requests, replies, state changes, logs and tests as described in the [30-project scenario matrix](../../E2_CAPTURE_EVIDENCE_MATRIX.md). A filter match alone does not prove these semantics. Apply each check at the assessment stage specified in the canonical brief; E3 requirements are not moved into E2.

For local TLS test sessions, `--tls-keylog PATH` forwards the test key log to tshark. Keep session secrets outside Git. TLS 1.3 encrypted handshake records do not by themselves prove application delivery.

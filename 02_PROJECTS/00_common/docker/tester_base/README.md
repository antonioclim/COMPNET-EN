# 00_common/docker/tester_base — Reference Tester Image

Dockerfile and entrypoint script that define the E2 tester container pattern. The tester starts a packet capture, executes the pytest E2 suite against the application container and validates the resulting PCAP file before exiting.

## File Index

| File | Description | Lines |
|---|---|---|
| [`Dockerfile`](Dockerfile) | Image definition: Python 3, tshark, tcpdump, pytest | 20 |
| [`entrypoint.sh`](entrypoint.sh) | Orchestration script: tcpdump → pytest → validate_pcap.py | 33 |

## Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  tcpdump     │────►│  pytest      │────►│  stop        │────►│  validate    │
│  (start)     │     │  -m e2       │     │  tcpdump     │     │  _pcap.py    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

## Usage

Students copy this directory into their project and reference it from `docker-compose.yml`:

```yaml
services:
  tester:
    build: ./docker/tester_base
    depends_on:
      - <application-service>
    volumes:
      - ./artifacts:/artifacts
      - ./tools:/tools
      - ./tests:/tests
```

## Cross-References

The entrypoint invokes [`../../tools/validate_pcap.py`](../../tools/validate_pcap.py) with project-specific rules from [`../../tools/pcap_rules/`](../../tools/pcap_rules/). The lifecycle is documented in [`../../assets/puml/fig-tester-container-lifecycle.puml`](../../assets/puml/fig-tester-container-lifecycle.puml).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/docker/tester_base
```

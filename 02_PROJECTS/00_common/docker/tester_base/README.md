# 00_common/docker/tester_base — Reference Tester Image

Dockerfile and entrypoint script that define the E2 tester container pattern. The tester starts a packet capture, executes the pytest E2 suite against the application container and validates the resulting PCAP file before exiting.

## File Index

| File | Description |
|---|---|
| [`Dockerfile`](Dockerfile) | Starting image: Python 3, tshark and tcpdump; install pytest and the chosen test dependencies |
| [`entrypoint.sh`](entrypoint.sh) | Orchestration script: tcpdump → pytest → validate_pcap.py |

## Workflow

The tester starts capture, checks that it is running, executes `pytest -m e2`, stops and waits for capture, then runs the capture validator. Failed tests still reach capture cleanup and validation. The final status preserves a pytest failure; otherwise a capture failure returns 2 and the validator status is propagated. EXIT, INT and TERM handlers bound cleanup and prevent an orphaned capture.

## Usage

Students copy this directory into their project. Install `pytest` and any project-specific test dependencies through the commented dependency-installation section in the Dockerfile, placing `requirements.txt` in the build context. Then reference it from `docker-compose.yml` (replace the application-service placeholder):

```yaml
services:
  tester:
    build: ./docker/tester_base
    environment:
      PROJECT_CODE: S01  # Set this to the selected project code.
    depends_on:
      - <application-service>
    volumes:
      - ./artifacts:/artifacts
      - ./tools:/work/tools:ro
      - ./tests:/work/tests:ro
```

## Cross-References

The entrypoint invokes [`../../tools/validate_pcap.py`](../../tools/validate_pcap.py) with project-specific rules from [`../../tools/pcap_rules/`](../../tools/pcap_rules/). The lifecycle is documented in [`../../assets/puml/fig-tester-container-lifecycle.puml`](../../assets/puml/fig-tester-container-lifecycle.puml).

## Selective Clone

```bash
git sparse-checkout set 02_PROJECTS/00_common/docker/tester_base
```

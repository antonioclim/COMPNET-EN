# Portainer Benefits for RC2026 Projects (S01–S15)

> **Detailed per-project guides** live alongside each project brief:
> `02_PROJECTS/01_network_applications/assets/PORTAINER/S{NN}/PORTAINER_GUIDE_S{NN}.md`
>
> This file is the overview map. The per-project files contain container-specific debugging checklists, log-observation strategies and console commands tailored to each project's architecture.

## Why Every Project Benefits

The RC2026 standard requires a `docker/docker-compose.yml` for every project. The E2 gate — `make e2` — spins up the student's application alongside a `tester` container that runs `pytest`, captures traffic with `tcpdump` and validates the PCAP. At minimum, every project runs **two containers** (service + tester). Several projects run five or more.

Portainer sits at `http://localhost:9050` throughout the semester. Once installed (see `INIT_GUIDE/`), it requires no further configuration and shows every container regardless of which project created it.

## What Portainer Gives You During Project Work

Across all projects, Portainer addresses four recurring situations:

1. **"Did my stack actually start?"** — The tester container may exit immediately with a non-zero code if the application container is not ready. Portainer shows the exit code and the logs in two clicks, without guessing which container name to `docker logs`.

2. **"What ports are published?"** — Several projects use dynamic or unusual port ranges (S02: 60000–60100, S11: five different ports). The Published Ports column in Portainer lists them all.

3. **"Why did the tester fail?"** — Open the tester's logs. The pytest output is there: which test failed, what assertion tripped, what the expected vs actual values were. No need to re-run `docker compose up` with `--abort-on-container-exit` to see it.

4. **"What is happening inside my service?"** — Open the application container's logs. For long-running services (S05 load balancer, S06 broker, S11 microservices), the log stream shows incoming requests, routing decisions and error conditions in real time.

## Per-Project Map

The table below shows the expected container architecture and the Portainer benefit tier for each project. Tiers are:

- 🟩 **Baseline** — 2 containers (service + tester). Portainer helps with E2 debugging but adds no architectural insight.
- 🟨 **Useful** — 3 containers or notable port complexity. Portainer helps distinguish the services and verify port assignments.
- 🟧 **Significant** — 4+ containers or multi-protocol architecture. Portainer's network and log views become genuinely productive.
- 🟥 **High** — 5+ containers with inter-service communication, failover testing or multi-network segmentation. Portainer is the most practical way to observe the system.

| Project | Expected E2 Containers | Key Portainer Benefit | Tier |
|:-------:|----------------------|----------------------|:----:|
| **S01** | `chat-server` + `tester` (2) | Verify server started before tester connects; check tester exit code when multi-client tests fail | 🟩 |
| **S02** | `ftp-server` + `tester` (2) | Verify passive data-port range (60000–60100) is published; observe control vs data channel in server logs | 🟨 |
| **S03** | `http-server` + `tester` (2) | Verify raw-socket HTTP server started; log inspection for malformed request handling | 🟩 |
| **S04** | `proxy` + `origin` + `tester` (3) | Two network hops visible: tester → proxy → origin. Logs on the proxy show filter decisions (allow/block). Published ports: 3128 (proxy) and 8080 (origin) | 🟨 |
| **S05** | `lb` + `backend1` + `backend2` + `backend3` + `tester` (5) | **Round-robin observation in parallel log tabs** (identical to S11 seminar exercise). Stop a backend from Portainer to test failover. Health-check requests visible in backend logs | 🟥 |
| **S06** | `broker` + `publisher` + `subscriber1` + `subscriber2` + `tester` (4–5) | Observe topic routing in broker logs. Verify both subscribers receive messages. Disconnect a subscriber from Portainer to test reconnection behaviour | 🟧 |
| **S07** | `resolver` + `upstream-stub` + `tester` (3) | Resolver logs show local-zone hits vs forwarded queries vs cache hits. Verify upstream container is reachable | 🟨 |
| **S08** | `smtp-server` + `pop3-server` + `tester` (2–3) | Two protocol endpoints on different ports (2525, 2110). Verify both services started. SMTP logs show DATA command and dot-terminator processing | 🟨 |
| **S09** | `tunnel-server` + `echo-svc` + `http-svc` + `tester` (4) | Multiplexed sessions visible in tunnel-server logs: session IDs, routing to the correct backend. Backend logs confirm demultiplexed traffic arrives correctly | 🟧 |
| **S10** | `sync-server` + `sync-client` + `tester` (3) | Observe manifest exchange and conflict resolution in server logs. Verify file hash comparisons | 🟨 |
| **S11** | `gateway` + `registry` + `svc-a` + `svc-b` + `svc-c` + `discovery` + `tester` (7) | **Maximum complexity.** Network topology with 7 containers. Heartbeat/registration traffic in registry logs. Failover: stop a microservice from Portainer, observe gateway's 503 response. Service-discovery multicast visible in logs | 🟥 |
| **S12** | `tls-server` + `tls-client` + `tester` (3) | Verify TLS server started (log shows "listening on 5443"). Tester logs show handshake outcome (success/failure, cipher negotiated) | 🟨 |
| **S13** | `grpc-server` + `raw-protobuf-server` + `tester` (3) | Two servers on different ports (50051, 50052). Verify both started. gRPC server logs show unary vs streaming method invocations | 🟨 |
| **S14** | Mininet-based + `tester` (2–3) | Lower benefit — routing runs inside Mininet. Portainer helps verify the Mininet host container started and the tester completed | 🟩 |
| **S15** | `iot-gateway` + `sensor-sim` + `tester` (3–4) | Two traffic types: UDP telemetry (5515) and HTTP API (8080). Gateway logs show ingestion rate, validation failures and API responses. Sensor simulator logs confirm send rate | 🟧 |

## Per-Project Guides

Each project has a dedicated Portainer guide at:

```text
02_PROJECTS/01_network_applications/assets/PORTAINER/S{NN}/PORTAINER_GUIDE_S{NN}.md
```

These guides contain the project-specific container architecture, log-observation strategies, console commands and debugging checklists referenced in the table above. Open the one that matches your project code.

## General Recommendations

1. **Keep Portainer open during `make e2`.** Watch the containers start, run and (ideally) succeed. If the tester exits red, its logs are your first stop.

2. **Use the Console for quick checks.** Need to verify a config file inside the container? Click Console instead of typing `docker exec -it <long-name> cat /app/config.yaml`.

3. **Use the Networks view for multi-container projects (S04, S05, S06, S09, S11, S15).** Confirm that your containers are on the same Docker network and can reach each other by name.

4. **Portainer does not replace Wireshark.** It shows application-level logs and Docker state. For packet-level analysis (TCP handshakes, retransmissions, protocol fields), you still need the PCAP.

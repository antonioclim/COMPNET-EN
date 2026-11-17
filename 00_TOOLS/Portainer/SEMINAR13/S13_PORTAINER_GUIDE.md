# S13 — Portainer Integration (Instructor Notes)

> **Execution route:** PowerShell commands in this guide use Docker Desktop on
> Windows. With the primary MININET-SDN OVA, run the Compose commands in the Linux
> guest and test guest endpoints there; translate `..\folder` to `../folder`.
> Windows `127.0.0.1:2222` is the OVA SSH forward, not automatically an S10
> container endpoint. Use the [environment routes](../../../00_APPENDIX/docs/environment_routes.md)
> and the canonical seminar README for the chosen route.

**Reading the dashboard:** a port mapping is configuration, a running container is
process state and a successful application request is service evidence. Record
these separately. `EXPOSE`/Compose `expose` documents a container port; it does not
create an access-control boundary. On normal Linux bridge networks the daemon
host can reach container addresses even without published ports. Docker Desktop's
Windows host normally accesses them through published ports. See
[Docker port publishing](https://docs.docker.com/engine/network/port-publishing/).


## Context

Seminar 13 deploys intentionally vulnerable services — DVWA, WebGoat and a backdoored vsftpd 2.3.4 — inside Docker containers on a fixed-IP subnet. Students scan and enumerate these targets from a separate "tool container" (`nicolaka/netshoot`). The session is conceptually dense: ethical framing, reconnaissance, port scanning, banner grabbing, basic exploitation — packed into roughly 40 minutes.

Portainer enters this seminar not as a convenience tool but as a **perspective shift**. The administrator sees declared containers, images, addresses and mappings; the scanner observes reachability and protocol responses. These are different kinds of evidence and can disagree. This duality — asymmetric information between attacker and defender — is one of the foundational ideas in network security, and Portainer makes it tangible.

## Pedagogical Objectives Augmented

| Objective already in the seminar | What Portainer adds |
|---|---|
| Reconnaissance: discover hosts and open ports | Administrator sees declared addresses and mappings; scans test actual listeners and reachability |
| Service enumeration: version detection via banners | Compare the Docker image tag (admin view) with the banner returned by `nmap -sV` (attacker view) |
| Understand attack surfaces | Published-ports column lists configured mappings, which must be combined with listener, routing and application checks |
| Ethical framing: attacker vs defender roles | Portainer embodies the defender perspective throughout the exercise |
| Detect scanning activity | Compare application logs with a packet capture; a connection-only scan may produce no HTTP access entry |

Use two controlled probes: a TCP connect scan and a real HTTP request. Record whether each appears in application logs and in a packet capture. A missing HTTP access entry after a connect scan is a valid result: opening and closing TCP does not necessarily send an HTTP request. Docker logs show stdout/stderr; file-based service logs may require a different view.

## How to Use It — Instructor Perspective

### Pre-seminar checklist

- [ ] Portainer running on 9050
- [ ] No leftover containers from previous seminars
- [ ] Images pre-pulled (these are large — do this well in advance):
  ```powershell
  docker pull vulnerables/web-dvwa
  docker pull webgoat/webgoat-8.0
  docker pull clintmint/vsftpd-2.3.4:1.0
  docker pull nicolaka/netshoot
  ```

---

### After `docker compose up` (minutes 4–8)

Start the pentest lab:

```powershell
docker compose -f S13_Part02_Config_Docker_Compose_Pentest.yml up -d
```

**Administrator's view.** Open Portainer → Containers:

The table shows the default host ports. If `.env` overrides them, use the values
shown by `docker compose -f S13_Part02_Config_Docker_Compose_Pentest.yml config`
and the actual container mappings for every host-side URL below.

| Container      | Image                         | Published Ports          |
|----------------|-------------------------------|--------------------------|
| `dvwa`         | `vulnerables/web-dvwa`        | **8888 → 80**            |
| `webgoat`      | `webgoat/webgoat-8.0`         | **8080 → 8080**          |
| `vsftpd_vuln`  | `clintmint/vsftpd-2.3.4:1.0` | **2121 → 21, 6200 → 6200** |

> *▸ "As administrators, we see configuration and container state. We still need protocol requests or listener checks to establish that a service is ready. The scanner provides an independent observation of reachability."*

**Network with static IPs.** Open `dvwa` in Portainer and follow its network link.
`pentestnet` is the Compose network key; Docker normally prefixes its actual name
with the Compose project name, for example `s13_pentestnet`. Do not assume that an
unprefixed Docker network named `pentestnet` exists.

| Container      | Static IP    |
|----------------|-------------|
| `dvwa`         | 172.20.0.10 |
| `webgoat`      | 172.20.0.11 |
| `vsftpd_vuln`  | 172.20.0.12 |

Share these IPs with students (or write them on the board). In a real engagement they would need to discover them; here you skip that step to save time.

**Service health check.** Before any scanning, verify that the targets are actually running:

1. **DVWA:** click → **Logs** → look for the Apache startup line. Also test `curl http://localhost:8888` from PowerShell. Note: DVWA requires a one-time database initialisation at `http://localhost:8888/setup.php` → "Create / Reset Database."

2. **WebGoat:** click → **Logs** → look for "Started WebGoat." This container is slow to start (30–60 seconds).

3. **vsftpd:** click → **Logs** → the container runs `start-vsftpd && tail -f /dev/null`. Inspect any available startup errors, then test the FTP greeting. A long-running `tail` process can keep the container running even when its service is unavailable.

> *▸ "As administrators, we verify that the services are actually working. A scan that finds nothing may mean the service is not running — or the scanner is wrong. Portainer gives supporting state and logs; only a successful service-level check addresses that possibility."*

---

### Tool container and scan detection (minutes 12–21)

Launch the scanner:

```powershell
$s13Networks = @(docker inspect dvwa --format '{{range $name, $_ := .NetworkSettings.Networks}}{{println $name}}{{end}}' | Where-Object { $_.Trim() })
if ($LASTEXITCODE -ne 0 -or $s13Networks.Count -ne 1) {
    throw 'Expected one network on the existing dvwa container; inspect its configuration.'
}
$s13Network = $s13Networks[0].Trim()
docker run -it --rm --name scanner --network $s13Network nicolaka/netshoot bash
```

Refresh Portainer. A fourth container (`scanner`) appears on that same network,
with no published ports. The snippet above is PowerShell; in the VM route, read
the network name from `docker inspect dvwa` and pass that exact name to `--network`.

> *▸ "The scanner is on the same network as the targets. From Windows using Docker Desktop, use published loopback endpoints. From the scanner, use the Compose service network. On the Linux daemon host, direct bridge-IP access normally also works."*

**Dual-screen observation.** Open the target logs and run a TCP connect scan from the scanner. Save the actual result, including an absence of application log entries. Then run `curl -v http://172.20.0.10/` from the same scanner and compare. If Docker logs contain no access log, inspect the service’s configured log destination. A packet capture provides transport evidence independently of application logging.

> *▸ "Compare the request we sent, the packets captured and the application events logged. They describe different layers; an empty application log does not prove that no scan occurred."*

---

### Version disclosure and the backdoor port (minutes 27–33)

**Image tags vs banners.** In Portainer, the image tag for vsftpd reads `clintmint/vsftpd-2.3.4:1.0`. An attacker running `nmap -sV` against port 21 sees the banner `vsFTPd 2.3.4`. The information matches.

> *▸ "An image tag and a service banner are claims about identity. Record both, but do not treat either as proof of the exact binary or vulnerability state."*

**The backdoor port.** In Portainer, `vsftpd_vuln` shows two published port mappings: `2121 → 21` and `6200 → 6200`. Port 6200 is unusual for an FTP server.

> *▸ "This intentionally vulnerable image maps port 6200 for the backdoor exercise. A mapping does not mean a listener is active. Record its state before and after the authorised local exercise, then explain the observed difference."*

---

### Closing (minutes 37–40)

> *▸ "Today we worked from two perspectives at the same time:*
> - *The attacker: discovery through scanning, enumeration via banners, exploitation.*
> - *The administrator (Portainer): configuration and process visibility, log inspection and correlation with network evidence.*
>
> *A good administrator uses observability tools — Portainer, Prometheus, Grafana and the ELK stack — to see what the attacker would see, before the attacker sees it."*

## How to Use It — Student Perspective

Students receive `S13_PORTAINER_TASKS.md` with six tasks structured around the attacker-vs-administrator duality. Task P1 asks them to fill in the infrastructure inventory from Portainer *without scanning anything*. Task P3 reverses the perspective: students watch the target logs while their own scans run. Task P5 compares version information obtained from two sources (Portainer image tag vs nmap banner). The post-exercise reflection (Task P6) explicitly asks what each side knew that the other did not.

The tasks are designed so that the security concepts emerge from observation rather than memorisation.

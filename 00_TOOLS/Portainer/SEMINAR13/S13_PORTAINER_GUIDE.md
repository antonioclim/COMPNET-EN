# S13 — Portainer Integration (Instructor Notes)

## Context

Seminar 13 deploys intentionally vulnerable services — DVWA, WebGoat and a backdoored vsftpd 2.3.4 — inside Docker containers on a fixed-IP subnet. Students scan and enumerate these targets from a separate "tool container" (`nicolaka/netshoot`). The session is conceptually dense: ethical framing, reconnaissance, port scanning, banner grabbing, basic exploitation — packed into roughly 40 minutes.

Portainer enters this seminar not as a convenience tool but as a **perspective shift**. Everything the attacker must discover through scanning, the administrator already sees in the dashboard. This duality — asymmetric information between attacker and defender — is one of the foundational ideas in network security, and Portainer makes it tangible.

## Pedagogical Objectives Augmented

| Objective already in the seminar | What Portainer adds |
|---|---|
| Reconnaissance: discover hosts and open ports | Administrator already sees all containers, IPs and ports — the asymmetry is immediate |
| Service enumeration: version detection via banners | Compare the Docker image tag (admin view) with the banner returned by `nmap -sV` (attacker view) |
| Understand attack surfaces | Published-ports column is literally a list of the attack surface |
| Ethical framing: attacker vs defender roles | Portainer embodies the defender perspective throughout the exercise |
| Detect scanning activity | Log tailing on target containers shows incoming connection attempts as they happen |

The scan-detection angle is particularly effective. Students run `nmap` from the scanner container while watching the target's logs in Portainer. They see, in real time, that the target "feels" the scan — connection attempts appear in the Apache or vsftpd logs. This makes the abstract concept of "noisy scanning" concrete.

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

| Container      | Image                         | Published Ports          |
|----------------|-------------------------------|--------------------------|
| `dvwa`         | `vulnerables/web-dvwa`        | **8888 → 80**            |
| `webgoat`      | `webgoat/webgoat-8.0`         | **8080 → 8080**          |
| `vsftpd_vuln`  | `clintmint/vsftpd-2.3.4:1.0` | **2121 → 21, 6200 → 6200** |

> *▸ "As administrators, we can see everything: which services are running, on which ports, and which images they use. The attacker does not have this information — they must discover it through scanning."*

**Network with static IPs.** Navigate to **Networks** → **pentestnet**:

| Container      | Static IP    |
|----------------|-------------|
| `dvwa`         | 172.20.0.10 |
| `webgoat`      | 172.20.0.11 |
| `vsftpd_vuln`  | 172.20.0.12 |

Share these IPs with students (or write them on the board). In a real engagement they would need to discover them; here you skip that step to save time.

**Service health check.** Before any scanning, verify that the targets are actually running:

1. **DVWA:** click → **Logs** → look for the Apache startup line. Also test `curl http://localhost:8888` from PowerShell. Note: DVWA requires a one-time database initialisation at `http://localhost:8888/setup.php` → "Create / Reset Database."

2. **WebGoat:** click → **Logs** → look for "Started WebGoat." This container is slow to start (30–60 seconds).

3. **vsftpd:** click → **Logs** → the container runs `start-vsftpd && tail -f /dev/null`. If FTP fails to start, the log will show why.

> *▸ "As administrators, we verify that the services are actually working. A scan that finds nothing may mean the service is not running — or the scanner is wrong. Portainer removes the first possibility."*

---

### Tool container and scan detection (minutes 12–21)

Launch the scanner:

```powershell
docker run -it --rm --name scanner --network pentestnet nicolaka/netshoot bash
```

Refresh Portainer. A fourth container (`scanner`) appears on `pentestnet`, with no published ports.

> *▸ "The scanner is on the same network as the targets. From the host, the 172.20.0.x addresses are not directly reachable — but from inside the container they are."*

**Dual-screen observation.** While students run `nmap` in the scanner, open the DVWA and vsftpd logs in Portainer with auto-refresh. As nmap probes port 80 on DVWA, connection entries appear in the Apache log. As it probes port 21 on vsftpd, FTP banner negotiations show up.

> *▸ "From Portainer we can see how the targets 'feel' the scan. DVWA receives new connections; vsftpd receives banner requests. This is the defender's perspective."*

---

### Version disclosure and the backdoor port (minutes 27–33)

**Image tags vs banners.** In Portainer, the image tag for vsftpd reads `clintmint/vsftpd-2.3.4:1.0`. An attacker running `nmap -sV` against port 21 sees the banner `vsFTPd 2.3.4`. The information matches.

> *▸ "The administrator knows the version from the Docker image tag. The attacker infers it from the banner. They usually match — which is why banners are a security issue."*

**The backdoor port.** In Portainer, `vsftpd_vuln` shows two published port mappings: `2121 → 21` and `6200 → 6200`. Port 6200 is unusual for an FTP server.

> *▸ "Port 6200 is the backdoor port in vsftpd 2.3.4. The administrator sees it in the Docker configuration. The attacker discovers it with nmap. The question is: why is anything listening on port 6200?"*

---

### Closing (minutes 37–40)

> *▸ "Today we worked from two perspectives at the same time:*
> - *The attacker: discovery through scanning, enumeration via banners, exploitation.*
> - *The administrator (Portainer): full visibility, log monitoring, detection of suspicious activity.*
>
> *A good administrator uses observability tools — Portainer, Prometheus, Grafana and the ELK stack — to see what the attacker would see, before the attacker sees it."*

## How to Use It — Student Perspective

Students receive `S13_PORTAINER_TASKS.md` with six tasks structured around the attacker-vs-administrator duality. Task P1 asks them to fill in the infrastructure inventory from Portainer *without scanning anything*. Task P3 reverses the perspective: students watch the target logs while their own scans run. Task P5 compares version information obtained from two sources (Portainer image tag vs nmap banner). The post-exercise reflection (Task P6) explicitly asks what each side knew that the other did not.

The tasks are designed so that the security concepts emerge from observation rather than memorisation.

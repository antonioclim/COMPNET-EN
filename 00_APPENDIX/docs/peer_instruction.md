# 🗳️ Peer Instruction Questions — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Preparatory materials:** Lab environment setup

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)   │  Read the question and think individually              │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec)  │  Vote for your answer (A/B/C/D) — no discussion!       │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)   │  Discuss with your neighbour — convince them!          │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec)  │  Re-vote — you may change your answer                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)   │  Instructor explains the correct answer                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Question 1: WSL2 vs Virtual Machine

> 💭 **PREDICTION:** Before reading the options, think: what is different between WSL2 and a traditional VM like VirtualBox?

### Scenario
You installed Ubuntu 22.04 in WSL2 on Windows 11. Your colleague installed Ubuntu 22.04 in a VirtualBox VM.

### Question
Which statement about the differences between these two configurations is **CORRECT**?

### Options
- **A)** WSL2 emulates hardware, VirtualBox runs a real Linux kernel
- **B)** WSL2 runs a real Linux kernel, VirtualBox emulates a Linux kernel
- **C)** Both run real Linux kernels, but WSL2 shares resources more efficiently with Windows
- **D)** WSL2 and VirtualBox are technically identical, only the interface differs

### Correct Answer
**C** — WSL2 runs a complete Linux kernel (not emulated) in a lightweight VM optimised for Windows integration. VirtualBox also runs a real kernel but with more overhead and complete isolation.

### Targeted Misconception
Many students confuse WSL1 (which translated system calls) with WSL2 (which runs a real Linux kernel).

### Instructor Notes
- **Target accuracy:** ~50% on first vote
- **After discussion:** Demonstrate with `uname -r` in WSL2 and explain "-microsoft-standard-WSL2"
- **Timing:** 7-8 minutes total

---

## Question 2: Container vs Docker Image

> 💭 **PREDICTION:** If you have a cake recipe and a baked cake, which is the image and which is the container?

### Scenario
```bash
docker pull nginx:latest
docker run -d --name web1 nginx:latest
docker run -d --name web2 nginx:latest
```

### Question
After executing the commands above, how many **images** and how many **containers** will exist?

### Options
- **A)** 2 images, 2 containers — each `run` creates a new image
- **B)** 1 image, 2 containers — both containers use the same image
- **C)** 2 images, 1 container — only the last `run` counts
- **D)** 1 image, 1 container — `web2` overwrites `web1`

### Correct Answer
**B** — A single `nginx:latest` image is downloaded and two independent containers (`web1` and `web2`) are created from it. The image is the template, containers are instances.

### Targeted Misconception
Students frequently confuse images with containers. They believe each container has its own image or that running a new container replaces the old one.

### Instructor Notes
- **Target accuracy:** ~40% on first vote
- **Key concept:** Image = read-only blueprint, Container = runnable instance
- **After discussion:** Demonstrate with `docker images` and `docker ps`
- **Analogy:** Image = plastic mould, Container = cast object

---

## Question 3: Port Mapping in Docker

> 💭 **PREDICTION:** If a container listens on port 80, can you access the service from your browser at `localhost:80`?

### Scenario
```bash
docker run -d --name nginx1 -p 8080:80 nginx
docker run -d --name nginx2 -p 8081:80 nginx
```

### Question
Which URLs will work to access the two nginx servers from the Windows browser?

### Options
- **A)** `localhost:80` for nginx1, `localhost:80` for nginx2
- **B)** `localhost:8080` for nginx1, `localhost:8081` for nginx2
- **C)** `localhost:80` for both — Docker does automatic load balancing
- **D)** No URL will work — you must use the container's IP address

### Correct Answer
**B** — The format `-p HOST:CONTAINER` maps the host port to the container port. nginx1 is accessible on 8080, nginx2 on 8081. Internally, both containers listen on port 80.

### Targeted Misconception
Confusion between internal (container) and external (host) ports. Students believe the container port is automatically accessible or that it must match.

### Instructor Notes
- **Target accuracy:** ~55% on first vote
- **Key concept:** `-p HOST:CONTAINER` — HOST is what you see from outside
- **After discussion:** Draw the port mapping diagram on the board

---

## Question 4: Localhost in Container vs Host

> 💭 **PREDICTION:** If you run `curl localhost:9000` from inside a container, will you access Portainer?

### Scenario
```bash
# On host (Ubuntu WSL):
docker run -d --name portainer -p 9000:9000 portainer/portainer-ce

# Verification from host:
curl localhost:9000  # ✓ Works

# Enter another container:
docker run -it --rm alpine sh
# From inside the alpine container:
wget -qO- localhost:9000  # ???
```

### Question
What happens when you try to access `localhost:9000` from inside the Alpine container?

### Options
- **A)** Works — `localhost` is the same for all containers
- **B)** Fails — `localhost` in a container refers to the container itself, not the host
- **C)** Works — Docker automatically redirects `localhost` to the host
- **D)** Fails — containers have no network access

### Correct Answer
**B** — `localhost` (127.0.0.1) inside a container refers to that container's loopback interface, not the host. To access host services, you need `host.docker.internal` or the host's IP.

### Targeted Misconception
This is one of the most common confusions: assuming `localhost` is global. In reality, each container has its own network namespace.

### Instructor Notes
- **Target accuracy:** ~35% on first vote (difficult)
- **Key concept:** Network namespaces — each container has its own network stack
- **After discussion:** Demonstrate with `docker exec` and show `ip addr` in the container

---

## Question 5: Docker Service in WSL

> 💭 **PREDICTION:** After restarting Windows, will Docker work immediately in WSL?

### Scenario
```
1. You configure the complete environment (WSL + Docker + Portainer)
2. Everything works perfectly
3. You restart the computer
4. You open WSL and run: docker ps
```

### Question
What will the `docker ps` command display immediately after restarting Windows?

### Options
- **A)** The list of containers that were running before restart
- **B)** Error "Cannot connect to Docker daemon" — the service doesn't start automatically
- **C)** Empty list — containers are stopped but Docker works
- **D)** Error "docker: command not found" — Docker needs to be reinstalled

### Correct Answer
**B** — In WSL2, the Docker service does not start automatically at boot (unlike Docker Desktop). You must run `sudo service docker start` manually or configure auto-start.

### Targeted Misconception
Students who have used Docker Desktop expect Docker to start automatically. In native WSL, services must be started manually or explicitly configured.

### Instructor Notes
- **Target accuracy:** ~45% on first vote
- **Key concept:** WSL doesn't have a traditional init system (systemd) by default
- **After discussion:** Show the auto-start configuration from Prerequisites (section 10)
- **In previous years, students often missed this step and thought their Docker installation was broken**

---

## Questions Summary

| # | Topic | Difficulty | Target Accuracy |
|---|-------|------------|-----------------|
| 1 | WSL2 vs VM | Medium | ~50% |
| 2 | Container vs Image | Medium | ~40% |
| 3 | Port Mapping | Medium | ~55% |
| 4 | Localhost in Container | Difficult | ~35% |
| 5 | Docker Service WSL | Medium | ~45% |

---

## Additional Resources

- [docs/misconceptions.md](misconceptions.md) — Detailed common errors
- [docs/concept_analogies.md](concept_analogies.md) — Concept analogies
- [glossary.md](glossary.md) — Technical term definitions

---

*Peer Instruction Questions — Week 0: Lab Environment Setup*
*Computer Networks — ASE Bucharest, CSIE*
*Version: 1.6.0 | January 2026*

# 🖧 Computer Networks Lab — Environment Setup Guide

> **Alternative WSL2 setup.** The ASE classroom route uses the [MININET-SDN VirtualBox appliance](../../01_GUIDE_MININET-SDN/). Use that guide for an imported OVA; do not run the WSL installation steps inside the appliance.
>
> This guide prepares a separate WSL environment for suitable container-based exercises. Mininet/OpenFlow work uses the dedicated VM route unless the exercise explicitly supplies a WSL alternative.
> Bucharest University of Economic Studies — Faculty of Cybernetics, Statistics and Economic Informatics
> *Economic Informatics & AI in Economics and Business Programmes*

---

## 📋 Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Standard Credentials](#3-standard-credentials)
4. [Step 1: Enable WSL2](#4-step-1-enable-wsl2)
5. [Step 2: Install Ubuntu 22.04](#5-step-2-install-ubuntu-2204)
6. [Step 3: Install Docker in WSL](#6-step-3-install-docker-in-wsl)
7. [Step 4: Install Portainer CE](#7-step-4-install-portainer-ce)
8. [Step 5: Install Wireshark](#8-step-5-install-wireshark)
9. [Step 6: Python Packages](#9-step-6-python-packages)
10. [Step 7: Auto-start Configuration](#10-step-7-auto-start-configuration-optional)
11. [Final Verification](#11-final-verification)
12. [Troubleshooting](#12-troubleshooting)
13. [Quick Reference Sheet](#13-quick-reference-sheet)

---

## 1. Introduction

### 1.1 Purpose of This Guide

This guide prepares Ubuntu in WSL2 for container-based networking exercises. Its checks establish prerequisite availability; each chosen exercise still requires its own functional test. The environment supports:

- **Running isolated network experiments** using Docker containers
- **Capturing and analysing network traffic** with Wireshark
- **Visually managing containers** through the Portainer web interface
- **Automating network interactions** using Python

### 1.2 Why This Architecture?

This alternative places Docker Engine and the course Python environment inside Ubuntu on WSL2. Keep commands in that Linux environment so that the Docker socket, installed Python packages and exercise files refer to the same machine. Docker Desktop is a separate optional route; it is not needed for this one.

### 1.3 What You Will Install

| Component | Version | Purpose |
|-----------|---------|---------|
| WSL2 | 2.x | Windows Subsystem for Linux |
| Ubuntu | 22.04 LTS | Linux distribution |
| Docker | Version installed from the selected Ubuntu repository | Container runtime |
| Docker Compose | v2 plugin (`docker compose`) | Multi-container orchestration |
| Portainer CE | Optional; selected in the [Portainer guide](../Portainer/INIT_GUIDE/) | Web-based container management |
| Wireshark | 4.4.x | Network protocol analyser |
| Python | 3.10+ in a Linux virtual environment | Packages for the selected exercises |

### 1.4 Time Estimate

- **Total installation time:** 30-45 minutes
- **Requires restart:** Yes (after WSL2 installation)
- **Internet connection:** Required for downloads

---

## 2. Architecture Overview

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS 11                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Wireshark     │  │    Browser      │  │   PowerShell    │  │
│  │   (Capture)     │  │  (Portainer)    │  │   (Commands)    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              vEthernet (WSL) - Virtual Network              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐  │
│  │                        WSL2                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  Ubuntu 22.04 LTS                    │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │              Docker Engine                   │    │  │  │
│  │  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │    │  │  │
│  │  │  │  │Container│ │Container│ │Portainer│       │    │  │  │
│  │  │  │  │   A     │ │   B     │ │  :9000  │       │    │  │  │
│  │  │  │  └─────────┘ └─────────┘ └─────────┘       │    │  │  │
│  │  │  │         Docker Network (bridge)             │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Network Flow

1. **Docker containers** communicate through Docker's internal bridge network
2. **Traffic exits** via the WSL2 virtual network interface
3. **Wireshark on Windows** can capture traffic crossing the WSL virtual interface; internal container and loopback traffic may require capture inside Linux
4. **Portainer** is accessible via `localhost:9050` from the Windows browser

### 2.3 Port Mapping

| Service | Container Port | Host Port | Access URL |
|---------|----------------|-----------|------------|
| Portainer HTTP | 9000 | 127.0.0.1:9050 | http://localhost:9050 |

The optional course setup does not publish ports 9443 or 8000. Port 9000 on the host remains available for the S10 SSH tunnel.

---

## 3. Standard Credentials

> The following are teaching-account defaults. Preserve existing personal accounts and Portainer credentials. Shared lab credentials are used only with the local access configuration in this guide.

### 3.1 Ubuntu WSL User

| Field | Value |
|-------|-------|
| **Username** | `stud` |
| **Password** | `stud` |

This user is created during Ubuntu installation and has `sudo` privileges.

### 3.2 Portainer Administrator

| Field | Value |
|-------|-------|
| **Username** | `stud` |
| **Password** | `studstudstud` |
| **Access URL** | http://localhost:9050 |

> 📝 **Note:** Portainer requires a minimum 12-character password, hence `studstudstud`.

---

## 4. Step 1: Enable WSL2

### 4.1 What Is WSL2?

**Windows Subsystem for Linux 2 (WSL2)** is a compatibility layer that enables running a genuine Linux kernel directly on Windows. Alike WSL1, which translated Linux system calls, WSL2 runs a complete Linux kernel in a lightweight virtual machine, providing:

- Complete system call compatibility
- Dramatically improved file system performance
- Full Docker support without emulation
- Native Linux networking capabilities

### 4.2 System Requirements

- **Operating System:** Windows 10 version 2004+ or Windows 11
- **Architecture:** 64-bit processor with virtualisation support
- **RAM:** Minimum 4GB (8GB+ recommended)
- **BIOS:** Virtualisation enabled (VT-x/AMD-V)

### 4.3 Installation Steps

#### Step 1: Open PowerShell as Administrator

1. Press `Win + X` or right-click the Start button
2. Select **"Windows Terminal (Admin)"** or **"PowerShell (Admin)"**
3. Click **"Yes"** at the User Account Control prompt

#### Step 2: Install WSL2

Execute the following command:

```powershell
wsl --install --no-distribution
```

This prepares the WSL platform without also creating an unintended default Ubuntu distribution. System-feature installation can require elevation; distribution installation in section 5 is performed under the Windows account that will use the labs. If elevation requires a different administrator account, return to your normal account before section 5.

**What these commands do:**
- Enables the WSL optional feature
- Enables the Virtual Machine Platform feature
- Downloads and installs the Linux kernel
- Sets WSL2 as the default version

#### Step 3: Restart Your Computer

> 🔄 **A restart is required.** Save all work before continuing.

```powershell
Restart-Computer
```

Or restart manually through the Start menu.

#### Step 4: Verify Installation

After restart, open PowerShell and verify:

```powershell
wsl --set-default-version 2
wsl --status
```

The default WSL version should be 2. There may be no installed distribution yet; section 5 installs the named course distribution. Existing distributions are preserved.

### 4.4 Checklist

- [ ] `wsl --status` shows "Default Version: 2"
- [ ] No errors about virtualisation
- [ ] WSL service is running

---

## 5. Step 2: Install Ubuntu 22.04

### 5.1 Why Ubuntu 22.04 LTS?

**Ubuntu 22.04 LTS (Jammy Jellyfish)** is our chosen distribution because:

- **Long Term Support (LTS):** Security updates until April 2027
- **Stability:** Thoroughly tested, production-ready packages
- **Compatibility:** Excelslow Docker support and documentation
- **Community:** Largest Linux community for troubleshooting

### 5.2 Installation Steps

#### Step 1: Install Ubuntu from PowerShell

Open a normal PowerShell window under the Windows account that will use the labs. Check `wsl --list --verbose` first. If `Ubuntu-22.04` already exists, use it and preserve its accounts and data. For a fresh named distribution, execute:

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

**Command explanation:**
- `wsl --install`: Invokes the WSL installer
- `-d Ubuntu-22.04`: Specifies the distribution
- `--web-download`: Downloads from Microsoft servers (more reliable)

#### Step 2: Initial Setup

After the download completes, Ubuntu will start automatically. You will see:

```
Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username:
```

#### Step 3: Create the User Account

> For a new disposable teaching account, the laboratory convention is shown below. Preserve any existing Linux user and password.

```
Enter new UNIX username: stud
New password: stud
Retype new password: stud
```

**Note:** The password will not be displayed as you type - this is normal Linux behaviour.

#### Step 4: Verify Installation

```powershell
wsl -l -v
```

**Expected output:**
```
  NAME            STATE           VERSION
  Ubuntu-22.04    Running         2
```

Open this exact distribution with `wsl -d Ubuntu-22.04`; the default distribution can be different. Do not unregister an existing distribution to change the default.

### 5.3 Understanding the Ubuntu Environment

When you open Ubuntu, you are in a complete Linux environment:

```
stud@HOSTNAME:~$
```

- `stud` — Your username
- `HOSTNAME` — Your computer name
- `~` — Current directory (home folder: `/home/stud`)
- `$` — Normal user prompt (vs `#` for root)

### 5.4 Checklist

- [ ] Ubuntu appears in `wsl -l -v` with VERSION 2
- [ ] You can log in as user `stud`
- [ ] Home directory is `/home/stud`

---

## 6. Step 3: Install Docker in WSL

### 6.1 What Is Docker?

**Docker** is a platform for developing, shipping and running applications in containers. A container is a lightweight, standalone, executable package that includes everything needed to run software:

- Application code
- Runtime environment
- System tools and libraries
- Configuration settings

### 6.2 Why Docker in WSL (Not Docker Desktop)?

| Aspect | Docker in WSL | Docker Desktop |
|--------|---------------|----------------|
| **Licensing** | Free for all uses | Paid for large companies |
| **Performance** | Native Linux performance | Additional abstraction layer |
| **Learning** | Real Linux Docker environment | Windows-specific behaviour |
| **Networking** | Standard Linux networking | Custom network stack |

### 6.3 Installation Steps

#### Step 1: Open Ubuntu Terminal

Either:
- Click on "Ubuntu" in the Start menu, or
- Type `wsl -d Ubuntu-22.04` in PowerShell

#### Step 2: Refresh Package Metadata

```bash
sudo apt update
```

**What this does:**
- `sudo`: Execute as superuser (administrator)
- `apt update`: Refresh package list
No blanket system upgrade is required by this setup step.

**Expected duration:** 2-5 minutes depending on internet speed.

#### Step 3: Install Docker and Docker Compose

```bash
sudo apt install -y docker.io docker-compose-v2 curl python3 iproute2
```

**Packages installed:**
- `docker.io`: The Docker container runtime
- `docker-compose-v2`: Compose plugin invoked as `docker compose`

These Ubuntu packages apply to a fresh WSL distribution. If a working Docker installation already exists, verify it first and do not mix Ubuntu packages with packages from Docker's own repository. The [Ubuntu package index](https://packages.ubuntu.com/search?keywords=docker-compose-v2) lists the plugin for supported releases; `jammy-updates` and the `universe` component must be available for Ubuntu 22.04. If the package has no installation candidate, check those configured repositories or use the [official Docker installation route](https://docs.docker.com/engine/install/ubuntu/) without combining the two package sources.

#### Step 4: Add User to Docker Group

By default, Docker requires `sudo`. To run Docker commands without `sudo`:

```bash
sudo usermod -aG docker $USER
```

**Command explanation:**
- `usermod`: Modify user account
- `-aG docker`: Add to `docker` group
- `$USER`: Current username (expands to `stud`)

#### Step 5: Start Docker Service

```bash
sudo service docker start
```

**Note:** Service startup depends on whether systemd is enabled in this WSL distribution. Section 10 distinguishes the two cases.

#### Step 6: Apply Group Changes

For the group change to take effect:

```bash
newgrp docker
```

Or log out and log back in:
Exit the Linux shell, then in **PowerShell** reopen the named distribution:

```powershell
wsl -d Ubuntu-22.04
```

#### Step 7: Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker functionality
docker run hello-world
```

**Illustrative version output (your installed version can differ):**
```
Docker version 28.2.2, build e6534b4
```

**Expected hello-world output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 6.4 Aderstanding Docker Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Architecture                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                            │
│  │ Docker CLI  │ ◄── Commands you type                     │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │Docker Daemon│ ◄── Background service (dockerd)          │
│  │  (dockerd)  │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│    ┌────┴────┬─────────────┐                                │
│    ▼         ▼             ▼                                │
│ ┌──────┐ ┌──────┐    ┌──────────┐                          │
│ │Images│ │Conta-│    │ Networks │                          │
│ │      │ │iners │    │          │                          │
│ └──────┘ └──────┘    └──────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### 6.5 Checklist

- [ ] `docker --version` shows version 28.x or higher
- [ ] `docker run hello-world` succeeds without `sudo`
- [ ] `docker ps` runs without permission errors

---

## 7. Step 4: Install Portainer CE

### 7.1 What Is Portainer?

**Portainer Community Edition** is a lightweight management interface that allows you to easily manage Docker environments. Features include:

- Visual container management
- Image and volume management
- Network configuration
- Log viewing
- Container console access
- Stack deployment with docker-compose

### 7.2 Why Portainer?

For educational purposes, Portainer provides:
- **Visual feedback** on container states
- **Easy troubleshooting** through the integrated console
- **Log access** without command-line complexity
- **Network visualisation** for understanding inter-container communication

### 7.3 Installation Steps

Use the [Portainer setup guide](../Portainer/INIT_GUIDE/PORTAINER_SETUP.md) for the selected image and account. From the repository root **inside WSL**, run:

```bash
bash 00_TOOLS/Portainer/INIT_GUIDE/portainer-init.sh
```

The script binds `127.0.0.1:9050` on this Linux machine to container port 9000. It preserves existing containers, data and accounts, checks authentication and confirms local Docker access through Portainer. An absent image requires internet access; a cached image is reused without a pull. Do not run the Windows installer to manage this WSL engine.

### 7.4 Initial Portainer Setup

After the installer succeeds, open `http://localhost:9050` in Windows and use the account confirmed by the installer. For a fresh lab account, the defaults are `stud` / `studstudstud`. A Compose-only start does not create those credentials automatically.

If the interface works in WSL but not on Windows, check WSL localhost forwarding. If an administrator already exists, use that account rather than resetting the data volume. The [Portainer troubleshooting section](../Portainer/INIT_GUIDE/PORTAINER_SETUP.md#7-troubleshooting) describes diagnostic steps.

### 7.5 Portainer Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PORTAINER.io                    [Notifications] [stud ▼]  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────────────────────────┐  │
│  │ Home        │  │  Environment: local                 │  │
│  │ Environments│  │  ┌─────────────────────────────────┐│  │
│  │             │  │  │ Containers: 1   Running: 1     ││  │
│  │ ─────────── │  │  │ Images: 2       Volumes: 1     ││  │
│  │ Containers  │  │  │ Networks: 3                     ││  │
│  │ Images      │  │  └─────────────────────────────────┘│  │
│  │ Networks    │  │                                     │  │
│  │ Volumes     │  │                                     │  │
│  │ Stacks      │  │                                     │  │
│  └─────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 7.6 Checklist

- [ ] `docker ps` shows portainer container running
- [ ] http://localhost:9050 loads in Windows browser
- [ ] You can log in with stud/studstudstud
- [ ] Dashboard shows "local" Docker environment

---

## 8. Step 5: Install Wireshark

### 8.1 What Is Wireshark?

**Wireshark** is the world's foremost and most widely-used network protocol analyser. It allows you to:

- **Capture** network traffic in real time
- **Inspect** packets at multiple protocol levels
- **Filter** traffic by various criteria
- **Analyse** network behaviour and troubleshoot issues
- **Export** captures for later analysis

### 8.2 Why Wireshark on Windows?

We install Wireshark on Windows (not in WSL) because:

1. **GUI Performance:** Native Windows application with better graphics
2. **Interface Access:** Direct access to Windows network interfaces
3. **WSL Traffic:** The `vEthernet (WSL)` interface captures traffic crossing that interface; use Linux capture tools for traffic that remains inside Linux or Docker
4. **Integration:** Easy saving and sharing of files on Windows

### 8.3 Installation Steps

#### Step 1: Download Wireshark

1. Visit: https://www.wireshark.org/download.html
2. Click on **"Windows x64 Installer"**
3. Save the installer file

#### Step 2: Run the Installer

1. Double-click the downloaded `.exe` file
2. Click **"Yes"** at the User Account Control prompt
3. Follow the installation wizard with default options

#### Step 3: Install Npcap

> ⚠️ **Critical:** Npcap is required for packet capture!

During Wireshark installation, you will be prompted to install Npcap:

1. Click **"Install"** when prompted for Npcap
2. In the Npcap installer, ensure these options are checked:
   - ✅ **Install Npcap in WinPcap API-compatible Mode**
   - ✅ **Support raw 802.11 traffic (for wireless packet capture)**
3. Complete the Npcap installation
4. Continue with Wireshark installation

#### Step 4: Complete Installation

1. Finish the Wireshark installer
2. Optionally restart your computer if prompted

### 8.4 Wireshark Interface Selection

When you open Wireshark, you will see a list of network interfaces. For capturing Docker/WSL traffic:

| Interface | Description | Use For |
|-----------|-------------|---------|
| **vEthernet (WSL)** | WSL2 virtual network | Docker container traffic |
| **vEthernet (WSL) (Hyper-V firewall)** | Same, with firewall | Docker container traffic |
| Ethernet | Physical network card | External traffic |
| Wi-Fi | Wireless adapter | External wireless traffic |

### 8.5 Basic Wireshark Usage

#### Starting a Capture

1. Open Wireshark from the Start menu
2. Double-click on the **"vEthernet (WSL)"** interface
3. Capture starts immediately

#### Useful Display Filters

| Filter | Purpose |
|--------|---------|
| `icmp` | Show only ping (ICMP) packets |
| `tcp` | Show only TCP packets |
| `http` | Show only HTTP traffic |
| `dns` | Show only DNS queries |
| `ip.addr == 172.17.0.2` | Filter by IP address |
| `tcp.port == 80` | Filter by port |

#### Stopping a Capture

- Click the red **Stop** button in the toolbar
- Or press `Ctrl + E`

### 8.6 Checklist

- [ ] Wireshark starts from the Start menu
- [ ] Network interfaces are visible
- [ ] "vEthernet (WSL)" interface is present
- [ ] You can start and stop a capture

---

## 9. Step 6: Python Packages

### 9.1 Why Python for Networking?

Python is widely used for network automation and analysis:

- **docker**: Programmatic container management
- **scapy**: Packet manipulation and creation
- **dpkt**: Fast packet parsing

### 9.2 Prerequisites

Install and use Python **inside Ubuntu in WSL**, where the Docker daemon runs. Packages installed in Windows Python are separate and cannot satisfy the Linux verifier.

```bash
sudo apt install -y python3 python3-venv python3-pip git curl wget tcpdump netcat-openbsd iproute2
python3 --version
```

The supported baseline is Python 3.10 or later. If the selected exercise requires a newer interpreter, use its documented environment. Keep the existing MININET-SDN appliance environment unchanged.

### 9.3 Installation Steps

Create a separate Linux virtual environment and activate it before installation, verification and exercises:

```bash
python3 -m venv ~/venvs/compnet-wsl
source ~/venvs/compnet-wsl/bin/activate
python3 -m pip install docker scapy dpkt requests flask PyYAML colorama
```

Exercise-dependent packages:

```bash
python3 -m pip install paramiko pyftpdlib paho-mqtt dnspython grpcio protobuf
```

Downloads require internet. These commands prepare a fresh environment and do not constitute a frozen package lock. Keep package versions with your experiment records where exact replay is required. Do not install into the system Python with `--break-system-packages` as a routine remedy.

Check the active interpreter and basic imports:

```bash
which python3
python3 -c "import docker, scapy.all, dpkt; print('Core imports: OK')"
```

After opening another WSL terminal, activate this same environment again:

```bash
source ~/venvs/compnet-wsl/bin/activate
```

### 9.4 What the Packages Do

#### docker (Python Docker SDK)

```python
import docker
client = docker.from_env()

# List containers
for container in client.containers.list():
    print(container.name, container.status)

# Run container
container = client.containers.run("alpine", "echo hello", detach=True)
```

#### scapy (Packet Manipulation)

```python
from scapy.all import *

# Create and send ping packet
packet = IP(dst="8.8.8.8")/ICMP()
response = sr1(packet, timeout=2)
print(response.summary())
```

#### dpkt (Packet Parsing)

```python
import dpkt

# Parse pcap file
with open('capture.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        print(eth)
```

### 9.5 Checklist

- [ ] `pip show docker` displays package information
- [ ] `pip show scapy` displays package information
- [ ] `pip show dpkt` displays package information
- [ ] Import statements work without errors

---

## 10. Step 7: Auto-start Configuration (Optional)

Check which init system is running **inside WSL**:

```bash
ps -p 1 -o comm=
```

If it reports `systemd`, enable and start the installed Docker service:

```bash
sudo systemctl enable --now docker
```

Otherwise start Docker for the current WSL session:

```bash
sudo service docker start
```

A container restart policy takes effect after the Docker daemon starts; it does not itself start WSL when Windows boots. This guide does not append repeated shell startup commands or grant passwordless sudo. See [Microsoft's WSL systemd guidance](https://learn.microsoft.com/en-us/windows/wsl/systemd) if you deliberately choose to enable systemd. Preserve any existing `/etc/wsl.conf` settings.

---

## 11. Final Verification

### 11.1 Complete System Test

#### Test 1: Docker and Portainer

```bash
# In Ubuntu terminal
docker ps
```

**Expected:** Portainer container running.

#### Test 2: Wireshark Capture

1. Open Wireshark on Windows
2. Start capture on **vEthernet (WSL)**
3. In Ubuntu, run:

```bash
docker run --rm alpine ping -c 5 8.8.8.8
```

4. In Wireshark, apply filter: `icmp`
5. Verify you can see ICMP Echo Request and Reply packets

**Expected Wireshark Output:**

| No. | Time | Source | Destination | Protocol | Info |
|-----|------|--------|-------------|----------|------|
| 1 | 0.000 | 172.27.159.165 | 8.8.8.8 | ICMP | Echo request |
| 2 | 0.087 | 8.8.8.8 | 172.27.159.165 | ICMP | Echo reply |

#### Test 3: Python Integration

```bash
# Inside WSL, after activating ~/venvs/compnet-wsl
python3 -c "import docker; c = docker.from_env(); print(f'Containers: {len(c.containers.list())}')"
```

**Expected:** `Containers: 1` (or more)

### 11.2 Component Summary

| Component | Version | Status Check |
|-----------|---------|--------------|
| WSL2 | 2.x | `wsl --status` |
| Ubuntu | 22.04 LTS | `lsb_release -a` |
| Docker | Installed version | `docker --version` |
| Docker Compose | v2 | `docker compose version` |
| Portainer | Selected image; optional | http://localhost:9050 |
| Wireshark | 4.4.x | Launch application |
| Python docker | Installed version | `python3 -m pip show docker` |
| Python scapy | Installed version | `python3 -m pip show scapy` |
| Python dpkt | Installed version | `python3 -m pip show dpkt` |

### 11.3 Prerequisite Verification

From the repository root, inside WSL:

```bash
source ~/venvs/compnet-wsl/bin/activate
bash 00_TOOLS/Prerequisites/verify_lab_environment.sh
```

The default checks are local and do not pull Docker images. To request additional bounded HTTPS connectivity probes:

```bash
bash 00_TOOLS/Prerequisites/verify_lab_environment.sh --online
```

Review warnings for the chosen exercise. Passing these checks is not a complete course acceptance test. For the VirtualBox appliance use [its own verifier](../../01_GUIDE_MININET-SDN/verify_mininet_vm.sh).

---

## 12. Troubleshooting

### 12.0 Top 5 Errors and Quick Fixes

| # | Error | Common Cause | Quick Fix |
|:-:|-------|--------------|-----------|
| 1 | `Cannot connect to Docker daemon` | Docker service not running | `sudo service docker start` |
| 2 | `Permission denied` on docker commands | User not in docker group | `sudo usermod -aG docker $USER` + logout/login |
| 3 | `Address already in use` | Port already occupied | `ss -tlnp \| grep :PORT` then stop the process |
| 4 | `wsl --install` does nothing | WSL already partially installed | `wsl --update` then restart |
| 5 | Portainer won't open | Container stopped or port blocked | `docker start portainer` |

### Docker Debugging Flowchart

```
                    Docker Problem?
                          │
                          ▼
              ┌───────────────────────┐
              │    docker info        │
              │    works?             │
              └───────────┬───────────┘
                          │
               ┌──────────┴──────────┐
               │                     │
              YES                    NO
               │                     │
               ▼                     ▼
    ┌──────────────────┐   ┌──────────────────────┐
    │  docker ps -a    │   │ sudo service docker  │
    │  see containers  │   │ start                │
    └────────┬─────────┘   └──────────┬───────────┘
             │                        │
             ▼                        ▼
    ┌──────────────────┐        Try again
    │ Container stopped?│        docker info
    │ → docker start X │
    └──────────────────┘

    ┌──────────────────────────────────────────────────────┐
    │ If you get "Permission denied":                      │
    │   1. sudo usermod -aG docker $USER                   │
    │   2. newgrp docker  (or logout + login)              │
    └──────────────────────────────────────────────────────┘
```

### 30-Second Quick Check

```bash
# Run this sequence for fast diagnosis:
echo "1. Docker daemon:" && docker info >/dev/null 2>&1 && echo "   ✓ OK" || echo "   ✗ Not running"
echo "2. Portainer:" && docker ps --filter name=portainer --format "   ✓ {{.Status}}" 2>/dev/null || echo "   ✗ Container absent"
echo "3. Ports:" && ss -tlnp 2>/dev/null | grep -E ":(9050|8080)" | awk '{print "   ✓ " $4}' || echo "   ✓ Free"
```

---

### 12.1 WSL Issues

#### "WSL 2 requires an update to its kernel component"

```powershell
wsl --update
```

#### "Please enable the Virtual Machine Platform feature"

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Restart your computer afterwards.

#### WSL won't start

```powershell
# Reset WSL
wsl --shutdown
wsl
```

### 12.2 Docker Issues

#### "Cannot connect to the Docker daemon"

```bash
# Start Docker service
sudo service docker start

# Check if dockerd is running
ps aux | grep dockerd
```

#### "Permission denied while trying to connect to the Docker daemon socket"

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker
# Or log out and log back in
```

#### "docker: command not found" in PowerShell

This is normal. Docker is installed in WSL, not Windows. Use:

```powershell
wsl docker ps
```

### 12.3 Portainer Issues

#### Cannot access http://localhost:9050

1. Check if container is running:
```bash
docker ps | grep portainer
```

2. If not running, check logs:
```bash
docker logs portainer
```

3. Restart Portainer:
```bash
docker restart portainer
```

#### "Portainer has already been initialised"

An administrator already exists. Use its actual credentials; this does not mean the volume is faulty. For an uninitialised setup that has timed out, restart the container and complete initialisation promptly:

```bash
docker restart portainer
```

Preserve `portainer_data`. Deleting it would remove users and settings and is not a routine setup repair.

### 12.4 Wireshark Issues

#### No interfaces visible

- Ensure Npcap is installed
- Run Wireshark as Administrator
- Reinstall Npcap from https://npcap.com/

#### "vEthernet (WSL)" doesn't appear

- WSL must be running
- Try: `wsl` in PowerShell, then restart Wireshark

#### No traffic captured

- Ensure capture is on the correct interface
- Generate traffic: `docker run --rm alpine ping -c 3 8.8.8.8`
- Check that display filter is not too restrictive

---

## 13. Quick Reference Sheet

### Essential Commands

```bash
# WSL Management (PowerShell)
wsl --status           # Check WSL status
wsl --shutdown         # Stop all WSL instances
wsl                    # Open default distribution
wsl -l -v              # List distributions

# Docker (Ubuntu Terminal)
docker ps              # List running containers
docker ps -a           # List all containers
docker images          # List images
docker logs <n>        # View container logs
docker exec -it <n> sh # Shell into container
docker stop <n>        # Stop container
docker rm <n>          # Delete container

# Service Management (Ubuntu Terminal)
sudo service docker start   # Start Docker
sudo service docker status  # Check Docker status
sudo service docker stop    # Stop Docker
```

### Important URLs

| Service | URL |
|---------|-----|
| Portainer | http://localhost:9050 |
| Docker Docs | https://docs.docker.com/ |
| Wireshark Docs | https://www.wireshark.org/docs/ |
| WSL Docs | https://learn.microsoft.com/en-us/windows/wsl/ |

### Credentials

| Service | Username | Password |
|---------|----------|----------|
| Ubuntu WSL | stud | stud |
| Portainer | stud | studstudstud |

---

## 🎉 Setup Complete!

Your lab environment is fully configured. You can now:

- ✅ Run isolated network experiments with Docker containers
- ✅ Capture and analyse traffic with Wireshark
- ✅ Manage containers through the Portainer web interface
- ✅ Automate network tasks with Python

**Next Steps:**
- Explore the Portainer interface
- Try creating custom Docker networks
- Practise filtering in Wireshark
- Run your first lab exercise

---

*Computer Networks Lab — ASE Bucharest, CSIE*
*Documentation version: January 2026*

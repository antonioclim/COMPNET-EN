# Installation and Configuration Guide — Computer Networks (CompNet)

## The MININET-SDN Virtual Workstation on Windows 10/11

**Course:** Computer Networks — ASE-CSIE  
**Author:** ing. dr. Antonio Clim  
**Last updated:** February 2026  
**Level:** Step-by-step guide (no prior virtualisation knowledge required)

---

## Contents

1. [What you will install and why](#1-what-you-will-install-and-why)
2. [Minimum requirements (hardware & software)](#2-minimum-requirements-hardware--software)
3. [Step 1 — Installing VirtualBox](#3-step-1--installing-virtualbox)
4. [Step 2 — Importing the MININET-SDN virtual workstation](#4-step-2--importing-the-mininet-sdn-virtual-workstation)
5. [Step 3 — Configuring the network in VirtualBox](#5-step-3--configuring-the-network-in-virtualbox)
6. [Step 4 — Starting the VM and first login](#6-step-4--starting-the-vm-and-first-login)
7. [Step 5 — Installing PuTTY and connecting via SSH](#7-step-5--installing-putty-and-connecting-via-ssh)
8. [Step 6 — Docker Desktop and testing `docker compose`](#8-step-6--docker-desktop-and-testing-docker-compose)
9. [Step 7 — Installing Wireshark on Windows](#9-step-7--installing-wireshark-on-windows)
10. [Step 8 — Shared Folders (file sharing between Windows and the VM)](#10-step-8--shared-folders-file-sharing-between-windows-and-the-vm)
11. [Step 9 — Cloning the course repository](#11-step-9--cloning-the-course-repository)
12. [Step 10 — Full end-to-end test](#12-step-10--full-end-to-end-test)
13. [Troubleshooting — Common problems](#13-troubleshooting--common-problems)
14. [The cleanup script clean.ps1](#14-the-cleanup-script-cleanps1)
15. [References and useful links](#15-references-and-useful-links)
16. [Appendix A — Linux host guide (alternative)](#16-appendix-a--linux-host-guide-alternative)

---

## 1. What you will install and why

Throughout the semester you will work inside a **pre-built Ubuntu 24.04 LTS virtual workstation** designed specifically for the networking labs. It contains every tool you need — from the Mininet network simulator and Open vSwitch software switches to Docker Engine, Wireshark (tshark), Scapy, nmap and many more.

The purpose of this guide is to take you from a "bare" Windows installation to a fully working environment in which you can:

- connect via **SSH** (through PuTTY) to the VM
- run lab scenarios with `docker compose up` / `docker compose down`
- capture and analyse traffic with **Wireshark** (on Windows) or **tshark** (inside the VM)
- transfer files between Windows and the VM via **Shared Folders**

### Working architecture (simplified diagram)

```
┌──────────────────────────────────────────────────────────────┐
│  HOST (Windows 10/11)                                        │
│                                                              │
│  ┌─────────────┐  ┌────────────┐  ┌────────────────────┐    │
│  │  PuTTY      │  │ Wireshark  │  │  Shared Folder     │    │
│  │  (SSH)      │  │ (capture)  │  │  C:\SHARED         │    │
│  └──────┬──────┘  └──────┬─────┘  └─────────┬──────────┘    │
│         │ port 2222      │                   │ vboxsf        │
│  ═══════╪════════════════╪═══════════════════╪═══════════    │
│         │       VirtualBox NAT               │               │
│  ┌──────┴────────────────┴───────────────────┴──────────┐    │
│  │  VM: MININET-SDN (Ubuntu 24.04)                      │    │
│  │                                                      │    │
│  │  user: stud / pass: stud                             │    │
│  │  enp0s3: 10.0.2.15 (NAT)   docker0: 172.17.0.1      │    │
│  │                                                      │    │
│  │  ┌────────────────────────────────────────────┐      │    │
│  │  │  Docker Engine 28.x + Compose v2           │      │    │
│  │  │  ┌──────┐ ┌──────┐ ┌──────┐               │      │    │
│  │  │  │ web1 │ │ web2 │ │ dns  │  ...scenarios │      │    │
│  │  │  └──────┘ └──────┘ └──────┘               │      │    │
│  │  └────────────────────────────────────────────┘      │    │
│  │                                                      │    │
│  │  Mininet 2.3 │ OVS 3.3 │ Python 3.12 (venv compnet) │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Minimum requirements (hardware & software)

| Component | Minimum | Recommended |
|---|---|---|
| **Processor** | Intel/AMD with VT-x/AMD-V support | Any CPU from the past 5 years |
| **RAM** | 8 GB (of which 2 GB for the VM) | 16 GB |
| **Free disc space** | 10 GB | 20 GB |
| **Operating system** | Windows 10 (64-bit), build 1903+ | Windows 11 |
| **Hardware virtualisation** | Enabled in BIOS/UEFI | — |

### Checking hardware virtualisation (VT-x / AMD-V)

Open **Task Manager** → the **Performance** tab → **CPU**. In the bottom-right corner you should see:

```
Virtualisation: Enabled
```

If it reads **Disabled**, you must enter BIOS/UEFI and enable the relevant option. The exact name varies by motherboard manufacturer:

- **Intel**: "Intel Virtualization Technology (VT-x)"
- **AMD**: "SVM Mode" or "AMD-V"

> **Warning:** Without hardware virtualisation enabled, VirtualBox will NOT be able to run the VM.

### A note on Hyper-V and WSL2

If you already have **Hyper-V** or **WSL2** enabled on Windows, VirtualBox 7.x can coexist with them, though performance may be slightly reduced. There is no need to disable Hyper-V.

---

## 3. Step 1 — Installing VirtualBox

### 3.1 Download VirtualBox

Go to the official downloads page:

```
https://www.virtualbox.org/wiki/Downloads
```

Click **"Windows hosts"** to download the installer (`.exe` file, roughly 105 MB).

### 3.2 Run the installer

1. Double-click the downloaded file (e.g. `VirtualBox-7.x.y-xxxxx-Win.exe`)
2. Click **Next** at every step — the default configuration is perfectly adequate
3. The installer will display a warning about temporarily disconnecting the network — click **Yes**
4. Click **Install** and wait for it to finish
5. Click **Finish**

### 3.3 Install the Extension Pack (optional but recommended)

The Extension Pack adds USB 2.0/3.0 passthrough, RDP and PXE boot support. Download it from the same page (the "All supported platforms" link), then:

1. Open VirtualBox
2. Go to **File → Tools → Extension Pack Manager** (or **File → Preferences → Extensions** on older versions)
3. Click the **Install** button (the "+" icon) and select the downloaded `.vbox-extpack` file
4. Accept the licence and confirm the installation

### 3.4 Verification

Open VirtualBox. You should see the main "Oracle VirtualBox Manager" window without any errors.

---

## 4. Step 2 — Importing the MININET-SDN virtual workstation

### 4.1 Download the `.ova` file

The virtual workstation is distributed as an OVA file (Open Virtualization Appliance):

```
https://drive.google.com/file/d/1LqnyD64gzePBjYEXpIGen41mNdjBKU3x/view?usp=drive_link
```

The file is called `MININET-SDN.ova` (size: roughly 2–3 GB). Save it somewhere easy to find, for example `C:\Users\<YourName>\Downloads\`.

### 4.2 Import the workstation into VirtualBox

1. Open **VirtualBox**
2. Go to **File → Import Appliance…** (or `Ctrl+I`)
3. Click **Browse** and select the downloaded `MININET-SDN.ova` file
4. Click **Next**

You will see a screen showing the virtual machine settings. Review and adjust if necessary:

| Setting | Recommended value |
|---|---|
| **Name** | `MININET-SDN` |
| **CPU** | 2 (or more if you have 8+ cores) |
| **RAM** | 2048 MB (2 GB) minimum |
| **Network** | NAT (the default) |

5. Click **Finish** (or **Import**) and wait 1–3 minutes

Once the import completes, the `MININET-SDN` machine will appear in the left-hand panel of VirtualBox Manager.

---

## 5. Step 3 — Configuring the network in VirtualBox

The VM uses **NAT** (Network Address Translation) as its network mode. This means the VM can access the internet through the host's connection, but the host (Windows) cannot reach the VM directly — except on ports that we explicitly configure via **Port Forwarding**.

### 5.1 Configuring Port Forwarding

We need at least the following rules:

| Purpose | Protocol | Host IP | Host Port | Guest IP | Guest Port |
|---|---|---|---|---|---|
| **SSH** | TCP | 127.0.0.1 | 2222 | 10.0.2.15 | 22 |
| **Docker API** (optional) | TCP | 127.0.0.1 | 2375 | 10.0.2.15 | 2375 |
| **HTTP test** (optional) | TCP | 127.0.0.1 | 8080 | 10.0.2.15 | 8080 |

Here is how to set them up:

1. In VirtualBox Manager, select the **MININET-SDN** machine (left-click on it)
2. Click **Settings** (the cog icon) → **Network**
3. Under **Adapter 1** (which should read "Attached to: **NAT**"), click **Advanced** (the small arrow) to expand the options
4. Click the **Port Forwarding** button
5. Add the rules from the table above by clicking the **+** (plus) icon on the right:

   **SSH rule (required):**
   - Name: `ssh`
   - Protocol: `TCP`
   - Host IP: `127.0.0.1`
   - Host Port: `2222`
   - Guest IP: `10.0.2.15`
   - Guest Port: `22`

   **Docker API rule (optional — useful if you want to control Docker from Windows):**
   - Name: `docker-api`
   - Protocol: `TCP`
   - Host IP: `127.0.0.1`
   - Host Port: `2375`
   - Guest IP: `10.0.2.15`
   - Guest Port: `2375`

   **HTTP test rule (optional — useful for labs 8–11):**
   - Name: `http-test`
   - Protocol: `TCP`
   - Host IP: `127.0.0.1`
   - Host Port: `8080`
   - Guest IP: `10.0.2.15`
   - Guest Port: `8080`

6. Click **OK** → **OK** to save

> **Why port 2222 rather than 22?** Port 22 on Windows might already be occupied by another SSH service (for instance if you have OpenSSH Server installed). We use 2222 on the host to avoid conflicts; inside the VM, the SSH daemon listens on the standard port 22.

---

## 6. Step 4 — Starting the VM and first login

### 6.1 Starting the virtual machine

1. In VirtualBox Manager, select **MININET-SDN**
2. Click **Start** (the green arrow)
3. Wait roughly 30–60 seconds until the login prompt appears

### 6.2 Direct console login (for verification only)

At the `mininet-vm login:` prompt, enter:

```
Login:    stud
Password: stud
```

> **Note:** The password is NOT displayed on screen as you type it. This is normal — type it and press Enter.

If you see a prompt like `stud@mininet-vm:~$`, congratulations — the VM is working.

### 6.3 Quick component check

Run the following commands one by one to confirm that everything is installed:

```bash
# Check the Docker version
docker --version
# Expected: Docker version 28.2.2, ...

# Check Docker Compose
docker compose version
# Expected: Docker Compose version 2.37.1+...

# Check Mininet
sudo mn --version
# Expected: 2.3.0

# Check Open vSwitch
ovs-vsctl --version
# Expected: ovs-vsctl (Open vSwitch) 3.3.4

# Check Python (the venv activates automatically at login)
python3 --version
# Expected: Python 3.12.3

# Check key Python libraries
python3 -c "import scapy; print('scapy OK')"
python3 -c "import paramiko; print('paramiko OK')"
python3 -c "import flask; print('flask OK')"

# Check internet connectivity
ping -c 3 google.com
```

> **Note:** The Python virtual environment (`compnet`) activates automatically at every login via `.bashrc`. The prompt will read `(compnet) stud@mininet-vm:~$`.

---

## 7. Step 5 — Installing PuTTY and connecting via SSH

The VirtualBox console is rather awkward (copy-paste is cumbersome and the window cannot be resized). For day-to-day work we connect to the VM over **SSH** using **PuTTY** — a free SSH client for Windows.

### 7.1 Download and install PuTTY

Download the MSI installer from the official site:

```
https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
```

Choose the **64-bit MSI** version (e.g. `putty-64bit-0.82-installer.msi`). Run the installer with the default options.

**Alternative:** If you prefer a more modern terminal, you can use **Windows Terminal** together with the SSH client built into Windows 10/11. The PowerShell command would be:

```powershell
ssh -p 2222 stud@127.0.0.1
```

### 7.2 Configuring the PuTTY session

1. Open **PuTTY**
2. Fill in the fields:
   - **Host Name (or IP address):** `127.0.0.1`
   - **Port:** `2222`
   - **Connection type:** SSH
3. (Optional but recommended) Save the session:
   - In the **Saved Sessions** field type `MININET-SDN`
   - Click **Save**
4. Click **Open**

### 7.3 First login via PuTTY

On first connection PuTTY will display a warning about the host key fingerprint. Click **Accept** — this is normal the first time you connect.

```
Login as: stud
stud@127.0.0.1's password: stud
```

You should see:

```
(compnet) stud@mininet-vm:~$
```

You now have full SSH access to the VM, with copy-paste support (right-click = paste in PuTTY).

### 7.4 PuTTY tips

- **Copy from PuTTY:** select text with the mouse → it is copied to the clipboard automatically
- **Paste into PuTTY:** right-click
- **Saved sessions:** next time, open PuTTY → double-click `MININET-SDN` in the saved sessions list
- **Larger window:** Settings → Window → Rows/Columns (80×40 is far more comfortable than 80×24)
- **Keep-alive:** Settings → Connection → "Seconds between keepalives" → set to `30` (prevents disconnection during inactivity)

---

## 8. Step 6 — Docker Desktop and testing `docker compose`

### Two ways to work with Docker

You can work with Docker **in two ways** — choose whichever suits you best:

| Option | Advantages | Disadvantages |
|---|---|---|
| **A) Docker ONLY inside the VM** (recommended) | Nothing to install on Windows; everything runs via SSH | You must work exclusively through the terminal |
| **B) Docker Desktop on Windows** | Visual GUI, IDE integration | Consumes additional RAM on the host |

### Option A — Docker inside the VM (recommended for this course)

Docker Engine is already installed and configured in the VM. You do not need to install anything extra on Windows. All `docker compose up/down` commands are run through your SSH session (PuTTY).

**Quick test** — connect via PuTTY and run:

```bash
# Check that Docker Engine responds
docker info | head -5

# Minimal test with a container
docker run --rm hello-world
```

If you see the "Hello from Docker!" message, everything is working correctly.

### Option B — Docker Desktop on Windows (optional)

If you also want Docker on Windows (useful if you work on other projects):

1. Download Docker Desktop from `https://www.docker.com/products/docker-desktop/`
2. Run the installer (requires a restart)
3. After the restart, Docker Desktop starts automatically (system tray icon)

> **Important:** Docker Desktop on Windows and Docker Engine inside the VM are **separate instances**. Containers created on one do not appear on the other. For the course labs, use the Docker inside the VM.

---

## 9. Step 7 — Installing Wireshark on Windows

Wireshark is a graphical protocol analyser that you will use to inspect network traffic.

### 9.1 Download and install

```
https://www.wireshark.org/download.html
```

Choose the **Windows x64 Installer** (`.exe`). During installation:

1. Accept all default components
2. **Important:** When asked about **Npcap** (the packet capture driver), tick **"Install Npcap"** — without it Wireshark cannot capture traffic
3. Complete the installation

### 9.2 Capturing traffic from the VM (via port forwarding)

Wireshark on Windows captures traffic **on the host's interfaces**. To see relevant traffic from the VM:

**Method 1 — Loopback capture (Npcap Loopback Adapter)**

When you communicate with the VM through port forwarding (127.0.0.1:2222 etc.), the traffic passes through the loopback interface. In Wireshark:

1. Open Wireshark
2. Select the **"Adapter for loopback traffic capture"** interface (or **"Npcap Loopback Adapter"**)
3. Apply a capture filter, for example: `tcp port 2222`
4. Start the capture (blue button)
5. Connect with PuTTY — you will see the SSH packets

**Method 2 — Capturing from inside the VM with `tshark`**

For more complex captures (traffic between Docker containers or Mininet hosts), run `tshark` directly in the VM:

```bash
# Capture traffic on the Docker interface
sudo tshark -i docker0 -w /tmp/capture.pcap

# Or capture traffic on any interface
sudo tshark -i any -f "tcp port 8080" -w /tmp/capture_http.pcap
```

Then transfer the `.pcap` file to Windows (via Shared Folder — see Step 8) and open it with Wireshark.

### 9.3 Capturing traffic from a `docker compose` scenario

A practical example — you will do this frequently during the labs:

```bash
# 1. Start a scenario (e.g. lab 8 — nginx reverse proxy)
cd ~/compnet-2025-redo-main/assets/tutorial/s8/4_nginx/
docker compose up -d

# 2. Start a tshark capture on the relevant interface
sudo tshark -i any -f "tcp port 8080" -w /tmp/s8_nginx.pcap &

# 3. Generate test traffic
curl http://localhost:8080

# 4. Stop the capture (Ctrl+C or kill %1)
kill %1

# 5. Copy the pcap file to the Shared Folder
cp /tmp/s8_nginx.pcap /media/sf_SHARED/

# 6. Tear down the scenario
docker compose down
```

On Windows, open `C:\SHARED\s8_nginx.pcap` with Wireshark.

---

## 10. Step 8 — Shared Folders (file sharing between Windows and the VM)

VirtualBox Shared Folders allow you to access a folder on Windows directly from inside the VM. This is the simplest way to transfer files.

### 10.1 Create the shared folder on Windows

Create a folder on Windows. For example:

```
C:\SHARED
```

### 10.2 Configure the Shared Folder in VirtualBox

1. With the VM **powered off** (or from Settings at runtime), go to **Settings → Shared Folders**
2. Click the **+** icon (Add Share) on the right
3. Fill in:
   - **Folder Path:** `C:\SHARED`
   - **Folder Name:** `SHARED` (this name will appear in Linux as the mount point)
   - **Read-only:** NO (unticked)
   - **Auto-mount:** YES (ticked)
   - **Mount point:** leave blank (VirtualBox will auto-mount at `/media/sf_SHARED`)
4. Click **OK** → **OK**

### 10.3 Verification from the VM

Start the VM and connect via PuTTY:

```bash
# Check that the folder is mounted
ls -la /media/sf_SHARED/

# Create a test file
echo "hello from the VM" > /media/sf_SHARED/test.txt
```

On Windows, open `C:\SHARED` — you should see the file `test.txt`.

> **Permissions note:** The user `stud` is already a member of the `vboxsf` group (verified in the VM blueprint). If you get "Permission denied", run:
> ```bash
> sudo usermod -aG vboxsf stud
> ```
> then log out and back in (or run `newgrp vboxsf`).

---

## 11. Step 9 — Cloning the course repository

The course repository contains all the materials for the labs: scenarios, Python scripts, `docker-compose.yml` files and explanations.

### 11.1 Cloning with `git` (from the VM)

Connect via PuTTY to the VM and run:

```bash
cd ~
git clone https://github.com/hypothetical-andrei/compnet-2025-redo.git
cd compnet-2025-redo
ls -la
```

You will see the following structure:

```
compnet-2025-redo/
├── assets/
│   ├── course/           ← lecture materials (c1–c13)
│   ├── tutorial/          ← lab materials (s1–s13)
│   ├── tutorial-solve/    ← partial solutions
│   └── tools/             ← utilities (plantuml.jar etc.)
└── prompts/               ← content-generation prompts
```

### 11.2 Alternative — downloading as a ZIP

If you have no internet access from the VM, download the archive on Windows:

```
https://github.com/hypothetical-andrei/compnet-2025-redo/archive/refs/heads/main.zip
```

Copy it to `C:\SHARED`, then from the VM:

```bash
cp /media/sf_SHARED/compnet-2025-redo-main.zip ~
cd ~
unzip compnet-2025-redo-main.zip
cd compnet-2025-redo-main
```

### 11.3 Running the setup script (recommended after cloning)

The VM includes a compatibility script that creates the necessary symlinks, verifies Python dependencies and patches the `docker-compose.yml` files:

```bash
cd ~
chmod +x compnet_mininetvm_setup.sh
./compnet_mininetvm_setup.sh --kit-root ~/compnet-2025-redo --self-test
```

If everything is in order, the output will show a series of `[OK]` entries with no major errors.

---

## 12. Step 10 — Full end-to-end test

Now we verify everything together — from SSH to Docker Compose, including a Wireshark capture.

### 12.1 Preparation

Make sure you are connected via PuTTY to the VM.

### 12.2 Test scenario: Nginx Reverse Proxy (Lab 8)

```bash
# 1. Navigate to the scenario directory
cd ~/compnet-2025-redo/assets/tutorial/s8/4_nginx/

# 2. Start a Python HTTP server on port 8000 (the backend)
python3 -m http.server 8000 &

# 3. Start the Docker Compose scenario (nginx as reverse proxy)
docker compose up -d

# 4. Check the running containers
docker compose ps

# 5. Test with curl
curl http://localhost:8080

# 6. (Optional) Start a tshark capture
sudo tshark -i lo -f "tcp port 8080 or tcp port 8000" -c 20

# 7. Generate traffic again
curl http://localhost:8080

# 8. Tear everything down
docker compose down
kill %1  # stop the background Python HTTP server
```

### 12.3 What you should see

- At step 4: the `seminar8_nginx` container with status `Up`
- At step 5: the HTML content returned by the backend through the nginx reverse proxy
- At steps 6–7: TCP packets captured by tshark showing the flow `client → nginx:8080 → backend:8000`

### 12.4 Full Docker Compose up/down test (FTP scenario — Lab 9)

```bash
# Navigate to the multi-client FTP scenario
cd ~/compnet-2025-redo/assets/tutorial/s9/3_multi-client-containers/

# Start everything
docker compose up -d

# Check the containers
docker compose ps
# Expected: 3 containers (ftp-server, client1, client2)

# Check the Docker network created
docker network ls

# Tear everything down
docker compose down
```

If everything worked — **you are ready for the labs!**

---

## 13. Troubleshooting — Common problems

### The VM will not start: "VT-x is disabled in BIOS"

**Cause:** Hardware virtualisation is not enabled in BIOS/UEFI.

**Solution:**
1. Restart your computer
2. Enter BIOS (usually `F2`, `F10`, `Del` or `Esc` at startup)
3. Find the "Intel Virtualization Technology" or "SVM Mode" option
4. Enable it → Save & Exit

---

### PuTTY: "Connection refused" at 127.0.0.1:2222

**Possible causes:**
1. The VM is not running
2. Port forwarding is not configured correctly
3. The SSH service inside the VM is not running

**Solutions:**
1. Check that the VM is running and has passed the login screen
2. Double-check the Port Forwarding rules (Section 5.1)
3. In the VirtualBox console of the VM, log in and run:
   ```bash
   sudo systemctl status ssh
   # If it is not running:
   sudo systemctl start ssh
   sudo systemctl enable ssh
   ```

---

### `docker compose up` reports port conflicts

**Cause:** Stale containers left over from a previous session.

**Quick fix (from the VM):**

```bash
# The nuclear option — stop and remove EVERYTHING
docker rm -f $(docker ps -aq) 2>/dev/null
docker network prune -f
```

Or use the `clean.ps1` script on Windows (see Section 14).

---

### `docker compose` returns "permission denied"

**Cause:** The user `stud` is not in the `docker` group.

**Solution:**

```bash
sudo usermod -aG docker stud
# Then log out and back in:
exit
# (reconnect with PuTTY)
```

---

### The Shared Folder does not appear in the VM

**Possible causes:**
1. Guest Additions are not installed
2. The folder is not configured as Auto-mount

**Solutions:**
1. Guest Additions are already included in the OVA (verified: version 7.0.16). If they are missing:
   ```bash
   sudo apt install virtualbox-guest-utils virtualbox-guest-x11
   sudo reboot
   ```
2. Double-check the "Auto-mount" setting in VirtualBox → Settings → Shared Folders
3. Manual mount (workaround):
   ```bash
   sudo mkdir -p /media/sf_SHARED
   sudo mount -t vboxsf SHARED /media/sf_SHARED
   ```

---

### Wireshark on Windows cannot see the VM's traffic

**Explanation:** The VM's internal traffic (between Docker containers or Mininet hosts) does not cross the physical interface of the Windows host. This traffic exists only inside the VM.

**Solution:** Use `tshark` or `tcpdump` inside the VM for internal captures, then transfer the `.pcap` files to Windows via the Shared Folder:

```bash
# Capture inside the VM
sudo tshark -i docker0 -w /tmp/capture.pcap -c 100

# Transfer
cp /tmp/capture.pcap /media/sf_SHARED/

# Open on Windows: C:\SHARED\capture.pcap (double-click → Wireshark)
```

---

### The VM is extremely slow

**Solutions:**
1. Allocate more RAM (Settings → System → Base Memory → 3072 MB or more)
2. Allocate more CPUs (Settings → System → Processor → 2 or more)
3. Disable visual effects in VirtualBox: Settings → Display → Graphics Controller → VBoxVGA, Video Memory → 32 MB
4. Run the VM **headless** (without a graphical window) — still via SSH:
   - Right-click the VM → **Start → Headless Start**
   - You connect exclusively through PuTTY

---

### Error at `sudo mn --test pingall`: "Cannot find required executable …"

**Cause:** Open vSwitch is not running.

**Solution:**

```bash
sudo systemctl start openvswitch-switch
sudo systemctl enable openvswitch-switch
# Then test again:
sudo mn --test pingall
```

---

### Python reports "No module named …"

**Cause:** The `compnet` virtual environment is not activated.

**Solution:**

```bash
# Manual activation
source ~/venvs/compnet/bin/activate

# Verification (the prompt should begin with (compnet))
which python3
# Expected: /home/stud/venvs/compnet/bin/python3
```

> Note: `.bashrc` should activate the venv automatically at login. If it does not, check the last section of `~/.bashrc`.

---

## 14. The cleanup script clean.ps1

When Docker containers get stuck and ports remain occupied, you can run this PowerShell script **on Windows** (if you have Docker Desktop) or the equivalent inside the VM.

### 14.1 On Windows (PowerShell)

Save the `clean.ps1` file and run it from PowerShell:

```powershell
# Navigate to the folder where you saved clean.ps1
cd C:\SHARED

# Allow script execution (first time only)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Run
.\clean.ps1
```

**Script contents:**

```powershell
# clean.ps1 — Automated Docker cleanup script
Write-Host "[INFO] Starting Docker cleanup..." -ForegroundColor Cyan

# 1. Tear down the current compose project
Write-Host " -> Docker Compose Down..." -NoNewline
docker compose down 2>$null
Write-Host " OK" -ForegroundColor Green

# 2. Force-remove ALL containers on the VM (including stuck ones)
Write-Host " -> Force-removing containers..." -NoNewline
$containers = docker ps -aq
if ($containers) {
    docker rm -f $containers 2>$null
    Write-Host " OK (containers removed)" -ForegroundColor Green
} else {
    Write-Host " OK (none found)" -ForegroundColor Gray
}

# 3. Prune unused networks (to avoid the 'network in use' error)
Write-Host " -> Pruning networks..." -NoNewline
docker network prune -f 2>$null
Write-Host " OK" -ForegroundColor Green

Write-Host "[DONE] All clean!" -ForegroundColor Cyan
```

### 14.2 VM equivalent (Bash)

If you work exclusively via SSH inside the VM, you can create an equivalent script:

```bash
#!/bin/bash
# clean.sh — Automated Docker cleanup script (Linux version)
echo "[INFO] Starting Docker cleanup..."

echo -n " -> Docker Compose Down..."
docker compose down 2>/dev/null
echo " OK"

echo -n " -> Force-removing containers..."
CONTAINERS=$(docker ps -aq)
if [ -n "$CONTAINERS" ]; then
    docker rm -f $CONTAINERS 2>/dev/null
    echo " OK (containers removed)"
else
    echo " OK (none found)"
fi

echo -n " -> Pruning networks..."
docker network prune -f 2>/dev/null
echo " OK"

echo "[DONE] All clean!"
```

Save it in the VM:

```bash
cat > ~/clean.sh << 'EOF'
#!/bin/bash
echo "[INFO] Starting Docker cleanup..."
docker compose down 2>/dev/null
docker rm -f $(docker ps -aq) 2>/dev/null
docker network prune -f 2>/dev/null
echo "[DONE] All clean!"
EOF
chmod +x ~/clean.sh
```

To run it: `~/clean.sh`

---

## 15. References and useful links

| Resource | URL |
|---|---|
| **VM MININET-SDN** (.ova file) | `https://drive.google.com/file/d/1LqnyD64gzePBjYEXpIGen41mNdjBKU3x/view?usp=drive_link` |
| **Course repository (GitHub)** | `https://github.com/hypothetical-andrei/compnet-2025-redo` |
| **VirtualBox** (download) | `https://www.virtualbox.org/wiki/Downloads` |
| **PuTTY** (download) | `https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html` |
| **Wireshark** (download) | `https://www.wireshark.org/download.html` |
| **Docker Desktop** (optional) | `https://www.docker.com/products/docker-desktop/` |
| **Docker Compose docs** | `https://docs.docker.com/compose/` |
| **Mininet docs** | `http://mininet.org/walkthrough/` |

### VM Credentials

| Field | Value |
|---|---|
| **User** | `stud` |
| **Password** | `stud` |
| **Hostname** | `mininet-vm` |
| **Internal IP** | `10.0.2.15` (NAT) |
| **SSH** | Port 22 (accessed on Windows via `127.0.0.1:2222`) |

---

## 16. Appendix A — Linux host guide (alternative)

If you use **Linux** (Ubuntu/Debian/Fedora) as your host operating system instead of Windows, the installation is similar with a few differences.

### Installing VirtualBox on Linux (Ubuntu/Debian)

```bash
# Add the Oracle repository
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib"

# Install
sudo apt update
sudo apt install virtualbox-7.0

# Or install from the distribution's own repository:
sudo apt install virtualbox
```

### Importing the OVA on Linux

```bash
VBoxManage import ~/Downloads/MININET-SDN.ova
```

### Configuring Port Forwarding from the command line

```bash
VBoxManage modifyvm "MININET-SDN" --natpf1 "ssh,tcp,127.0.0.1,2222,,22"
VBoxManage modifyvm "MININET-SDN" --natpf1 "http-test,tcp,127.0.0.1,8080,,8080"
```

### SSH connection (without PuTTY)

Linux has a native SSH client:

```bash
ssh -p 2222 stud@127.0.0.1
# Password: stud
```

### Wireshark on Linux

```bash
sudo apt install wireshark
# When asked about setuid: answer "Yes"
sudo usermod -aG wireshark $USER
# Log out and back in, then:
wireshark &
```

### Shared Folders on Linux

```bash
# After configuring via the VirtualBox GUI:
# Add your user to the vboxsf group
sudo usermod -aG vboxsf $USER
# Log out and back in
# The folder will be at: /media/sf_SHARED/
```

---

**Best of luck with the labs!**

> If you encounter problems not covered by this guide, contact the lab instructor or open an issue on the course repository.

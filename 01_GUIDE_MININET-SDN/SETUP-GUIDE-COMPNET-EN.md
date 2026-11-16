# Installation and Configuration Guide — Computer Networks and SDN

## The MININET-SDN virtual workstation on Windows

**Course:** Networking and SDN — Year 3, Semester 2, Economic Informatics, ASE-CSIE  
**Author:** ing. dr. Antonio Clim  
**Last updated:** 16 November 2026  
**Level:** Step-by-step guide; no prior virtualisation knowledge required

The MININET-SDN appliance was built, configured and tested by Antonio Clim for the ASE laboratories. This guide explains how students use that appliance and the files in the current COMPNET-EN repository.

**On an ASE classroom PC:** use the existing MININET-SDN VM. Start at Section 6, check the available connection and continue to Section 11. The institutional deployment script used to prepare classroom PCs is not a student prerequisite.

**On your own PC:** follow the installation and import steps below. The Zenodo DOI has been reserved; publication is pending. See Section 4 for the current download status.

## Contents

1. [What runs where](#1-what-runs-where)
2. [Hardware and software requirements](#2-hardware-and-software-requirements)
3. [Installing VirtualBox](#3-installing-virtualbox)
4. [Obtaining and importing MININET-SDN](#4-obtaining-and-importing-mininet-sdn)
5. [Configuring NAT and port forwarding](#5-configuring-nat-and-port-forwarding)
6. [First boot and component checks](#6-first-boot-and-component-checks)
7. [Connecting through SSH](#7-connecting-through-ssh)
8. [Using Docker inside the VM](#8-using-docker-inside-the-vm)
9. [Capturing and inspecting traffic](#9-capturing-and-inspecting-traffic)
10. [Transferring files](#10-transferring-files)
11. [Obtaining the course repository](#11-obtaining-the-course-repository)
12. [Testing the student workflow](#12-testing-the-student-workflow)
13. [Troubleshooting](#13-troubleshooting)
14. [Stopping your lab scenario](#14-stopping-your-lab-scenario)
15. [References and useful links](#15-references-and-useful-links)
16. [Linux hosts and the separate WSL route](#16-linux-hosts-and-the-separate-wsl-route)

---

## 1. What runs where

The supplied workstation provides the Ubuntu environment used for Mininet, Open vSwitch, Docker Engine, packet capture and the Python networking exercises. Keep the two operating systems distinct when copying commands:

| Location | What you do there |
|---|---|
| Windows host | Start VirtualBox, import the OVA on a personal PC, open PuTTY or PowerShell, inspect saved captures with Wireshark |
| Ubuntu guest — VM console or an SSH terminal | Clone COMPNET-EN, run Python, Mininet, Docker Compose, curl and packet captures |
| A Docker container inside the guest | Run commands explicitly introduced with `docker compose ... exec` |
| Mininet CLI (`mininet>`) | Run commands prefixed with a Mininet host, such as `h1 ping ...` |

In the Docker exercises, **host means the Ubuntu VM that runs Docker Engine**. It does not mean Windows. In S08, both the Python backend and the host-networked nginx container use the guest's network stack.

The main route requires VirtualBox, an SSH client and optionally the Wireshark desktop application on Windows. Docker Desktop is not required. Its separate Docker engine does not manage the containers running inside MININET-SDN.

## 2. Hardware and software requirements

| Component | Guidance for a personal PC |
|---|---|
| Processor | Intel/AMD x86-64 with hardware virtualisation enabled |
| RAM | 8 GB on the host; allocate at least 2 GB to the VM. 16 GB host RAM gives more room for other applications |
| Storage | Check the virtual disk size shown during import. Allow additional free space for the 1.18 GB download, the imported disk, repository files and Docker images |
| Operating system | A Windows installation supported by the VirtualBox release you install |
| Network | Needed for the repository, container image pulls and any exercise that installs dependencies at startup |

On Windows, open **Task Manager → Performance → CPU** and check that **Virtualisation** is enabled. If it is disabled on a personal PC, enable Intel VT-x or AMD-V/SVM in BIOS/UEFI. On a classroom PC, contact the instructor instead of changing the machine configuration.

If Hyper-V or WSL2 is already installed, consult the current VirtualBox host requirements if startup or performance problems occur. Follow the supplied VM route without altering unrelated working projects.

## 3. Installing VirtualBox

Skip this section when VirtualBox and MININET-SDN are already available on the classroom PC.

1. Open the [official VirtualBox download page](https://www.virtualbox.org/wiki/Downloads).
2. Download the installer for **Windows hosts** supported by your Windows version.
3. Run the installer and retain the default components. Installation may require administrator approval and may briefly interrupt host networking.
4. Open **Oracle VirtualBox Manager** after installation.

The networking examples in this guide use NAT, SSH and shared folders. They do not require the separately licensed Extension Pack. Guest Additions inside the VM provide shared-folder support; they are a different component.

## 4. Obtaining and importing MININET-SDN

### 4.1 Publication status and exact file identity

**Reserved Zenodo DOI — publication pending:** [https://doi.org/10.5281/zenodo.24289763](https://doi.org/10.5281/zenodo.24289763).

The verified Zenodo export describes a **draft**. The DOI is reserved and must not yet be treated as a public download. Until publication, classroom students use the installed VM and home students use a copy supplied by the instructor. After publication, the DOI landing page will provide the release files.

| Field | Value |
|---|---|
| OVA filename | `MININET-SDN.ova` |
| Exact size of the deposited file | `1182349312` bytes — approximately 1.18 GB |
| SHA-256 | `e2e02971bc23546e9e46914e1fcd249411afdcba281b8c21a1dfba153844dff5` |

On **Windows PowerShell**, open the folder containing your downloaded OVA and run:

```powershell
$expected = 'e2e02971bc23546e9e46914e1fcd249411afdcba281b8c21a1dfba153844dff5'
$actual = (Get-FileHash -LiteralPath .\MININET-SDN.ova -Algorithm SHA256).Hash
if ($actual -ieq $expected) { 'SHA-256: MATCH' } else { throw 'SHA-256: MISMATCH' }
(Get-Item -LiteralPath .\MININET-SDN.ova).Length
```

A matching hash identifies the deposited file. Do not apply this expected hash to a later re-export: a new OVA requires its own checksum and version information.

### 4.2 Import on your personal PC

1. Open **VirtualBox → File → Import Appliance** (`Ctrl+I`).
2. Select `MININET-SDN.ova` and click **Next**.
3. Review the imported settings: name `MININET-SDN`, 2 virtual CPUs and at least 2048 MB RAM are suitable starting values. Retain the appliance's other working settings.
4. Check the proposed disk location and available space.
5. Click **Import** and wait until the VM appears in VirtualBox Manager.

Use an existing classroom VM directly; importing another copy is unnecessary. If a VM with the same name already exists on your personal PC, distinguish the new copy before import instead of overwriting your work.

## 5. Configuring NAT and port forwarding

For a new personal-PC import, keep **Adapter 1 attached to NAT**. With the VM powered off, open **Settings → Network → Adapter 1 → Advanced → Port Forwarding**.

| Rule | Protocol | Host IP | Host port | Guest IP | Guest port |
|---|---|---|---|---|---|
| `ssh` | TCP | `127.0.0.1` | `2222` | Leave blank for the NAT-assigned guest | `22` |
| `http-test` — optional Windows browser access | TCP | `127.0.0.1` | `8080` | Leave blank for the NAT-assigned guest | `8080` |

Add each missing rule with **+**, then save with **OK**. Inspect existing rules first; do not add duplicate rules to a working classroom VM. The usual NAT guest address is `10.0.2.15`, but the connection from Windows uses `127.0.0.1` and the configured host port.

SSH forwarding is sufficient for the primary workflow. The HTTP rule is needed only if you want a Windows browser to reach nginx inside the guest. All curl tests below run inside the VM and do not require that HTTP rule.

No Docker TCP API forwarding is needed: Docker commands run in the SSH session inside the guest.

## 6. First boot and component checks

Start **MININET-SDN** and wait for the console login prompt. Use the course account:

```text
Username: stud
Password: stud
```

The password is not displayed while you type. Keep the standard classroom account unchanged unless instructed otherwise.

Run these checks **inside the VM**:

```bash
cat /etc/os-release
python3 --version
docker --version
docker compose version
mn --version
ovs-vsctl --version
command -v tshark
command -v osken-manager
```

A version command confirms that a client program is available; it does not by itself prove that its service or an exercise works. Section 12 tests actual course scenarios.

The course Python environment is normally activated at login. If the prompt does not show `(compnet)` and the environment exists, activate it:

```bash
test -f "$HOME/venvs/compnet/bin/activate" && source "$HOME/venvs/compnet/bin/activate"
python3 -c "import scapy, paramiko, flask; print('Course Python imports: OK')"
```

Preserve the working course environment. S06 uses the installed **osken-manager** entry point. OS-Ken 4.x removed that command, so upgrading the package blindly is not a repair for a missing command. The S06 instructions explain how to check the installed environment.

## 7. Connecting through SSH

### 7.1 Windows built-in SSH

Open **PowerShell on Windows** and run:

```powershell
ssh -p 2222 stud@127.0.0.1
```

Check that the host and port refer to your intended VM before accepting its first host-key prompt. Enter the course password. Once connected, Bash commands run inside Ubuntu even though the terminal window is on Windows.

### 7.2 PuTTY alternative

1. Install PuTTY from its [official download page](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), if it is not already installed.
2. Set **Host Name** to `127.0.0.1`, **Port** to `2222` and **Connection type** to **SSH**.
3. Save the session as `MININET-SDN` and click **Open**.
4. Log in as `stud` with the course password.

Select text to copy in PuTTY; right-click to paste. Saved sessions make it easy to open the second terminal needed for capture exercises. In **Connection**, a keepalive interval of 30 seconds can help with idle sessions.

## 8. Using Docker inside the VM

Run all course Docker commands in the **Ubuntu guest**, through its console or SSH. Check the server as well as the client:

```bash
docker info --format '{{.ServerVersion}}'
docker compose version
docker run --rm hello-world
```

The first `hello-world` run may pull an image from the internet. A download or DNS failure is different from a stopped Docker service; retain the error message for troubleshooting.

Compose files in this repository often have descriptive filenames. Always supply their actual filename, for example:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S08/4_nginx"
docker compose -f S08_Part04_Config_Docker_Compose.yml config --quiet
```

The same `-f` argument is required for `up`, `ps`, `logs` and `down`. A bare `docker compose up` does not automatically select `S08_Part04_Config_Docker_Compose.yml`.

If you already use Docker Desktop for another project, leave it separate. It is not needed to operate the Docker engine inside MININET-SDN.

## 9. Capturing and inspecting traffic

### 9.1 Wireshark on Windows

Download the Windows installer from the [official Wireshark site](https://www.wireshark.org/download.html). Npcap is needed for live capture on Windows interfaces. Opening an existing capture file is a separate operation.

Windows loopback capture can show the SSH connection on host port 2222. It does not expose the decrypted commands or all traffic between Mininet hosts and guest containers. Capture that internal traffic inside the VM, then transfer the saved file.

### 9.2 A bounded capture using two SSH terminals

First start the S08 backend and nginx scenario in **Terminal A**, following Section 12.2. Keep that terminal open. Open a second SSH session, **Terminal B**, and run:

```bash
mkdir -p "$HOME/compnet-captures"
capture_file="$HOME/compnet-captures/s08-$(date -u +%Y%m%dT%H%M%SZ).pcapng"
sudo tshark -i lo -a duration:20 -f 'tcp port 8080 or tcp port 8000' -w "$capture_file"
sudo chown "$(id -u):$(id -g)" "$capture_file"
printf 'Capture saved: %s\n' "$capture_file"
```

While Terminal B displays **Capturing on**, run in **Terminal A**:

```bash
curl --fail --show-error --max-time 5 -I http://127.0.0.1:8080/
curl --fail --show-error --max-time 5 http://127.0.0.1:8080/
```

The capture ends after 20 seconds even if no packets arrive. Wait for completion before copying the file. The `lo` interface is appropriate here because S08 uses host networking and both test endpoints are inside the guest. For a bridge-network container exercise, select its actual bridge/interface or use `-i any`; `docker0` is not automatically the interface for every Compose network.

Copy the file using Section 10 and open it with Wireshark. Look for the request to nginx on port 8080 and its separate backend request on port 8000. A capture with zero matching packets is a diagnostic result, not a successful traffic test.

## 10. Transferring files

### 10.1 VirtualBox Shared Folders

On Windows, create `C:\SHARED`. In **VirtualBox → Settings → Shared Folders**, add:

| Setting | Value |
|---|---|
| Folder Path | `C:\SHARED` |
| Folder Name | `SHARED` |
| Read-only | Unticked |
| Auto-mount | Ticked |
| Mount point | Leave blank |

Start the VM or reopen the SSH session, then check **inside the guest**:

```bash
ls -ld /media/sf_SHARED
printf 'hello from the VM\n' > /media/sf_SHARED/compnet-transfer-check.txt
```

The test file should appear in `C:\SHARED` on Windows. After a completed capture in Terminal B, copy its exact file:

```bash
cp -- "$capture_file" /media/sf_SHARED/
```

If the mount exists but access is denied, check `id` and the `vboxsf` group. On your own VM, `sudo usermod -aG vboxsf stud` followed by logout/login can correct a missing membership. On classroom PCs, ask the instructor before changing configuration.

### 10.2 SCP alternative

Shared folders are convenient but not required. In **Windows PowerShell**, copy the completed captures through the existing SSH connection:

```powershell
scp -P 2222 'stud@127.0.0.1:compnet-captures/*.pcapng' .
```

This downloads the files into the current Windows directory. PuTTY installations can use `pscp` with the same uppercase `-P` port option.

## 11. Obtaining the course repository

### 11.1 Git clone inside the VM

For a new student copy, run **inside Ubuntu**:

```bash
cd "$HOME"
git clone https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
ls
```

If `COMPNET-EN` already exists, inspect that directory and your work instead of cloning over it. To update an existing Git clone, inspect `git status` and use `git pull --ff-only` only when the working copy is ready to update.

The current top-level directories include:

| Directory | Contents |
|---|---|
| `00_TOOLS/` | Utilities and alternative environment instructions |
| `01_GUIDE_MININET-SDN/` | This guide and the VM verification helper |
| `02_PROJECTS/` | Project specifications and supporting assets |
| `03_LECTURES/` | Lecture materials |
| `04_SEMINARS/` | Seminar instructions, scripts and configurations |
| `00_APPENDIX/` | Supplementary learning and teaching materials |

### 11.2 ZIP alternative

On Windows, download the [current repository ZIP](https://github.com/antonioclim/COMPNET-EN/archive/refs/heads/main.zip). Put `COMPNET-EN-main.zip` in `C:\SHARED`. In the VM:

```bash
cd "$HOME"
unzip /media/sf_SHARED/COMPNET-EN-main.zip
```

If `~/COMPNET-EN` does not already exist, normalise the extracted directory name so the later commands work unchanged:

```bash
if [ -e "$HOME/COMPNET-EN" ]; then
    printf 'COMPNET-EN already exists; keep your existing work and select the intended copy.\n'
else
    mv -- "$HOME/COMPNET-EN-main" "$HOME/COMPNET-EN"
fi
```

A ZIP checkout has no Git history. Do not run `git pull` inside it.

### 11.3 Check the supplied environment

From the repository root:

```bash
cd "$HOME/COMPNET-EN"
bash 01_GUIDE_MININET-SDN/verify_mininet_vm.sh
```

The helper reads the available environment and reports missing requirements. It does not install packages or repair the VM. Keep its output if a required component is missing.

No separate compatibility script is needed to find the course files. The commands below use their real paths and explicit Compose filenames. The institutional classroom deployment script is not part of the student setup route.

## 12. Testing the student workflow

These checks exercise specific paths. Successful results establish those paths on your machine; they do not replace the remaining seminar exercises.

### 12.1 Mininet check

Run in the VM, when no other Mininet exercise is active:

```bash
sudo mn --switch ovsbr --controller none --test pingall
```

This uses an OVS bridge without a remote controller and should report zero dropped pings. S06 separately tests the Os-Ken/OpenFlow controller path; follow the [S06 instructions](../04_SEMINARS/S06/README.md) for that exercise.

### 12.2 S08: backend, nginx and HTTP

Run this sequence in **SSH Terminal A inside the guest**. Keep the terminal open so the backend process identifier remains available for cleanup.

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S08/4_nginx"
ss -ltn '( sport = :8000 or sport = :8080 )'
```

If either port is already in use, identify your previous exercise before continuing. Start the backend using a new log file:

```bash
backend_log=$(mktemp /tmp/compnet-s08-backend.XXXXXX)
python3 -m http.server 8000 --bind 127.0.0.1 --directory ../2_simple-http >"$backend_log" 2>&1 &
backend_pid=$!
printf 'Backend PID: %s; log: %s\n' "$backend_pid" "$backend_log"
curl --fail --show-error --retry 5 --retry-connrefused --retry-delay 1 --max-time 5 http://127.0.0.1:8000/
```

Then start nginx with the actual configuration file:

```bash
docker compose -f S08_Part04_Config_Docker_Compose.yml config --quiet
docker compose -f S08_Part04_Config_Docker_Compose.yml up -d
docker compose -f S08_Part04_Config_Docker_Compose.yml ps
curl --fail --show-error --retry 5 --retry-connrefused --retry-delay 1 --max-time 5 -I http://127.0.0.1:8080/
curl --fail --show-error --max-time 5 http://127.0.0.1:8080/
```

Expected evidence: HTTP 200, an `X-Student-Lab: Seminar8` response header and the backend content. An `Up` container alone is insufficient. The supplied configuration uses `network_mode: host`, so nginx can reach the Python backend at the guest's `127.0.0.1:8000`.

For the packet capture, keep this scenario running and follow Section 9 in Terminal B. If you configured the optional NAT HTTP rule, a Windows browser can also open `http://127.0.0.1:8080/`.

When finished, run **in the same Terminal A**:

```bash
docker compose -f S08_Part04_Config_Docker_Compose.yml down
kill "$backend_pid"
wait "$backend_pid" 2>/dev/null || true
```

Only the backend started by this sequence and this Compose project are stopped.

### 12.3 S09: one client uploads, another downloads

Run in the VM:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S09/3_multi-client-containers"
mkdir -p server-data server-anon client1-data client2-data
printf 'Hello from client1\n' > client1-data/setup-check.txt
docker compose -f S09_Part03_Config_Docker_Compose.yml config --quiet
docker compose -f S09_Part03_Config_Docker_Compose.yml up -d
docker compose -f S09_Part03_Config_Docker_Compose.yml ps
```

Image downloads and the FTP server's initial dependency installation require internet access unless the required artefacts are already available. Wait for FTP readiness with this bounded check:

```bash
docker compose -f S09_Part03_Config_Docker_Compose.yml exec -T client1 python - <<'PYREADY'
import ftplib
import time

deadline = time.monotonic() + 60
while True:
    try:
        with ftplib.FTP() as ftp:
            ftp.connect('ftp-server', 2121, timeout=2)
            ftp.login('test', '12345')
            print('FTP login: OK')
        break
    except (OSError, ftplib.Error) as exc:
        if time.monotonic() >= deadline:
            raise SystemExit(f'FTP not ready: {exc}')
        time.sleep(1)
PYREADY
```

Then exercise the supplied clients:

```bash
docker compose -f S09_Part03_Config_Docker_Compose.yml exec -T client1 python S09_Part03_Script_Pyftpd_Multi_Client.py upload setup-check.txt
docker compose -f S09_Part03_Config_Docker_Compose.yml exec -T client2 python S09_Part03_Script_Pyftpd_Multi_Client.py download setup-check.txt
cmp client1-data/setup-check.txt client2-data/setup-check.txt && printf 'Transferred file: MATCH\n'
docker compose -f S09_Part03_Config_Docker_Compose.yml down
```

The expected evidence is a successful upload, a successful download and `Transferred file: MATCH`. The test uses the shared container network, where both clients can resolve `ftp-server`. Publishing an FTP control port alone does not establish a working passive data path from Windows; that separate networking case is not required here.

## 13. Troubleshooting

### VM startup or SSH connection fails

Check that the intended VM is running and that the NAT forwarding rule exists. From the VM console, inspect:

```bash
systemctl status ssh --no-pager
```

On your own VM, start the service if it is stopped:

```bash
sudo systemctl start ssh
```

Check host port conflicts before changing a working forwarding rule. On classroom PCs, retain the configuration provided by the instructor.

### Docker reports permission denied or cannot connect

Run inside the VM:

```bash
id
systemctl status docker --no-pager
docker context show
```

Use the guest's local Docker engine. On your own VM, a missing `docker` group membership can be corrected with `sudo usermod -aG docker stud`, followed by logout/login. A stopped service is a separate issue. Do not redirect Docker to a different engine to hide the original error.

### Compose reports no configuration file

Change to the scenario directory and include the actual filename with `-f`. For S08:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S08/4_nginx"
docker compose -f S08_Part04_Config_Docker_Compose.yml config --quiet
```

### Port conflict or nginx returns 502

Inspect the listeners and scenario logs:

```bash
ss -ltn '( sport = :8000 or sport = :8080 )'
docker compose -f S08_Part04_Config_Docker_Compose.yml logs --tail 30 nginx
curl --fail --show-error --max-time 5 http://127.0.0.1:8000/
```

A 502 response commonly means nginx cannot reach its backend. Confirm that the Python server runs in the same Ubuntu guest and inspect the backend log created in Section 12. Stop only your own conflicting exercise using Section 14.

### FTP containers exist but login or transfer fails

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S09/3_multi-client-containers"
docker compose -f S09_Part03_Config_Docker_Compose.yml logs --tail 40 ftp-server
```

Look for a failed image/dependency download, a missing bind-mounted file or a server startup error. Retry the readiness check after resolving the cause. For the supplied scenario, run the clients inside `client1` and `client2`.

### Shared folder missing or capture unavailable

Confirm the VirtualBox share name `SHARED`, Auto-mount and the guest's `vboxsf` membership. Use SCP if shared folders are unavailable. Wait for the bounded capture to finish before transferring it. Select the interface where the exercise traffic actually flows; S08 loopback traffic does not use `docker0`.

### Python import or osken-manager missing

Activate the existing course environment and inspect its installed package:

```bash
test -f "$HOME/venvs/compnet/bin/activate" && source "$HOME/venvs/compnet/bin/activate"
command -v python3
command -v osken-manager
python3 -c "from importlib.metadata import version; print(version('os-ken'))"
```

Do not replace the course environment with an unpinned upgrade. OS-Ken 4.x no longer supplies the legacy manager command. Keep the diagnostic output and use the course environment supplied with the appliance or ask the instructor to restore it.

### Mininet fails

Read the exact error. Check the installed tools and Open vSwitch service:

```bash
command -v mn
command -v ovs-vsctl
systemctl status openvswitch-switch --no-pager
```

A missing executable is not the same as a stopped service. If no other Mininet exercise is active, `sudo mn -c` can clear remnants of your failed Mininet run. Repeat the Section 12.1 check after resolving the cause.

## 14. Stopping your lab scenario

Run cleanup **inside the VM** with the same Compose file used to start that scenario:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S08/4_nginx"
docker compose -f S08_Part04_Config_Docker_Compose.yml down
```

For S09:

```bash
cd "$HOME/COMPNET-EN/04_SEMINARS/S09/3_multi-client-containers"
docker compose -f S09_Part03_Config_Docker_Compose.yml down
```

These commands stop and remove the selected project's containers and networks. The bind-mounted exercise files remain in their directories. Stop the separately launched S08 Python backend with its recorded PID in the original terminal, as shown in Section 12.2.

For an interactive Mininet exercise, type `exit` at `mininet>` so its script can stop its topology. Stop the controller with `Ctrl+C` in the controller terminal. Use `sudo mn -c` only when no other Mininet session is active and a failed run left resources behind.

There is no need to run a Windows-wide or Docker-wide cleanup script. Keep other projects and their containers intact.

## 15. References and useful links

| Resource | Link |
|---|---|
| MININET-SDN DOI — reserved, publication pending | [Zenodo DOI](https://doi.org/10.5281/zenodo.24289763) |
| Course repository | [antonioclim/COMPNET-EN](https://github.com/antonioclim/COMPNET-EN) |
| VirtualBox downloads and documentation | [virtualbox.org](https://www.virtualbox.org/wiki/Downloads) |
| PuTTY | [Official download page](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) |
| Wireshark | [Downloads](https://www.wireshark.org/download.html) |
| Explicit Compose files | [Docker Compose CLI documentation](https://docs.docker.com/reference/cli/docker/compose/) |
| Docker network modes | [Docker Compose networking](https://docs.docker.com/compose/how-tos/networking/) |
| Mininet walkthrough | [mininet.org](https://mininet.org/walkthrough/) |
| OS-Ken application API | [OpenStack documentation](https://docs.openstack.org/os-ken/latest/os_ken_app_api.html) |
| OS-Ken manager removal in 4.x | [OS-Ken 2026.1 release notes](https://docs.openstack.org/releasenotes/os-ken/2026.1.html) |

Use the version-specific appliance DOI together with the matching checksum when identifying the course image. A reserved DOI becomes a public record only after publication.

## 16. Linux hosts and the separate WSL route

### 16.1 A Linux host running VirtualBox

Install a VirtualBox release supported by your Linux distribution using its documented package route or the [official Linux download instructions](https://www.virtualbox.org/wiki/Linux_Downloads). Import the same OVA through VirtualBox Manager. The guest-side commands remain the same.

With a new VM powered off, the equivalent NAT SSH rule can be added from the Linux host:

```bash
VBoxManage modifyvm "MININET-SDN" --natpf1 "ssh,tcp,127.0.0.1,2222,,22"
```

Inspect existing rules first to avoid duplicates. Connect from the Linux host:

```bash
ssh -p 2222 stud@127.0.0.1
```

Use SCP or a configured VirtualBox share for captures. A `vboxsf` group change, if needed, belongs **inside the guest**, where the share is mounted. Opening saved captures on the Linux host does not require a live-capture privilege change.

### 16.2 WSL is a separate environment

The [WSL prerequisites](../00_TOOLS/Prerequisites/Prerequisites.md) describe another course setup route. Its account, virtual environment, service addresses and installation steps must be followed as a complete route. Do not combine institutional WSL deployment settings with the VirtualBox account, ports or paths in this guide.

For students using the supplied MININET-SDN appliance, continue with its existing guest environment and the seminar instructions.

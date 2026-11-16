# MININET-SDN — VirtualBox lab environment

MININET-SDN is the virtual workstation used for Networking and SDN in the
second semester of the third-year Economic Informatics undergraduate programme
at ASE CSIE. Antonio Clim built, configured and tested the appliance for the
teaching laboratories. Students can import the same appliance on a compatible
personal computer.

## Download the lab virtual machine

**Version 1.0.0:** [https://doi.org/10.5281/zenodo.24289763](https://doi.org/10.5281/zenodo.24289763)

**Publication status:** Published on 16 November 2026.
Download `MININET-SDN.ova` and `SHA256SUMS.txt` from the
[Zenodo release record](https://zenodo.org/records/24289763).

| Item | Value |
|---|---|
| Appliance | MININET-SDN.ova |
| File size | 1,182,349,312 bytes (1.182 GB / 1.101 GiB) |
| SHA-256 | e2e02971bc23546e9e46914e1fcd249411afdcba281b8c21a1dfba153844dff5 |
| Machine-readable identity | [appliance.json](appliance.json) |
| Checksum manifest | [SHA256SUMS.txt](SHA256SUMS.txt) |
| Installation | [Markdown guide](SETUP-GUIDE-COMPNET-EN.md) or [HTML guide](SETUP-GUIDE-COMPNET-EN.html) |

The DOI identifies the virtual appliance. The course materials remain in
[COMPNET-EN](https://github.com/antonioclim/COMPNET-EN). Use this specific appliance
version when following instructions for the corresponding teaching environment.

The [concept DOI](https://doi.org/10.5281/zenodo.24289762) represents all versions
of the appliance. Use the version-specific DOI above with the matching checksum
to identify the exact classroom image; the concept DOI follows the latest release.

### Cite this appliance

Clim, A. (2026). *MININET-SDN: VirtualBox lab environment for computer networking
and software-defined networking* (Version 1.0.0) [Software]. Zenodo.
[https://doi.org/10.5281/zenodo.24289763](https://doi.org/10.5281/zenodo.24289763)

### Verify the download

Download the OVA and SHA256SUMS.txt into the same directory. In Windows PowerShell:

~~~powershell
$expected = ((Get-Content -LiteralPath .\SHA256SUMS.txt -TotalCount 1) -split '  ', 2)[0]
$actual = (Get-FileHash -LiteralPath .\MININET-SDN.ova -Algorithm SHA256).Hash
if ($actual -ieq $expected) { 'SHA-256: MATCH' } else { throw 'SHA-256: MISMATCH' }
~~~

On GNU/Linux, from that directory:

~~~bash
sha256sum -c SHA256SUMS.txt
~~~

## Choose the correct setup route

| Situation | Route |
|---|---|
| ASE classroom PC with MININET-SDN already installed | Start the existing VM and use the course repository inside it. |
| Student's compatible personal computer | Import the OVA in VirtualBox and follow this directory's setup guide. |
| WSL2 alternative for supported exercises | Use [00_TOOLS/Prerequisites](../00_TOOLS/Prerequisites/). That checker is separate from the VM checks. |
| Institutional PC provisioning | The ASE deployment script is an administrator's multi-subject setup tool; it is not required for student OVA import. |

Docker Engine runs **inside the VM** on the appliance route. The Windows host
provides VirtualBox and, optionally, an SSH client and Wireshark. Installing
Docker Desktop or the institutional WSL stack is not part of importing this OVA.

The course guide documents Ubuntu 24.04, x86-64, 2 vCPUs and at least 2048 MB
guest RAM. These are the guide's configuration baseline. Host requirements,
network settings and access instructions are in the setup guide; the compressed
OVA size is not the amount of disk space needed after import.

## First use and prerequisite checks

1. Import the OVA using VirtualBox's Import Appliance dialogue.
2. Use NAT. If SSH is required, forward host 127.0.0.1:2222 to guest port 22.
3. Start the guest and use the documented lab account, stud / stud.
4. Obtain the COMPNET-EN repository inside the guest.
5. From the repository root, run the guest prerequisite checker:

~~~bash
bash 01_GUIDE_MININET-SDN/verify_mininet_vm.sh
~~~

The checker reads versions, tests imports and probes access to the Docker daemon
and the OVS service. It does not install packages, create containers, start a
Mininet topology or request sudo. It prefers the existing course Python at
~/venvs/compnet/bin/python3 when present. It returns 1 for required failures and 2
for configuration warnings.

A successful prerequisite check is followed by the functional exercises in the
[setup guide](SETUP-GUIDE-COMPNET-EN.md) and [S06](../04_SEMINARS/S06/).
The SDN route uses the course environment's osken-manager command. OS-Ken 4 removed
that command, so an unpinned upgrade is not a substitute for the prepared course
environment. The optional requirements file preserves the pre-4 CLI compatibility
range; it is not a lockfile of the appliance's installed packages.

For the packet-capture exercises, capture inside the guest when inspecting
Mininet links or Docker networks. Host Wireshark does not directly expose every
interface inside the VM.

## Files in this directory

| File | Purpose |
|---|---|
| [SETUP-GUIDE-COMPNET-EN.md](SETUP-GUIDE-COMPNET-EN.md) | Student instructions, command contexts, examples and troubleshooting |
| [SETUP-GUIDE-COMPNET-EN.html](SETUP-GUIDE-COMPNET-EN.html) | Browser version of the installation guide |
| [verify_mininet_vm.sh](verify_mininet_vm.sh) | Read-only guest prerequisite probes |
| [SHA256SUMS.txt](SHA256SUMS.txt) | Integrity reference for the OVA |
| [appliance.json](appliance.json) | Version, DOI and exact file identity |

## Course connections

| Material | Role |
|---|---|
| [S01](../04_SEMINARS/S01/) | First practical session |
| [S05](../04_SEMINARS/S05/) | Addressing and Mininet simulation |
| [S06](../04_SEMINARS/S06/) | Routing, OpenFlow and application traffic |
| [C07](../03_LECTURES/C07/) | Routing theory and demonstrations |
| [Projects](../02_PROJECTS/) | Application and SDN project briefs |
| [Portainer setup](../00_TOOLS/Portainer/INIT_GUIDE/) | Optional container interface; use the guest's Docker daemon |
| [Instructor notes](../00_APPENDIX/d%29instructor_NOTES4sem/) | Teaching and delivery guidance |

## Provenance and distribution

- Appliance author and course maintainer: ing. dr. Antonio Clim, ASE CSIE.
- File identity: supplied by the author's PowerShell SHA-256 computation on
  16 November 2026 and checked for consistency with the published Zenodo export.
- The author confirmed that the appliance was built, configured and tested for
  the ASE laboratories.
- Third-party software retains its own licences. Course materials keep the terms
  in [LICENCE.md](../LICENCE.md); the OVA is not a blanket relicensing of its
  operating system and installed packages.

## Obtain the teaching repository

~~~bash
git clone https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
~~~

For a ZIP download, use GitHub's Code → Download ZIP and follow the setup guide's
ZIP instructions. Downloading the course repository does not download the OVA.

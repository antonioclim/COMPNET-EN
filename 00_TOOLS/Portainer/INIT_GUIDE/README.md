# Portainer — Installation and Configuration

Portainer is optional: Docker commands can run without its web interface. The course uses host port **9050**, with the HTTP listener bound to **127.0.0.1**. Port 9000 is available for the S10 SSH tunnel exercise.

## Choose the machine that runs Docker

| Docker runs in | Use | Browser access |
|---|---|---|
| MININET-SDN VirtualBox guest | `bash portainer-init.sh` inside the guest | SSH tunnel described in the [setup guide](PORTAINER_SETUP.md) |
| Ubuntu in WSL2 | `bash portainer-init.sh` inside that distribution | Windows `http://localhost:9050`, subject to WSL localhost forwarding |
| Docker Desktop on Windows, Linux containers | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\portainer-init.ps1` | Windows `http://localhost:9050` |

The Windows script does not install or manage Docker inside the VirtualBox guest. Do not install Docker Desktop merely to use Docker already running in MININET-SDN.

## Files

| File | Purpose |
|---|---|
| [PORTAINER_SETUP.md](PORTAINER_SETUP.md) | Import route, commands, access and troubleshooting |
| [docker-compose-portainer.yml](docker-compose-portainer.yml) | Declarative container setup; initial administrator setup is separate |
| [portainer-init.sh](portainer-init.sh) | Local Linux/WSL/VM setup with API, login and Docker connectivity checks |
| [portainer-init.ps1](portainer-init.ps1) | Local Windows Docker Desktop setup; PowerShell 5.1 syntax |

The scripts preserve existing containers, accounts and volumes. They reuse a matching local instance or stop with a diagnostic if it differs. They do not reset existing passwords, delete data or update an existing image automatically. An uncached image requires internet access. A cached image can be used without pulling it again.

The default image remains the kit's `portainer/portainer-ce:2.21-alpine`. This tag identifies a version family, not an immutable image digest. A successful API and Docker check is required for the selected Docker/Portainer pair; the tag alone does not establish compatibility with every Docker release.

## Related materials

- [MININET-SDN setup](../../../01_GUIDE_MININET-SDN/)
- [Alternative WSL2 prerequisites](../../Prerequisites/Prerequisites.md)
- [Portainer in S08](../SEMINAR08/S08_PORTAINER_TEASER.md)
- [Portainer in S09](../SEMINAR09/S09_PORTAINER_GUIDE.md)

## Selective checkout

```bash
git clone --filter=blob:none --sparse https://github.com/antonioclim/COMPNET-EN.git
cd COMPNET-EN
git sparse-checkout set 00_TOOLS/Portainer/INIT_GUIDE
```

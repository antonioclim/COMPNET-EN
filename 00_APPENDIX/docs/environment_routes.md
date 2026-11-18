# Choose one environment route

The course repository is **COMPNET-EN**. The primary ready-made appliance is
[MININET-SDN 1.0.0](https://doi.org/10.5281/zenodo.24289763); its version is independent
of the repository release. Follow the [VirtualBox guide](../../01_GUIDE_MININET-SDN/SETUP-GUIDE-COMPNET-EN.md)
or the separate [WSL guide](../../00_TOOLS/Prerequisites/Prerequisites.md).

| Route | Where lab commands run | Docker daemon | Portainer access if installed |
|---|---|---|---|
| VirtualBox OVA | Linux guest, normally user `stud` | Inside the guest | Guest `http://127.0.0.1:9050`; Windows needs an explicit tunnel/forward |
| WSL2 with native Engine | Selected Linux distribution | That distribution's Engine | `http://localhost:9050` in Windows when WSL forwarding works |
| Docker Desktop alternative | Terminal configured for Desktop | Docker Desktop's Linux environment | `http://localhost:9050` on the Windows host |

Portainer is optional. The course installer publishes **host loopback 9050 →
container HTTP 9000**. The product's HTTPS 9443 is a different endpoint and is not
published by this course configuration. Read the actual mappings with
`docker port portainer`. Existing personal users and credentials are preserved;
the teaching account defaults apply only when the installer created that account.

From the repository root in the selected Linux route:

```bash
docker context show
docker info
bash 00_TOOLS/Portainer/INIT_GUIDE/portainer-init.sh
```

The Windows PowerShell installer is for the separately documented Docker Desktop
route. Do not use it to manage the Engine installed inside the OVA or WSL.

For Windows access to Portainer in the OVA, keep this SSH tunnel open in a separate
Windows terminal, provided local port 9050 is free:

```powershell
ssh -N -L 127.0.0.1:9050:127.0.0.1:9050 -p 2222 stud@127.0.0.1
```

Then visit `http://127.0.0.1:9050` on Windows. Close that SSH process when finished.

## Services and GUI applications in WSL

Current WSL supports systemd. Check PID 1 (`ps -p 1 -o comm=`) and the installed
WSL version before choosing `systemctl` or a non-systemd service command. Whether
Docker starts automatically depends on that configuration and whether its service
is enabled. WSLg is also available with current Store WSL on supported Windows 10
and Windows 11 installations; an external X server is not a universal Windows 10
requirement. See Microsoft's [systemd guidance](https://learn.microsoft.com/en-us/windows/wsl/systemd)
and [WSLg project](https://github.com/microsoft/wslg).

`host.docker.internal` is provided by Docker Desktop. Native Linux Engine does not
promise that alias; add an explicit `host-gateway` mapping when that is the intended
route, and ensure the host service listens on an address reachable from that network.
A service bound only to host loopback is not automatically reachable via a bridge.

## Password recovery

Keep the Portainer data volume. Follow the repository's
[Portainer recovery procedure](../../00_TOOLS/Portainer/INIT_GUIDE/PORTAINER_SETUP.md#7-troubleshooting)
and the [official password helper documentation](https://docs.portainer.io/advanced/reset-admin).
Confirm the container and volume names before running the helper. Removing the
volume erases configuration and is a separate full reset, not password recovery.

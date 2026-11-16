# Portainer CE — Installation and Configuration Guide

Portainer provides a browser interface to the Docker daemon used by the exercises. It is optional for command-line Docker work.

| Setting | Course default |
|---|---|
| Host HTTP address | `127.0.0.1:9050` |
| Container HTTP port | `9000` |
| Initial lab account | `stud` / `studstudstud` |
| Image selected by this kit | `portainer/portainer-ce:2.21-alpine` |
| Data volume | `portainer_data` |

Port 9000 is used by the S10 SSH tunnel exercise. The external Portainer port is therefore 9050. The default image is a version-family tag rather than a digest; record the actual installed image when preparing a fixed teaching release. These instructions do not upgrade the image embedded in MININET-SDN.

## 1. Choose the execution environment

**MININET-SDN VirtualBox route:** connect to the VM and run Linux commands there. Docker Desktop and the PowerShell Portainer installer are not required on Windows. The working appliance already supplies its Docker environment; do not replace its packages as part of this optional installation.

**WSL2 route:** run Linux commands in the Ubuntu distribution containing Docker Engine. Windows Python and a second Docker daemon on Windows are separate environments.

**Docker Desktop route:** run the PowerShell script on Windows with Docker Desktop running in Linux-containers mode. This operates on the local Desktop engine, not the VirtualBox guest.

All routes require a responsive local Linux Docker daemon. The Bash installer also checks for `curl`, `python3`, `ss` and `mktemp`. The scripts reject remote Docker contexts because a remote daemon cannot be reached through the local loopback URL used by this setup.

## 2. Automated setup

Run from this directory in the intended environment.

### Linux, WSL or MININET-SDN guest

```bash
bash portainer-init.sh
```

For an existing account with different credentials, supply its actual details without resetting the account:

```bash
read -r -p 'Portainer username: ' PORTAINER_USER
read -r -s -p 'Portainer password: ' PORTAINER_PASSWORD
printf '\n'
export PORTAINER_USER PORTAINER_PASSWORD
bash portainer-init.sh
unset PORTAINER_USER PORTAINER_PASSWORD
```

Optional environment variables are `PORTAINER_IMAGE`, `PORTAINER_NAME`, `PORTAINER_PORT`, `PORTAINER_VOLUME`, `PORTAINER_USER` and `PORTAINER_PASSWORD`. Set these only for a deliberate alternative instance. Changing the requested port or volume does not reconfigure an existing container automatically.

### Windows with Docker Desktop

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\portainer-init.ps1
```

This execution-policy choice applies to the new PowerShell process. The script requires no administrator elevation of its own, although Docker Desktop must already be installed and accessible.

For an existing Portainer account:

```powershell
$portainerCredential = Get-Credential -UserName stud -Message 'Existing Portainer account'
.\portainer-init.ps1 -User $portainerCredential.UserName -Password ($portainerCredential.GetNetworkCredential().Password)
Remove-Variable portainerCredential
```

The script accepts `-Image`, `-Name`, `-Port`, `-Volume`, `-User` and `-Password`.

### What the scripts verify

The scripts check the Docker daemon, its Linux container mode and the requested local binding. They preserve existing containers and volumes, reuse a matching instance and download the image only when it is absent locally. They then require a responding Portainer API, successful authentication and `OK` from the local Docker endpoint through Portainer.

A failed login, failed endpoint registration or HTTP 500 produces an error exit. An existing administrator is not treated as proof that the supplied password works. An existing service with a different binding or volume remains untouched and is reported for review.

A successful setup check verifies these management operations. It does not execute every networking seminar or validate a different Docker/Portainer version pair.

## 3. Open the interface

### Docker Desktop or WSL2

Open `http://localhost:9050` in the Windows browser. In WSL, if the Linux API responds but the Windows page does not, check WSL's localhost forwarding and the actual Docker context; do not replace the container to fix an unrelated host-access problem.

### VirtualBox guest from Windows

The guest's `127.0.0.1` is different from Windows' `127.0.0.1`. With the course SSH forwarding already configured (`127.0.0.1:2222` on Windows to guest port 22), open a Windows terminal and run:

```powershell
ssh -N -p 2222 -L 127.0.0.1:9050:127.0.0.1:9050 stud@127.0.0.1
```

Use the guest's confirmed SSH login. Keep that terminal open, then browse to `http://127.0.0.1:9050` on Windows. Stop the tunnel with Ctrl+C when finished.

If Windows port 9050 is already used by another Docker environment, use a different **Windows** port without changing Portainer in the VM:

```powershell
ssh -N -p 2222 -L 127.0.0.1:19050:127.0.0.1:9050 stud@127.0.0.1
```

Then open `http://127.0.0.1:19050`. This tunnel requires the SSH service and the matching VirtualBox SSH rule; it does not require exposing the Docker API or Portainer to the LAN.

## 4. Compose alternative

For a new instance, the included Compose file starts the container:

```bash
docker compose -f docker-compose-portainer.yml up -d
```

The Compose file does **not** create the administrator or authenticate to Docker. Use the browser for initial setup, or run the matching installer afterwards to perform those steps and its checks. Do not run Compose over an existing unmanaged container of the same name expecting an automatic migration.

The named volume retains the database across container restarts. Avoid `down -v` and volume deletion when preserving accounts and settings.

## 5. First browser setup

If the administrator has not been initialised, create the lab account shown above or the account selected for your deployment, then connect the local Docker socket through the environment wizard. Portainer may time out an uninitialised installation. Restart the container and complete setup promptly:

```bash
docker restart portainer
```

A message saying that Portainer is already initialised means an account already exists; use that account. Deleting the volume is not the remedy for an unknown password or a timed-out setup page.

## 6. Daily use

```bash
# Status, binding and diagnostic logs
docker ps -a --filter name=portainer --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker logs --tail 80 portainer

# Stop or restart this management interface
docker stop portainer
docker start portainer
```

Do not stop an unrelated service merely because it occupies port 9050. Select another intentional host port, or close the competing instance after identifying it.

## 7. Troubleshooting

| Symptom | Action |
|---|---|
| Docker CLI missing or daemon unavailable | Start the intended engine and confirm `docker info`; the installer does not install Docker |
| Linux socket permission denied | Check membership of the Docker group and re-login if it was just changed; do not run the Windows installer against the guest |
| Existing container has another binding or volume | Inspect it and retain its data; the installer refuses automatic replacement |
| API works in VM but Windows page fails | Use the SSH tunnel in section 3 and confirm the guest SSH port forwarding |
| Administrator already exists, login fails | Use the existing credentials; no password reset occurs |
| API starts but local endpoint cannot communicate | Inspect `docker logs`, the socket mount and the selected engine/image compatibility |
| Image unavailable and no internet | Obtain the selected image beforehand; a failed pull does not delete the existing instance |
| HTTP 500 during environment registration | Treat as a server error, inspect the logs and do not label it “already configured” |

## 8. Scope and upstream references

Binding to loopback keeps the shared teaching login off the LAN. Portainer has administrative control over the selected Docker daemon through its socket. The course configuration is for the local teaching environment.

The automation retains the existing image choice and does not promise compatibility with every newer Docker engine. The executable check must pass for the actual pair used. Consult [Portainer's API documentation](https://docs.portainer.io/api/docs) and [installation documentation](https://docs.portainer.io/start/install-ce/server/docker/linux) when selecting a different version.

Scalar endpoint fields in the selected 2.21 API are read through [`Request.FormValue`](https://github.com/portainer/portainer/blob/2.21.5/pkg/libhttp/request/request.go). The Bash script uses multipart form fields; the Windows PowerShell 5.1 script uses URL-encoded scalar form fields for the local socket endpoint.

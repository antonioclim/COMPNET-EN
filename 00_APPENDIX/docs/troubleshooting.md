# 🔧 Troubleshooting Guide — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Quick solutions to common issues in the WSL2 + Docker lab environment.

---

## Quick Diagnostic Commands

Before examining specific issues, run these commands to check your environment:

```bash
# Check WSL status (from PowerShell)
wsl --status

# Check Docker daemon
sudo service docker status

# Check running containers
docker ps

# Check Docker networks
docker network ls

# Check port usage
ss -tlnp | grep LISTEN
```

---

## 🐳 Docker Issues

### Container won't start

**Symptom:** `docker-compose up` fails or container exits immediately.

**Diagnostic:**
```bash
# Check container logs
docker logs <container_name>

# Check container status
docker ps -a
```

**Common causes and solutions:**

| Cause | Solution |
|-------|----------|
| Port already in use | `sudo lsof -i :PORT` then stop conflicting service |
| Image not found | `docker pull <image_name>` |
| Volume permission denied | `sudo chown -R $USER:$USER ./volumes` |
| Out of disk space | `docker system prune -a` |

---

### Port already in use

**Symptom:** `Error: bind: address already in use`

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :8080

# Or using ss
ss -tlnp | grep 8080

# Kill the process (if safe to do so)
sudo kill -9 <PID>

# Or stop the container using it
docker stop <container_name>
```

**Prevention:** Use unique ports per lab week. Check `docker ps` before starting new labs.

---

### Volume permission denied

**Symptom:** Container can't write to mounted volume.

**Solution:**
```bash
# Fix ownership
sudo chown -R 1000:1000 ./volumes

# Or run container as root (not recommended for production)
docker run --user root ...
```

---

### Docker daemon not running

**Symptom:** `Cannot connect to the Docker daemon`

**Solution:**
```bash
# Start Docker service
sudo service docker start

# Verify it's running
sudo service docker status

# If it fails, check logs
sudo cat /var/log/docker.log
```

**Auto-start Docker in WSL2:**
Add to `~/.bashrc`:
```bash
if service docker status 2>&1 | grep -q "is not running"; then
    sudo service docker start
fi
```

---

### Container networking issues

**Symptom:** Containers can't communicate with each other.

**Diagnostic:**
```bash
# Check if containers are on same network
docker network inspect bridge

# Test connectivity from inside container
docker exec -it <container> ping <other_container>
```

**Solution:**
```bash
# Create custom network
docker network create lab_network

# Run containers on same network
docker run --network lab_network ...
```

---

## 🐧 WSL Issues

### WSL not starting

**Symptom:** WSL command hangs or fails.

**Solution (PowerShell as Administrator):**
```powershell
# Restart WSL
wsl --shutdown
wsl

# If still failing, restart LxssManager
Restart-Service LxssManager

# Check WSL version
wsl --list --verbose
```

---

### Network not available in WSL

**Symptom:** `ping: network unreachable` or DNS failures.

**Diagnose before changing configuration:**

```bash
ip route
getent hosts example.com
cat /etc/resolv.conf
cat /etc/wsl.conf 2>/dev/null || true
```

Check connectivity and the DNS/VPN policy of your institution. A public DNS server
may be blocked or unable to resolve institutional names. Current WSL can use DNS
tunnelling; first follow [Microsoft's WSL networking guidance](https://learn.microsoft.com/en-us/windows/wsl/networking).

If an administrator requires a manual resolver, back up both files before editing:

```bash
compnet_dns_backup="$HOME/compnet-dns-backup-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -- "$compnet_dns_backup"
sudo cp -a -- /etc/resolv.conf "$compnet_dns_backup/resolv.conf"
if [ -e /etc/wsl.conf ]; then sudo cp -a -- /etc/wsl.conf "$compnet_dns_backup/wsl.conf"; fi
sudoedit /etc/wsl.conf
```

Add or edit `generateResolvConf=false` **inside the existing `[network]` section**,
retaining `[boot]`, `[user]`, `[automount]` and other settings. Do not append a second
`[network]` section or replace the entire file. Configure the approved DNS addresses
using `sudoedit /etc/resolv.conf`; inspect whether it is a generated symlink first.
Save Linux work, then run `wsl --shutdown` in Windows PowerShell and restart the
selected distribution. Restore the backups if the change does not resolve the issue.

---

### File permission issues

**Symptom:** Can't execute scripts or access files.

**Solution:**
```bash
# Make script executable
chmod +x script.sh

# Fix file ownership
sudo chown $USER:$USER filename

# Check current permissions
ls -la filename
```

**WSL metadata note:** Files created from Windows may have wrong permissions. Copy them within WSL or use `chmod`.

---

### Path confusion (Windows vs WSL)

**Reference:**

| Location | Windows path | WSL path |
|----------|--------------|----------|
| Windows C: | `C:\Users\...` | `/mnt/c/Users/...` |
| Windows D: | `D:\Labs\...` | `/mnt/d/Labs/...` |
| WSL home | `\\wsl$\Ubuntu\home\stud` | `/home/stud` |
| Current dir | - | `pwd` |

**Tip:** When sharing files between Windows and WSL, use `/mnt/c/...` paths from WSL.

---

## 🐍 Python Issues

### Socket connection refused

**Symptom:** `ConnectionRefusedError: [Errno 111] Connection refused`

**Diagnostic:**
```bash
# Check if server is running
ss -tlnp | grep <port>

# Check if port is open
nc -zv localhost <port>
```

**Common causes:**

| Cause | Solution |
|-------|----------|
| Server not started | Start the server first |
| Wrong port | Verify port number matches |
| Firewall blocking | Check `sudo ufw status` |
| Server bound to wrong interface | Use `0.0.0.0` not `127.0.0.1` |

---

### Encoding errors

**Symptom:** `UnicodeDecodeError: 'utf-8' codec can't decode byte...`

**Solution:**
```python
# Safe decode with error handling
text = data.decode('utf-8', errors='replace')

# Or try different encoding
text = data.decode('latin-1')

# For binary data, don't decode at all
print(data.hex())
```

---

### Import errors

**Symptom:** `ModuleNotFoundError: No module named 'xxx'`

**Solution:**
```bash
# Install missing module
pip install <module_name>

# Or for user installation
pip install --user <module_name>

# Check installed packages
pip list | grep <module_name>

# Verify Python path
python -c "import sys; print(sys.path)"
```

---

### Socket already in use (TIME_WAIT)

**Symptom:** `OSError: [Errno 98] Address already in use` even after stopping server.

**Explanation:** TCP connections linger in TIME_WAIT state for ~60 seconds after closing.

**Solution:**
```python
# Add SO_REUSEADDR before bind()
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('', port))
```

---

## 🌐 Portainer Issues

### Can't access Portainer (localhost:9050)

**Diagnostic:**
```bash
# Check if Portainer container is running
docker ps | grep portainer

# Check Portainer logs
docker logs portainer
```

**Solutions:**

| Issue | Solution |
|-------|----------|
| Container not running | `docker start portainer` |
| Port conflict | Check `ss -tlnp \| grep 9050` |
| Wrong URL | Use `http://localhost:9050` (not https) |

---

### Portainer password forgotten

**Solution:** Preserve the existing data volume and use the [official password reset helper](https://docs.portainer.io/advanced/reset-admin). Confirm the container name and `/data` mount first:

```bash
docker inspect portainer --format '{{json .Mounts}}'
# The following assumes container portainer and named volume portainer_data.
docker stop portainer
docker run --rm -v portainer_data:/data portainer/helper-reset-password
docker start portainer
```

Use the account and password printed by the helper. Existing personal accounts do
not automatically become the teaching account `stud`. See [environment routes](environment_routes.md).

---

## 🦈 Wireshark Issues

### No interfaces visible

**Symptom:** Wireshark shows no capture interfaces.

**Solution (Windows):**
1. Run Wireshark as Administrator
2. Install/reinstall Npcap (select "WinPcap API-compatible mode")
3. Restart computer after Npcap installation

---

### Can't capture Docker traffic

**Symptom:** Wireshark doesn't see traffic between containers.

**Explanation:** Docker internal traffic doesn't pass through host interfaces.

**Solutions:**

1. **Use tcpdump inside container:**
```bash
docker exec -it <container> tcpdump -i eth0 -w /tmp/capture.pcap
docker cp <container>:/tmp/capture.pcap ./capture.pcap
```

2. **Capture on Docker bridge:**
```bash
# Find bridge interface
ip link show | grep docker

# Capture on host (WSL)
sudo tcpdump -i docker0 -w capture.pcap
```

3. **Use host network mode:**
```bash
docker run --network host ...
```

---

## 🔄 General Recovery Procedures

### Full environment reset

When nothing else works:

```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all networks (except default)
docker network prune -f

# Remove all volumes (WARNING: deletes data)
docker volume prune -f

# Restart Docker
sudo service docker restart
```

### Quick sanity check script

Save as `check_env.sh`:

```bash
#!/bin/bash
echo "=== Environment Check ==="
echo -n "Docker: "
docker --version 2>/dev/null || echo "NOT INSTALLED"

echo -n "Docker daemon: "
if ! command -v docker >/dev/null 2>&1; then
    echo "CLIENT MISSING"
elif docker info >/dev/null 2>&1; then
    echo "DAEMON ACCESSIBLE"
else
    echo "DAEMON INACCESSIBLE (inspect context, service and permissions)"
fi

echo -n "Running containers: "
if container_ids=$(docker ps -q 2>/dev/null); then
    if [ -z "$container_ids" ]; then
        echo 0
    else
        printf '%s\n' "$container_ids" | wc -l
    fi
else
    echo "UNKNOWN (daemon query failed)"
fi

echo -n "Portainer: "
curl -s -o /dev/null -w "%{http_code}" http://localhost:9050 2>/dev/null || echo "NOT ACCESSIBLE"

echo -n "WSL IP: "
hostname -I | awk '{print $1}'

echo "=== Done ==="
```

---

## Getting Help

If you're still stuck:

1. **Check the error message carefully** — it usually tells you what's wrong
2. **Search the exact error** on Stack Overflow or Docker forums
3. **Ask in the course forum** with:
   - Exact error message
   - Commands you ran
   - Output of diagnostic commands
4. **Office hours** — bring your laptop with the issue reproducible

---

*Troubleshooting Guide — Week 0 | Computer Networks | ASE-CSIE*

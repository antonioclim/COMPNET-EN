# 🔧 Troubleshooting Guide
## Computer Networks Projects — ASE Bucharest, CSIE

> **Purpose:** Solutions to common problems in network projects.  
> **Applies to:** All projects P01-P20

This usually breaks when students forget to start Docker before running their code, or when WSL networking gets confused after a Windows update. Most issues below come from real debugging sessions during office hours.

---

## Quick Diagnostic Commands

Run these first when something goes wrong:

```bash
# Check Docker status
docker ps -a
docker-compose ps

# Check Docker logs
docker-compose logs -f [service-name]

# Check network connectivity
docker network ls
docker network inspect [network-name]

# Check WSL status (from PowerShell)
wsl --status
wsl -l -v

# Check system resources
docker system df
free -h
df -h
```

---

## Docker Issues

### Container Won't Start

**Symptoms:** `docker-compose up` fails, container exits immediately

**Diagnosis:**
```bash
# Check exit code
docker ps -a | grep [container-name]

# Check logs
docker logs [container-name]
```

**Common causes and solutions:**

| Exit Code | Meaning | Solution |
|-----------|---------|----------|
| 0 | Normal exit | Container finished its task — check if it should stay running |
| 1 | Application error | Check logs for error message |
| 137 | Out of memory | Increase Docker memory limit |
| 126 | Permission denied | Check file permissions, use `chmod +x` |
| 127 | Command not found | Check Dockerfile CMD/ENTRYPOINT |

**Fix permission issues:**
```bash
# Make script executable
chmod +x scripts/start.sh

# Fix ownership
sudo chown -R $USER:$USER .
```

---

### Port Already in Use

**Symptoms:** `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Diagnosis:**
```bash
# Find what's using the port
sudo lsof -i :8080
# Or
sudo netstat -tlnp | grep 8080
```

**Solutions:**
```bash
# Option 1: Kill the process
sudo kill -9 [PID]

# Option 2: Change port in docker-compose.yml
ports:
  - "8081:80"  # Use different host port

# Option 3: Stop other containers
docker stop $(docker ps -q)
```

---

### Containers Can't Communicate

**Symptoms:** `ping` fails between containers, connection refused

**Diagnosis:**
```bash
# Check containers are on same network
docker network inspect [network-name]

# Test DNS resolution
docker exec container1 nslookup container2

# Test connectivity
docker exec container1 ping container2
```

**Solutions:**

1. **Use Docker Compose default network:**
```yaml
# Containers in same compose file auto-connect
services:
  server:
    ...
  client:
    ...
# Both are on [project]_default network
```

2. **Create explicit network:**
```yaml
networks:
  app-network:
    driver: bridge

services:
  server:
    networks:
      - app-network
  client:
    networks:
      - app-network
```

3. **Use container names for DNS:**
```python
# Use service name, not localhost
host = "server"  # Not "localhost" or "127.0.0.1"
```

---

### Docker Compose Syntax Errors

**Symptoms:** `yaml.scanner.ScannerError` or compose file won't parse

**Common mistakes:**

```yaml
# ✗ BAD: Tabs instead of spaces
services:
	server:    # This is a TAB — will fail

# ✓ GOOD: Spaces only
services:
  server:      # Two spaces

# ✗ BAD: Missing quotes around port strings
ports:
  - 8080:80

# ✓ GOOD: Quoted to avoid YAML interpretation
ports:
  - "8080:80"

# ✗ BAD: Wrong indentation
services:
  server:
  image: nginx    # Should be indented under server

# ✓ GOOD: Correct indentation
services:
  server:
    image: nginx
```

**Validate your compose file:**
```bash
docker-compose config
```

---

## WSL2 Issues

### WSL Won't Start

**Symptoms:** `wsl` command hangs or errors

**Solutions (run in PowerShell as Admin):**
```powershell
# Restart WSL
wsl --shutdown
wsl

# Check WSL version
wsl --status

# Update WSL
wsl --update

# Reset if corrupted
wsl --unregister Ubuntu
wsl --install -d Ubuntu
```

---

### Docker Not Running in WSL

**Symptoms:** `Cannot connect to Docker daemon`

**Solutions:**
```bash
# Start Docker service
sudo service docker start

# Check status
sudo service docker status

# If systemd is available
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (then logout/login)
sudo usermod -aG docker $USER
```

---

### File Permission Issues Between Windows and WSL

**Symptoms:** Scripts won't execute, files have wrong permissions

**Solutions:**
```bash
# Fix execute permission
chmod +x script.sh

# Fix ownership
sudo chown -R $USER:$USER /path/to/project

# Create /etc/wsl.conf to fix metadata
sudo nano /etc/wsl.conf
```

Add to `/etc/wsl.conf`:
```ini
[automount]
enabled = true
options = "metadata,umask=22,fmask=11"

[interop]
enabled = true
appendWindowsPath = true
```

Then restart WSL: `wsl --shutdown`

---

### Slow File Access in /mnt/c/

**Symptoms:** Operations on Windows files are very slow

**Solution:** Work in WSL filesystem instead:
```bash
# Move project to WSL home
cp -r /mnt/c/Users/You/project ~/project
cd ~/project

# Access from Windows Explorer at:
# \\wsl$\Ubuntu\home\[username]\project
```

---

## Python Issues

### Module Not Found

**Symptoms:** `ModuleNotFoundError: No module named 'X'`

**Solutions:**
```bash
# Check if installed
pip list | grep [module-name]

# Install missing module
pip install [module-name]

# If in virtual environment, activate it first
source venv/bin/activate
pip install [module-name]

# Use requirements.txt
pip install -r requirements.txt
```

---

### Socket Permission Denied

**Symptoms:** `PermissionError: [Errno 13]` when binding to port

**Cause:** Ports below 1024 require root privileges

**Solutions:**
```bash
# Option 1: Use port above 1024
server.bind(('0.0.0.0', 8080))  # Instead of port 80

# Option 2: Run with sudo (not recommended)
sudo python server.py

# Option 3: Use capabilities (Linux)
sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3
```

---

### Address Already in Use

**Symptoms:** `OSError: [Errno 98] Address already in use`

**Solutions:**
```python
# Add SO_REUSEADDR before binding
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
```

Or kill the previous process:
```bash
# Find and kill
lsof -i :8080
kill -9 [PID]
```

---

### Connection Refused

**Symptoms:** `ConnectionRefusedError: [Errno 111]`

**Diagnosis checklist:**
```
□ Is the server running?
□ Is the server listening on the correct port?
□ Is the server listening on the correct interface (0.0.0.0 vs 127.0.0.1)?
□ Is there a firewall blocking the connection?
□ Are you using the correct hostname/IP?
```

**Common fixes:**
```python
# Server: Listen on all interfaces
server.bind(('0.0.0.0', 8080))  # Not ('127.0.0.1', 8080)

# Client: Use correct host
# Inside Docker: use container name
# Outside Docker: use localhost or host IP
```

---

## Network Debugging

### Packets Not Reaching Destination

**Diagnosis:**
```bash
# Check routing
ip route

# Trace the path
traceroute [destination]

# Check if port is open
nc -zv [host] [port]

# Capture traffic
sudo tcpdump -i any port [port]
```

---

### Wireshark Shows No Traffic

**Symptoms:** Capture is empty or doesn't show expected packets

**Solutions:**
1. **Select correct interface:**
   - For Docker: use `docker0` or `br-*` bridge
   - For WSL: use `\Device\NPF_{...}` adapter
   - For loopback: use `Loopback` or `lo`

2. **Check capture filter:**
   ```
   # Remove filters first, then add back
   tcp port 8080
   host 172.17.0.2
   ```

3. **Run Wireshark as admin:**
   - Right-click → Run as Administrator

---

### DNS Resolution Fails

**Symptoms:** `Name or service not known`

**Diagnosis:**
```bash
# Test DNS
nslookup google.com
dig google.com

# Check DNS configuration
cat /etc/resolv.conf
```

**Solutions:**
```bash
# Temporary fix
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# For Docker containers, add to compose:
dns:
  - 8.8.8.8
  - 8.8.4.4
```

---

## Git Issues

### Push Rejected

**Symptoms:** `! [rejected] main -> main (fetch first)`

**Solution:**
```bash
# Pull first, then push
git pull origin main
# Resolve any conflicts
git push origin main
```

---

### Accidentally Committed Secrets

**Symptoms:** API keys, passwords in repository

**Solution (if not pushed):**
```bash
# Remove from last commit
git reset --soft HEAD~1
# Edit .gitignore to exclude secrets
# Commit again without secrets
```

**If already pushed:**
```bash
# Remove from history (DESTRUCTIVE)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch [filename]' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with team!)
git push origin --force --all
```

**Then immediately:** Rotate any exposed credentials!

---

## Performance Issues

### Docker Using Too Much Disk

**Diagnosis:**
```bash
docker system df
```

**Solution:**
```bash
# Remove unused resources
docker system prune -a

# Remove specific items
docker container prune  # Stopped containers
docker image prune -a   # Unused images
docker volume prune     # Unused volumes
```

---

### Slow Container Builds

**Solutions:**
1. **Use .dockerignore:**
   ```
   .git
   __pycache__
   *.pyc
   venv/
   artifacts/
   ```

2. **Order Dockerfile for caching:**
   ```dockerfile
   # Dependencies first (rarely change)
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   # Code last (frequently changes)
   COPY src/ ./src/
   ```

3. **Use smaller base images:**
   ```dockerfile
   # Instead of python:3.11
   FROM python:3.11-slim
   # Or even smaller
   FROM python:3.11-alpine
   ```

---

## Getting Help

If this guide doesn't solve your problem:

1. **Search the error message** — Stack Overflow usually has answers
2. **Check Docker documentation** — docs.docker.com
3. **Ask on the course forum** — Include error message and what you tried
4. **Contact the instructor** — During office hours or by email

**When asking for help, include:**
- Exact error message (copy-paste, not screenshot)
- What command you ran
- What you expected to happen
- What you already tried
- Relevant configuration files

---

*Troubleshooting Guide v1.0 — Computer Networks, ASE Bucharest*

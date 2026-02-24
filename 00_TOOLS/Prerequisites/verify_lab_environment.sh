#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
# verify_lab_environment.sh
# Complete verification script for the Computer Networks lab environment
# 
# Academia de Studii Economice din București — CSIE
# Programmes: Economic Informatics & AI in Economics and Business
# 
# Version: 2.0 (January 2025)
# Author: Revolvix
#
# Checks: WSL2, Ubuntu, Docker, Portainer, Python, network tools
# Compatible with: netENwsl & netROwsl repositories
#═══════════════════════════════════════════════════════════════════════════════

# Colours for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No colour

# Result counters
ERRORS=0
WARNINGS=0
PASSED=0

# Reserved port for Portainer
PORTAINER_PORT=9000

#───────────────────────────────────────────────────────────────────────────────
# Verification functions
#───────────────────────────────────────────────────────────────────────────────

print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    echo "║   🖧  COMPUTER NETWORKS LAB — ENVIRONMENT VERIFICATION                       ║"
    echo "║                                                                               ║"
    echo "║       Academia de Studii Economice din București — CSIE                       ║"
    echo "║       by Revolvix | Version 2.0 | January 2025                                ║"
    echo "║                                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
}

print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}▶ $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

check_required() {
    local name="$1"
    local command="$2"
    
    if eval "$command" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name"
        ((PASSED++))
        return 0
    else
        echo -e "  ${RED}✗${NC} $name ${RED}[MISSING]${NC}"
        ((ERRORS++))
        return 1
    fi
}

check_optional() {
    local name="$1"
    local command="$2"
    
    if eval "$command" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name"
        ((PASSED++))
        return 0
    else
        echo -e "  ${YELLOW}○${NC} $name ${YELLOW}(optional — recommended)${NC}"
        ((WARNINGS++))
        return 1
    fi
}

check_info() {
    local name="$1"
    local value="$2"
    echo -e "  ${CYAN}ℹ${NC} $name: ${BOLD}$value${NC}"
}

check_port() {
    local port="$1"
    local service="$2"
    
    if ss -tlnp 2>/dev/null | grep -q ":$port "; then
        echo -e "  ${GREEN}✓${NC} Port $port ($service) — ${GREEN}ACTIVE${NC}"
        return 0
    else
        echo -e "  ${YELLOW}○${NC} Port $port ($service) — ${YELLOW}INACTIVE${NC}"
        return 1
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# Begin verification
#───────────────────────────────────────────────────────────────────────────────

print_header

#───────────────────────────────────────────────────────────────────────────────
# SECTION 1: System Information
#───────────────────────────────────────────────────────────────────────────────

print_section "SYSTEM INFORMATION"

check_info "Hostname" "$(hostname 2>/dev/null || echo 'N/A')"
check_info "User" "$(whoami 2>/dev/null || echo 'N/A')"
check_info "Home" "$HOME"
check_info "Shell" "$SHELL"

# Check whether we are running inside WSL
if grep -qi microsoft /proc/version 2>/dev/null || grep -qi WSL /proc/version 2>/dev/null; then
    check_info "Environment" "${GREEN}WSL2 detected${NC}"
    IS_WSL=true
else
    check_info "Environment" "${YELLOW}Native Linux (not WSL)${NC}"
    IS_WSL=false
fi

# Ubuntu version
if [ -f /etc/os-release ]; then
    . /etc/os-release
    check_info "Distribution" "$PRETTY_NAME"
    
    # Check for recommended Ubuntu version
    if [[ "$VERSION_ID" == "22.04" ]]; then
        echo -e "  ${GREEN}✓${NC} Recommended Ubuntu version (22.04 LTS)"
        ((PASSED++))
    elif [[ "$VERSION_ID" =~ ^2[2-4]\. ]]; then
        echo -e "  ${YELLOW}○${NC} Acceptable Ubuntu version ($VERSION_ID)"
        ((WARNINGS++))
    else
        echo -e "  ${RED}✗${NC} Unexpected Ubuntu version ($VERSION_ID) — 22.04 LTS recommended"
        ((ERRORS++))
    fi
fi

check_info "Kernel" "$(uname -r 2>/dev/null || echo 'N/A')"
check_info "Architecture" "$(uname -m 2>/dev/null || echo 'N/A')"

#───────────────────────────────────────────────────────────────────────────────
# SECTION 2: Core Components
#───────────────────────────────────────────────────────────────────────────────

print_section "CORE COMPONENTS"

# Python
check_required "Python 3.11+" "python3 --version 2>&1 | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
if python3 --version &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    check_info "Python version" "$PYTHON_VERSION"
fi

check_required "pip3" "pip3 --version"
check_required "Git" "git --version"
check_required "curl" "curl --version"
check_required "wget" "wget --version"

#───────────────────────────────────────────────────────────────────────────────
# SECTION 3: Docker
#───────────────────────────────────────────────────────────────────────────────

print_section "DOCKER"

check_required "Docker Engine" "docker --version"
if docker --version &>/dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1 | cut -d' ' -f3 | tr -d ',')
    check_info "Docker version" "$DOCKER_VERSION"
fi

check_required "Docker Compose (plugin)" "docker compose version"
if docker compose version &>/dev/null; then
    COMPOSE_VERSION=$(docker compose version 2>&1 | cut -d' ' -f4)
    check_info "Compose version" "$COMPOSE_VERSION"
fi

# Verify Docker daemon
if docker info &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Docker daemon is active and responding"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Docker daemon is not responding"
    echo -e "      ${YELLOW}→ Try: sudo service docker start${NC}"
    ((ERRORS++))
fi

# Check whether Docker runs without sudo
if docker ps &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Docker can run without sudo"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Docker requires sudo"
    echo -e "      ${YELLOW}→ Run: sudo usermod -aG docker \$USER && newgrp docker${NC}"
    ((ERRORS++))
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTION 4: Portainer (PORT 9000 RESERVED!)
#───────────────────────────────────────────────────────────────────────────────

print_section "PORTAINER CE (Port 9000 — RESERVED!)"

echo -e "  ${MAGENTA}⚠️  WARNING: Port 9000 is PERMANENTLY RESERVED for Portainer!${NC}"
echo -e "  ${MAGENTA}   No lab service should use this port.${NC}"
echo ""

if docker ps 2>/dev/null | grep -q portainer; then
    echo -e "  ${GREEN}✓${NC} Portainer container is running"
    ((PASSED++))
    
    # Verify port 9000
    if check_port 9000 "Portainer HTTP"; then
        ((PASSED++))
    fi
    
    # Display access URL
    echo -e "  ${CYAN}ℹ${NC} Access URL: ${BOLD}http://localhost:9000${NC}"
    echo -e "  ${CYAN}ℹ${NC} Credentials: ${BOLD}stud / studstudstud${NC}"
else
    echo -e "  ${YELLOW}○${NC} Portainer is not running"
    echo -e "      ${YELLOW}→ Start with: docker start portainer${NC}"
    echo -e "      ${YELLOW}→ Or install using the command from the setup guide${NC}"
    ((WARNINGS++))
fi

# Check whether another service occupies port 9000
if ss -tlnp 2>/dev/null | grep -q ":9000 " && ! docker ps 2>/dev/null | grep -q portainer; then
    echo -e "  ${RED}✗${NC} WARNING: Port 9000 is occupied by ANOTHER service!"
    echo -e "      ${RED}   This will cause conflicts with Portainer!${NC}"
    ((ERRORS++))
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTION 5: Active Containers
#───────────────────────────────────────────────────────────────────────────────

print_section "ACTIVE DOCKER CONTAINERS"

if docker ps &>/dev/null; then
    CONTAINER_COUNT=$(docker ps --format "{{.Names}}" 2>/dev/null | wc -l)
    
    if [ "$CONTAINER_COUNT" -gt 0 ]; then
        echo -e "  ${GREEN}✓${NC} $CONTAINER_COUNT active container(s):"
        echo ""
        docker ps --format "    │ {{.Names}}: {{.Status}} ({{.Ports}})" 2>/dev/null | head -10
        
        if [ "$CONTAINER_COUNT" -gt 10 ]; then
            echo "    │ ... and $((CONTAINER_COUNT - 10)) more container(s)"
        fi
    else
        echo -e "  ${CYAN}ℹ${NC} No active containers (apart from Portainer)"
    fi
else
    echo -e "  ${RED}✗${NC} Unable to list containers"
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTION 6: Docker Networks
#───────────────────────────────────────────────────────────────────────────────

print_section "DOCKER NETWORKS"

if docker network ls &>/dev/null; then
    echo -e "  ${CYAN}ℹ${NC} Available networks:"
    docker network ls --format "    │ {{.Name}}: {{.Driver}}" 2>/dev/null
else
    echo -e "  ${RED}✗${NC} Unable to list Docker networks"
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTION 7: Network Tools
#───────────────────────────────────────────────────────────────────────────────

print_section "NETWORK TOOLS"

check_required "tcpdump" "which tcpdump"
check_optional "tshark (CLI Wireshark)" "which tshark"
check_required "netcat (nc)" "which nc"
check_optional "nmap" "which nmap"
check_optional "iperf3" "which iperf3"
check_optional "traceroute" "which traceroute"
check_optional "mtr" "which mtr"
check_optional "dig (DNS)" "which dig"
check_optional "ss (socket stat)" "which ss"

# Check for Wireshark on Windows (only when running in WSL)
if [ "$IS_WSL" = true ]; then
    echo ""
    echo -e "  ${CYAN}ℹ${NC} Checking for Wireshark on Windows..."
    
    if [ -d "/mnt/c/Program Files/Wireshark" ] || [ -d "/mnt/c/Program Files (x86)/Wireshark" ]; then
        echo -e "  ${GREEN}✓${NC} Wireshark detected on Windows"
        ((PASSED++))
    else
        echo -e "  ${YELLOW}○${NC} Wireshark does not appear to be installed on Windows"
        echo -e "      ${YELLOW}→ Download from: https://www.wireshark.org/download.html${NC}"
        ((WARNINGS++))
    fi
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTION 8: Essential Python Libraries
#───────────────────────────────────────────────────────────────────────────────

print_section "ESSENTIAL PYTHON LIBRARIES (Required)"

check_required "docker" "python3 -c 'import docker'"
check_required "scapy" "python3 -c 'import scapy.all'"
check_required "dpkt" "python3 -c 'import dpkt'"
check_required "requests" "python3 -c 'import requests'"
check_required "flask" "python3 -c 'import flask'"
check_required "PyYAML" "python3 -c 'import yaml'"
check_required "colorama" "python3 -c 'import colorama'"

#───────────────────────────────────────────────────────────────────────────────
# SECTION 9: Advanced Python Libraries
#───────────────────────────────────────────────────────────────────────────────

print_section "ADVANCED PYTHON LIBRARIES (Recommended for Weeks 9–14)"

check_optional "paramiko (SSH)" "python3 -c 'import paramiko'"
check_optional "pyftpdlib (FTP)" "python3 -c 'import pyftpdlib'"
check_optional "paho-mqtt (MQTT/IoT)" "python3 -c 'import paho.mqtt.client'"
check_optional "dnspython (DNS)" "python3 -c 'import dns.resolver'"
check_optional "grpcio (gRPC)" "python3 -c 'import grpc'"
check_optional "protobuf" "python3 -c 'import google.protobuf'"

#───────────────────────────────────────────────────────────────────────────────
# SECTION 10: Lab Port Availability
#───────────────────────────────────────────────────────────────────────────────

print_section "LAB PORTS (Availability Check)"

echo -e "  ${CYAN}ℹ${NC} Port 9000: ${MAGENTA}RESERVED for Portainer${NC} (DO NOT use!)"
echo ""

# Common ports used in lab sessions
declare -A LAB_PORTS=(
    [8080]="HTTP / Load Balancer"
    [8081]="Backend Server 1"
    [8082]="Backend Server 2"
    [8083]="Backend Server 3"
    [9090]="Echo Server / TCP Test"
    [1883]="MQTT plaintext (Week 13)"
    [8883]="MQTT TLS (Week 13)"
    [2525]="SMTP test (Week 12)"
    [5000]="JSON-RPC / Flask (Week 12)"
    [50051]="gRPC (Week 12)"
    [2121]="FTP test (Week 13)"
)

echo -e "  ${CYAN}ℹ${NC} Ports currently in use:"

PORTS_IN_USE=0
for port in "${!LAB_PORTS[@]}"; do
    if ss -tlnp 2>/dev/null | grep -q ":$port "; then
        echo -e "    │ ${YELLOW}:$port${NC} - ${LAB_PORTS[$port]} - ${YELLOW}IN USE${NC}"
        ((PORTS_IN_USE++))
    fi
done

if [ "$PORTS_IN_USE" -eq 0 ]; then
    echo -e "    │ ${GREEN}No lab ports currently in use${NC}"
fi

echo ""
echo -e "  ${CYAN}ℹ${NC} Ports ${GREEN}8080–8089${NC} and ${GREEN}9001–9099${NC} are available for lab work."

#───────────────────────────────────────────────────────────────────────────────
# SECTION 11: Internet Connectivity
#───────────────────────────────────────────────────────────────────────────────

print_section "CONNECTIVITY"

# Ping test
if ping -c 1 -W 2 8.8.8.8 &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Internet access (ping 8.8.8.8)"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} No Internet access"
    ((ERRORS++))
fi

# DNS test
if host google.com &>/dev/null || dig google.com +short &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} DNS resolution is working"
    ((PASSED++))
else
    echo -e "  ${YELLOW}○${NC} DNS resolution issues"
    ((WARNINGS++))
fi

# Docker Hub test
if docker pull hello-world &>/dev/null 2>&1 || docker images hello-world --format "{{.Repository}}" 2>/dev/null | grep -q hello-world; then
    echo -e "  ${GREEN}✓${NC} Docker Hub access"
    ((PASSED++))
else
    echo -e "  ${YELLOW}○${NC} Docker Hub access issues"
    ((WARNINGS++))
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTION 12: Disc Space
#───────────────────────────────────────────────────────────────────────────────

print_section "DISC SPACE"

# Available space in home
DISK_AVAIL=$(df -h ~ 2>/dev/null | awk 'NR==2 {print $4}')
DISK_USED_PERCENT=$(df -h ~ 2>/dev/null | awk 'NR==2 {print $5}' | tr -d '%')

check_info "Available space in ~" "$DISK_AVAIL"

if [ -n "$DISK_USED_PERCENT" ]; then
    if [ "$DISK_USED_PERCENT" -lt 80 ]; then
        echo -e "  ${GREEN}✓${NC} Sufficient disc space available ($DISK_USED_PERCENT% used)"
        ((PASSED++))
    elif [ "$DISK_USED_PERCENT" -lt 90 ]; then
        echo -e "  ${YELLOW}○${NC} Limited disc space ($DISK_USED_PERCENT% used)"
        ((WARNINGS++))
    else
        echo -e "  ${RED}✗${NC} Insufficient disc space ($DISK_USED_PERCENT% used)"
        ((ERRORS++))
    fi
fi

# Docker disc usage
if docker system df &>/dev/null; then
    echo ""
    echo -e "  ${CYAN}ℹ${NC} Docker disc usage:"
    docker system df --format "    │ {{.Type}}: {{.Size}} ({{.Reclaimable}} reclaimable)" 2>/dev/null
fi

#───────────────────────────────────────────────────────────────────────────────
# FINAL SUMMARY
#───────────────────────────────────────────────────────────────────────────────

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                           VERIFICATION SUMMARY                                ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

TOTAL=$((PASSED + ERRORS + WARNINGS))

echo -e "  ${GREEN}✓ Checks passed:${NC}       $PASSED"
echo -e "  ${RED}✗ Critical errors:${NC}     $ERRORS"
echo -e "  ${YELLOW}○ Warnings:${NC}            $WARNINGS"
echo -e "  ─────────────────────────"
echo -e "  ${BOLD}Total checks:${NC}          $TOTAL"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo -e "║  ${GREEN}✅ LAB ENVIRONMENT IS CORRECTLY CONFIGURED!${NC}                                ║"
    echo -e "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    if [ $WARNINGS -gt 0 ]; then
        echo -e "  ${YELLOW}Note: $WARNINGS optional components are missing. These may be needed${NC}"
        echo -e "  ${YELLOW}for advanced lab sessions (Weeks 9–14).${NC}"
        echo ""
    fi
    
    echo -e "  📚 Available repositories:"
    echo -e "     🇬🇧 https://github.com/antonioclim/netENwsl"
    echo -e "     🇷🇴 https://github.com/antonioclim/netROwsl"
    echo ""
    echo -e "  🌐 Portainer: http://localhost:9000 (stud / studstudstud)"
    echo ""
else
    echo -e "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo -e "║  ${RED}❌ ERRORS DETECTED — ENVIRONMENT IS NOT FULLY CONFIGURED${NC}                   ║"
    echo -e "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "  ${RED}Resolve the errors marked with ✗ before continuing.${NC}"
    echo ""
    echo -e "  Common issues and solutions:"
    echo -e "  ─────────────────────────────"
    echo -e "  • Docker daemon not responding → ${CYAN}sudo service docker start${NC}"
    echo -e "  • Docker requires sudo → ${CYAN}sudo usermod -aG docker \$USER && newgrp docker${NC}"
    echo -e "  • Missing Python packages → ${CYAN}pip3 install --break-system-packages <package>${NC}"
    echo -e "  • Portainer not running → ${CYAN}docker start portainer${NC}"
    echo ""
fi

echo -e "─────────────────────────────────────────────────────────────────────────────────"
echo -e "  ${BOLD}Computer Networks Lab${NC} — ASE București, CSIE"
echo -e "  Verification script v2.0 | January 2025 | by Revolvix"
echo -e "─────────────────────────────────────────────────────────────────────────────────"
echo ""

exit $ERRORS

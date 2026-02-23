#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
# verify_lab_environment.sh
# Script de verificare completa a mediului de laborator Retele de Calculatoare
# 
# Academia de Studii Economice din Bucuresti — CSIE
# Programele: Informatica Economica & IA in Economie si Afaceri
# 
# Versiune: 2.0 (Ianuarie 2025)
# Autor: Revolvix
#
# Verifica: WSL2, Ubuntu, Docker, Portainer, Python, instrumente retea
# Compatibil cu: netENwsl & netROwsl repository-uri
#═══════════════════════════════════════════════════════════════════════════════

# Culori pentru output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Contoare pentru rezultate
ERRORS=0
WARNINGS=0
PASSED=0

# Port rezervat pentru Portainer
PORTAINER_PORT=9000

#───────────────────────────────────────────────────────────────────────────────
# Functii de verificare
#───────────────────────────────────────────────────────────────────────────────

print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                               ║"
    echo "║   🖧  VERIFICARE MEDIU LABORATOR RETELE DE CALCULATOARE                       ║"
    echo "║                                                                               ║"
    echo "║       Academia de Studii Economice din Bucuresti — CSIE                       ║"
    echo "║       by Revolvix | Versiune 2.0 | Ianuarie 2025                              ║"
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
        echo -e "  ${RED}✗${NC} $name ${RED}[LIPSESTE]${NC}"
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
        echo -e "  ${YELLOW}○${NC} $name ${YELLOW}(optional - recomandat)${NC}"
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
        echo -e "  ${GREEN}✓${NC} Portul $port ($service) - ${GREEN}ACTIV${NC}"
        return 0
    else
        echo -e "  ${YELLOW}○${NC} Portul $port ($service) - ${YELLOW}INACTIV${NC}"
        return 1
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# Incepe verificarea
#───────────────────────────────────────────────────────────────────────────────

print_header

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 1: Informatii Sistem
#───────────────────────────────────────────────────────────────────────────────

print_section "INFORMATII SISTEM"

check_info "Hostname" "$(hostname 2>/dev/null || echo 'N/A')"
check_info "Utilizator" "$(whoami 2>/dev/null || echo 'N/A')"
check_info "Home" "$HOME"
check_info "Shell" "$SHELL"

# Verificare daca rulam in WSL
if grep -qi microsoft /proc/version 2>/dev/null || grep -qi WSL /proc/version 2>/dev/null; then
    check_info "Mediu" "${GREEN}WSL2 detectat${NC}"
    IS_WSL=true
else
    check_info "Mediu" "${YELLOW}Linux nativ (nu WSL)${NC}"
    IS_WSL=false
fi

# Versiune Ubuntu
if [ -f /etc/os-release ]; then
    . /etc/os-release
    check_info "Distributie" "$PRETTY_NAME"
    
    # Verificare versiune Ubuntu recomandata
    if [[ "$VERSION_ID" == "22.04" ]]; then
        echo -e "  ${GREEN}✓${NC} Versiune Ubuntu recomandata (22.04 LTS)"
        ((PASSED++))
    elif [[ "$VERSION_ID" =~ ^2[2-4]\. ]]; then
        echo -e "  ${YELLOW}○${NC} Versiune Ubuntu acceptabila ($VERSION_ID)"
        ((WARNINGS++))
    else
        echo -e "  ${RED}✗${NC} Versiune Ubuntu neasteptata ($VERSION_ID) - recomandat 22.04 LTS"
        ((ERRORS++))
    fi
fi

check_info "Kernel" "$(uname -r 2>/dev/null || echo 'N/A')"
check_info "Arhitectura" "$(uname -m 2>/dev/null || echo 'N/A')"

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 2: Componente Principale
#───────────────────────────────────────────────────────────────────────────────

print_section "COMPONENTE PRINCIPALE"

# Python
check_required "Python 3.11+" "python3 --version 2>&1 | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
if python3 --version &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    check_info "Versiune Python" "$PYTHON_VERSION"
fi

check_required "pip3" "pip3 --version"
check_required "Git" "git --version"
check_required "curl" "curl --version"
check_required "wget" "wget --version"

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 3: Docker
#───────────────────────────────────────────────────────────────────────────────

print_section "DOCKER"

check_required "Docker Engine" "docker --version"
if docker --version &>/dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1 | cut -d' ' -f3 | tr -d ',')
    check_info "Versiune Docker" "$DOCKER_VERSION"
fi

check_required "Docker Compose (plugin)" "docker compose version"
if docker compose version &>/dev/null; then
    COMPOSE_VERSION=$(docker compose version 2>&1 | cut -d' ' -f4)
    check_info "Versiune Compose" "$COMPOSE_VERSION"
fi

# Verificare daemon Docker
if docker info &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Docker daemon activ si raspunde"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Docker daemon nu raspunde"
    echo -e "      ${YELLOW}→ Incercati: sudo service docker start${NC}"
    ((ERRORS++))
fi

# Verificare rulare fara sudo
if docker ps &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Docker poate rula fara sudo"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Docker necesita sudo"
    echo -e "      ${YELLOW}→ Rulati: sudo usermod -aG docker \$USER && newgrp docker${NC}"
    ((ERRORS++))
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 4: Portainer (PORT 9000 REZERVAT!)
#───────────────────────────────────────────────────────────────────────────────

print_section "PORTAINER CE (Port 9000 - REZERVAT!)"

echo -e "  ${MAGENTA}⚠️  ATENTIE: Portul 9000 este REZERVAT PERMANENT pentru Portainer!${NC}"
echo -e "  ${MAGENTA}   Niciun serviciu de laborator nu trebuie sa foloseasca acest port.${NC}"
echo ""

if docker ps 2>/dev/null | grep -q portainer; then
    echo -e "  ${GREEN}✓${NC} Containerul Portainer ruleaza"
    ((PASSED++))
    
    # Verificare port 9000
    if check_port 9000 "Portainer HTTP"; then
        ((PASSED++))
    fi
    
    # Afisare URL acces
    echo -e "  ${CYAN}ℹ${NC} URL Acces: ${BOLD}http://localhost:9000${NC}"
    echo -e "  ${CYAN}ℹ${NC} Credentiale: ${BOLD}stud / studstudstud${NC}"
else
    echo -e "  ${YELLOW}○${NC} Portainer nu ruleaza"
    echo -e "      ${YELLOW}→ Porniti cu: docker start portainer${NC}"
    echo -e "      ${YELLOW}→ Sau instalati cu comanda din ghidul de instalare${NC}"
    ((WARNINGS++))
fi

# Verificare daca alt serviciu foloseste portul 9000
if ss -tlnp 2>/dev/null | grep -q ":9000 " && ! docker ps 2>/dev/null | grep -q portainer; then
    echo -e "  ${RED}✗${NC} AVERTISMENT: Portul 9000 este ocupat de un ALT serviciu!"
    echo -e "      ${RED}   Aceasta va cauza conflicte cu Portainer!${NC}"
    ((ERRORS++))
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 5: Containere Active
#───────────────────────────────────────────────────────────────────────────────

print_section "CONTAINERE DOCKER ACTIVE"

if docker ps &>/dev/null; then
    CONTAINER_COUNT=$(docker ps --format "{{.Names}}" 2>/dev/null | wc -l)
    
    if [ "$CONTAINER_COUNT" -gt 0 ]; then
        echo -e "  ${GREEN}✓${NC} $CONTAINER_COUNT container(e) activ(e):"
        echo ""
        docker ps --format "    │ {{.Names}}: {{.Status}} ({{.Ports}})" 2>/dev/null | head -10
        
        if [ "$CONTAINER_COUNT" -gt 10 ]; then
            echo "    │ ... si inca $((CONTAINER_COUNT - 10)) container(e)"
        fi
    else
        echo -e "  ${CYAN}ℹ${NC} Niciun container activ (in afara de Portainer)"
    fi
else
    echo -e "  ${RED}✗${NC} Nu se pot lista containerele"
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 6: Retele Docker
#───────────────────────────────────────────────────────────────────────────────

print_section "RETELE DOCKER"

if docker network ls &>/dev/null; then
    echo -e "  ${CYAN}ℹ${NC} Retele disponibile:"
    docker network ls --format "    │ {{.Name}}: {{.Driver}}" 2>/dev/null
else
    echo -e "  ${RED}✗${NC} Nu se pot lista retelele Docker"
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 7: Instrumente de Retea
#───────────────────────────────────────────────────────────────────────────────

print_section "INSTRUMENTE DE RETEA"

check_required "tcpdump" "which tcpdump"
check_optional "tshark (CLI Wireshark)" "which tshark"
check_required "netcat (nc)" "which nc"
check_optional "nmap" "which nmap"
check_optional "iperf3" "which iperf3"
check_optional "traceroute" "which traceroute"
check_optional "mtr" "which mtr"
check_optional "dig (DNS)" "which dig"
check_optional "ss (socket stat)" "which ss"

# Verificare Wireshark pe Windows (doar daca suntem in WSL)
if [ "$IS_WSL" = true ]; then
    echo ""
    echo -e "  ${CYAN}ℹ${NC} Verificare Wireshark pe Windows..."
    
    if [ -d "/mnt/c/Program Files/Wireshark" ] || [ -d "/mnt/c/Program Files (x86)/Wireshark" ]; then
        echo -e "  ${GREEN}✓${NC} Wireshark detectat pe Windows"
        ((PASSED++))
    else
        echo -e "  ${YELLOW}○${NC} Wireshark nu pare a fi instalat pe Windows"
        echo -e "      ${YELLOW}→ Descarcati de la: https://www.wireshark.org/download.html${NC}"
        ((WARNINGS++))
    fi
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 8: Biblioteci Python Esentiale
#───────────────────────────────────────────────────────────────────────────────

print_section "BIBLIOTECI PYTHON ESENTIALE (Obligatorii)"

check_required "docker" "python3 -c 'import docker'"
check_required "scapy" "python3 -c 'import scapy.all'"
check_required "dpkt" "python3 -c 'import dpkt'"
check_required "requests" "python3 -c 'import requests'"
check_required "flask" "python3 -c 'import flask'"
check_required "PyYAML" "python3 -c 'import yaml'"
check_required "colorama" "python3 -c 'import colorama'"

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 9: Biblioteci Python Avansate
#───────────────────────────────────────────────────────────────────────────────

print_section "BIBLIOTECI PYTHON AVANSATE (Recomandate pentru Sapt. 9-14)"

check_optional "paramiko (SSH)" "python3 -c 'import paramiko'"
check_optional "pyftpdlib (FTP)" "python3 -c 'import pyftpdlib'"
check_optional "paho-mqtt (MQTT/IoT)" "python3 -c 'import paho.mqtt.client'"
check_optional "dnspython (DNS)" "python3 -c 'import dns.resolver'"
check_optional "grpcio (gRPC)" "python3 -c 'import grpc'"
check_optional "protobuf" "python3 -c 'import google.protobuf'"

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 10: Verificare Porturi Laborator
#───────────────────────────────────────────────────────────────────────────────

print_section "PORTURI LABORATOR (Verificare Disponibilitate)"

echo -e "  ${CYAN}ℹ${NC} Portul 9000: ${MAGENTA}REZERVAT pentru Portainer${NC} (NU utilizati!)"
echo ""

# Porturi comune folosite in laboratoare
declare -A LAB_PORTS=(
    [8080]="HTTP / Load Balancer"
    [8081]="Backend Server 1"
    [8082]="Backend Server 2"
    [8083]="Backend Server 3"
    [9090]="Echo Server / TCP Test"
    [1883]="MQTT plaintext (Sapt. 13)"
    [8883]="MQTT TLS (Sapt. 13)"
    [2525]="SMTP test (Sapt. 12)"
    [5000]="JSON-RPC / Flask (Sapt. 12)"
    [50051]="gRPC (Sapt. 12)"
    [2121]="FTP test (Sapt. 13)"
)

echo -e "  ${CYAN}ℹ${NC} Porturi utilizate in prezent:"

PORTS_IN_USE=0
for port in "${!LAB_PORTS[@]}"; do
    if ss -tlnp 2>/dev/null | grep -q ":$port "; then
        echo -e "    │ ${YELLOW}:$port${NC} - ${LAB_PORTS[$port]} - ${YELLOW}IN FOLOSINTA${NC}"
        ((PORTS_IN_USE++))
    fi
done

if [ "$PORTS_IN_USE" -eq 0 ]; then
    echo -e "    │ ${GREEN}Niciun port de laborator in folosinta${NC}"
fi

echo ""
echo -e "  ${CYAN}ℹ${NC} Porturile ${GREEN}8080-8089${NC} si ${GREEN}9001-9099${NC} sunt disponibile pentru laboratoare."

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 11: Verificare Acces Internet
#───────────────────────────────────────────────────────────────────────────────

print_section "CONECTIVITATE"

# Test ping
if ping -c 1 -W 2 8.8.8.8 &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Acces Internet (ping 8.8.8.8)"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Fara acces Internet"
    ((ERRORS++))
fi

# Test DNS
if host google.com &>/dev/null || dig google.com +short &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Rezolvare DNS functionala"
    ((PASSED++))
else
    echo -e "  ${YELLOW}○${NC} Probleme la rezolvarea DNS"
    ((WARNINGS++))
fi

# Test Docker Hub
if docker pull hello-world &>/dev/null 2>&1 || docker images hello-world --format "{{.Repository}}" 2>/dev/null | grep -q hello-world; then
    echo -e "  ${GREEN}✓${NC} Acces Docker Hub"
    ((PASSED++))
else
    echo -e "  ${YELLOW}○${NC} Probleme la accesarea Docker Hub"
    ((WARNINGS++))
fi

#───────────────────────────────────────────────────────────────────────────────
# SECTIUNEA 12: Spatiu pe Disc
#───────────────────────────────────────────────────────────────────────────────

print_section "SPATIU PE DISC"

# Spatiu disponibil in home
DISK_AVAIL=$(df -h ~ 2>/dev/null | awk 'NR==2 {print $4}')
DISK_USED_PERCENT=$(df -h ~ 2>/dev/null | awk 'NR==2 {print $5}' | tr -d '%')

check_info "Spatiu disponibil in ~" "$DISK_AVAIL"

if [ -n "$DISK_USED_PERCENT" ]; then
    if [ "$DISK_USED_PERCENT" -lt 80 ]; then
        echo -e "  ${GREEN}✓${NC} Spatiu suficient disponibil ($DISK_USED_PERCENT% utilizat)"
        ((PASSED++))
    elif [ "$DISK_USED_PERCENT" -lt 90 ]; then
        echo -e "  ${YELLOW}○${NC} Spatiu limitat ($DISK_USED_PERCENT% utilizat)"
        ((WARNINGS++))
    else
        echo -e "  ${RED}✗${NC} Spatiu insuficient ($DISK_USED_PERCENT% utilizat)"
        ((ERRORS++))
    fi
fi

# Spatiu Docker
if docker system df &>/dev/null; then
    echo ""
    echo -e "  ${CYAN}ℹ${NC} Utilizare spatiu Docker:"
    docker system df --format "    │ {{.Type}}: {{.Size}} ({{.Reclaimable}} recuperabil)" 2>/dev/null
fi

#───────────────────────────────────────────────────────────────────────────────
# SUMAR FINAL
#───────────────────────────────────────────────────────────────────────────────

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                              SUMAR VERIFICARE                                  ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

TOTAL=$((PASSED + ERRORS + WARNINGS))

echo -e "  ${GREEN}✓ Verificari trecute:${NC}   $PASSED"
echo -e "  ${RED}✗ Erori critice:${NC}       $ERRORS"
echo -e "  ${YELLOW}○ Avertismente:${NC}        $WARNINGS"
echo -e "  ─────────────────────────"
echo -e "  ${BOLD}Total verificari:${NC}      $TOTAL"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo -e "║  ${GREEN}✅ MEDIUL DE LABORATOR ESTE CONFIGURAT CORECT!${NC}                             ║"
    echo -e "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    if [ $WARNINGS -gt 0 ]; then
        echo -e "  ${YELLOW}Nota: $WARNINGS componente optionale lipsesc. Acestea pot fi necesare${NC}"
        echo -e "  ${YELLOW}pentru laboratoarele avansate (Saptamanile 9-14).${NC}"
        echo ""
    fi
    
    echo -e "  📚 Repository-uri disponibile:"
    echo -e "     🇬🇧 https://github.com/antonioclim/netENwsl"
    echo -e "     🇷🇴 https://github.com/antonioclim/netROwsl"
    echo ""
    echo -e "  🌐 Portainer: http://localhost:9000 (stud / studstudstud)"
    echo ""
else
    echo -e "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo -e "║  ${RED}❌ ERORI DETECTATE - MEDIUL NU ESTE COMPLET CONFIGURAT${NC}                      ║"
    echo -e "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "  ${RED}Rezolvati erorile marcate cu ✗ inainte de a continua.${NC}"
    echo ""
    echo -e "  Probleme comune si solutii:"
    echo -e "  ─────────────────────────────"
    echo -e "  • Docker daemon nu raspunde → ${CYAN}sudo service docker start${NC}"
    echo -e "  • Docker necesita sudo → ${CYAN}sudo usermod -aG docker \$USER && newgrp docker${NC}"
    echo -e "  • Pachete Python lipsa → ${CYAN}pip3 install --break-system-packages <pachet>${NC}"
    echo -e "  • Portainer nu ruleaza → ${CYAN}docker start portainer${NC}"
    echo ""
fi

echo -e "─────────────────────────────────────────────────────────────────────────────────"
echo -e "  ${BOLD}Laborator Retele de Calculatoare${NC} — ASE Bucuresti, CSIE"
echo -e "  Script de verificare v2.0 | Ianuarie 2025 | by Revolvix"
echo -e "─────────────────────────────────────────────────────────────────────────────────"
echo ""

exit $ERRORS

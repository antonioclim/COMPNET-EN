#!/usr/bin/env bash
# WSL alternative environment checks for COMPNET-EN.
# Based on the original v2.0 verifier credited to Revolvix (January 2025).
# This revision checks prerequisites only; it does not install or pull images.
# For the VirtualBox appliance use 01_GUIDE_MININET-SDN/verify_mininet_vm.sh.
set -u

ERRORS=0
WARNINGS=0
PASSED=0
ONLINE=false
PORTAINER_PORT=9050
for option in "$@"; do
    case "$option" in
        --online) ONLINE=true ;;
        --help|-h) printf 'Usage: bash verify_lab_environment.sh [--online]\nDefault: local WSL checks only. --online adds bounded HTTPS probes; no downloads or image pulls.\n'; exit 0 ;;
        *) printf 'Unknown option: %s\n' "$option" >&2; exit 2 ;;
    esac
done
if ! command -v timeout >/dev/null 2>&1; then
    printf 'GNU timeout is required (Ubuntu coreutils). No prerequisite commands were run.\n' >&2
    exit 2
fi
# A stalled daemon, import or helper must not block the readiness report forever.
probe() {
    if [[ "$1" == command && "${2:-}" == -v ]]; then
        command -v "$3"
    else
        timeout -k 2s 15s "$@"
    fi
}
pass() { printf 'PASS  %s\n' "$*"; PASSED=$((PASSED+1)); }
warn() { printf 'WARN  %s\n' "$*"; WARNINGS=$((WARNINGS+1)); }
fail() { printf 'FAIL  %s\n' "$*"; ERRORS=$((ERRORS+1)); }
required() { local label="$1"; shift; if probe "$@" >/dev/null 2>&1; then pass "$label"; else fail "$label"; fi; }
optional() { local label="$1"; shift; if probe "$@" >/dev/null 2>&1; then pass "$label"; else warn "$label"; fi; }

printf 'COMPNET-EN — WSL alternative: prerequisite verification\n'
kernel="$(probe uname -r)"
if [[ "$kernel" != *[Mm]icrosoft* && "$kernel" != *WSL* ]]; then
    printf 'This script targets the WSL route. For MININET-SDN in VirtualBox, run:\n'
    printf '  bash 01_GUIDE_MININET-SDN/verify_mininet_vm.sh\n'
    printf 'No acceptance claim has been made for this native Linux/VirtualBox environment.\n'
    exit 2
fi
if [[ "$kernel" == *[Mm]icrosoft-standard* || "$kernel" == *WSL2* ]]; then
    pass 'WSL2 kernel identified'
else
    fail 'WSL detected but WSL2 not established; confirm VERSION 2 with wsl --list --verbose on Windows'
fi
if [[ -r /etc/os-release ]]; then
    # Standard distribution metadata; no user configuration is sourced.
    . /etc/os-release
    printf 'Distribution: %s\n' "${PRETTY_NAME:-unknown}"
    if [[ "${ID:-}" == ubuntu && "${VERSION_ID:-}" =~ ^(22\.04|24\.04)$ ]]; then
        pass 'Ubuntu LTS release documented by this setup route'
    else
        warn 'This distribution is outside the documented Ubuntu 22.04/24.04 route'
    fi
else
    warn 'Distribution metadata unavailable'
fi

required 'Python 3.10 or later in this Linux environment' python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)'
required 'pip for the same Python interpreter' python3 -m pip --version
required 'Git' git --version
required 'curl' curl --version
required 'Docker CLI' docker --version
required 'Docker Compose v2 plugin (docker compose)' docker compose version
if probe docker info >/dev/null 2>&1; then
    pass 'Docker daemon responds to the current Linux user'
    docker_type="$(probe docker info --format '{{.OSType}}' 2>/dev/null)"
    if [[ "$docker_type" == linux ]]; then pass 'Docker daemon uses Linux containers'; else fail 'Docker daemon does not report Linux containers'; fi
    if [[ -n "${DOCKER_HOST:-}" && -z "${DOCKER_CONTEXT:-}" ]]; then
        daemon_address="$DOCKER_HOST"
    else
        daemon_address="$(probe docker context inspect --format '{{.Endpoints.docker.Host}}' 2>/dev/null)"
    fi
    if [[ "$daemon_address" == unix://* ]]; then
        pass 'Docker context uses a local Unix socket'
    else
        fail 'Docker context is remote or unresolved; a remote daemon does not establish local WSL capability'
    fi
else
    fail 'Docker daemon unavailable to this user; check service, context and permissions before changing group membership'
fi
required 'Docker container listing works' docker ps

printf '\nNetwork tools\n'
for name in tcpdump nc; do required "$name available" command -v "$name"; done
for name in tshark nmap iperf3 traceroute mtr dig ss; do optional "$name available (exercise dependent)" command -v "$name"; done

printf '\nPython packages in the active Linux interpreter\n'
for module in docker scapy.all dpkt requests flask yaml colorama; do
    required "Python import: $module" python3 -c "import $module"
done
for module in paramiko pyftpdlib paho.mqtt.client dns.resolver grpc google.protobuf; do
    optional "Python import: $module (exercise dependent)" python3 -c "import $module"
done
printf 'These checks use Linux Python. Installing packages in Windows Python does not satisfy them.\n'

printf '\nOptional Portainer\n'
if probe docker inspect --format '{{.State.Running}}' portainer 2>/dev/null | grep -qx true; then
    pass 'Named Portainer container is running'
    if probe curl -fsS --connect-timeout 2 --max-time 4 "http://127.0.0.1:${PORTAINER_PORT}/api/status" 2>/dev/null |
        probe python3 -c 'import json,sys; s=json.load(sys.stdin); raise SystemExit(0 if isinstance(s,dict) and "Version" in s else 1)' >/dev/null 2>&1; then
        pass 'Portainer API responds on loopback port 9050'
    else
        warn 'Portainer API not confirmed on 9050; inspect the actual mapping. No container was replaced.'
    fi
else
    warn 'Portainer is not running; it is optional for CLI-based exercises'
fi
printf 'Portainer, when configured: http://localhost:9050. Port 9000 remains available for the S10 tunnel.\n'
printf 'Account authentication and endpoint access are checked by portainer-init.sh, not by this verifier.\n'

printf '\nStorage\n'
if disk_kib="$(probe df -Pk "${HOME:-.}" 2>/dev/null | awk 'NR==2 {print $4}')" && [[ "$disk_kib" =~ ^[0-9]+$ ]]; then
    if (( disk_kib >= 5 * 1024 * 1024 )); then
        pass 'At least 5 GiB free on the Linux home filesystem'
    else
        warn 'Less than 5 GiB free on the Linux home filesystem; image builds may require more'
    fi
else
    warn 'Could not determine free filesystem space'
fi
printf 'Also check free space on the Windows volume storing the WSL virtual disk.\n'

if [[ "$ONLINE" == true ]]; then
    printf '\nOptional HTTPS connectivity probes\n'
    if curl -fsS -I --connect-timeout 3 --max-time 10 https://github.com >/dev/null 2>&1; then
        pass 'HTTPS connection to GitHub succeeded'
    else
        warn 'HTTPS connection to GitHub failed; proxy, DNS, network or service availability may be responsible'
    fi
    registry_status="$(probe curl -sS -o /dev/null -w '%{http_code}' --connect-timeout 3 --max-time 10 https://registry-1.docker.io/v2/ 2>/dev/null || true)"
    case "$registry_status" in
        200|401) pass 'Docker registry HTTPS endpoint responds (this does not verify image-pull authorisation)' ;;
        *) warn 'Docker registry HTTPS endpoint not confirmed; cached images do not prove online access' ;;
    esac
else
    printf '\nInternet access was not tested. Use --online to request bounded HTTPS probes.\n'
fi

printf '\nSummary: %s passed, %s errors, %s warnings.\n' "$PASSED" "$ERRORS" "$WARNINGS"
printf 'Each subprocess prerequisite probe is limited to 15 seconds, with a 2-second forced-stop grace.\n'
printf 'Scope: prerequisite availability only. No Mininet/SDN exercise, packet capture or complete seminar was executed.\n'
printf 'Course: https://github.com/antonioclim/COMPNET-EN\n'
if (( ERRORS == 0 )); then
    printf 'Required WSL prerequisites checked; review warnings for the selected exercise.\n'
    exit 0
fi
printf 'Resolve the reported prerequisite failures before the affected exercise.\n'
exit 1

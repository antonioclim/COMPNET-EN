#!/usr/bin/env bash
# Read-only prerequisite checks inside the MININET-SDN guest.
# No installations, privilege escalation, downloads, containers or network topologies.
set -uo pipefail

usage() {
    cat <<'USAGE'
Usage: bash 01_GUIDE_MININET-SDN/verify_mininet_vm.sh [--help]
Run inside the imported MININET-SDN VM as the normal lab user.
The course Python at ~/venvs/compnet/bin/python3 is preferred when present.
Exit 0: prerequisite probes passed. Exit 1: a required probe failed.
Exit 2: required probes passed but configuration warnings remain.
This is not a functional Mininet, SDN, packet-capture or container acceptance test.
USAGE
}

if [[ $# -gt 0 ]]; then
    if [[ $# -eq 1 && ( $1 == --help || $1 == -h ) ]]; then
        usage
        exit 0
    fi
    usage >&2
    exit 64
fi

passed=0
failed=0
warnings=0
pass() { printf 'PASS  %s\n' "$*"; passed=$((passed + 1)); }
fail() { printf 'FAIL  %s\n' "$*"; failed=$((failed + 1)); }
warn() { printf 'WARN  %s\n' "$*"; warnings=$((warnings + 1)); }

if ! command -v timeout >/dev/null 2>&1; then
    printf 'FAIL  GNU timeout is required for bounded read-only probes.\n' >&2
    exit 1
fi

probe() {
    local label=$1
    shift
    if ! command -v "$1" >/dev/null 2>&1; then
        fail "$label: command unavailable ($1)"
    elif timeout --kill-after=2s 15s "$@" >/dev/null 2>&1; then
        pass "$label"
    else
        fail "$label: command failed or timed out; check the guest configuration"
    fi
}

printf '%s\n' 'MININET-SDN guest prerequisite check'
printf '%s\n' 'Scope: read-only probes in this Linux environment; no lab scenarios are started.'

if [[ $(uname -s) != Linux ]]; then
    fail 'Run this checker in the Linux guest, not the host terminal.'
else
    pass 'Linux kernel'
fi
if [[ $(uname -r) == *[Mm]icrosoft* ]]; then
    fail 'This is WSL. Use the WSL prerequisites checker for that alternative route.'
fi
if [[ $(uname -m) == x86_64 ]]; then
    pass 'x86-64 architecture'
else
    warn 'Architecture differs from the documented x86-64 appliance.'
fi
if [[ -r /etc/os-release ]] &&
   grep -Eq '^ID="?ubuntu"?$' /etc/os-release &&
   grep -Eq '^VERSION_ID="?24\.04"?$' /etc/os-release; then
    pass 'Ubuntu 24.04 documented guest baseline'
else
    warn 'OS differs from the documented Ubuntu 24.04 guest; inspect /etc/os-release.'
fi
if [[ $EUID -eq 0 ]]; then
    warn 'Running as root does not verify the normal lab user permissions.'
fi

probe 'Git' git --version
probe 'Mininet CLI' mn --version
probe 'Open vSwitch CLI' ovs-vsctl --version
probe 'Open vSwitch service' systemctl is-active --quiet openvswitch-switch
probe 'Docker client' docker --version
probe 'Docker daemon accessible as the current user' docker info --format '{{.ServerVersion}}'
probe 'Docker Compose v2 plugin' docker compose version
probe 'Packet-capture CLI' tshark --version
probe 'curl' curl --version
probe 'Netcat command' nc -h
probe 'SSH client' ssh -V

python_command=$(command -v python3 || true)
if [[ -x "$HOME/venvs/compnet/bin/python3" ]]; then
    python_command="$HOME/venvs/compnet/bin/python3"
fi
if [[ -z "$python_command" ]]; then
    fail 'Python 3: command unavailable'
else
    probe 'Course Python interpreter' "$python_command" --version
    probe 'Course Python networking libraries (Scapy, Paramiko, Flask)' \
        "$python_command" -c 'import scapy.all, paramiko, flask'
    probe 'OS-Ken application API imports in course Python' \
        "$python_command" -c 'from os_ken.base.app_manager import OSKenApp; from os_ken.controller.handler import CONFIG_DISPATCHER'
fi

system_python=/usr/bin/python3
probe 'System Python can import Mininet (used by sudo topology commands)' \
    "$system_python" -c 'import mininet.net, mininet.node'

manager=$(command -v osken-manager || true)
if [[ -x "$HOME/venvs/compnet/bin/osken-manager" ]]; then
    manager="$HOME/venvs/compnet/bin/osken-manager"
fi
if [[ -z "$manager" ]]; then
    fail 'osken-manager is missing. Preserve the course environment; OS-Ken 4 removed this CLI.'
else
    probe 'Course osken-manager starts and parses --help' "$manager" --help
fi

printf '\nPassed: %s; failed: %s; warnings: %s\n' "$passed" "$failed" "$warnings"
printf '%s\n' 'Next: run the documented Mininet and S06 exercises in the guest.'
printf '%s\n' 'CLI/import probes do not establish forwarding, capture permissions or full seminar compatibility.'
if (( failed > 0 )); then exit 1; fi
if (( warnings > 0 )); then exit 2; fi
exit 0

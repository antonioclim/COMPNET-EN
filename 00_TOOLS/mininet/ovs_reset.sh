#!/usr/bin/env bash
# ovs_reset.sh — Open vSwitch + Mininet deep reset
#
# Purpose (lab context)
# ---------------------
# In Mininet/OVS labs, an unclean shutdown may leave stale bridges and
# controller processes behind. The symptom is typically:
#   "*** Waiting for switches to connect"
#
# This script performs a *deep* reset:
#   1) Terminates common Mininet/OVS controller processes
#   2) Deletes all OVS bridges recorded in the OVS database
#   3) Runs the standard Mininet cleanup: mn -c
#   4) Restarts the Open vSwitch service (best effort)
#   5) Verifies a clean state
#
# WARNING
# -------
# This is a lab utility. It removes *all* OVS bridges on the host.
# Do not run it on a machine where Open vSwitch is used for production.
#
# Usage:
#   sudo bash ovs_reset.sh
#   bash ovs_reset.sh --verify
#   bash ovs_reset.sh --help
#
# Notes
# -----
# - Verification mode (--verify) is non-destructive; it needs permission to read OVSDB.
# - Full reset requires sudo because it manipulates OVS and namespaces.

set -euo pipefail

# --- output helpers -------------------------------------------------------
QUIET=0
USE_COLOR=1

if [[ ! -t 1 ]]; then
  USE_COLOR=0
fi

RED=$([[ $USE_COLOR -eq 1 ]] && echo $'\033[0;31m' || echo '')
GREEN=$([[ $USE_COLOR -eq 1 ]] && echo $'\033[0;32m' || echo '')
YELLOW=$([[ $USE_COLOR -eq 1 ]] && echo $'\033[1;33m' || echo '')
BLUE=$([[ $USE_COLOR -eq 1 ]] && echo $'\033[0;34m' || echo '')
NC=$([[ $USE_COLOR -eq 1 ]] && echo $'\033[0m' || echo '')

log_info()    { [[ $QUIET -eq 1 ]] && return 0; echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { [[ $QUIET -eq 1 ]] && return 0; echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*" 1>&2; }

die() { log_error "$*"; exit 1; }

require_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || die "Required command not found in PATH: $cmd"
}

check_root() {
  if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
    die "This script must be run with sudo. Example: sudo bash $0"
  fi
}

kill_mininet_processes() {
  log_info "Stopping Mininet/OVS-related processes (best effort)…"

  # Mininet python processes (topologies)
  pkill -9 -f "python.*mininet" 2>/dev/null || true
  pkill -9 -f "python.*S0[0-9]_" 2>/dev/null || true

  # Common controllers
  pkill -9 -f "controller" 2>/dev/null || true
  pkill -9 -f "ovs-testcontroller" 2>/dev/null || true
  pkill -9 -f "ryu-manager" 2>/dev/null || true
  pkill -9 -f "osken-manager" 2>/dev/null || true
  pkill -9 -f "os_ken\.cmd\.manager" 2>/dev/null || true

  sleep 1
  log_success "Process cleanup done"
}

delete_ovs_bridges() {
  log_info "Removing OVS bridges from the OVS database…"
  require_cmd ovs-vsctl

  local bridges
  if ! bridges=$(ovs-vsctl --timeout=10 list-br); then
    log_error "Cannot read OVSDB; a failed query does not prove that it is empty."
    return 1
  fi

  if [[ -z "${bridges}" ]]; then
    log_success "No OVS bridges found"
    return 0
  fi

  while IFS= read -r br; do
    [[ -z "$br" ]] && continue
    log_info "  deleting bridge: $br"
    ovs-vsctl --timeout=10 --if-exists del-br "$br" || return 1
  done <<<"${bridges}"

  log_success "OVS bridges removed"
}

mininet_cleanup() {
  if command -v mn >/dev/null 2>&1; then
    log_info "Running standard Mininet cleanup: mn -c"
    if mn -c; then
      log_success "Mininet cleanup complete"
    else
      log_warn "Mininet cleanup returned an error; inspect the output before continuing."
      return 1
    fi
  else
    log_warn "Mininet command 'mn' not found; skipped mn -c"
    return 1
  fi
}

restart_ovs() {
  log_info "Restarting Open vSwitch service…"
  local restarted=0
  if command -v systemctl >/dev/null 2>&1 &&
     systemctl restart openvswitch-switch; then
    restarted=1
  elif command -v service >/dev/null 2>&1 &&
       service openvswitch-switch restart; then
    restarted=1
  fi
  if [[ $restarted -ne 1 ]]; then
    log_error "Open vSwitch restart failed; the reset is incomplete."
    return 1
  fi
  # Do not ask ovs-vswitchd to exit after successfully starting the service.
  sleep 2
  log_success "Open vSwitch service restarted"
}

verify_clean() {
  require_cmd ovs-vsctl

  log_info "Verifying clean OVS state…"
  local bridges
  if ! bridges=$(ovs-vsctl --timeout=10 list-br); then
    log_error "Cannot read OVSDB; a failed query does not prove that it is empty."
    return 1
  fi

  if [[ -z "${bridges}" ]]; then
    log_success "OVS is clean (no bridges)"
  else
    log_warn "Remaining bridges detected: ${bridges}"
    return 1
  fi

  if [[ $QUIET -eq 0 ]]; then
    echo ""
    log_info "Current OVS status:"
    ovs-vsctl --timeout=10 show || return 1
    echo ""
  fi

  return 0
}

show_usage() {
  cat <<'USAGE'
Usage:
  sudo bash ovs_reset.sh [--verify] [--quiet]

Options:
  --verify   Only verify whether OVS has leftover bridges (non-destructive).
  --quiet    Reduce informational output (warnings and errors still printed).
  -h, --help Show this help.

Typical workflow:
  1) Try the gentle cleanup first:
       sudo mn -c
  2) If Mininet still hangs at switch connection, use this deep reset:
       sudo bash ovs_reset.sh

Afterwards, re-run your Mininet topology.
USAGE
}

main() {
  local verify_only=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --verify)
        verify_only=1
        shift
        ;;
      --quiet)
        QUIET=1
        shift
        ;;
      -h|--help)
        show_usage
        exit 0
        ;;
      *)
        die "Unknown option: $1 (use --help)"
        ;;
    esac
  done

  if [[ $verify_only -eq 1 ]]; then
    # Verification is read-only; do not require root.
    if ! command -v ovs-vsctl >/dev/null 2>&1; then
      die "ovs-vsctl not found (is Open vSwitch installed?)"
    fi
    verify_clean
    exit $?
  fi

  check_root

  echo ""
  echo "================================================"
  echo "  OVS & Mininet Deep Reset (lab utility)"
  echo "================================================"
  echo ""

  kill_mininet_processes
  delete_ovs_bridges
  local cleanup_rc=0
  mininet_cleanup || cleanup_rc=1
  restart_ovs || cleanup_rc=1

  echo ""
  if verify_clean && [[ $cleanup_rc -eq 0 ]]; then
    echo "================================================"
    log_success "Reset complete — environment looks clean."
    echo "================================================"
    exit 0
  else
    echo "================================================"
    log_warn "Reset incomplete — inspect Mininet cleanup, service and OVS diagnostics above."
    echo "================================================"
    exit 1
  fi
}

main "$@"

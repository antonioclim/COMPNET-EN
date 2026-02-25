#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
#  Portainer CE — Automated setup for COMPNET labs
#
#  Port        : 9050  (9000 reserved by S10 SSH tunnel)
#  Credentials : stud / studstudstud
#  Requires    : Docker Engine running
# ─────────────────────────────────────────────────────
set -euo pipefail

IMAGE="portainer/portainer-ce:2.21-alpine"
NAME="portainer"
PORT=9050
VOLUME="portainer_data"
ADMIN="stud"
PASS="studstudstud"
BASE="http://localhost:${PORT}"

cyan()   { printf '\033[1;36m>> %s\033[0m\n' "$1"; }
green()  { printf '\033[1;32m%s\033[0m\n'   "$1"; }
yellow() { printf '\033[1;33m   %s\033[0m\n' "$1"; }
red()    { printf '\033[1;31mERROR: %s\033[0m\n' "$1"; }

# ── 1  Check Docker ──────────────────────────────────────────────
cyan "Checking Docker availability"
if ! docker version --format '{{.Server.Version}}' >/dev/null 2>&1; then
    red "Docker is not running."
    exit 1
fi
echo "   Docker Engine $(docker version --format '{{.Server.Version}}') detected."

# ── 2  Check port ────────────────────────────────────────────────
cyan "Checking port ${PORT}"
if ss -tlnp 2>/dev/null | grep -q ":${PORT} "; then
    yellow "Port ${PORT} may be in use (could be a previous instance)."
fi

# ── 3  Remove previous container ─────────────────────────────────
cyan "Removing previous instance (if present)"
if docker ps -a --filter "name=^${NAME}$" --format '{{.Names}}' | grep -q "^${NAME}$"; then
    docker stop "${NAME}" 2>/dev/null || true
    docker rm   "${NAME}" 2>/dev/null || true
    echo "   Previous container removed."
fi

# ── 4  Pull image ────────────────────────────────────────────────
cyan "Pulling ${IMAGE}"
docker pull "${IMAGE}"

# ── 5  Create volume ─────────────────────────────────────────────
cyan "Creating volume: ${VOLUME}"
docker volume create "${VOLUME}" >/dev/null

# ── 6  Start container ───────────────────────────────────────────
cyan "Starting Portainer on port ${PORT}"
docker run -d                                          \
    -p "${PORT}:9000"                                  \
    --name "${NAME}"                                   \
    --restart unless-stopped                            \
    -v /var/run/docker.sock:/var/run/docker.sock        \
    -v "${VOLUME}:/data"                                \
    "${IMAGE}" >/dev/null

# ── 7  Wait for API ──────────────────────────────────────────────
cyan "Waiting for Portainer API"
for i in $(seq 1 30); do
    if curl -sf "${BASE}/api/status" >/dev/null 2>&1; then
        echo "   API ready (attempt ${i}/30)."
        break
    fi
    [ "$i" -eq 30 ] && { red "API did not respond after 30 seconds."; exit 1; }
    sleep 1
done

# ── 8  Create admin user ─────────────────────────────────────────
cyan "Creating admin user: ${ADMIN}"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "${BASE}/api/users/admin/init"     \
    -H "Content-Type: application/json"         \
    -d "{\"Username\":\"${ADMIN}\",\"Password\":\"${PASS}\"}")

case "${HTTP}" in
    200) echo "   Admin user created." ;;
    409) yellow "Admin user already exists — reusing." ;;
    *)   yellow "Could not create admin (HTTP ${HTTP}). Create manually at ${BASE}" ;;
esac

# ── 9  Register local environment ────────────────────────────────
cyan "Registering local Docker environment"
TOKEN=$(curl -sf -X POST "${BASE}/api/auth"    \
    -H "Content-Type: application/json"          \
    -d "{\"Username\":\"${ADMIN}\",\"Password\":\"${PASS}\"}" \
    | grep -o '"jwt":"[^"]*"' | cut -d'"' -f4) || true

if [ -n "${TOKEN}" ]; then
    EC=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "${BASE}/api/endpoints"          \
        -H "Authorization: Bearer ${TOKEN}"       \
        -d "Name=local&EndpointCreationType=1")
    case "${EC}" in
        200|201) echo "   Local environment registered." ;;
        409|500) yellow "Environment already configured." ;;
        *)       yellow "Auto-registration skipped — click 'Get Started' in browser." ;;
    esac
else
    yellow "Could not obtain token — click 'Get Started' in browser."
fi

# ── 10  Done ──────────────────────────────────────────────────────
echo ""
green "================================================================"
green "  Portainer is running."
green "================================================================"
echo ""
echo "  URL       : ${BASE}"
echo "  Username  : ${ADMIN}"
echo "  Password  : ${PASS}"
echo ""
echo "  Stop      : docker stop portainer"
echo "  Start     : docker start portainer"
echo ""

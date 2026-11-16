#!/usr/bin/env bash
# Local Linux/WSL/VM Portainer setup. Existing containers and volumes are preserved.
# Run against the Docker daemon on this machine, as a user with Docker access.
set -euo pipefail

IMAGE="${PORTAINER_IMAGE:-portainer/portainer-ce:2.21-alpine}"
NAME="${PORTAINER_NAME:-portainer}"
PORT="${PORTAINER_PORT:-9050}"
VOLUME="${PORTAINER_VOLUME:-portainer_data}"
ADMIN="${PORTAINER_USER:-stud}"
PASS="${PORTAINER_PASSWORD:-studstudstud}"
BASE="http://127.0.0.1:${PORT}"

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
step() { printf '\n>> %s\n' "$*"; }
for command_name in docker curl python3 ss mktemp; do
    command -v "$command_name" >/dev/null 2>&1 || die "Required command missing: $command_name"
done
[[ "$PORT" =~ ^[0-9]+$ ]] && (( 10#$PORT > 0 && 10#$PORT < 65536 )) || die 'PORTAINER_PORT must be 1..65535.'
[[ "$NAME" =~ ^[A-Za-z0-9][A-Za-z0-9_.-]*$ ]] || die 'Invalid container name.'
[[ "$VOLUME" =~ ^[A-Za-z0-9][A-Za-z0-9_.-]*$ ]] || die 'Invalid volume name.'
[[ -n "$ADMIN" && ! "$ADMIN" =~ [[:space:]] ]] || die 'Invalid administrator username.'
(( ${#PASS} >= 12 )) || die 'Use a password of at least 12 characters.'

step 'Checking the local Linux Docker daemon'
docker info >/dev/null 2>&1 || die 'Docker is not responding or this user lacks Docker access.'
[[ "$(docker info --format '{{.OSType}}')" == linux ]] || die 'Linux containers are required.'
if [[ -n "${DOCKER_HOST:-}" && -z "${DOCKER_CONTEXT:-}" ]]; then
    daemon_address="$DOCKER_HOST"
else
    daemon_address="$(docker context inspect --format '{{.Endpoints.docker.Host}}')"
fi
[[ "$daemon_address" == unix://* ]] || die "Use a local Unix-socket Docker context; remote contexts are not supported."

work_directory="$(mktemp -d)"
chmod 700 "$work_directory"
trap 'rm -rf -- "$work_directory"' EXIT

existing_names="$(docker ps -a --filter "name=^/${NAME}$" --format '{{.Names}}')"
if [[ "$existing_names" == "$NAME" ]]; then
    step 'Inspecting the existing container without replacing it'
    docker container inspect "$NAME" > "$work_directory/container.json"
    python3 - "$work_directory/container.json" "$PORT" "$VOLUME" <<'PY_CHECK'
import json,sys
c=json.load(open(sys.argv[1],encoding='utf-8'))[0]
image=c.get('Config',{}).get('Image','')
if not image.startswith(('portainer/portainer-ce:', 'portainer/portainer-ce@', 'docker.io/portainer/portainer-ce:', 'docker.io/portainer/portainer-ce@')):
    raise SystemExit('Existing container is not identified as Portainer CE; it has been preserved.')
bindings=c.get('HostConfig',{}).get('PortBindings',{}).get('9000/tcp') or []
if not any(p.get('HostPort')==sys.argv[2] and p.get('HostIp') == '127.0.0.1' for p in bindings):
    raise SystemExit('Existing container does not use the requested loopback port; it has been preserved. Review its configuration manually.')
all_bindings=[p for group in c.get('HostConfig',{}).get('PortBindings',{}).values() for p in (group or [])]
if any(p.get('HostIp') not in ('127.0.0.1','::1') for p in all_bindings):
    raise SystemExit('Existing container also publishes a port beyond loopback; preserved. Review before using shared lab credentials.')
mounts=c.get('Mounts',[])
if not any(m.get('Destination')=='/data' and m.get('Type')=='volume' and m.get('Name')==sys.argv[3] for m in mounts):
    raise SystemExit('Existing Portainer data volume differs; container and data preserved. Select the intended PORTAINER_VOLUME.')
if not any(m.get('Destination')=='/var/run/docker.sock' for m in mounts):
    raise SystemExit('Existing container lacks the local Docker socket mount; preserved.')
print('Existing image:',image)
PY_CHECK
    running="$(docker inspect --format '{{.State.Running}}' "$NAME")"
    if [[ "$running" != true ]]; then
        docker start "$NAME" >/dev/null
    fi
else
    step "Preparing Portainer on loopback port ${PORT}"
    if [[ -n "$(ss -H -ltn "sport = :${PORT}")" ]]; then
        die "Port ${PORT} is already listening. No existing service has been stopped."
    fi
    if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
        step "Downloading ${IMAGE} (internet required because the image is not cached)"
        docker pull "$IMAGE"
    fi
    docker volume create "$VOLUME" >/dev/null
    docker run -d -p "127.0.0.1:${PORT}:9000" --name "$NAME" \
        --restart unless-stopped \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v "${VOLUME}:/data" "$IMAGE" >/dev/null
fi

step 'Waiting for the Portainer API'
ready=false
for attempt in $(seq 1 30); do
    if curl -fsS --connect-timeout 2 --max-time 3 "${BASE}/api/status" > "$work_directory/status.json" 2>/dev/null &&
       python3 - "$work_directory/status.json" <<'PY_STATUS'
import json,sys
s=json.load(open(sys.argv[1],encoding='utf-8'))
raise SystemExit(0 if isinstance(s,dict) and ('Version' in s or 'version' in s) else 1)
PY_STATUS
    then
        ready=true
        break
    fi
    sleep 1
done
[[ "$ready" == true ]] || die 'Portainer API did not become ready. Container and data preserved; inspect docker logs.'

# Keep credentials and the session token in a private temporary directory.
printf '%s\0%s' "$ADMIN" "$PASS" | python3 -c 'import json,sys; u,p=sys.stdin.read().split("\0",1); json.dump({"Username":u,"Password":p},sys.stdout)' > "$work_directory/credentials.json"
init_status="$(curl -sS --connect-timeout 3 --max-time 15 -o "$work_directory/init.json" -w '%{http_code}' \
    -X POST -H 'Content-Type: application/json' --data-binary "@$work_directory/credentials.json" "${BASE}/api/users/admin/init")"
case "$init_status" in
    200|201) printf 'Administrator account initialised.\n' ;;
    409) printf 'Administrator already exists; checking the supplied credentials without changing them.\n' ;;
    *) die "Administrator initialisation failed (HTTP ${init_status}). No account or volume was reset." ;;
esac

curl -fsS --connect-timeout 3 --max-time 15 -X POST -H 'Content-Type: application/json' \
    --data-binary "@$work_directory/credentials.json" "${BASE}/api/auth" > "$work_directory/login.json" ||
    die 'Login failed. Use the credentials of the existing instance; its account and data have been preserved.'
python3 - "$work_directory/login.json" "$work_directory/auth-header" <<'PY_TOKEN'
import json,sys
s=json.load(open(sys.argv[1],encoding='utf-8'))
token=s.get('jwt')
if not isinstance(token,str) or not token or '\n' in token or '\r' in token:
    raise SystemExit('Authentication response does not contain a valid token.')
open(sys.argv[2],'w',encoding='utf-8').write('Authorization: Bearer '+token+'\n')
PY_TOKEN

step 'Checking the local Docker environment'
curl -fsS --connect-timeout 3 --max-time 15 -H "@$work_directory/auth-header" "${BASE}/api/endpoints" > "$work_directory/endpoints.json"
endpoint_id="$(python3 - "$work_directory/endpoints.json" <<'PY_ENDPOINT'
import json,sys
items=json.load(open(sys.argv[1],encoding='utf-8'))
if not isinstance(items,list): raise SystemExit('Unexpected environment-list response.')
for e in items:
    if e.get('Type')==1 and e.get('URL')=='unix:///var/run/docker.sock':
        print(int(e['Id'])); break
else:
    if any(e.get('Name')=='local' for e in items):
        raise SystemExit('An environment named local exists with a different connection; preserved. Review it in the browser.')
PY_ENDPOINT
)"
if [[ -z "$endpoint_id" ]]; then
    curl -fsS --connect-timeout 3 --max-time 30 -X POST -H "@$work_directory/auth-header" \
        -F 'Name=local' -F 'EndpointCreationType=1' -F 'URL=unix:///var/run/docker.sock' \
        "${BASE}/api/endpoints" > "$work_directory/created-endpoint.json" || die 'Local environment registration failed.'
    endpoint_id="$(python3 - "$work_directory/created-endpoint.json" <<'PY_CREATED'
import json,sys
s=json.load(open(sys.argv[1],encoding='utf-8'))
if s.get('Type')!=1 or s.get('URL')!='unix:///var/run/docker.sock':
    raise SystemExit('Created environment does not identify the local Docker socket.')
print(int(s['Id']))
PY_CREATED
)"
fi
[[ "$endpoint_id" =~ ^[0-9]+$ ]] || die 'No valid local environment ID was returned.'
ping_result="$(curl -fsS --connect-timeout 3 --max-time 15 -H "@$work_directory/auth-header" "${BASE}/api/endpoints/${endpoint_id}/docker/_ping")"
[[ "$ping_result" == OK ]] || die 'Portainer cannot confirm access to the local Docker daemon.'

printf '\nPortainer setup verified: API ready, login accepted and local Docker ping returned OK.\n'
printf 'URL on this Linux machine: %s\nUsername: %s\n' "$BASE" "$ADMIN"
printf 'From Windows to a VirtualBox guest, use the SSH tunnel in PORTAINER_SETUP.md.\n'
printf 'Existing accounts, containers and volumes were not deleted or reset.\n'

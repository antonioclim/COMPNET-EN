<#
.SYNOPSIS
    Automated Portainer CE setup for the COMPNET lab environment.

.DESCRIPTION
    Pulls the Portainer image, creates a persistent volume, starts the
    container on port 9050, waits for the API to respond and creates the
    admin user (stud / studstudstud) without manual browser interaction.

.NOTES
    Port        : 9050  (9000 is reserved by S10 SSH tunnel)
    Credentials : stud / studstudstud
    Requires    : Docker Desktop running in Linux-containers mode
#>

param(
    [string] $Image    = "portainer/portainer-ce:2.21-alpine",
    [string] $Name     = "portainer",
    [int]    $Port     = 9050,
    [string] $Volume   = "portainer_data",
    [string] $User     = "stud",
    [string] $Password = "studstudstud"
)

$ErrorActionPreference = "Stop"

function Write-Step ([string] $Msg) {
    Write-Host "`n>> $Msg" -ForegroundColor Cyan
}

# ── 1  Check Docker ──────────────────────────────────────────────
Write-Step "Checking Docker availability"
try {
    $dockerVer = docker version --format '{{.Server.Version}}' 2>&1
    Write-Host "   Docker Engine $dockerVer detected."
} catch {
    Write-Host "ERROR: Docker is not running. Start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# ── 2  Check port ────────────────────────────────────────────────
Write-Step "Checking port $Port"
$portCheck = netstat -ano | Select-String ":$Port\s"
if ($portCheck) {
    Write-Host "   WARNING: port $Port may be in use (could be a previous instance)." -ForegroundColor Yellow
}

# ── 3  Remove previous container (if any) ────────────────────────
Write-Step "Removing previous Portainer instance (if present)"
$existing = docker ps -a --filter "name=^${Name}$" --format "{{.Names}}" 2>$null
if ($existing -eq $Name) {
    docker stop $Name  2>$null | Out-Null
    docker rm   $Name  2>$null | Out-Null
    Write-Host "   Previous container removed."
}

# ── 4  Pull image ────────────────────────────────────────────────
Write-Step "Pulling $Image"
docker pull $Image

# ── 5  Create volume ─────────────────────────────────────────────
Write-Step "Creating volume: $Volume"
docker volume create $Volume | Out-Null

# ── 6  Start container ───────────────────────────────────────────
Write-Step "Starting Portainer on port $Port"
docker run -d                                             `
    -p "${Port}:9000"                                     `
    --name $Name                                          `
    --restart unless-stopped                               `
    -v /var/run/docker.sock:/var/run/docker.sock           `
    -v "${Volume}:/data"                                   `
    $Image | Out-Null

# ── 7  Wait for API ──────────────────────────────────────────────
Write-Step "Waiting for Portainer API"
$baseUrl     = "http://localhost:$Port"
$maxAttempts = 30

for ($i = 1; $i -le $maxAttempts; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "$baseUrl/api/status" `
                    -UseBasicParsing -TimeoutSec 2
        if ($resp.StatusCode -eq 200) {
            Write-Host "   API ready (attempt $i/$maxAttempts)."
            break
        }
    } catch {
        if ($i -eq $maxAttempts) {
            Write-Host "ERROR: API did not respond after $maxAttempts seconds." -ForegroundColor Red
            exit 1
        }
        Start-Sleep -Seconds 1
    }
}

# ── 8  Create admin user ─────────────────────────────────────────
Write-Step "Creating admin user: $User"
$body = @{ Username = $User; Password = $Password } | ConvertTo-Json

try {
    $resp = Invoke-WebRequest -Uri "$baseUrl/api/users/admin/init" `
                -Method POST                                        `
                -ContentType "application/json"                      `
                -Body $body                                          `
                -UseBasicParsing -TimeoutSec 10

    if ($resp.StatusCode -eq 200) {
        Write-Host "   Admin user created."
    }
} catch {
    $sc = $_.Exception.Response.StatusCode.Value__
    if ($sc -eq 409) {
        Write-Host "   Admin user already exists — reusing." -ForegroundColor Yellow
    } else {
        Write-Host "   Could not create admin user (HTTP $sc). Create manually at $baseUrl" -ForegroundColor Yellow
    }
}

# ── 9  Register local environment ────────────────────────────────
Write-Step "Registering local Docker environment"
try {
    $loginBody = @{ Username = $User; Password = $Password } | ConvertTo-Json
    $loginResp = Invoke-WebRequest -Uri "$baseUrl/api/auth"     `
                    -Method POST -ContentType "application/json"  `
                    -Body $loginBody -UseBasicParsing -TimeoutSec 10
    $token  = ($loginResp.Content | ConvertFrom-Json).jwt
    $headers = @{ Authorization = "Bearer $token" }

    Invoke-WebRequest -Uri "$baseUrl/api/endpoints"              `
        -Method POST -Headers $headers                            `
        -ContentType "application/x-www-form-urlencoded"          `
        -Body "Name=local&EndpointCreationType=1"                 `
        -UseBasicParsing -TimeoutSec 10 | Out-Null

    Write-Host "   Local environment registered."
} catch {
    Write-Host "   Auto-registration skipped — click 'Get Started' in the browser." -ForegroundColor Yellow
}

# ── 10  Done ──────────────────────────────────────────────────────
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  Portainer is running." -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  URL       : $baseUrl"
Write-Host "  Username  : $User"
Write-Host "  Password  : $Password"
Write-Host ""
Write-Host "  Stop      : docker stop portainer"
Write-Host "  Start     : docker start portainer"
Write-Host ""

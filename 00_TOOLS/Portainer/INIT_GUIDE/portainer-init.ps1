<#
Local Windows Docker Desktop setup. Requires Linux-containers mode.
For Docker inside MININET-SDN, run portainer-init.sh INSIDE that VM instead.
Existing containers, accounts and data volumes are never deleted or reset.
Windows PowerShell 5.1 compatible syntax; native Windows validation is separate.
#>
#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Image = 'portainer/portainer-ce:2.21-alpine',
    [string]$Name = 'portainer',
    [ValidateRange(1,65535)][int]$Port = 9050,
    [string]$Volume = 'portainer_data',
    [string]$User = 'stud',
    [string]$Password = 'studstudstud'
)
Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Invoke-Docker {
    param([string[]]$DockerArguments, [switch]$AllowFailure)
    # Native non-zero exit codes do not reliably throw in Windows PowerShell 5.1.
    $savedPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $output = @(& docker @DockerArguments 2>&1)
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $savedPreference
    }
    if ($exitCode -ne 0 -and -not $AllowFailure) {
        throw ('Docker command failed (exit {0}): {1}' -f $exitCode, ($output -join [Environment]::NewLine))
    }
    [pscustomobject]@{ ExitCode = $exitCode; Text = ($output -join [Environment]::NewLine) }
}

function Invoke-Portainer {
    param([string]$Path, [string]$Method = 'GET', $Body = $null,
          [string]$ContentType = 'application/json', [hashtable]$Headers = @{})
    $arguments = @{
        Uri = $script:BaseUrl + $Path
        Method = $Method
        Headers = $Headers
        UseBasicParsing = $true
        TimeoutSec = 15
        ErrorAction = 'Stop'
    }
    if ($null -ne $Body) { $arguments.Body = $Body; $arguments.ContentType = $ContentType }
    try {
        $response = Invoke-WebRequest @arguments
        [pscustomobject]@{ Status = [int]$response.StatusCode; Content = [string]$response.Content }
    } catch {
        $response = $_.Exception.Response
        if ($null -eq $response) { throw }
        [pscustomobject]@{ Status = [int]$response.StatusCode; Content = '' }
    }
}

function Assert-HttpSuccess {
    param($Response, [string]$Operation)
    if ($Response.Status -lt 200 -or $Response.Status -ge 300) {
        throw ('{0} failed (HTTP {1}). Existing accounts and data were preserved.' -f $Operation, $Response.Status)
    }
}

try {
    if ($Name -notmatch '^[A-Za-z0-9][A-Za-z0-9_.-]*$') { throw 'Invalid container name.' }
    if ($Volume -notmatch '^[A-Za-z0-9][A-Za-z0-9_.-]*$') { throw 'Invalid volume name.' }
    if ([string]::IsNullOrWhiteSpace($User) -or $User -match '\s') { throw 'Invalid administrator username.' }
    if ($Password.Length -lt 12) { throw 'Use a password of at least 12 characters.' }
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker CLI not found. Start Docker Desktop in Linux-containers mode.' }
    $script:BaseUrl = 'http://127.0.0.1:' + $Port
    Write-Host 'Checking the local Linux Docker daemon.'
    $null = Invoke-Docker -DockerArguments @('info')
    $os = (Invoke-Docker -DockerArguments @('info','--format','{{.OSType}}')).Text.Trim()
    if ($os -ne 'linux') { throw 'Docker Desktop must use Linux containers.' }
    if ($env:DOCKER_HOST -and -not $env:DOCKER_CONTEXT) {
        $daemonAddress = $env:DOCKER_HOST
    } else {
        $daemonAddress = (Invoke-Docker -DockerArguments @('context','inspect','--format','{{.Endpoints.docker.Host}}')).Text.Trim()
    }
    if ($daemonAddress -notmatch '^(npipe|unix)://') { throw 'Use a local Docker context. Remote SSH/TCP contexts are not supported by this installer.' }

    $existing = (Invoke-Docker -DockerArguments @('ps','-a','--filter',('name=^/' + $Name + '$'),'--format','{{.Names}}')).Text.Trim()
    if ($existing -eq $Name) {
        Write-Host 'Inspecting the existing container without replacing it.'
        $objects = @((Invoke-Docker -DockerArguments @('container','inspect',$Name)).Text | ConvertFrom-Json)
        $container = $objects[0]
        if ($container.Config.Image -notmatch '^(docker.io/)?portainer/portainer-ce[:@]') { throw 'Existing container is not identified as Portainer CE; it has been preserved.' }
        $portProperty = $container.HostConfig.PortBindings.PSObject.Properties['9000/tcp']
        if ($null -eq $portProperty) { throw 'Existing container has no HTTP mapping. Its configuration was preserved.' }
        $bindings = @($portProperty.Value)
        $matching = @($bindings | Where-Object { $_.HostPort -eq [string]$Port -and $_.HostIp -eq '127.0.0.1' })
        $allBindings = @($container.HostConfig.PortBindings.PSObject.Properties | ForEach-Object { $_.Value } | Where-Object { $null -ne $_ })
        $exposed = @($allBindings | Where-Object { $_.HostIp -notin @('127.0.0.1','::1') })
        if ($matching.Count -eq 0 -or $exposed.Count -gt 0) { throw 'Existing container does not use only the requested loopback binding. Review its configuration; no replacement was made.' }
        $dataMounts = @($container.Mounts | Where-Object { $_.Destination -eq '/data' -and $_.Type -eq 'volume' -and $_.Name -eq $Volume })
        $socketMounts = @($container.Mounts | Where-Object { $_.Destination -eq '/var/run/docker.sock' })
        if ($dataMounts.Count -eq 0 -or $socketMounts.Count -eq 0) { throw 'Existing mounts differ from the requested local setup. Container and volumes were preserved.' }
        Write-Host ('Existing image: ' + $container.Config.Image)
        if (-not $container.State.Running) { $null = Invoke-Docker -DockerArguments @('start',$Name) }
    } else {
        $listeners = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
        if (@($listeners | Where-Object { $_.Port -eq $Port }).Count -gt 0) { throw ('Port {0} is already listening. No existing service has been stopped.' -f $Port) }
        $cached = Invoke-Docker -DockerArguments @('image','inspect',$Image) -AllowFailure
        if ($cached.ExitCode -ne 0) {
            Write-Host ('Downloading {0}; internet is required because it is not cached.' -f $Image)
            $null = Invoke-Docker -DockerArguments @('pull',$Image)
        }
        $null = Invoke-Docker -DockerArguments @('volume','create',$Volume)
        $null = Invoke-Docker -DockerArguments @('run','-d','-p',('127.0.0.1:' + $Port + ':9000'),
            '--name',$Name,'--restart','unless-stopped','-v','/var/run/docker.sock:/var/run/docker.sock',
            '-v',($Volume + ':/data'),$Image)
    }

    Write-Host 'Waiting for the Portainer API.'
    $ready = $false
    for ($attempt = 1; $attempt -le 30; $attempt++) {
        try {
            $status = Invoke-Portainer -Path '/api/status'
            if ($status.Status -eq 200) {
                $statusJson = $status.Content | ConvertFrom-Json
                if ($statusJson.PSObject.Properties['Version']) { $ready = $true; break }
            }
        } catch { }
        Start-Sleep -Seconds 1
    }
    if (-not $ready) { throw 'Portainer API did not become ready. Container and data preserved; inspect docker logs.' }

    $credentials = @{ Username = $User; Password = $Password } | ConvertTo-Json -Compress
    $initialise = Invoke-Portainer -Path '/api/users/admin/init' -Method 'POST' -Body $credentials
    if ($initialise.Status -in @(200,201)) {
        Write-Host 'Administrator account initialised.'
    } elseif ($initialise.Status -eq 409) {
        Write-Host 'Administrator already exists; checking the supplied credentials without changing them.'
    } else {
        throw ('Administrator initialisation failed (HTTP {0}). No account or volume was reset.' -f $initialise.Status)
    }
    $login = Invoke-Portainer -Path '/api/auth' -Method 'POST' -Body $credentials
    Assert-HttpSuccess $login 'Login (use the existing account credentials if already initialised)'
    $loginJson = $login.Content | ConvertFrom-Json
    if (-not $loginJson.PSObject.Properties['jwt'] -or [string]::IsNullOrWhiteSpace([string]$loginJson.jwt)) { throw 'Authentication returned no valid token.' }
    $headers = @{ Authorization = 'Bearer ' + $loginJson.jwt }

    $listed = Invoke-Portainer -Path '/api/endpoints' -Headers $headers
    Assert-HttpSuccess $listed 'Environment listing'
    $endpoints = @($listed.Content | ConvertFrom-Json)
    $local = @($endpoints | Where-Object { $_.Type -eq 1 -and $_.URL -eq 'unix:///var/run/docker.sock' })
    if ($local.Count -gt 0) {
        $endpointId = [int]$local[0].Id
    } else {
        if (@($endpoints | Where-Object { $_.Name -eq 'local' }).Count -gt 0) { throw 'An environment named local uses a different connection. It has been preserved; review it in the browser.' }
        # The 2.21 API reads these scalar fields through Go Request.FormValue.
        $form = @{ Name = 'local'; EndpointCreationType = '1'; URL = 'unix:///var/run/docker.sock' }
        $created = Invoke-Portainer -Path '/api/endpoints' -Method 'POST' -Headers $headers -Body $form -ContentType 'application/x-www-form-urlencoded'
        Assert-HttpSuccess $created 'Local environment registration'
        $createdJson = $created.Content | ConvertFrom-Json
        if ($createdJson.Type -ne 1 -or $createdJson.URL -ne 'unix:///var/run/docker.sock') { throw 'Created environment does not identify the local Docker socket.' }
        $endpointId = [int]$createdJson.Id
    }
    if ($endpointId -le 0) { throw 'No valid local environment ID was returned.' }
    $ping = Invoke-Portainer -Path ('/api/endpoints/' + $endpointId + '/docker/_ping') -Headers $headers
    Assert-HttpSuccess $ping 'Local Docker connectivity'
    if ($ping.Content.Trim() -ne 'OK') { throw 'Portainer did not confirm access to the local Docker daemon.' }

    Write-Host 'Portainer setup verified: API ready, login accepted and local Docker ping returned OK.' -ForegroundColor Green
    Write-Host ('URL on this Windows host: ' + $script:BaseUrl)
    Write-Host ('Username: ' + $User)
    Write-Host 'Existing accounts, containers and volumes were not deleted or reset.'
} catch {
    Write-Error $_.Exception.Message -ErrorAction Continue
    exit 1
}

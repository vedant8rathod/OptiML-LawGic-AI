param()

$ErrorActionPreference = "Stop"

function Write-Step {
    param(
        [string]$Message,
        [string]$Color = "Cyan"
    )
    Write-Host $Message -ForegroundColor $Color
}

try {
    $repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    if (-not $repoRoot) {
        throw "Unable to determine repository root."
    }
    Set-Location $repoRoot

    Write-Step -Message "LawGic AI setup starting from $repoRoot" -Color Green

    Write-Step -Message "Checking for Python executable..." -Color Yellow
    $python = Get-Command python -ErrorAction Stop

    Write-Step -Message "Upgrading pip to the latest version..." -Color Yellow
    & $python.Source -m pip install --upgrade pip | Out-Host

    $backendDir = Join-Path $repoRoot "backend"
    if (-not (Test-Path $backendDir)) {
        throw "Backend directory not found at $backendDir"
    }

    $frontendDir = Join-Path $repoRoot "frontend"
    if (-not (Test-Path $frontendDir)) {
        throw "Frontend directory not found at $frontendDir"
    }

    $venvPath = Join-Path $backendDir "venv"
    $venvPython = Join-Path $venvPath "Scripts\python.exe"

    if (-not (Test-Path $venvPath)) {
        Write-Step -Message "Creating Python virtual environment in backend\\venv" -Color Yellow
        & $python.Source -m venv $venvPath | Out-Host
    } else {
        Write-Step -Message "Python virtual environment already exists at backend\\venv" -Color Cyan
    }

    if (-not (Test-Path $venvPython)) {
        throw "Virtual environment appears invalid. Expected python at $venvPython"
    }

    Write-Step -Message "Activating virtual environment..." -Color Yellow
    & (Join-Path $venvPath "Scripts\Activate.ps1")

    $requirementsPath = Join-Path $backendDir "requirements.txt"
    if (-not (Test-Path $requirementsPath)) {
        throw "requirements.txt not found at $requirementsPath"
    }

    Write-Step -Message "Installing backend dependencies from requirements.txt" -Color Yellow
    & $venvPython -m pip install -r $requirementsPath | Out-Host

    Write-Step -Message "Checking for npm executable..." -Color Yellow
    $npm = Get-Command npm.cmd -ErrorAction Stop
    $npmExecutable = $npm.Path

    Write-Step -Message "Installing frontend dependencies via npm install" -Color Yellow
    Push-Location $frontendDir
    try {
        & $npmExecutable install | Out-Host
    } finally {
        Pop-Location
    }

    $backendScript = Join-Path $backendDir "start-backend.ps1"
    if (-not (Test-Path $backendScript)) {
        throw "Backend startup script not found at $backendScript"
    }

    $frontendScript = Join-Path $frontendDir "start-frontend.ps1"
    if (-not (Test-Path $frontendScript)) {
        throw "Frontend startup script not found at $frontendScript"
    }

    Write-Step -Message "Starting backend using backend\\start-backend.ps1" -Color Green
    $backendProcess = Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$backendScript" -WorkingDirectory $backendDir -PassThru

    Write-Step -Message "Starting frontend using frontend\\start-frontend.ps1" -Color Green
    $frontendProcess = Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$frontendScript" -WorkingDirectory $frontendDir -PassThru

    Write-Step -Message "Opening backend in default browser: http://127.0.0.1:8000" -Color Cyan
    Start-Process "http://127.0.0.1:8000"

    Write-Step -Message "Opening frontend in default browser: http://localhost:3000" -Color Cyan
    Start-Process "http://localhost:3000"

    Write-Step -Message "Backend Process ID: $($backendProcess.Id)" -Color DarkGray
    Write-Step -Message "Frontend Process ID: $($frontendProcess.Id)" -Color DarkGray
    Write-Step -Message "LawGic AI setup complete. Servers are launching in separate windows." -Color Green

} catch {
    Write-Host "An error occurred: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.InvocationInfo.PositionMessage) {
        Write-Host $_.InvocationInfo.PositionMessage -ForegroundColor DarkRed
    }
    exit 1
}

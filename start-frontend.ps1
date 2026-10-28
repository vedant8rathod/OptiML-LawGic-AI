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

    Write-Step -Message "Starting LawGic AI frontend..." -Color Green

    Push-Location (Join-Path $repoRoot "frontend")

    Write-Step -Message "Checking for npm executable..." -Color Yellow
    $npmCmd = Get-Command npm.cmd -ErrorAction Stop
    $npmExecutable = $npmCmd.Path

    if (-not (Test-Path "node_modules")) {
        Write-Step -Message "Installing frontend dependencies (npm install)..." -Color Yellow
        & $npmExecutable install | Out-Host
    } else {
        Write-Step -Message "node_modules directory found. Skipping npm install." -Color Cyan
    }

    Write-Step -Message "Launching Vite development server (npm run dev)..." -Color Green
    Write-Step -Message "Frontend server running at http://localhost:3000" -Color Cyan
    Write-Step -Message "Press Ctrl+C to stop the server" -Color Yellow

    & $npmExecutable run dev
}
catch {
    Write-Host "An error occurred while launching frontend: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.InvocationInfo.PositionMessage) {
        Write-Host $_.InvocationInfo.PositionMessage -ForegroundColor DarkRed
    }
    exit 1
}
finally {
    try {
        Pop-Location | Out-Null
    } catch {
        # Ignore cleanup errors
    }
}

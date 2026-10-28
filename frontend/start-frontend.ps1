param()

$ErrorActionPreference = "Stop"

try {
    $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    $repoRoot = Split-Path $scriptRoot -Parent
    if (-not $repoRoot) {
        throw "Unable to determine repository root from $scriptRoot"
    }

    $rootScript = Join-Path $repoRoot "start-frontend.ps1"
    if (-not (Test-Path $rootScript)) {
        throw "Expected frontend launcher at $rootScript"
    }

    Set-Location $repoRoot
    & $rootScript
} catch {
    Write-Host "An error occurred while launching frontend: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.InvocationInfo.PositionMessage) {
        Write-Host $_.InvocationInfo.PositionMessage -ForegroundColor DarkRed
    }
    exit 1
}

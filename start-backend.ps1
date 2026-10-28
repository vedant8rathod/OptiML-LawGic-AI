Write-Host "Starting LawGic AI backend..." -ForegroundColor Green

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

try {
    Push-Location $scriptDir
    Push-Location backend

    $venvPath = Join-Path (Get-Location) "venv"

    if (-not (Test-Path $venvPath)) {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
    } else {
        Write-Host "Virtual environment already exists." -ForegroundColor Cyan
    }

    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & (Join-Path $venvPath "Scripts\Activate.ps1")

    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt

    Write-Host "Launching Uvicorn (app.main:app) with reload enabled..." -ForegroundColor Green
    Write-Host "Backend available at http://127.0.0.1:8000" -ForegroundColor Cyan
    Write-Host "API docs at http://127.0.0.1:8000/docs" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
}
finally {
    Pop-Location
    Pop-Location
}

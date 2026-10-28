# LawGic AI - Start Application Script
# This script starts both backend and frontend servers

Write-Host "🏛️ Starting LawGic AI - लॉजिक AI" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
if (!(Test-Path "backend") -or !(Test-Path "frontend")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    Write-Host "Make sure you're in the final-Lawgic directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "🔧 Initializing database..." -ForegroundColor Yellow
Set-Location backend
python init_db.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Database initialization failed" -ForegroundColor Red
    exit 1
}
Set-Location ..

Write-Host ""
Write-Host "🚀 Starting servers..." -ForegroundColor Green
Write-Host ""

# Start backend server in a new PowerShell window
Write-Host "📡 Starting Backend Server (Port 8000)..." -ForegroundColor Magenta
$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; Write-Host '🐍 FastAPI Backend Server' -ForegroundColor Green; Write-Host 'API Docs: http://localhost:8000/docs' -ForegroundColor Cyan; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -PassThru

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend server in a new PowerShell window  
Write-Host "⚛️ Starting Frontend Server (Vite)..." -ForegroundColor Blue
$frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host '⚡ React + Vite Frontend Server' -ForegroundColor Blue; Write-Host 'App URL: http://localhost:5173' -ForegroundColor Cyan; npm run dev" -PassThru

# Wait for servers to fully start
Write-Host ""
Write-Host "⏳ Waiting for servers to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "✅ LawGic AI is now running!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Access your application:" -ForegroundColor White
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor Cyan  
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌍 Features Available:" -ForegroundColor White
Write-Host "   • English/Hindi (हिंदी) Language Toggle" -ForegroundColor Yellow
Write-Host "   • AI Legal Analysis & Document Processing" -ForegroundColor Yellow
Write-Host "   • Voice Upload Support" -ForegroundColor Yellow
Write-Host "   • Complete Translation (No English leakage)" -ForegroundColor Yellow
Write-Host ""
Write-Host "📝 Test the multilingual features:" -ForegroundColor White
Write-Host "   1. Click language toggle (EN/हिं) in header" -ForegroundColor Gray
Write-Host "   2. Try: 'What are my tenant rights?' or 'किरायेदार के अधिकार क्या हैं?'" -ForegroundColor Gray
Write-Host "   3. Upload a document (.pdf, .docx, .txt)" -ForegroundColor Gray
Write-Host "   4. Verify all headers translate (Category, Disclaimer, etc.)" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 To stop servers: Close both PowerShell windows or press Ctrl+C in each" -ForegroundColor Red
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
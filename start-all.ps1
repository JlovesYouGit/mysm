Write-Host "Starting All Services..." -ForegroundColor Green

# Kill existing processes
Write-Host "Cleaning up..." -ForegroundColor Yellow
taskkill /F /IM python.exe 2>$null
taskkill /F /IM node.exe 2>$null

Start-Sleep -Seconds 2

# Start backend
Write-Host "Starting backend on port 8084..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'N:\sms'; python main_simple.py"

# Wait for backend
Start-Sleep -Seconds 5

# Start frontend
Write-Host "Starting frontend on port 3000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'N:\sms\Frontend components\nexus-dialer-hub'; yarn dev --port 3000"

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "All Services Started!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8084/docs" -ForegroundColor Cyan
Write-Host "Frontend UI: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening frontend..." -ForegroundColor Green
Start-Sleep -Seconds 3
Start-Process "http://localhost:3000"
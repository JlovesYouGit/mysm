Write-Host "Starting Telecom Service..."

# Activate venv
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
}

# Start MongoDB if not running
$mongoProcess = Get-Process mongod -ErrorAction SilentlyContinue
if (-not $mongoProcess) {
    Write-Host "Starting MongoDB..."
    Start-Process -FilePath "mongod" -ArgumentList "--dbpath=db" -WindowStyle Hidden
    Start-Sleep 3
}

# Start API
Write-Host "Starting API server..."
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--reload", "--port", "8081", "--host", "0.0.0.0"

# Start worker
Write-Host "Starting background worker..."
Start-Process -FilePath "python" -ArgumentList "src/workers/worker.py"

# Open browser
Start-Sleep 2
Start-Process "http://localhost:8081/docs"

Write-Host "Services started. API: http://localhost:8081/docs"
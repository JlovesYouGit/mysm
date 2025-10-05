Write-Host "Starting Telecom Services..." -ForegroundColor Green

# Kill existing processes on specific ports
Write-Host "Cleaning up old processes..." -ForegroundColor Yellow

# Kill processes using port 8083 (Python/FastAPI API)
$port8083 = netstat -ano | findstr :8083
if ($port8083) {
    $lines = $port8083 -split "`n"
    foreach ($line in $lines) {
        if ($line -match "\s+(\d+)\s*$") {
            $processId = $matches[1]
            if ($processId -and $processId -ne "0") {
                try {
                    Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                    Write-Host "Killed process $processId using port 8083" -ForegroundColor Yellow
                } catch {}
            }
        }
    }
}

# Kill processes using port 8084 (Python/FastAPI Spectrum API)
$port8084 = netstat -ano | findstr :8084
if ($port8084) {
    $lines = $port8084 -split "`n"
    foreach ($line in $lines) {
        if ($line -match "\s+(\d+)\s*$") {
            $processId = $matches[1]
            if ($processId -and $processId -ne "0") {
                try {
                    Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                    Write-Host "Killed process $processId using port 8084" -ForegroundColor Yellow
                } catch {}
            }
        }
    }
}

# Kill processes using port 8080 (React frontend)
$port8080 = netstat -ano | findstr :8080
if ($port8080) {
    $processId2 = ($port8080 -split '\s+')[-1]
    if ($processId2 -and $processId2 -ne "0") {
        try {
            Stop-Process -Id $processId2 -Force -ErrorAction SilentlyContinue
            Write-Host "Killed process $processId2 using port 8080" -ForegroundColor Yellow
        } catch {}
    }
}

# Also kill any remaining Node processes
Get-Process -Name "node" -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        Write-Host "Killed Node process $($_.Id)" -ForegroundColor Yellow
    } catch {}
}

# Kill any Python processes
Get-Process -Name "python" -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        Write-Host "Killed Python process $($_.Id)" -ForegroundColor Yellow
    } catch {}
}

Start-Sleep -Seconds 3

# Set environment variables for independent provider mode
$env:SS7_SIGTRAN = "false"
$env:SS7_PRIVATE_NETWORK = "true"

Write-Host "Environment Variables Set for Independent Provider Mode:" -ForegroundColor Green
Write-Host "  SS7_SIGTRAN = $env:SS7_SIGTRAN" -ForegroundColor Cyan
Write-Host "  SS7_PRIVATE_NETWORK = $env:SS7_PRIVATE_NETWORK" -ForegroundColor Cyan
Write-Host ""

# Start Python/FastAPI backend
Write-Host "Starting Python/FastAPI backend on port 8083 with Private Network Simulation..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'N:\sms'; `$env:SS7_SIGTRAN='false'; `$env:SS7_PRIVATE_NETWORK='true'; python -m pip install -r requirements.txt; python main.py"

# Start Python/FastAPI spectrum backend
Write-Host "Starting Python/FastAPI spectrum backend on port 8084..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'N:\sms'; python main_simple.py"

# Wait for Python backends to start
Write-Host "Waiting for Python backends to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start React frontend
Write-Host "Starting React frontend on port 8080..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'N:\sms\Frontend components\nexus-dialer-hub'; npm install; npm run dev"

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "Services started successfully!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "Python API: http://localhost:8083/" -ForegroundColor Cyan
Write-Host "Spectrum API: http://localhost:8084/" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8083/docs" -ForegroundColor Cyan
Write-Host "React Frontend: http://localhost:8080/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Provider Mode: INDEPENDENT (Private Network Simulation)" -ForegroundColor Green
Write-Host "Network Type: Self-Contained Private Network" -ForegroundColor Green
Write-Host "Carrier Dependency: NONE" -ForegroundColor Green
Write-Host "Security Features: TLS Encryption, Authentication, IP Whitelisting" -ForegroundColor Green
Write-Host ""
Write-Host "Opening frontend in browser..." -ForegroundColor Green
Start-Process "http://localhost:8080"
Write-Host ""
Write-Host "Check the opened PowerShell windows for logs" -ForegroundColor Yellow

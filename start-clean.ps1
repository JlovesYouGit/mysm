Write-Host "Cleaning up old processes..."

# Kill any processes on port 8084
$port8084 = Get-NetTCPConnection -LocalPort 8084 -ErrorAction SilentlyContinue
if ($port8084) {
    $pid = $port8084.OwningProcess
    Write-Host "Killing process $pid on port 8084"
    taskkill /F /PID $pid
}

# Kill any processes on port 8080
$port8080 = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($port8080) {
    $pid = $port8080.OwningProcess
    Write-Host "Killing process $pid on port 8080"
    taskkill /F /PID $pid
}

Start-Sleep -Seconds 2

Write-Host "Starting services..."
& "$PSScriptRoot\start-fullstack.ps1"
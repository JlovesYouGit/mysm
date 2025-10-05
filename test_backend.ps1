# Test backend import and start server
Write-Host "Testing backend import..."
python -c "from main import app; print('Backend import successful')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Starting FastAPI server..."
    Start-Process -NoNewWindow python -ArgumentList "-m", "uvicorn", "main:app", "--port", "8081"
    
    Write-Host "Waiting for server to start..."
    Start-Sleep 3
    
    Write-Host "Checking health endpoint..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8081/health"
        Write-Host "Backend Status:" $response.status
    } catch {
        Write-Host "Backend not ready"
    }
} else {
    Write-Host "Backend import failed"
}
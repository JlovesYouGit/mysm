Write-Host "Starting Telecom API..."
Write-Host "API will be available at: http://localhost:8081/docs"
python -m uvicorn main:app --reload --port 8081
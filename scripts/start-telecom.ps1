# start-telecom.ps1
# one-click: MongoDB + FastAPI + worker (background)
$mongoBin = "C:\Program Files\MongoDB\Server\8.2\bin"
$env:Path += ";$mongoBin"

Write-Host "Starting MongoDB ..."
Start-Process -FilePath mongod -ArgumentList "--dbpath","N:\sms\db","--port","27017" -WindowStyle Hidden

Write-Host "Starting FastAPI ..."
Start-Process -FilePath python -ArgumentList "main.py" -WindowStyle Hidden

Write-Host "Starting worker ..."
Start-Process -FilePath python -ArgumentList "worker.py" -WindowStyle Hidden

Write-Host "All services running on port 8081 (MongoDB 27017)"
Write-Host "API docs: http://localhost:8081/docs"
Write-Host "WebSocket: ws://localhost:8081/ws/events"
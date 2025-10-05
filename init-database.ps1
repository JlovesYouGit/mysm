Write-Host "Initializing MongoDB database..." -ForegroundColor Green

# Check if MongoDB is running
Write-Host "Checking if MongoDB is running..." -ForegroundColor Yellow

# Try different possible service names for MongoDB
$mongoServiceNames = @("MongoDB", "MongoDB Server", "mongodb", "MongoDBServer")
$mongoService = $null

foreach ($serviceName in $mongoServiceNames) {
    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($service) {
        $mongoService = $service
        Write-Host "Found MongoDB service: $serviceName" -ForegroundColor Green
        break
    }
}

if ($mongoService) {
    if ($mongoService.Status -eq "Running") {
        Write-Host "MongoDB is already running" -ForegroundColor Green
    } else {
        Write-Host "Starting MongoDB service..." -ForegroundColor Yellow
        try {
            Start-Service -Name $mongoService.Name
            Start-Sleep -Seconds 5
            Write-Host "MongoDB service started successfully" -ForegroundColor Green
        } catch {
            Write-Host "Failed to start MongoDB service: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "Attempting to start MongoDB manually..." -ForegroundColor Yellow
            
            # Try to start MongoDB manually
            try {
                Start-Process -FilePath "mongod" -ArgumentList "--dbpath", "C:\data\db" -PassThru -WindowStyle Hidden
                Start-Sleep -Seconds 3
                Write-Host "MongoDB started manually" -ForegroundColor Green
            } catch {
                Write-Host "Failed to start MongoDB manually: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "Please start MongoDB manually and then run this script again" -ForegroundColor Yellow
            }
        }
    }
} else {
    Write-Host "MongoDB service not found as a Windows service." -ForegroundColor Yellow
    Write-Host "Checking if MongoDB is running on default port 27017..." -ForegroundColor Yellow
    
    # Try to connect to MongoDB directly
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect("localhost", 27017)
        if ($tcpClient.Connected) {
            Write-Host "MongoDB is running on port 27017" -ForegroundColor Green
            $tcpClient.Close()
        }
    } catch {
        Write-Host "MongoDB is not running. Attempting to start MongoDB manually..." -ForegroundColor Yellow
        
        # Try to start MongoDB manually
        try {
            Start-Process -FilePath "mongod" -ArgumentList "--dbpath", "C:\data\db" -PassThru -WindowStyle Hidden
            Start-Sleep -Seconds 5
            Write-Host "MongoDB started manually" -ForegroundColor Green
        } catch {
            Write-Host "Failed to start MongoDB manually: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "Please ensure MongoDB is installed and running." -ForegroundColor Red
            Write-Host "You can:" -ForegroundColor Yellow
            Write-Host "1. Download MongoDB from: https://www.mongodb.com/try/download/community" -ForegroundColor Cyan
            Write-Host "2. Install it as a service, or" -ForegroundColor Cyan
            Write-Host "3. Run mongod.exe manually" -ForegroundColor Cyan
            Write-Host "4. Or continue with mock data (some features will work without persistent storage)" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Press any key to continue with mock data, or Ctrl+C to exit..." -ForegroundColor Yellow
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    }
}

# Seed the database
Write-Host "Seeding database with phone numbers..." -ForegroundColor Yellow
cd "N:\sms"
python seed_database.py

Write-Host "Database initialization complete!" -ForegroundColor Green
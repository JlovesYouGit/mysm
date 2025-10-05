# MongoDB Installation Script for Windows
# This script downloads and installs MongoDB Community Edition

Write-Host "MongoDB Community Edition Installation Script" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This script needs to run as Administrator to install MongoDB as a service." -ForegroundColor Yellow
    Write-Host "Please right-click PowerShell and select 'Run as administrator' then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternatively, you can manually download MongoDB from:" -ForegroundColor Cyan
    Write-Host "https://www.mongodb.com/try/download/community" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or run '.\setup-mongodb-manual.ps1' for manual installation instructions" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit
}

# Create temporary directory for download
$tempDir = "$env:TEMP\mongodb_install"
if (!(Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

Write-Host "1. Downloading MongoDB Community Edition..." -ForegroundColor Yellow

# MongoDB download URL (latest stable version for Windows x64)
# Using a specific version to ensure compatibility
$mongoUrl = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4-signed.msi"
$downloadPath = "$tempDir\mongodb.msi"

try {
    Write-Host "Downloading from $mongoUrl" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $mongoUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "✅ Download completed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download MongoDB: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please manually download MongoDB from https://www.mongodb.com/try/download/community" -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "2. Installing MongoDB..." -ForegroundColor Yellow

# Installation parameters
$installDir = "C:\Program Files\MongoDB\Server\7.0"
$dataDir = "C:\data\db"
$logDir = "C:\data\log"

# Create data and log directories
if (!(Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
}
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Install MongoDB using msiexec
try {
    $installArgs = @(
        "/i",
        "`"$downloadPath`"",
        "/quiet",
        "INSTALLLOCATION=`"$installDir`"",
        "ADDLOCAL=Server,Client,MonitoringTools,ImportExportTools,MiscellaneousTools"
    )
    
    Write-Host "Installing MongoDB silently..." -ForegroundColor Cyan
    Start-Process -FilePath "msiexec.exe" -ArgumentList $installArgs -Wait -NoNewWindow
    
    Write-Host "✅ MongoDB installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install MongoDB: $($_.Exception.Message)" -ForegroundColor Red
    pause
    exit
}

Write-Host ""
Write-Host "3. Configuring MongoDB as a Windows Service..." -ForegroundColor Yellow

try {
    # Ensure the bin directory exists
    $mongoBin = "C:\Program Files\MongoDB\Server\7.0\bin"
    if (!(Test-Path $mongoBin)) {
        Write-Host "⚠️  MongoDB bin directory not found, creating it..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $mongoBin -Force | Out-Null
    }
    
    # Create MongoDB configuration file
    $configPath = "$mongoBin\mongod.cfg"
    $configContent = @"
systemLog:
  destination: file
  path: C:\data\log\mongod.log
storage:
  dbPath: C:\data\db
net:
  bindIp: 127.0.0.1
  port: 27017
"@
    
    # Ensure the directory exists before creating the file
    $configDir = Split-Path $configPath -Parent
    if (!(Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    
    $configContent | Out-File -FilePath $configPath -Encoding ASCII
    Write-Host "✅ Created MongoDB configuration file at $configPath" -ForegroundColor Green
    
    # Install MongoDB as a service using the configuration file
    $installServiceCmd = "& `"$mongoBin\mongod.exe`" --config `"$configPath`" --install"
    
    # Try to install the service
    Invoke-Expression $installServiceCmd
    Write-Host "✅ MongoDB configured as a Windows Service" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Failed to configure MongoDB service: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "You can still run MongoDB manually using: mongod --dbpath C:\data\db" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "4. Starting MongoDB Service..." -ForegroundColor Yellow

try {
    Start-Service -Name "MongoDB" -ErrorAction Stop
    Write-Host "✅ MongoDB service started successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Failed to start MongoDB service automatically" -ForegroundColor Yellow
    Write-Host "You can start it manually with: Start-Service -Name 'MongoDB'" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "5. Adding MongoDB to PATH..." -ForegroundColor Yellow

try {
    # Add MongoDB to system PATH
    $mongoPath = "C:\Program Files\MongoDB\Server\7.0\bin"
    $envPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
    
    if ($envPath -notlike "*$mongoPath*") {
        $newPath = $envPath + ";$mongoPath"
        [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
        Write-Host "✅ MongoDB added to system PATH" -ForegroundColor Green
        Write-Host "⚠️  You may need to restart your PowerShell session to use 'mongo' or 'mongod' commands" -ForegroundColor Yellow
    } else {
        Write-Host "✅ MongoDB is already in system PATH" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Failed to add MongoDB to PATH: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "You can manually add 'C:\Program Files\MongoDB\Server\7.0\bin' to your PATH" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "6. Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 MongoDB Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Cyan
Write-Host "  - Installation Directory: C:\Program Files\MongoDB\Server\7.0" -ForegroundColor Cyan
Write-Host "  - Data Directory: C:\data\db" -ForegroundColor Cyan
Write-Host "  - Log Directory: C:\data\log" -ForegroundColor Cyan
Write-Host "  - Configuration File: C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Restart your PowerShell/command prompt to use MongoDB commands" -ForegroundColor Yellow
Write-Host "2. Run '.\init-database.ps1' to seed the database with phone numbers" -ForegroundColor Yellow
Write-Host "3. Run '.\start-fullstack.ps1' to start the full application" -ForegroundColor Yellow
Write-Host ""
Write-Host "MongoDB Commands:" -ForegroundColor Cyan
Write-Host "  - Start service: Start-Service MongoDB" -ForegroundColor Cyan
Write-Host "  - Stop service: Stop-Service MongoDB" -ForegroundColor Cyan
Write-Host "  - Check status: Get-Service MongoDB" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
pause
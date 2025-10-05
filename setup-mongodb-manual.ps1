# Manual MongoDB Setup Script
# This script provides detailed instructions for manually setting up MongoDB

Write-Host "Manual MongoDB Community Edition Setup Instructions" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Overview" -ForegroundColor Yellow
Write-Host "--------" -ForegroundColor Yellow
Write-Host "This guide will help you manually install MongoDB Community Edition on Windows." -ForegroundColor Cyan
Write-Host "MongoDB will be installed as a Windows service for automatic startup." -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 1: Download MongoDB Community Edition" -ForegroundColor Yellow
Write-Host "------------------------------------------" -ForegroundColor Yellow
Write-Host "1. Go to: https://www.mongodb.com/try/download/community" -ForegroundColor Cyan
Write-Host "2. Select:" -ForegroundColor Cyan
Write-Host "   - Version: 7.0.4 (Recommended for stability)" -ForegroundColor Cyan
Write-Host "   - Platform: Windows x64" -ForegroundColor Cyan
Write-Host "   - Package: msi" -ForegroundColor Cyan
Write-Host "3. Click 'Download'" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 2: Install MongoDB" -ForegroundColor Yellow
Write-Host "----------------------" -ForegroundColor Yellow
Write-Host "1. Run the downloaded .msi file as Administrator" -ForegroundColor Cyan
Write-Host "2. When the installer starts, click 'Next'" -ForegroundColor Cyan
Write-Host "3. Read and accept the End-User License Agreement, then click 'Next'" -ForegroundColor Cyan
Write-Host "4. Choose 'Complete' setup type for all features, then click 'Next'" -ForegroundColor Cyan
Write-Host "5. Select 'Run service as Network Service user' (recommended)" -ForegroundColor Cyan
Write-Host "6. Note the data directory path (default: C:\Program Files\MongoDB\Server\7.0\data)" -ForegroundColor Cyan
Write-Host "7. Click 'Next' then 'Install'" -ForegroundColor Cyan
Write-Host "8. Click 'Finish' when installation completes" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 3: Verify Installation" -ForegroundColor Yellow
Write-Host "--------------------------" -ForegroundColor Yellow
Write-Host "1. Open a new Command Prompt or PowerShell window (as Administrator)" -ForegroundColor Cyan
Write-Host "2. Run: mongod --version" -ForegroundColor Cyan
Write-Host "   You should see version information" -ForegroundColor Cyan
Write-Host "3. Run: mongosh --version" -ForegroundColor Cyan
Write-Host "   You should see version information" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 4: Configure MongoDB Service (if not done during installation)" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host "1. Create data and log directories:" -ForegroundColor Cyan
Write-Host "   mkdir C:\data\db" -ForegroundColor Cyan
Write-Host "   mkdir C:\data\log" -ForegroundColor Cyan
Write-Host "2. Create a configuration file at C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg:" -ForegroundColor Cyan
Write-Host "   systemLog:" -ForegroundColor Cyan
Write-Host "     destination: file" -ForegroundColor Cyan
Write-Host "     path: C:\data\log\mongod.log" -ForegroundColor Cyan
Write-Host "   storage:" -ForegroundColor Cyan
Write-Host "     dbPath: C:\data\db" -ForegroundColor Cyan
Write-Host "   net:" -ForegroundColor Cyan
Write-Host "     bindIp: 127.0.0.1" -ForegroundColor Cyan
Write-Host "     port: 27017" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 5: Start MongoDB Service" -ForegroundColor Yellow
Write-Host "----------------------------" -ForegroundColor Yellow
Write-Host "Option A - If installed as service:" -ForegroundColor Cyan
Write-Host "1. Run: Start-Service MongoDB" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option B - Manual startup:" -ForegroundColor Cyan
Write-Host "1. Create data directory: mkdir C:\data\db" -ForegroundColor Cyan
Write-Host "2. Run: mongod --dbpath C:\data\db" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 6: Initialize Database" -ForegroundColor Yellow
Write-Host "--------------------------" -ForegroundColor Yellow
Write-Host "1. Once MongoDB is running, run: .\init-database.ps1" -ForegroundColor Cyan
Write-Host "   This will populate the database with phone numbers" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 7: Start the Full Application" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Yellow
Write-Host "1. Run: .\start-fullstack.ps1" -ForegroundColor Cyan
Write-Host "2. Access the application at: http://localhost:8080/" -ForegroundColor Cyan

Write-Host ""
Write-Host "Troubleshooting Tips:" -ForegroundColor Yellow
Write-Host "--------------------" -ForegroundColor Yellow
Write-Host "1. If you get 'command not found' errors:" -ForegroundColor Cyan
Write-Host "   - Add MongoDB to your PATH environment variable" -ForegroundColor Cyan
Write-Host "   - Default path: C:\Program Files\MongoDB\Server\7.0\bin" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. If MongoDB won't start:" -ForegroundColor Cyan
Write-Host "   - Check if port 27017 is already in use" -ForegroundColor Cyan
Write-Host "   - Ensure the data directory (C:\data\db) exists and has proper permissions" -ForegroundColor Cyan
Write-Host "   - Check Windows Event Viewer for service errors" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. If you get connection errors:" -ForegroundColor Cyan
Write-Host "   - Verify MongoDB is running: Get-Service MongoDB" -ForegroundColor Cyan
Write-Host "   - Check firewall settings if connecting remotely" -ForegroundColor Cyan
Write-Host "   - Ensure no antivirus is blocking MongoDB" -ForegroundColor Cyan

Write-Host ""
Write-Host "Useful MongoDB Commands:" -ForegroundColor Yellow
Write-Host "-----------------------" -ForegroundColor Yellow
Write-Host "  - Start service: Start-Service MongoDB" -ForegroundColor Cyan
Write-Host "  - Stop service: Stop-Service MongoDB" -ForegroundColor Cyan
Write-Host "  - Check status: Get-Service MongoDB" -ForegroundColor Cyan
Write-Host "  - Manual start: mongod --dbpath C:\data\db" -ForegroundColor Cyan
Write-Host "  - Connect to shell: mongosh" -ForegroundColor Cyan

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
pause
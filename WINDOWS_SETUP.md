# Windows Setup Guide

## Prerequisites Installation

### 1. Install PHP
```powershell
# Download PHP 8.x from https://windows.php.net/download/
# Extract to C:\php
# Add C:\php to System PATH

# Or use Chocolatey
choco install php
```

### 2. Install Composer
```powershell
# Download from https://getcomposer.org/Composer-Setup.exe
# Run installer (will auto-detect PHP)
```

### 3. Install MongoDB
```powershell
# Download from https://www.mongodb.com/try/download/community
# Install as Windows Service
# Or use Chocolatey
choco install mongodb
```

### 4. Install Dependencies
```powershell
composer install
```

## Quick Start

### Start MongoDB
```powershell
net start MongoDB
```

### Start Web Server
```powershell
php -S localhost:80 -t N:\sms
```

### Start Queue Worker (separate terminal)
```powershell
php N:\sms\queue_worker.php
```

## Testing API

### Get Token
```powershell
Invoke-WebRequest -Uri http://localhost/api/auth/login -Method POST -Body '{"username":"admin","password":"telecom2025"}' -ContentType "application/json"
```

### Send SMS
```powershell
$token = "YOUR_TOKEN_HERE"
Invoke-WebRequest -Uri http://localhost/api/sms/send -Method POST -Headers @{Authorization="Bearer $token"} -Body '{"to":"+1234567890","from":"+0987654321","message":"Test"}' -ContentType "application/json"
```

## Troubleshooting

- **PHP not found**: Add `C:\php` to PATH, restart PowerShell
- **MongoDB not running**: Run `net start MongoDB` as Administrator
- **Port 80 in use**: Use different port `php -S localhost:8080`

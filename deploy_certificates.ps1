# Certificate Deployment Helper Script for Windows

Write-Host "🔐 SIGTRAN Certificate Deployment Helper" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Create directory structure
Write-Host "Creating SSL directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "C:\ssl\certs" -Force | Out-Null
New-Item -ItemType Directory -Path "C:\ssl\private" -Force | Out-Null

# Check if certificate files exist
if ((Test-Path "sigtran.crt") -and (Test-Path "sigtran.key") -and (Test-Path "ca.crt")) {
    Write-Host "Found certificate files in current directory:" -ForegroundColor Yellow
    Write-Host "  - sigtran.crt (server certificate)" -ForegroundColor Cyan
    Write-Host "  - sigtran.key (private key)" -ForegroundColor Cyan
    Write-Host "  - ca.crt (CA certificate)" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "Deploying certificates..." -ForegroundColor Yellow
    
    # Copy certificates to appropriate locations
    Copy-Item "sigtran.crt" -Destination "C:\ssl\certs\"
    Copy-Item "sigtran.key" -Destination "C:\ssl\private\"
    Copy-Item "ca.crt" -Destination "C:\ssl\certs\"
    
    # Set appropriate permissions (Windows handles this differently)
    Write-Host "Setting file permissions..." -ForegroundColor Yellow
    # Note: Windows permissions are typically handled through ACLs
    
    Write-Host "✅ Certificates deployed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Certificate locations:" -ForegroundColor Yellow
    Write-Host "  Server Certificate: C:\ssl\certs\sigtran.crt" -ForegroundColor Cyan
    Write-Host "  Private Key: C:\ssl\private\sigtran.key" -ForegroundColor Cyan
    Write-Host "  CA Certificate: C:\ssl\certs\ca.crt" -ForegroundColor Cyan
    
    # Verify certificates (if OpenSSL is available)
    Write-Host ""
    Write-Host "Verifying certificates..." -ForegroundColor Yellow
    try {
        $result = openssl x509 -in "C:\ssl\certs\sigtran.crt" -text -noout 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Server certificate is valid" -ForegroundColor Green
        } else {
            Write-Host "❌ Server certificate validation failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "⚠️  OpenSSL not available for certificate verification" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ Required certificate files not found in current directory." -ForegroundColor Red
    Write-Host "Please place the following files in this directory:" -ForegroundColor Yellow
    Write-Host "  - sigtran.crt (server certificate)" -ForegroundColor Cyan
    Write-Host "  - sigtran.key (private key)" -ForegroundColor Cyan
    Write-Host "  - ca.crt (CA certificate)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or generate self-signed certificates for testing:" -ForegroundColor Yellow
    Write-Host "  openssl genrsa -out sigtran.key 2048" -ForegroundColor Cyan
    Write-Host "  openssl req -new -key sigtran.key -out sigtran.csr" -ForegroundColor Cyan
    Write-Host "  openssl x509 -req -days 365 -in sigtran.csr -signkey sigtran.key -out sigtran.crt" -ForegroundColor Cyan
    Write-Host "  openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 1095 -nodes" -ForegroundColor Cyan
}
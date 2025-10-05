# Production Startup Script for Real Telephone Numbers and SS7 with SIGTRAN

Write-Host "🚀 Starting Telecom System with Real SS7 Connectivity" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green

# Set environment variables for production deployment
$env:SS7_SIGTRAN = "true"
$env:SS7_PRIVATE_NETWORK = "false"

Write-Host "Environment Variables Set:" -ForegroundColor Yellow
Write-Host "  SS7_SIGTRAN=$env:SS7_SIGTRAN" -ForegroundColor Cyan
Write-Host "  SS7_PRIVATE_NETWORK=$env:SS7_PRIVATE_NETWORK" -ForegroundColor Cyan
Write-Host ""

# Verify SSL/TLS certificates exist
Write-Host "Verifying SSL/TLS Certificates..." -ForegroundColor Yellow
if ((Test-Path "C:\ssl\certs\sigtran.crt") -and (Test-Path "C:\ssl\private\sigtran.key") -and (Test-Path "C:\ssl\certs\ca.crt")) {
    Write-Host "✅ SSL/TLS certificates found" -ForegroundColor Green
} else {
    Write-Host "⚠️  SSL/TLS certificates not found" -ForegroundColor Yellow
    Write-Host "   Please deploy certificates to:" -ForegroundColor Cyan
    Write-Host "   - C:\ssl\certs\sigtran.crt (server certificate)" -ForegroundColor Cyan
    Write-Host "   - C:\ssl\private\sigtran.key (private key)" -ForegroundColor Cyan
    Write-Host "   - C:\ssl\certs\ca.crt (CA certificate)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Continuing without SSL/TLS (NOT RECOMMENDED FOR PRODUCTION)" -ForegroundColor Red
}

# Verify SIGTRAN configuration
Write-Host ""
Write-Host "Verifying SIGTRAN Configuration..." -ForegroundColor Yellow
try {
    python -c "import sigtran_config; print('✅ SIGTRAN configuration loaded successfully')"
    Write-Host "SIGTRAN configuration verified" -ForegroundColor Green
} catch {
    Write-Host "❌ SIGTRAN configuration error" -ForegroundColor Red
    Write-Host "Please update sigtran_config.py with carrier information" -ForegroundColor Yellow
    exit 1
}

# Start the main application
Write-Host ""
Write-Host "Starting main application..." -ForegroundColor Yellow
python main.py
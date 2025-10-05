# SIGTRAN Production Startup Script for Windows

Write-Host "🚀 Starting Telecom System with SIGTRAN Production Configuration"
Write-Host "============================================================="

# Set environment variables for production SIGTRAN deployment
$env:SS7_SIGTRAN = "true"
$env:SS7_PRIVATE_NETWORK = "false"

Write-Host "Environment Variables:"
Write-Host "  SS7_SIGTRAN=$env:SS7_SIGTRAN"
Write-Host "  SS7_PRIVATE_NETWORK=$env:SS7_PRIVATE_NETWORK"
Write-Host ""

# Confirm SIGTRAN configuration
Write-Host "SIGTRAN Configuration:"
Write-Host "  Mode: Production SS7 over IP"
Write-Host "  Protocols: M3UA, SUA, M2PA, TCAP over IP"
Write-Host "  Security: TLS Encryption, Authentication, IP Whitelisting"
Write-Host "  Endpoints:"
Write-Host "    - STP1: 192.168.1.10:2905 (M3UA)"
Write-Host "    - MSC1: 192.168.1.30:2905 (M3UA)"
Write-Host ""

# Start the main application
Write-Host "Starting main application..."
python main.py
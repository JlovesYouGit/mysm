# Self-Contained Telecommunications Provider Setup
# This script configures the system to work as an independent provider
# without relying on external carriers.

Write-Host "🔧 Setting up Self-Contained Telecommunications Provider" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green

# 1. Configure for private network mode in start-fullstack.ps1
Write-Host "Updating start-fullstack.ps1 for independent provider mode..." -ForegroundColor Yellow

# Read the content of start-fullstack.ps1
$content = Get-Content -Path "start-fullstack.ps1" -Raw

# Replace the SS7 configuration lines
$content = $content -replace '\$env:SS7_SIGTRAN = "true"', '$env:SS7_SIGTRAN = "false"'
$content = $content -replace '\$env:SS7_PRIVATE_NETWORK = "false"', '$env:SS7_PRIVATE_NETWORK = "true"'

# Add provider mode
$content = $content -replace '\$env:SS7_PRIVATE_NETWORK = "true"', '$env:SS7_PRIVATE_NETWORK = "true"`n$env:PROVIDER_MODE = "independent"'

# Save the updated content
Set-Content -Path "start-fullstack.ps1" -Value $content

Write-Host "✅ Environment configured for independent provider mode" -ForegroundColor Green

# 2. Create local numbering plan
Write-Host "Creating local numbering plan..." -ForegroundColor Yellow

$numberingPlan = @{
    country_code = "+1"
    area_code = "555"
    prefix = "100"
    range_start = 1000
    range_end = 1999
    allocated_numbers = @()
}

# Generate test numbers
$testNumbers = @()
for ($i = 0; $i -lt 10; $i++) {
    $number = "+1555100$('{0:D4}' -f ($i + 1000))"
    $type = if ($i -lt 5) { "test" } else { "internal" }
    $testNumbers += @{
        number = $number
        status = "available"
        allocated_to = $null
        type = $type
    }
}

$numberingPlan.allocated_numbers = $testNumbers

# Save numbering plan
$numberingPlan | ConvertTo-Json -Depth 10 | Out-File -FilePath "local_numbering_plan.json" -Encoding UTF8

Write-Host "✅ Local numbering plan created" -ForegroundColor Green
Write-Host "   Generated $($testNumbers.Count) test numbers" -ForegroundColor Cyan

# 3. Create local routing configuration
Write-Host "Creating local routing configuration..." -ForegroundColor Yellow

$routingConfig = @{
    network_type = "private"
    routing_mode = "local"
    local_gateway = @{
        ip = "127.0.0.1"
        port = 8085
        protocol = "UDP"
    }
    message_store = @{
        type = "local"
        path = "./messages"
    }
    authentication = @{
        required = $false
        method = "none"
    }
}

# Save routing configuration
$routingConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath "local_routing_config.json" -Encoding UTF8

Write-Host "✅ Local routing configuration created" -ForegroundColor Green

# 4. Create system configuration
Write-Host "Creating provider configuration..." -ForegroundColor Yellow

$systemConfig = @{
    provider = @{
        name = "Self-Contained Telecom Provider"
        mode = "independent"
        network_type = "private"
        timestamp = (Get-Date).ToString("o")
    }
    capabilities = @{
        sms = $true
        voice = $true
        data = $true
        mms = $false
    }
    endpoints = @{
        sms = "http://localhost:8083/api/sms"
        voice = "http://localhost:8083/api/voice"
        admin = "http://localhost:8083/api"
    }
}

# Save system configuration
$systemConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath "provider_config.json" -Encoding UTF8

Write-Host "✅ Provider configuration created" -ForegroundColor Green

# 5. Create test devices
Write-Host "Creating test devices..." -ForegroundColor Yellow

$testDevices = @(
    @{
        id = "device_001"
        number = "+15551001001"
        type = "simulator"
        status = "active"
    },
    @{
        id = "device_002"
        number = "+15551001002"
        type = "simulator"
        status = "active"
    },
    @{
        id = "web_client"
        number = "+15551001003"
        type = "web"
        status = "active"
    }
)

# Save test devices
$testDevices | ConvertTo-Json -Depth 10 | Out-File -FilePath "test_devices.json" -Encoding UTF8

Write-Host "✅ Test devices created" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Provider Setup Complete!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "Your system is now configured as an independent provider." -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Restart your services with start-fullstack.ps1" -ForegroundColor White
Write-Host "   2. Use the web interface to send/receive messages" -ForegroundColor White
Write-Host "   3. Test with the local numbers: +15551001001 to +15551001010" -ForegroundColor White
Write-Host "   4. Add real devices by updating test_devices.json" -ForegroundColor White
Write-Host ""
Write-Host "📱 Available Test Numbers:" -ForegroundColor Yellow
for ($i = 0; $i -lt $testDevices.Count; $i++) {
    $device = $testDevices[$i]
    Write-Host "   $($i+1). $($device.number) ($($device.type))" -ForegroundColor White
}
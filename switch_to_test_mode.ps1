# Switch to Private Network Mode for Testing
# This script updates the start-fullstack.ps1 to use private network simulation

Write-Host "🔄 Switching to Private Network Simulation Mode..." -ForegroundColor Yellow

# Check if start-fullstack.ps1 exists
if (-not (Test-Path "start-fullstack.ps1")) {
    Write-Host "❌ start-fullstack.ps1 not found!" -ForegroundColor Red
    exit 1
}

# Read the content
$content = Get-Content -Path "start-fullstack.ps1" -Raw

# Replace the SS7 configuration lines
$content = $content -replace '\$env:SS7_SIGTRAN = "true"', '$env:SS7_SIGTRAN = "false"'
$content = $content -replace '\$env:SS7_PRIVATE_NETWORK = "false"', '$env:SS7_PRIVATE_NETWORK = "true"'

# Save the updated content
Set-Content -Path "start-fullstack.ps1" -Value $content

Write-Host "✅ Configuration updated successfully!" -ForegroundColor Green
Write-Host "   SS7_SIGTRAN = false" -ForegroundColor Cyan
Write-Host "   SS7_PRIVATE_NETWORK = true" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now you can restart your services with start-fullstack.ps1" -ForegroundColor Yellow
Write-Host "This will enable private network simulation mode for testing" -ForegroundColor Yellow
# Switch to Private Network Mode for Testing

This script will modify your configuration to use private network simulation mode instead of SIGTRAN mode, which will allow you to test SMS functionality without requiring real carrier connectivity.

## Instructions:

1. Close all PowerShell windows running the telecom services
2. Run this script
3. Start your services again with `start-fullstack.ps1`

```powershell
# Update the environment variables in start-fullstack.ps1
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
```

Save this as `switch_to_test_mode.ps1` and run it to switch your configuration for testing purposes.
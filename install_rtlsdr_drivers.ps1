# RTL-SDR Driver Installation Script for Windows
# This script helps install the necessary drivers for RTL-SDR dongles

Write-Host "RTL-SDR Driver Installation Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results." -ForegroundColor Yellow
    Write-Host "Some operations may fail without administrator privileges." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Step 1: Checking for RTL-SDR Dongle..." -ForegroundColor Yellow

# Check if RTL-SDR is connected
try {
    $usbDevices = Get-PnpDevice | Where-Object {$_.Class -eq "USB" -and $_.Name -like "*RTL*"}
    if ($usbDevices) {
        Write-Host "✅ RTL-SDR dongle detected:" -ForegroundColor Green
        $usbDevices | ForEach-Object {
            Write-Host "   - $($_.Name)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "⚠️  No RTL-SDR dongle detected. Please connect your RTL-SDR device and run this script again." -ForegroundColor Yellow
        Write-Host "   If you have connected the device, you may need to install the driver manually." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Unable to check for RTL-SDR device: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Installing RTL-SDR Driver..." -ForegroundColor Yellow

# Download and install RTL-SDR driver (updated to latest RTL-SDR Blog drivers)
$driverUrl = "https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest/download/Release.zip"
$downloadPath = "$env:TEMP\rtl-sdr.zip"
$extractPath = "$env:TEMP\rtl-sdr"

try {
    Write-Host "Downloading RTL-SDR driver from $driverUrl..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $driverUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "✅ Download completed" -ForegroundColor Green
    
    # Extract the driver
    Write-Host "Extracting driver files..." -ForegroundColor Cyan
    if (Test-Path $extractPath) {
        Remove-Item -Path $extractPath -Recurse -Force
    }
    Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force
    Write-Host "✅ Driver files extracted to $extractPath" -ForegroundColor Green
    
    # Add driver path to system PATH
    $driverBinPath = "$extractPath\rtl-sdr-release-x64"
    # Check if the specific directory exists, if not use the root extract path
    if (-not (Test-Path $driverBinPath)) {
        $driverBinPath = $extractPath
    }
    
    $envPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
    
    if ($envPath -notlike "*$driverBinPath*") {
        Write-Host "Adding RTL-SDR to system PATH..." -ForegroundColor Cyan
        $newPath = $envPath + ";$driverBinPath"
        [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
        Write-Host "✅ RTL-SDR added to system PATH" -ForegroundColor Green
    } else {
        Write-Host "✅ RTL-SDR is already in system PATH" -ForegroundColor Green
    }
    
    Write-Host "✅ RTL-SDR driver installation completed" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Failed to download/install RTL-SDR driver: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "You can manually download the driver from: https://github.com/rtlsdrblog/rtl-sdr-blog/releases" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Step 3: Installing Zadig for USB Driver Management..." -ForegroundColor Yellow

# Download Zadig for USB driver management (updated URL)
$zadigUrl = "https://zadig.akeo.ie/downloads/zadig-2.9.exe"
$zadigPath = "$env:TEMP\zadig.exe"

try {
    Write-Host "Downloading Zadig from $zadigUrl..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $zadigUrl -OutFile $zadigPath -UseBasicParsing
    Write-Host "✅ Zadig downloaded to $zadigPath" -ForegroundColor Green
    Write-Host "💡 You can run Zadig to install the WinUSB driver for your RTL-SDR device" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to download Zadig: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "You can manually download Zadig from: https://zadig.akeo.ie/" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host "1. RTL-SDR driver files downloaded and extracted" -ForegroundColor Cyan
Write-Host "2. Driver path added to system PATH" -ForegroundColor Cyan
Write-Host "3. Zadig downloaded for USB driver management" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "===========" -ForegroundColor Yellow
Write-Host "1. Connect your RTL-SDR dongle to your computer" -ForegroundColor Cyan
Write-Host "2. Run Zadig as Administrator" -ForegroundColor Cyan
Write-Host "3. Select your RTL-SDR device from the dropdown" -ForegroundColor Cyan
Write-Host "4. Choose 'WinUSB' as the driver" -ForegroundColor Cyan
Write-Host "5. Click 'Install Driver'" -ForegroundColor Cyan
Write-Host "6. Restart your computer" -ForegroundColor Cyan
Write-Host "7. Test the RTL-SDR with: rtl_test -t" -ForegroundColor Cyan
Write-Host ""
Write-Host "Testing RTL-SDR:" -ForegroundColor Yellow
Write-Host "===============" -ForegroundColor Yellow
Write-Host "After installation, open a new command prompt and run:" -ForegroundColor Cyan
Write-Host "   rtl_test -t" -ForegroundColor Cyan
Write-Host "This should show information about your RTL-SDR device." -ForegroundColor Cyan
Write-Host ""
Write-Host "Alternative Installation:" -ForegroundColor Yellow
Write-Host "=======================" -ForegroundColor Yellow
Write-Host "You can also install RTL-SDR support using conda:" -ForegroundColor Cyan
Write-Host "   conda install -c conda-forge rtl-sdr" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or using vcpkg on Windows:" -ForegroundColor Cyan
Write-Host "   vcpkg install rtl-sdr" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
pause
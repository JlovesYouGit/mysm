# Easy RTL-SDR Installation Script for Windows (Zero-Driver Alternative)
# This script installs RTL-SDR with the new librtlsdr that ships its own WinUSB driver

Write-Host "Easy RTL-SDR Installation Script" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results." -ForegroundColor Yellow
    Write-Host "Some operations may fail without administrator privileges." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Step 1: Downloading RTL-SDR Blog Nightly Build..." -ForegroundColor Yellow

# Download RTL-SDR Blog nightly build (zero-driver alternative)
$driverUrl = "https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest/download/Release.zip"
$downloadPath = "$env:TEMP\rtl-sdr-blog.zip"
$extractPath = "$env:TEMP\rtl-sdr-blog"

try {
    Write-Host "Downloading RTL-SDR Blog from $driverUrl..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $driverUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "✅ Download completed" -ForegroundColor Green
    
    # Extract the driver
    Write-Host "Extracting files..." -ForegroundColor Cyan
    if (Test-Path $extractPath) {
        Remove-Item -Path $extractPath -Recurse -Force
    }
    Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force
    Write-Host "✅ Files extracted to $extractPath" -ForegroundColor Green
    
    # Look for the executable that auto-installs WinUSB driver
    Write-Host "Looking for executable to auto-install WinUSB driver..." -ForegroundColor Cyan
    $exeFiles = Get-ChildItem -Path $extractPath -Recurse -Filter "*.exe" -ErrorAction SilentlyContinue
    
    if ($exeFiles.Count -gt 0) {
        Write-Host "Found executables:" -ForegroundColor Cyan
        $exeFiles | ForEach-Object {
            Write-Host "   - $($_.Name) at $($_.FullName)" -ForegroundColor Cyan
        }
        
        # Try to find rtl-sdr-blog.exe or similar
        $rtlSdrExe = $exeFiles | Where-Object {$_.Name -like "*rtl*sdr*blog*.exe"} | Select-Object -First 1
        if (-not $rtlSdrExe) {
            $rtlSdrExe = $exeFiles | Where-Object {$_.Name -like "*rtl*sdr*.exe"} | Select-Object -First 1
        }
        if (-not $rtlSdrExe) {
            $rtlSdrExe = $exeFiles | Select-Object -First 1
        }
        
        if ($rtlSdrExe) {
            Write-Host "Running $($rtlSdrExe.Name) to auto-install WinUSB driver..." -ForegroundColor Cyan
            # Run the executable to auto-install the driver
            Start-Process -FilePath $rtlSdrExe.FullName -Wait
            Write-Host "✅ WinUSB driver auto-installed" -ForegroundColor Green
        } else {
            Write-Host "⚠️  No suitable executable found. You may need to install the driver manually." -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  No executables found. You may need to install the driver manually." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Failed to download/install RTL-SDR Blog: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "You can manually download from: https://github.com/rtlsdrblog/rtl-sdr-blog/releases" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Step 2: Installing Python RTL-SDR Library..." -ForegroundColor Yellow

try {
    Write-Host "Installing pyrtlsdr Python package (correct package name)..." -ForegroundColor Cyan
    pip install pyrtlsdr
    Write-Host "✅ pyrtlsdr installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install pyrtlsdr: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Try running: pip install pyrtlsdr" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host "1. RTL-SDR Blog downloaded and extracted" -ForegroundColor Cyan
Write-Host "2. WinUSB driver auto-installed (no Zadig needed)" -ForegroundColor Cyan
Write-Host "3. pyrtlsdr Python package installed" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "===========" -ForegroundColor Yellow
Write-Host "1. Connect your RTL-SDR dongle to your computer" -ForegroundColor Cyan
Write-Host "2. Restart your computer" -ForegroundColor Cyan
Write-Host "3. Test the RTL-SDR with the test script: python test_rtlsdr.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage in Python code:" -ForegroundColor Yellow
Write-Host "===================" -ForegroundColor Yellow
Write-Host "from rtlsdr import RtlSdr" -ForegroundColor Cyan
Write-Host "sdr = RtlSdr()" -ForegroundColor Cyan
Write-Host "sdr.sample_rate = 2.048e6" -ForegroundColor Cyan
Write-Host "sdr.center_freq = 100e6" -ForegroundColor Cyan
Write-Host "samples = sdr.read_samples(256*1024)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
pause
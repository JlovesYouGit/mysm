#!/usr/bin/env python3
"""
Hardware Setup Script for RTL-SDR and Telecom System
This script helps set up the necessary hardware components for real-world functionality.
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def check_rtlsdr_library():
    """Check if RTL-SDR library is available."""
    print("Checking RTL-SDR library availability...")
    
    try:
        from rtlsdr import RtlSdr
        print("✅ RTL-SDR Python library found")
        
        # Try to create an SDR instance
        try:
            sdr = RtlSdr()
            print("✅ RTL-SDR device accessible")
            sdr.close()
            return True
        except Exception as e:
            print(f"⚠️  RTL-SDR device not found: {e}")
            print("   This is expected if no RTL-SDR hardware is connected")
            return False
            
    except ImportError as e:
        print(f"❌ RTL-SDR library not available: {e}")
        return False

def download_rtlsdr_windows():
    """Download and extract RTL-SDR drivers for Windows."""
    print("Setting up RTL-SDR for Windows...")
    
    # URLs for Windows RTL-SDR drivers (updated to latest)
    driver_url = "https://github.com/rtlsdrblog/rtl-sdr-blog/releases/latest/download/Release.zip"
    
    temp_dir = Path.home() / "temp_rtlsdr"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        print(f"Downloading from {driver_url}...")
        zip_path = temp_dir / "rtl-sdr.zip"
        urllib.request.urlretrieve(driver_url, zip_path)
        
        # Extract
        print("Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir / "rtl-sdr")
        
        print("✅ RTL-SDR drivers downloaded and extracted")
        
        # Try to copy DLLs to system directory or Python directory
        rtl_sdr_dir = temp_dir / "rtl-sdr" / "x64"  # Use x64 directory
        if not rtl_sdr_dir.exists():
            # Try without x64 subdirectory
            rtl_sdr_dir = temp_dir / "rtl-sdr"
            
        if rtl_sdr_dir.exists():
            # Copy DLLs to Python directory
            python_dir = Path(sys.executable).parent
            dll_files = list(rtl_sdr_dir.glob("*.dll"))
            
            if not dll_files:
                # Try with full path glob
                dll_files = list((rtl_sdr_dir / "x64").glob("*.dll"))
                if not dll_files:
                    dll_files = list(rtl_sdr_dir.glob("**/*.dll"))
            
            for dll in dll_files:
                dest = python_dir / dll.name
                try:
                    shutil.copy2(dll, dest)
                    print(f"✅ Copied {dll.name} to {dest}")
                except Exception as e:
                    print(f"❌ Failed to copy {dll.name}: {e}")
            
            if dll_files:
                return True
            else:
                print("❌ No DLL files found in extracted directory")
        else:
            print("❌ Could not find extracted RTL-SDR directory")
            
    except Exception as e:
        print(f"❌ Failed to download RTL-SDR drivers: {e}")
        print("   Please check your internet connection and try again")
    
    return False

def download_zadig():
    """Download Zadig for USB driver management."""
    print("Downloading Zadig...")
    
    # Updated Zadig download URL (try multiple options)
    zadig_urls = [
        "https://github.com/pbatard/libwdi/releases/latest/download/zadig-2.9.exe",
        "https://zadig.akeo.ie/downloads/zadig-2.9.exe",
        "https://github.com/pbatard/libwdi/releases/download/v1.5.1/zadig-2.9.exe"
    ]
    
    temp_dir = Path.home() / "temp_rtlsdr"
    zadig_path = temp_dir / "zadig.exe"
    
    for url in zadig_urls:
        try:
            print(f"Downloading Zadig from {url}...")
            urllib.request.urlretrieve(url, zadig_path)
            print(f"✅ Zadig downloaded to {zadig_path}")
            print("💡 You can run Zadig to install the WinUSB driver for your RTL-SDR device")
            return True
        except Exception as e:
            print(f"❌ Failed to download Zadig from {url}: {e}")
    
    print("You can manually download Zadig from: https://zadig.akeo.ie/")
    return False

def install_zadig():
    """Provide instructions for installing Zadig."""
    print("\nZadig Installation Instructions:")
    print("=" * 40)
    print("1. Download Zadig from: https://zadig.akeo.ie/")
    print("2. Run Zadig as Administrator")
    print("3. Connect your RTL-SDR device to your computer")
    print("4. In Zadig, select your RTL-SDR device from the dropdown")
    print("5. Choose 'WinUSB' as the driver")
    print("6. Click 'Install Driver'")
    print("7. Restart your computer")

def setup_wifi_scanning():
    """Setup WiFi scanning capabilities."""
    print("\nSetting up WiFi scanning...")
    
    os_name = platform.system().lower()
    
    if os_name == "windows":
        print("✅ Windows WiFi scanning uses built-in 'netsh wlan' commands")
        # Test WiFi scanning
        try:
            result = subprocess.run(["netsh", "wlan", "show", "networks"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Windows WiFi scanning available")
                return True
            else:
                print("❌ Windows WiFi scanning not available")
                return False
        except Exception as e:
            print(f"❌ Failed to test WiFi scanning: {e}")
            return False
            
    elif os_name == "linux":
        print("✅ Linux WiFi scanning uses 'nmcli' commands")
        try:
            result = subprocess.run(["nmcli", "-t", "-f", "SSID,BSSID,SIGNAL,CHAN,SECURITY", "device", "wifi", "list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Linux WiFi scanning available")
                return True
            else:
                print("❌ Linux WiFi scanning not available")
                return False
        except Exception as e:
            print(f"❌ Failed to test WiFi scanning: {e}")
            return False
            
    elif os_name == "darwin":  # macOS
        print("✅ macOS WiFi scanning uses 'airport' commands")
        try:
            result = subprocess.run(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ macOS WiFi scanning available")
                return True
            else:
                print("❌ macOS WiFi scanning not available")
                return False
        except Exception as e:
            print(f"❌ Failed to test WiFi scanning: {e}")
            return False
    else:
        print(f"❌ Unsupported OS: {os_name}")
        return False

def test_hardware():
    """Test all hardware components."""
    print("\nTesting Hardware Components...")
    print("=" * 40)
    
    # Test RTL-SDR
    rtlsdr_ok = check_rtlsdr_library()
    
    # Test WiFi scanning
    wifi_ok = setup_wifi_scanning()
    
    print("\nHardware Test Summary:")
    print("=" * 30)
    print(f"RTL-SDR: {'✅ Available' if rtlsdr_ok else '❌ Not available'}")
    print(f"WiFi Scanning: {'✅ Available' if wifi_ok else '❌ Not available'}")
    
    if rtlsdr_ok or wifi_ok:
        print("\n🎉 Hardware setup completed!")
        print("You can now use real hardware for spectrum analysis.")
    else:
        print("\n⚠️  No hardware detected.")
        print("Please connect RTL-SDR device or ensure WiFi scanning is available.")

def main():
    """Main setup function."""
    print("Telecom System Hardware Setup")
    print("=" * 40)
    print("This script will help you set up hardware for real-world functionality.")
    print()
    
    os_name = platform.system().lower()
    print(f"Detected OS: {os_name}")
    
    if os_name == "windows":
        print("\nWindows Setup:")
        print("1. Downloading RTL-SDR drivers...")
        download_rtlsdr_windows()
        print("2. Downloading Zadig for USB driver management...")
        download_zadig()
    
    # Test hardware components
    test_hardware()
    
    print("\nNext Steps:")
    print("1. Connect your RTL-SDR device")
    print("2. Install drivers using Zadig if needed")
    print("3. Restart your computer")
    print("4. Run this script again to verify setup")
    print("\nFor detailed instructions, visit:")
    print("https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/")

if __name__ == "__main__":
    main()
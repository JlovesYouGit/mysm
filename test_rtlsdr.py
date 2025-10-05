import sys
import time
import os

# Add the spectrum analyzer path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'spectrum_analyzer', 'intern'))

# Now we can import the modules
try:
    from spectrum_grabber.cellular_scanner import (
        scan_cellular_cross_platform, 
        get_common_cellular_frequencies,
        CellularScanError
    )
except ImportError as e:
    print(f"Failed to import spectrum grabber: {e}")
    # Try alternative import paths
    try:
        from spectrum_analyzer.intern.spectrum_grabber.cellular_scanner import (
            scan_cellular_cross_platform, 
            get_common_cellular_frequencies,
            CellularScanError
        )
    except ImportError:
        print("Could not import cellular scanner module")
        scan_cellular_cross_platform = None
        get_common_cellular_frequencies = None
        CellularScanError = Exception

def test_rtlsdr_connection():
    """Test RTL-SDR connection and basic functionality."""
    print("Testing RTL-SDR Connection...")
    print("=" * 40)
    
    try:
        # Import RTL-SDR library
        from rtlsdr import RtlSdr
        print("✅ RTL-SDR library imported successfully")
        
        # Try to connect to RTL-SDR device
        try:
            sdr = RtlSdr()
            print("✅ RTL-SDR device connected")
            
            # Get device info
            print(f"   Device name: {sdr.get_device_name(sdr.device_index)}")
            print(f"   Manufacturer: {sdr.get_device_manufacturer(sdr.device_index)}")
            print(f"   Product: {sdr.get_device_product(sdr.device_index)}")
            
            # Test basic settings
            sdr.sample_rate = 2.048e6
            sdr.center_freq = 100e6
            sdr.gain = 'auto'
            
            print("✅ Basic SDR settings configured")
            
            # Close device
            sdr.close()
            print("✅ RTL-SDR device closed properly")
            
        except Exception as e:
            print(f"⚠️  RTL-SDR device connection failed: {e}")
            print("   This is expected if no RTL-SDR device is connected")
            return False
            
    except ImportError as e:
        print(f"❌ RTL-SDR library not available: {e}")
        print("   Please install RTL-SDR drivers and libraries")
        return False
    
    return True

def test_cellular_scanning():
    """Test cellular scanning functionality."""
    print("\nTesting Cellular Scanning...")
    print("=" * 40)
    
    if get_common_cellular_frequencies is None:
        print("❌ Cellular scanning module not available")
        return False
    
    # Get common cellular frequencies
    freq_dict = get_common_cellular_frequencies()
    print("Available cellular frequency bands:")
    for band, freqs in freq_dict.items():
        print(f"   {band}: {freqs}")
    
    # Test with a few frequencies
    test_frequencies = [900, 1800, 2100]  # Common cellular bands in MHz
    
    if scan_cellular_cross_platform is None:
        print("❌ Cellular scanning function not available")
        return False
    
    try:
        print(f"\nScanning {len(test_frequencies)} frequencies...")
        signals = scan_cellular_cross_platform(
            frequencies_mhz=test_frequencies,
            sdr_type='rtlsdr',
            sample_rate=1.024e6,  # Lower sample rate for testing
            num_samples=1024*100,  # Fewer samples for faster testing
            dwell_time=0.5
        )
        
        print(f"✅ Scan completed, found {len(signals)} signals")
        for signal in signals:
            print(f"   {signal.frequency_mhz} MHz: {signal.signal_strength_dbm:.1f} dBm")
            
    except CellularScanError as e:
        print(f"⚠️  Cellular scanning failed: {e}")
        print("   This is expected if no RTL-SDR device is connected or properly configured")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during scanning: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("RTL-SDR and Cellular Scanning Test")
    print("==================================")
    
    # Test RTL-SDR connection
    rtlsdr_ok = test_rtlsdr_connection()
    
    # Test cellular scanning
    scanning_ok = test_cellular_scanning()
    
    print("\n" + "=" * 40)
    if rtlsdr_ok and scanning_ok:
        print("🎉 All tests passed! RTL-SDR is ready for use.")
    elif rtlsdr_ok:
        print("⚠️  RTL-SDR connected but scanning failed.")
        print("   This may be due to no signals detected or configuration issues.")
    else:
        print("❌ RTL-SDR not available.")
        print("   Please:")
        print("   1. Connect your RTL-SDR device")
        print("   2. Install drivers using install_rtlsdr_drivers.ps1")
        print("   3. Run rtl_test -t to verify device functionality")

if __name__ == "__main__":
    main()
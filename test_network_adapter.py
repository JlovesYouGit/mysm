"""
Test script to verify the system works with NETGEAR A6210 WiFi USB3.0 Adapter
instead of RTL-SDR.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Fix the import path
sys.path.append(os.path.join(os.path.dirname(__file__), 'spectrum_analyzer', 'intern'))
from spectrum_grabber.cellular_scanner import scan_cellular_cross_platform, CellularScanError

async def test_network_adapter_detection():
    """Test that the NETGEAR A6210 WiFi USB3.0 Adapter is properly detected."""
    print("Testing NETGEAR A6210 WiFi USB3.0 Adapter detection...")
    
    try:
        # Test adapter detection
        signals = scan_cellular_cross_platform(
            frequencies_mhz=[850, 1900],  # Test frequencies
            sdr_type='network_adapter',
            sample_rate=2.048e6,
            gain='auto',
            num_samples=1024*100,  # Smaller sample size for testing
            dwell_time=0.1
        )
        
        print(f"✅ NETGEAR A6210 WiFi USB3.0 Adapter detected successfully")
        print(f"✅ Captured {len(signals)} test signals")
        
        return True
        
    except CellularScanError as e:
        print(f"❌ NETGEAR A6210 WiFi USB3.0 Adapter detection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during adapter detection: {e}")
        return False

async def test_signal_capture():
    """Test signal capture functionality with NETGEAR A6210 WiFi USB3.0 Adapter."""
    print("\nTesting signal capture with NETGEAR A6210 WiFi USB3.0 Adapter...")
    
    try:
        # Test capturing signals on multiple frequencies
        frequencies = [850, 900, 1800, 1900, 2100]  # Common cellular frequencies
        signals = scan_cellular_cross_platform(
            frequencies_mhz=frequencies,
            sdr_type='network_adapter',
            sample_rate=2.048e6,
            gain='auto',
            num_samples=1024*200,
            dwell_time=0.2
        )
        
        print(f"✅ Signal capture completed successfully")
        print(f"✅ Captured signals on {len(signals)} frequencies")
        
        # Display some signal information
        for signal in signals[:3]:  # Show first 3 signals
            print(f"   - {signal.frequency_mhz} MHz: {signal.signal_strength_dbm:.1f} dBm")
        
        return True
        
    except CellularScanError as e:
        print(f"❌ Signal capture failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during signal capture: {e}")
        return False

async def main():
    """Main test function."""
    print("=== Testing NETGEAR A6210 WiFi USB3.0 Adapter Integration ===\n")
    
    # Test 1: Adapter detection
    if not await test_network_adapter_detection():
        print("\n❌ NETGEAR A6210 WiFi USB3.0 Adapter detection tests failed")
        return 1
    
    print("\n✅ NETGEAR A6210 WiFi USB3.0 Adapter detection tests passed")
    
    # Test 2: Signal capture
    if not await test_signal_capture():
        print("\n❌ Signal capture tests failed")
        return 1
    
    print("\n✅ Signal capture tests passed")
    
    print("\n=== ALL TESTS PASSED ===")
    print("The system is working properly with the NETGEAR A6210 WiFi USB3.0 Adapter")
    print("instead of RTL-SDR.")
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
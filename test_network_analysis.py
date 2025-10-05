import sys
import os

# Add the spectrum analyzer path
sys.path.append(os.path.join(os.path.dirname(__file__), 'spectrum_analyzer', 'intern'))

from spectrum_grabber.wifi_scanner import scan_wifi_cross_platform
from spectrum_grabber.cellular_scanner import get_common_cellular_frequencies

def main():
    print("=== Network Analysis Using USB Adapter ===")
    print()
    
    # WiFi Network Scanning
    print("1. WiFi Network Scanning:")
    print("-" * 30)
    try:
        networks = scan_wifi_cross_platform()
        print(f"Found {len(networks)} WiFi networks:")
        
        for i, net in enumerate(networks[:10]):  # Show first 10 networks
            print(f"  {i+1}. SSID: {net.ssid}")
            print(f"      Frequency: {getattr(net, 'frequency_mhz', 'N/A')} MHz")
            print(f"      BSSID: {getattr(net, 'bssid', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"Error scanning WiFi networks: {e}")
    
    print()
    
    # Cellular Frequency Information
    print("2. Common Cellular Frequencies:")
    print("-" * 30)
    try:
        cellular_freqs = get_common_cellular_frequencies()
        for band, frequencies in cellular_freqs.items():
            print(f"  {band}: {frequencies} MHz")
            
    except Exception as e:
        print(f"Error getting cellular frequencies: {e}")
    
    print()
    print("=== Analysis Complete ===")

if __name__ == "__main__":
    main()
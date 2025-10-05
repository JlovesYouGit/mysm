import sys
import os

# Add the spectrum analyzer path
sys.path.append(os.path.join(os.path.dirname(__file__), 'spectrum_analyzer', 'intern'))

from spectrum_grabber.wifi_scanner import scan_wifi_cross_platform

def main():
    print("Scanning WiFi networks using USB adapter...")
    try:
        networks = scan_wifi_cross_platform()
        print(f"Found {len(networks)} networks:")
        
        for i, net in enumerate(networks[:10]):  # Show first 10 networks
            print(f"  {i+1}. SSID: {net.ssid}")
            print(f"      Signal Strength: {getattr(net, 'signal_strength', 'N/A')}")
            print(f"      Frequency: {getattr(net, 'frequency_mhz', 'N/A')} MHz")
            print(f"      BSSID: {getattr(net, 'bssid', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"Error scanning networks: {e}")

if __name__ == "__main__":
    main()
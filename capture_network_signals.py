"""
This script detects and captures network signals using the NETGEAR A6210 WiFi USB3.0 Adapter,
specifically targeting cellular and SS7 signaling frequencies.
It utilizes the network adapter to scan the environment and capture signaling data for further analysis.

Usage:
    python capture_network_signals.py

Note:
    Ensure that the NETGEAR A6210 WiFi USB3.0 Adapter and software dependencies are properly configured before running this script.
"""

import pickle
import sys
import os
from typing import List, Dict, Any, Optional
sys.path.append(os.path.join(os.path.dirname(__file__), 'spectrum_analyzer', 'intern'))
from spectrum_grabber.cellular_scanner import scan_cellular_cross_platform, get_common_cellular_frequencies, CellularScanError

def capture_signaling_data(output_file: str = "captured_signals.bin", scan_mode: str = "cellular"):
    """
    Capture signaling data using NETGEAR A6210 WiFi USB3.0 Adapter.

    Args:
        output_file: File to save captured data
        scan_mode: 'cellular' for SS7 bands, 'wide' for broad spectrum scan
    """
    print(f"Initializing {scan_mode} signal capture with NETGEAR A6210 WiFi USB3.0 Adapter...")

    if scan_mode == "cellular":
        # Get common cellular frequencies for SS7 bands
        freq_dict = get_common_cellular_frequencies()
        frequencies = []
        for band, freqs in freq_dict.items():
            if band.startswith(('GSM', 'LTE', '5G')):  # Include 5G for future SS7
                frequencies.extend(freqs)
    elif scan_mode == "wide":
        # Wide spectrum scan for tower detection
        frequencies = []
        # GSM bands
        frequencies.extend([890, 935, 1805, 1842.5])
        # LTE bands
        frequencies.extend([700, 800, 1800, 2100, 2600])
        # 5G bands
        frequencies.extend([3500, 28000])  # Sub-6 and mmWave examples
        # Add more bands as needed
    else:
        print(f"Unknown scan mode: {scan_mode}")
        return False

    print(f"Scanning {len(frequencies)} frequencies: {frequencies}")

    try:
        # Scan frequencies using network adapter
        signals = scan_cellular_cross_platform(
            frequencies_mhz=frequencies,
            sample_rate=2.048e6,  # 2.048 MS/s for GSM/LTE
            gain='auto',
            num_samples=1024*1024,  # 1M samples per frequency
            dwell_time=0.5,
            sdr_type='network_adapter'
        )

        # Filter signals with detectable strength (above noise floor)
        detected_signals = [s for s in signals if s.signal_strength_dbm > -80]

        print(f"Detected {len(detected_signals)} potential signals")

        # Save captured data
        data_to_save = {
            'signals': detected_signals,
            'scan_time': signals[0].detected_at if signals else None,
            'frequencies_scanned': frequencies,
            'scan_mode': scan_mode
        }

        with open(output_file, 'wb') as f:
            pickle.dump(data_to_save, f)

        print(f"Captured data saved to {output_file}")

        # Also save raw samples for analysis if available
        for signal in detected_signals:
            if signal.raw_samples is not None:
                raw_file = f"raw_samples_freq_{signal.frequency_mhz:.0f}MHz.bin"
                signal.raw_samples.tofile(raw_file)
                print(f"Raw samples saved to {raw_file}")

    except CellularScanError as e:
        print(f"Scan failed: {e}")
        print("Ensure NETGEAR A6210 WiFi USB3.0 Adapter is connected and drivers are installed.")
        return False

    return True

def scan_wide_spectrum(output_file: str = "wide_spectrum_capture.bin", start_freq: float = 400, end_freq: float = 6000, step: float = 50):
    """
    Perform a wide spectrum scan to detect towers across frequency ranges using network adapter.

    Args:
        output_file: File to save captured data
        start_freq: Start frequency in MHz
        end_freq: End frequency in MHz
        step: Frequency step in MHz
    """
    print(f"Performing wide spectrum scan from {start_freq} MHz to {end_freq} MHz with NETGEAR A6210 WiFi USB3.0 Adapter...")

    frequencies = [float(f) for f in range(int(start_freq), int(end_freq) + 1, int(step))]

    try:
        signals = scan_cellular_cross_platform(
            frequencies_mhz=frequencies,
            sample_rate=2.048e6,
            gain='auto',
            num_samples=512*1024,  # Smaller samples for wide scan
            dwell_time=0.2,  # Shorter dwell time
            sdr_type='network_adapter'
        )

        # Filter strong signals (potential towers)
        tower_signals = [s for s in signals if s.signal_strength_dbm > -70]

        print(f"Detected {len(tower_signals)} strong signals (potential towers)")

        # Save data
        data_to_save = {
            'signals': tower_signals,
            'scan_time': signals[0].detected_at if signals else None,
            'frequency_range': (start_freq, end_freq),
            'step': step
        }

        with open(output_file, 'wb') as f:
            pickle.dump(data_to_save, f)

        print(f"Wide spectrum data saved to {output_file}")

    except CellularScanError as e:
        print(f"Wide spectrum scan failed: {e}")
        return False

    return True

def main():
    print("Starting network signal capture process with NETGEAR A6210 WiFi USB3.0 Adapter...")

    # Capture signaling data
    success = capture_signaling_data("captured_signals.bin")

    if success:
        print("Network signal capture completed. Data is ready for analysis.")
    else:
        print("Network signal capture failed.")

if __name__ == "__main__":
    main()
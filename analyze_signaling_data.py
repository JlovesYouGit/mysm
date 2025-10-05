"""
analyze_signaling_data.py

This script decodes intercepted SS7 signaling data from cellular scans and extracts point codes used by nearby cellular towers.

Usage:
    python analyze_signaling_data.py [captured_signals.bin]

Steps:
1. Load captured signaling data from cellular scanner output.
2. Process raw IQ samples to detect and decode SS7 signaling.
3. Identify and list SS7 point codes in use.
4. Output the extracted point codes for further processing.

Note:
This script assumes that the signaling data has been captured using capture_network_signals.py and stored in pickle format.
"""

import struct
import pickle
import sys
import os
import numpy as np

def load_captured_data(filename):
    """
    Load captured signaling data from pickle file.

    Args:
        filename (str): Path to the captured data file.

    Returns:
        dict: Captured data with signals and metadata.
    """
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return None

def process_raw_samples(signals):
    """
    Process raw IQ samples from cellular signals to extract SS7 data.

    Args:
        signals (list): List of CellularSignal objects with raw_samples.

    Returns:
        bytes: Concatenated raw signaling data for decoding.
    """
    all_data = b''

    for signal in signals:
        if signal.raw_samples is not None:
            # Convert complex IQ samples to bytes (simplified)
            # In reality, this would involve demodulation, filtering, etc.
            # For demo, convert magnitude to bytes
            magnitudes = np.abs(signal.raw_samples)
            # Normalize and convert to bytes
            normalized = (magnitudes / np.max(magnitudes) * 255).astype(np.uint8)
            all_data += normalized.tobytes()

    return all_data

def decode_ss7_packets(data):
    """
    Decode SS7 packets from raw data.

    Args:
        data (bytes): Raw signaling data.

    Returns:
        list of dict: List of decoded SS7 packets with extracted fields.
    """
    packets = []
    offset = 0
    data_length = len(data)

    while offset < data_length:
        # For demonstration, assume each packet starts with a 2-byte length field
        if offset + 2 > data_length:
            break
        packet_length = struct.unpack('>H', data[offset:offset+2])[0]
        offset += 2

        if offset + packet_length > data_length:
            break

        packet_data = data[offset:offset+packet_length]
        offset += packet_length

        # Parse the packet to extract point code and other info
        # This is a simplified example; real SS7 decoding is more complex
        if len(packet_data) < 4:
            continue

        # Assume point code is 3 bytes starting at byte 1 (example)
        point_code_bytes = packet_data[1:4]
        point_code = int.from_bytes(point_code_bytes, byteorder='big')

        packet_info = {
            'point_code': point_code,
            'raw_data': packet_data,
            'packet_length': packet_length
        }
        packets.append(packet_info)

    return packets

def extract_point_codes(packets):
    """
    Extract unique SS7 point codes from decoded packets.

    Args:
        packets (list of dict): Decoded SS7 packets.

    Returns:
        set: Unique SS7 point codes.
    """
    point_codes = set()
    for packet in packets:
        point_codes.add(packet['point_code'])
    return point_codes

def analyze_captured_signals(filename):
    """
    Analyze captured cellular signals to extract SS7 point codes.

    Args:
        filename (str): Path to captured data file.

    Returns:
        set: Extracted point codes.
    """
    print(f"Loading captured data from {filename}...")

    data = load_captured_data(filename)
    if not data:
        return set()

    signals = data.get('signals', [])
    print(f"Processing {len(signals)} captured signals...")

    # Process raw samples to extract signaling data
    raw_data = process_raw_samples(signals)

    if not raw_data:
        print("No raw signaling data found in captured signals.")
        return set()

    print(f"Processing {len(raw_data)} bytes of raw signaling data...")

    # Decode SS7 packets
    packets = decode_ss7_packets(raw_data)
    print(f"Decoded {len(packets)} potential SS7 packets.")

    # Extract point codes
    point_codes = extract_point_codes(packets)

    return point_codes

def main():
    """Main function to analyze captured signaling data."""
    filename = sys.argv[1] if len(sys.argv) > 1 else "captured_signals.bin"

    point_codes = analyze_captured_signals(filename)

    if point_codes:
        print(f"\nExtracted SS7 Point Codes: {sorted(point_codes)}")
        print(f"Total unique point codes: {len(point_codes)}")

        # Save point codes for further use
        with open("extracted_point_codes.txt", "w") as f:
            f.write("Extracted SS7 Point Codes:\n")
            for pc in sorted(point_codes):
                f.write(f"{pc}\n")
        print("Point codes saved to extracted_point_codes.txt")
    else:
        print("No SS7 point codes extracted from the captured data.")

if __name__ == "__main__":
    main()

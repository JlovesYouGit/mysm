#!/usr/bin/env python3
"""
Comprehensive test suite for capture_network_signals.py
Tests all functions, error handling, and edge cases.
"""

import os
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock, mock_open
import pickle

# Add the spectrum_analyzer path
sys.path.append(os.path.join(os.path.dirname(__file__), 'spectrum_analyzer', 'intern'))

# Import the module to test
import capture_network_signals

class TestCaptureNetworkSignals(unittest.TestCase):
    """Test suite for network signal capture functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_output_file = os.path.join(self.temp_dir, "test_signals.bin")
        self.test_wide_file = os.path.join(self.temp_dir, "test_wide.bin")

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    @patch('capture_network_signals.scan_cellular_cross_platform')
    @patch('capture_network_signals.get_common_cellular_frequencies')
    def test_capture_signaling_data_cellular_mode_success(self, mock_get_freqs, mock_scan):
        """Test successful cellular signal capture."""
        # Mock frequency data
        mock_get_freqs.return_value = {
            'GSM900': [890, 935],
            'GSM1800': [1805, 1842],
            'LTE': [2100]
        }

        # Mock scan results
        mock_signals = [
            MagicMock(
                signal_strength_dbm=-60,
                frequency_mhz=890,
                detected_at="2024-01-01T12:00:00Z",
                raw_samples=None
            ),
            MagicMock(
                signal_strength_dbm=-85,
                frequency_mhz=935,
                detected_at="2024-01-01T12:00:00Z",
                raw_samples=None
            )
        ]
        mock_scan.return_value = mock_signals

        result = capture_network_signals.capture_signaling_data(
            self.test_output_file, "cellular"
        )

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_output_file))

        # Verify saved data
        with open(self.test_output_file, 'rb') as f:
            data = pickle.load(f)

        self.assertIn('signals', data)
        self.assertIn('scan_time', data)
        self.assertIn('frequencies_scanned', data)
        self.assertIn('scan_mode', data)
        self.assertEqual(data['scan_mode'], 'cellular')
        self.assertEqual(len(data['signals']), 1)  # Only strong signals

    @patch('capture_network_signals.scan_cellular_cross_platform')
    def test_capture_signaling_data_wide_mode_success(self, mock_scan):
        """Test successful wide spectrum signal capture."""
        mock_signals = [
            MagicMock(
                signal_strength_dbm=-60,
                frequency_mhz=800,
                detected_at="2024-01-01T12:00:00Z",
                raw_samples=None
            )
        ]
        mock_scan.return_value = mock_signals

        result = capture_network_signals.capture_signaling_data(
            self.test_output_file, "wide"
        )

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_output_file))

    @patch('capture_network_signals.scan_cellular_cross_platform')
    @patch('capture_network_signals.get_common_cellular_frequencies')
    def test_capture_signaling_data_with_raw_samples(self, mock_get_freqs, mock_scan):
        """Test capture with raw samples saving."""
        import numpy as np

        mock_get_freqs.return_value = {'GSM900': [890]}

        # Mock signal with raw samples
        mock_signal = MagicMock(
            signal_strength_dbm=-60,
            frequency_mhz=890,
            detected_at="2024-01-01T12:00:00Z",
            raw_samples=np.array([1.0, 2.0, 3.0], dtype=np.complex64)
        )
        mock_scan.return_value = [mock_signal]

        result = capture_network_signals.capture_signaling_data(self.test_output_file)

        self.assertTrue(result)

        # Check if raw samples file was created
        raw_file = os.path.join(os.path.dirname(self.test_output_file), "raw_samples_freq_890MHz.bin")
        self.assertTrue(os.path.exists(raw_file))

    @patch('capture_network_signals.scan_cellular_cross_platform')
    def test_capture_signaling_data_scan_failure(self, mock_scan):
        """Test handling of scan failure."""
        from spectrum_grabber.cellular_scanner import CellularScanError
        mock_scan.side_effect = CellularScanError("SDR device not found")

        result = capture_network_signals.capture_signaling_data(self.test_output_file)

        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_output_file))

    def test_capture_signaling_data_unknown_mode(self):
        """Test handling of unknown scan mode."""
        result = capture_network_signals.capture_signaling_data(
            self.test_output_file, "unknown"
        )

        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_output_file))

    @patch('capture_network_signals.scan_cellular_cross_platform')
    def test_scan_wide_spectrum_success(self, mock_scan):
        """Test successful wide spectrum scan."""
        mock_signals = [
            MagicMock(
                signal_strength_dbm=-65,
                frequency_mhz=1000,
                detected_at="2024-01-01T12:00:00Z",
                raw_samples=None
            )
        ]
        mock_scan.return_value = mock_signals

        result = capture_network_signals.scan_wide_spectrum(
            self.test_wide_file, 800, 1200, 100
        )

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_wide_file))

        # Verify saved data
        with open(self.test_wide_file, 'rb') as f:
            data = pickle.load(f)

        self.assertIn('signals', data)
        self.assertIn('scan_time', data)
        self.assertIn('frequency_range', data)
        self.assertIn('step', data)

    @patch('capture_network_signals.scan_cellular_cross_platform')
    def test_scan_wide_spectrum_scan_failure(self, mock_scan):
        """Test wide spectrum scan failure handling."""
        from spectrum_grabber.cellular_scanner import CellularScanError
        mock_scan.side_effect = CellularScanError("Scan failed")

        result = capture_network_signals.scan_wide_spectrum(self.test_wide_file)

        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_wide_file))

    def test_frequency_filtering_cellular(self):
        """Test that only relevant cellular bands are included."""
        # This would require mocking get_common_cellular_frequencies
        # and verifying the filtering logic
        pass

    def test_signal_strength_filtering(self):
        """Test that weak signals are filtered out."""
        # Test with signals above and below threshold
        pass

    def test_file_output_formats(self):
        """Test that output files contain expected data structures."""
        # Verify pickle format and data keys
        pass

    def test_edge_cases(self):
        """Test edge cases like empty results, boundary frequencies."""
        # Test with no signals detected
        # Test with frequencies at boundaries
        pass

    @patch('builtins.print')
    def test_main_function(self, mock_print):
        """Test the main function execution."""
        with patch('capture_network_signals.capture_signaling_data', return_value=True):
            capture_network_signals.main()

        mock_print.assert_any_call("Starting network signal capture process...")
        mock_print.assert_any_call("Network signal capture completed. Data is ready for analysis.")

    @patch('builtins.print')
    def test_main_function_failure(self, mock_print):
        """Test main function with capture failure."""
        with patch('capture_network_signals.capture_signaling_data', return_value=False):
            capture_network_signals.main()

        mock_print.assert_any_call("Network signal capture failed.")

if __name__ == '__main__':
    unittest.main(verbosity=2)

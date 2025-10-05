"""
This script recursively scans the specified directory and its subdirectories,
looking for files that match expected naming conventions or formats related to SS7 point codes.

Usage:
    python scan_filesystem.py <directory_path>

Example:
    python scan_filesystem.py @N:\sms\spectrum
"""

import os
import sys

def scan_directory_for_ss7_files(root_dir):
    """
    Recursively scan the root_dir for files that might contain SS7 point code information.
    Prints the paths of matching files.
    """
    # Define file patterns or extensions that might be relevant for SS7 point codes
    # This can be adjusted based on actual file naming conventions or formats
    relevant_extensions = ['.txt', '.cfg', '.conf', '.log', '.dat']

    print(f"Scanning directory: {root_dir}")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file extension matches any of the relevant extensions
            if any(filename.lower().endswith(ext) for ext in relevant_extensions):
                file_path = os.path.join(dirpath, filename)
                print(f"Found potential SS7 file: {file_path}")

def main():
    # Check if a directory argument is provided
    if len(sys.argv) == 2:
        directory_to_scan = sys.argv[1]
    else:
        # Optionally, get from environment variable or default path
        directory_to_scan = os.environ.get('SPECTRUM_FOLDER_PATH', '@N:\\sms\\spectrum')

    if not os.path.isdir(directory_to_scan):
        print(f"Error: The specified path '{directory_to_scan}' is not a valid directory.")
        sys.exit(1)

    scan_directory_for_ss7_files(directory_to_scan)

if __name__ == "__main__":
    main()

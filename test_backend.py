#!/usr/bin/env python3
"""
Simple Backend Test Script
"""

import requests
import time

def test_backend():
    print("Testing backend connectivity...")
    
    # Test basic connectivity
    try:
        response = requests.get('http://localhost:8083/', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is responding")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - make sure it's running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Backend request timed out")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if not success:
        print("\n🔧 Troubleshooting steps:")
        print("   1. Check that start-fullstack.ps1 is still running")
        print("   2. Verify no firewall is blocking port 8083")
        print("   3. Check PowerShell windows for error messages")
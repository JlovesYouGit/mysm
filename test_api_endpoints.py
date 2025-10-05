import requests
import json

BASE_URL = "http://localhost:8084"

def test_login():
    response = requests.post(f"{BASE_URL}/api/auth/login", 
                           json={"username": "admin", "password": "telecom2025"})
    if response.status_code == 200:
        token = response.json()["token"]
        print("✓ Login successful")
        return token
    else:
        print("✗ Login failed")
        return None

def test_available_numbers(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/numbers/available", headers=headers)
    if response.status_code == 200:
        numbers = response.json()["numbers"]
        print(f"✓ Found {len(numbers)} available numbers")
        if numbers:
            print(f"  Sample numbers: {[n['number'] for n in numbers[:3]]}")
        return numbers
    else:
        print("✗ Failed to get available numbers")
        return []

def test_spectrum_scan(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/spectrum/scan", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Spectrum scan successful")
        print(f"  Towers detected: {data.get('towers_detected', 0)}")
        print(f"  Point codes: {len(data.get('point_codes', []))}")
        return data
    else:
        print("✗ Spectrum scan failed")
        return None

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    token = test_login()
    if token:
        test_available_numbers(token)
        test_spectrum_scan(token)
    
    print("Test complete!")
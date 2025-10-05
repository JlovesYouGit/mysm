import requests
import json

def test_real_api():
    # Login
    login_response = requests.post("http://localhost:8084/api/auth/login", 
                                 json={"username": "admin", "password": "telecom2025"})
    
    if login_response.status_code != 200:
        print("❌ LOGIN FAILED")
        print(f"Status: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test available numbers
    numbers_response = requests.get("http://localhost:8084/api/numbers/available", headers=headers)
    print(f"Numbers API Status: {numbers_response.status_code}")
    if numbers_response.status_code == 200:
        data = numbers_response.json()
        print(f"Available numbers: {len(data.get('numbers', []))}")
        if data.get('numbers'):
            print(f"First number: {data['numbers'][0]}")
    else:
        print(f"❌ NUMBERS API FAILED: {numbers_response.text}")
    
    # Test spectrum scan
    spectrum_response = requests.post("http://localhost:8084/api/spectrum/scan", headers=headers)
    print(f"Spectrum API Status: {spectrum_response.status_code}")
    if spectrum_response.status_code == 200:
        data = spectrum_response.json()
        print(f"Towers detected: {data.get('towers_detected', 0)}")
        print(f"Point codes: {len(data.get('point_codes', []))}")
    else:
        print(f"❌ SPECTRUM API FAILED: {spectrum_response.text}")

if __name__ == "__main__":
    test_real_api()
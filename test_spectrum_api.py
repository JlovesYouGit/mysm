import requests
import json

def test_spectrum_api():
    print("Testing Spectrum API...")
    print("=" * 40)
    
    # Login first to get token
    print("1. Logging in...")
    login_data = {"username": "admin", "password": "telecom2025"}
    response = requests.post("http://localhost:8083/api/auth/login", json=login_data, timeout=5)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    token_data = response.json()
    token = token_data.get("token")
    print(f"✅ Login successful, token: {token[:20]}...")
    
    # Test spectrum endpoints with token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test get towers
    print("2. Testing get spectrum towers...")
    try:
        response = requests.get("http://localhost:8084/api/spectrum/towers", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Got towers: {len(data.get('towers', []))} towers")
        else:
            print(f"   ❌ Failed to get towers: {response.text}")
    except Exception as e:
        print(f"   ❌ Error getting towers: {e}")
    
    # Test get point codes
    print("3. Testing get spectrum point codes...")
    try:
        response = requests.get("http://localhost:8084/api/spectrum/pointcodes", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Got point codes: {len(data.get('point_codes', []))} codes")
        else:
            print(f"   ❌ Failed to get point codes: {response.text}")
    except Exception as e:
        print(f"   ❌ Error getting point codes: {e}")
    
    # Test spectrum scan
    print("4. Testing spectrum scan...")
    try:
        response = requests.post("http://localhost:8084/api/spectrum/scan", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Spectrum scan completed")
            print(f"   Towers detected: {data.get('towers_detected', 'N/A')}")
        else:
            print(f"   ❌ Spectrum scan failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error during spectrum scan: {e}")

if __name__ == "__main__":
    test_spectrum_api()
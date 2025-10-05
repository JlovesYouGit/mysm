import requests
import json

def debug_numbers_api():
    print("Debugging Numbers API...")
    print("=" * 40)
    
    # Login first
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
    
    # Test available numbers
    print("2. Testing available numbers API...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get("http://localhost:8083/api/numbers/available", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Got available numbers: {len(data.get('numbers', []))} numbers")
        else:
            print(f"   ❌ Failed to get available numbers")
    except Exception as e:
        print(f"   ❌ Error getting available numbers: {e}")
    
    # Test user numbers
    print("3. Testing user numbers API...")
    try:
        response = requests.get("http://localhost:8083/api/numbers", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Got user numbers: {len(data.get('numbers', []))} numbers")
        else:
            print(f"   ❌ Failed to get user numbers")
    except Exception as e:
        print(f"   ❌ Error getting user numbers: {e}")

if __name__ == "__main__":
    debug_numbers_api()
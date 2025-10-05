import requests
import json

def test_authentication():
    print("Testing Authentication Flow...")
    print("=" * 40)
    
    # Test 1: Try to access protected endpoint without auth
    print("1. Testing access without authentication...")
    try:
        response = requests.get("http://localhost:8083/api/numbers", timeout=3)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 401:
            print("   ✅ Correctly blocked unauthorized access")
        else:
            print(f"   ⚠️  Expected 401, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Login with correct credentials
    print("2. Testing login with correct credentials...")
    try:
        login_data = {"username": "admin", "password": "telecom2025"}
        response = requests.post("http://localhost:8083/api/auth/login", json=login_data, timeout=3)
        print(f"   Login status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("token")
            if token:
                print("   ✅ Login successful, token received")
                print(f"   Token: {token[:20]}...")
                
                # Test 3: Access protected endpoint with token
                print("3. Testing access with valid token...")
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get("http://localhost:8083/api/numbers", headers=headers, timeout=3)
                print(f"   Numbers API status: {response.status_code}")
                print(f"   Response: {response.text}")
                if response.status_code == 200:
                    print("   ✅ Successfully accessed protected endpoint")
                else:
                    print(f"   ❌ Expected 200, got {response.status_code}")
            else:
                print("   ❌ No token in response")
        else:
            print(f"   ❌ Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error during login: {e}")
    
    print("\n" + "=" * 40)
    print("Authentication test complete.")

if __name__ == "__main__":
    test_authentication()
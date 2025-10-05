import requests
import json

def test_call_functionality():
    print("Testing Call Functionality...")
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
    print(f"✅ Login successful")
    
    # Test making a call
    print("2. Testing voice call...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    call_data = {
        "to": "+15551234567",
        "from_": "+15559876543"
    }
    
    try:
        response = requests.post("http://localhost:8083/api/voice/call", headers=headers, json=call_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Call initiated successfully")
            print(f"   Call ID: {data.get('call_id', 'N/A')}")
            print(f"   SS7 Status: {data.get('ss7_status', 'N/A')}")
        else:
            print(f"   ❌ Call failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error making call: {e}")
    
    # Test getting call log
    print("3. Testing call log retrieval...")
    try:
        response = requests.get("http://localhost:8083/api/voice/calls", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            calls = data.get('calls', [])
            print(f"   ✅ Retrieved call log with {len(calls)} calls")
            if calls:
                print(f"   Most recent call: {calls[0] if calls else 'None'}")
        else:
            print(f"   ❌ Failed to retrieve call log: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving call log: {e}")

if __name__ == "__main__":
    test_call_functionality()
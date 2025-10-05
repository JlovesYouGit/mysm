import requests
import json

def test_sms_functionality():
    print("Testing SMS Functionality...")
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
    
    # Test sending an SMS
    print("2. Testing SMS send...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    sms_data = {
        "to": "+15551234567",
        "from_": "+15559876543",
        "message": "Test message from telecom system"
    }
    
    try:
        response = requests.post("http://localhost:8083/api/sms/send", headers=headers, json=sms_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SMS sent successfully")
            print(f"   Message ID: {data.get('message_id', 'N/A')}")
            print(f"   SS7 Status: {data.get('ss7_status', 'N/A')}")
        else:
            print(f"   ❌ SMS send failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error sending SMS: {e}")
    
    # Test getting SMS messages
    print("3. Testing SMS retrieval...")
    try:
        response = requests.get("http://localhost:8083/api/sms/messages", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            print(f"   ✅ Retrieved SMS messages with {len(messages)} messages")
            if messages:
                print(f"   Most recent message: {messages[0]['message'] if messages else 'None'}")
        else:
            print(f"   ❌ Failed to retrieve SMS messages: {response.text}")
    except Exception as e:
        print(f"   ❌ Error retrieving SMS messages: {e}")

if __name__ == "__main__":
    test_sms_functionality()
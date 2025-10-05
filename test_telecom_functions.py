import requests
import json

BASE_URL = "http://localhost:8083"

def test_login():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "telecom2025"})
    if response.status_code == 200:
        token = response.json()['token']
        print("✅ Login successful")
        return token
    else:
        print("❌ Login failed:", response.text)
        return None

def test_get_available_numbers(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/numbers/available", headers=headers)
    if response.status_code == 200:
        numbers = response.json()['numbers']
        print(f"✅ Found {len(numbers)} available numbers")
        if numbers:
            print(f"   First number: {numbers[0]['number']}")
        return numbers
    else:
        print("❌ Failed to get available numbers:", response.text)
        return []

def test_assign_number(token, number):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/numbers/assign", 
                           json={"number": number}, 
                           headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Number {number} assigned successfully")
        return True
    else:
        print(f"❌ Failed to assign number {number}:", response.text)
        return False

def test_make_call(token, from_number, to_number):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/voice/call", 
                           json={"from_": from_number, "to": to_number}, 
                           headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Call initiated from {from_number} to {to_number}")
        return True
    else:
        print(f"❌ Failed to initiate call:", response.text)
        return False

def test_send_sms(token, from_number, to_number, message):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/sms/send", 
                           json={"from_": from_number, "to": to_number, "message": message}, 
                           headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SMS sent from {from_number} to {to_number}")
        return True
    else:
        print(f"❌ Failed to send SMS:", response.text)
        return False

def main():
    print("=== Testing Telecom Functions ===")
    print()
    
    # Login
    token = test_login()
    if not token:
        return
    
    print()
    
    # Get available numbers
    numbers = test_get_available_numbers(token)
    if not numbers:
        return
    
    print()
    
    # Assign a number
    test_number = numbers[0]['number']
    if test_assign_number(token, test_number):
        print()
        
        # Make a call
        test_make_call(token, test_number, "+15551234567")
        
        print()
        
        # Send an SMS
        test_send_sms(token, test_number, "+15551234567", "Hello from the telecom system!")

if __name__ == "__main__":
    main()
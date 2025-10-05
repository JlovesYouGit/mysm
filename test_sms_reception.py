#!/usr/bin/env python3
"""
SMS Testing Script - Simulate Receiving SMS from Mobile Device
"""

import requests
import json
import random
from datetime import datetime

def simulate_sms_reception():
    """Simulate receiving an SMS from your mobile device."""
    print("📱 Simulating SMS Reception from Your Mobile Device")
    print("=" * 50)
    
    try:
        # Login to get auth token
        print("🔑 Authenticating...")
        login_response = requests.post('http://localhost:8083/api/auth/login', 
                                     json={"username": "admin", "password": "telecom2025"})
        
        if login_response.status_code != 200:
            print("❌ Authentication failed")
            return False
            
        token = login_response.json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ Authentication successful")
        
        # Generate a realistic mobile number (simulating your phone)
        mobile_number = f"+1{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}"
        
        # Create a test SMS message (simulating what your phone would send)
        test_message = f"Test SMS from your mobile device at {datetime.now().strftime('%H:%M:%S')}"
        
        print(f"\n📤 Simulating SMS from your phone:")
        print(f"   From: {mobile_number}")
        print(f"   To: +12122001000")
        print(f"   Message: {test_message}")
        
        # Send SMS through the API (simulating reception)
        sms_response = requests.post('http://localhost:8083/api/sms/send', 
                                   headers=headers,
                                   json={
                                       "to": "+12122001000",  # This is the number in our system
                                       "from_": mobile_number,  # Simulating your mobile number
                                       "message": test_message
                                   })
        
        if sms_response.status_code != 200:
            print("❌ Failed to simulate SMS reception")
            return False
            
        sms_data = sms_response.json()
        print("✅ SMS simulated successfully!")
        print(f"   Message ID: {sms_data.get('message_id', 'N/A')}")
        
        # Verify the message appears in the conversation history
        print("\n🔍 Verifying message in conversation history...")
        messages_response = requests.get('http://localhost:8083/api/sms/messages', headers=headers)
        if messages_response.status_code == 200:
            messages = messages_response.json().get('messages', [])
            # Find our test message
            test_messages = [msg for msg in messages if msg.get('message') == test_message]
            if test_messages:
                print("✅ Message confirmed in conversation history")
                latest_msg = test_messages[0]
                print(f"   Timestamp: {latest_msg.get('timestamp')}")
                print(f"   Status: {latest_msg.get('status')}")
            else:
                print("⚠️  Message not found in conversation history")
        else:
            print("⚠️  Could not verify message in history")
            
        print("\n" + "=" * 50)
        print("📋 How to view this message:")
        print("   1. Open your web browser")
        print("   2. Visit http://localhost:8080/messages")
        print("   3. Login with admin/telecom2025")
        print("   4. Look for conversation with your mobile number")
        
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        return False
    
    return True

def show_real_sms_instructions():
    """Show instructions for receiving real SMS from mobile device."""
    print("\n" + "=" * 50)
    print("📡 FOR RECEIVING REAL SMS FROM YOUR MOBILE DEVICE:")
    print("=" * 50)
    print("To receive actual SMS from your phone, you need:")
    print("")
    print("1. 📞 REAL TELEPHONE NUMBER")
    print("   - Provisioned with a telecommunications carrier")
    print("   - Connected to the actual SS7 network")
    print("")
    print("2. 🔌 SS7 CONNECTIVITY")
    print("   - SIGTRAN configuration with carrier endpoints")
    print("   - Environment variable: SS7_SIGTRAN=true")
    print("   - SSL/TLS certificates deployed")
    print("")
    print("3. 🚀 PRODUCTION DEPLOYMENT")
    print("   - Update sigtran_config.py with carrier info")
    print("   - Start system with production settings")
    print("")
    print("Current status: This system can VIEW SMS but cannot")
    print("receive SMS from external phones without carrier integration.")

if __name__ == "__main__":
    print("SMS Reception Testing Tool")
    print("")
    
    # Ask user what they want to do
    print("Choose an option:")
    print("1. Simulate receiving SMS from mobile device (for testing)")
    print("2. Show instructions for real SMS reception")
    print("")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        simulate_sms_reception()
    elif choice == "2":
        show_real_sms_instructions()
    else:
        print("Invalid choice. Showing real SMS instructions:")
        show_real_sms_instructions()
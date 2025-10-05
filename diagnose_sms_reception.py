#!/usr/bin/env python3
"""
SMS Reception Diagnostic Tool
Helps diagnose why SMS sent from your phone aren't appearing in the frontend
"""

import requests
import json
import time
from datetime import datetime

def authenticate():
    """Authenticate with the backend and return token"""
    try:
        response = requests.post('http://localhost:8083/api/auth/login', 
                               json={"username": "admin", "password": "telecom2025"})
        
        if response.status_code == 200:
            return response.json()['token']
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def get_messages(token):
    """Retrieve all messages from the system"""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get('http://localhost:8083/api/sms/messages', headers=headers)
        if response.status_code == 200:
            return response.json().get('messages', [])
        else:
            print(f"Failed to retrieve messages: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        return []

def check_ss7_status(token):
    """Check SS7 network status"""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get('http://localhost:8083/api/ss7/transport-status', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve SS7 status: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error retrieving SS7 status: {e}")
        return None

def simulate_sms_reception_test(token):
    """Simulate receiving an SMS to test the full flow"""
    headers = {'Authorization': f'Bearer {token}'}
    test_message = {
        "to": "+12122001000",
        "from_": "+12125551234",  # Simulating a phone number
        "message": f"Test message sent at {datetime.now().strftime('%H:%M:%S')}"
    }
    
    try:
        response = requests.post('http://localhost:8083/api/sms/send', 
                               headers=headers,
                               json=test_message)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Test SMS sent successfully")
            print(f"   Message ID: {result.get('message_id', 'N/A')}")
            print(f"   Licensed: {result.get('licensed', False)}")
            return True
        else:
            print(f"❌ Failed to send test SMS: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending test SMS: {e}")
        return False

def main():
    print("📱 SMS Reception Diagnostic Tool")
    print("=" * 50)
    print("This tool will help diagnose why SMS sent from your phone")
    print("aren't appearing in the frontend interface.")
    print()
    
    # Authenticate
    print("🔑 Authenticating with backend...")
    token = authenticate()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    print("✅ Authentication successful")
    print()
    
    # Check SS7 status
    print("📡 Checking SS7 network status...")
    ss7_status = check_ss7_status(token)
    if ss7_status:
        print(f"✅ SS7 Status: {ss7_status.get('status', 'Unknown')}")
        print(f"   Mode: {ss7_status.get('mode', 'Unknown')}")
        print(f"   Transport: {ss7_status.get('transport', 'N/A')}")
        
        if ss7_status.get('mode') == 'sigtran':
            print("   ⚠️  SIGTRAN mode is enabled but may not be properly configured")
            print("   📋 Check sigtran_config.py for proper carrier configuration")
    print()
    
    # Get existing messages
    print("📬 Checking existing messages...")
    messages = get_messages(token)
    print(f"✅ Found {len(messages)} message(s) in the system")
    
    if messages:
        print("\nLatest messages:")
        # Sort by timestamp, newest first
        sorted_messages = sorted(messages, key=lambda x: x.get('timestamp', ''), reverse=True)
        for i, msg in enumerate(sorted_messages[:3]):  # Show latest 3
            print(f"  {i+1}. From: {msg.get('from_', 'Unknown')}")
            print(f"     To: {msg.get('to', 'Unknown')}")
            print(f"     Message: {msg.get('message', '')}")
            print(f"     Time: {msg.get('timestamp', 'Unknown')}")
            print(f"     Status: {msg.get('status', 'Unknown')}")
            if 'ss7_status' in msg:
                ss7_info = msg['ss7_status']
                print(f"     SS7 Status: {ss7_info.get('status', 'Unknown')}")
                if 'reason' in ss7_info:
                    print(f"     SS7 Reason: {ss7_info['reason']}")
            print()
    else:
        print("   No messages found in the system")
    print()
    
    # Simulate SMS reception
    print("🧪 Testing SMS flow with simulated message...")
    test_success = simulate_sms_reception_test(token)
    
    if test_success:
        print("\n🔄 Checking if test message appears in messages list...")
        time.sleep(2)  # Wait a moment for processing
        new_messages = get_messages(token)
        if new_messages and len(new_messages) > len(messages):
            print("✅ Test message successfully added to messages list")
        else:
            print("⚠️  Test message not found in messages list")
    print()
    
    # Provide recommendations
    print("📋 Diagnostic Summary & Recommendations")
    print("=" * 50)
    
    if ss7_status and ss7_status.get('mode') == 'sigtran':
        print("🔍 Issue Identified:")
        print("   Your system is running in SIGTRAN mode which requires")
        print("   proper configuration with real carrier information.")
        print()
        print("💡 Recommendations:")
        print("   1. Update sigtran_config.py with actual carrier information:")
        print("      - Point codes provided by your carrier")
        print("      - IP addresses of carrier's STP/MSC nodes")
        print("      - Authentication credentials from your carrier")
        print("   2. For testing without carrier connectivity:")
        print("      - Set SS7_SIGTRAN=false in your environment")
        print("      - Use SS7_PRIVATE_NETWORK=true for private network simulation")
        print("   3. Check that your frontend is properly connecting to the backend")
        print("      - Open browser console and check for JavaScript errors")
        print("      - Verify network requests to http://localhost:8083")
    else:
        print("🔍 Possible Issues:")
        print("   1. Frontend may not be properly connecting to backend")
        print("   2. Authentication issues between frontend and backend")
        print("   3. CORS configuration problems")
        print()
        print("💡 Recommendations:")
        print("   1. Check browser console for JavaScript errors")
        print("   2. Verify that frontend is making requests to http://localhost:8083")
        print("   3. Check that CORS is properly configured in main.py")
        print("   4. Ensure you're logged into the frontend with admin/telecom2025")

if __name__ == "__main__":
    main()
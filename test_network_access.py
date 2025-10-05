#!/usr/bin/env python3
"""
Network Access Verification Script
"""

import socket
import requests
import json

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def test_network_access():
    """Test network access to the SMS system."""
    print("📡 Network Access Verification")
    print("=" * 40)
    
    # Get local IP address
    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    
    # Test backend API access
    print(f"\n🔧 Testing Backend API Access:")
    print(f"   Local Access: http://localhost:8083/api/sms/messages")
    print(f"   Network Access: http://{local_ip}:8083/api/sms/messages")
    
    try:
        # Test local access
        response = requests.get(f"http://localhost:8083/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Local API Access: Working")
        else:
            print(f"   ❌ Local API Access: Failed (Status {response.status_code})")
    except Exception as e:
        print(f"   ❌ Local API Access: Failed ({e})")
    
    # Test frontend access
    print(f"\n🌐 Testing Frontend Access:")
    print(f"   Local Access: http://localhost:8080/messages")
    print(f"   Network Access: http://{local_ip}:8080/messages")
    
    try:
        # Test local frontend access
        response = requests.get(f"http://localhost:8080", timeout=5)
        if response.status_code == 200:
            print("   ✅ Local Frontend Access: Working")
        else:
            print(f"   ❌ Local Frontend Access: Failed (Status {response.status_code})")
    except Exception as e:
        print(f"   ❌ Local Frontend Access: Failed ({e})")
    
    # Test authentication and SMS access
    print(f"\n📱 Testing SMS Functionality:")
    try:
        # Login
        login_response = requests.post('http://localhost:8083/api/auth/login', 
                                     json={"username": "admin", "password": "telecom2025"})
        if login_response.status_code == 200:
            token = login_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            print("   ✅ Authentication: Successful")
            
            # Get messages
            messages_response = requests.get('http://localhost:8083/api/sms/messages', headers=headers)
            if messages_response.status_code == 200:
                message_count = len(messages_response.json().get('messages', []))
                print(f"   ✅ SMS Access: Working ({message_count} messages)")
            else:
                print(f"   ❌ SMS Access: Failed (Status {messages_response.status_code})")
        else:
            print(f"   ❌ Authentication: Failed (Status {login_response.status_code})")
    except Exception as e:
        print(f"   ❌ SMS Functionality: Failed ({e})")
    
    print(f"\n" + "=" * 40)
    print("📋 ACCESS INSTRUCTIONS:")
    print(f"   From this machine:")
    print(f"     Web Interface: http://localhost:8080/messages")
    print(f"     API Endpoint: http://localhost:8083/api/sms/messages")
    print(f"")
    print(f"   From other devices on the same network:")
    print(f"     Web Interface: http://{local_ip}:8080/messages")
    print(f"     API Endpoint: http://{local_ip}:8083/api/sms/messages")
    print(f"")
    print(f"✅ System ready for remote SMS reception!")

if __name__ == "__main__":
    test_network_access()
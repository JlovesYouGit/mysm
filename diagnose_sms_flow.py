#!/usr/bin/env python3
"""
SMS Flow Diagnostic Script
Helps diagnose issues with SMS reception and display in the frontend
"""

import requests
import json
import time
from datetime import datetime

def check_backend_status():
    """Check if backend services are running"""
    print("🔧 Checking Backend Services Status")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:8083/api/health')
        if response.status_code == 200:
            print("✅ Backend API: Running")
            return True
        else:
            print("❌ Backend API: Not responding")
            return False
    except Exception as e:
        print(f"❌ Backend API: Connection failed - {e}")
        return False

def check_frontend_status():
    """Check if frontend is accessible"""
    print("\n🎨 Checking Frontend Status")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:8080')
        if response.status_code == 200:
            print("✅ Frontend: Accessible")
            return True
        else:
            print("❌ Frontend: Not accessible")
            return False
    except Exception as e:
        print(f"❌ Frontend: Connection failed - {e}")
        return False

def authenticate():
    """Authenticate with the backend"""
    print("\n🔑 Authenticating")
    print("=" * 40)
    
    try:
        response = requests.post('http://localhost:8083/api/auth/login', 
                               json={"username": "admin", "password": "telecom2025"})
        
        if response.status_code == 200:
            token = response.json()['token']
            print("✅ Authentication successful")
            return token
        else:
            print("❌ Authentication failed")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def list_all_messages(token):
    """List all messages in the system"""
    print("\n📬 Checking All Messages")
    print("=" * 40)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get('http://localhost:8083/api/sms/messages', headers=headers)
        
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            print(f"✅ Found {len(messages)} message(s)")
            
            if messages:
                print("\nLatest messages:")
                # Sort by timestamp, newest first
                sorted_messages = sorted(messages, key=lambda x: x.get('timestamp', ''), reverse=True)
                for i, msg in enumerate(sorted_messages[:5]):  # Show latest 5
                    print(f"  {i+1}. From: {msg.get('from_', 'Unknown')}")
                    print(f"     To: {msg.get('to', 'Unknown')}")
                    print(f"     Message: {msg.get('message', '')[:50]}{'...' if len(msg.get('message', '')) > 50 else ''}")
                    print(f"     Time: {msg.get('timestamp', 'Unknown')}")
                    print(f"     Status: {msg.get('status', 'Unknown')}")
                    print()
            else:
                print("   No messages found")
                
            return messages
        else:
            print("❌ Failed to retrieve messages")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error retrieving messages: {e}")
        return []

def check_ss7_status(token):
    """Check SS7 connection status"""
    print("\n📡 Checking SS7 Connection Status")
    print("=" * 40)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get('http://localhost:8083/api/ss7/status', headers=headers)
        
        if response.status_code == 200:
            status = response.json()
            print("✅ SS7 Service Status:")
            for key, value in status.items():
                print(f"   {key}: {value}")
            return status
        else:
            print("⚠️  SS7 status endpoint not available")
            return None
    except Exception as e:
        print(f"⚠️  Could not check SS7 status: {e}")
        return None

def test_api_endpoints(token):
    """Test various API endpoints"""
    print("\n🔌 Testing API Endpoints")
    print("=" * 40)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    endpoints = [
        ('GET', 'http://localhost:8083/api/sms/conversations'),
        ('GET', 'http://localhost:8083/api/sms/stats'),
        ('GET', 'http://localhost:8083/api/config'),
    ]
    
    for method, url in endpoints:
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, headers=headers)
                
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {method} {url} -> {response.status_code}")
        except Exception as e:
            print(f"   ❌ {method} {url} -> Error: {e}")

def main():
    """Main diagnostic function"""
    print("📱 SMS Flow Diagnostic Tool")
    print("=" * 50)
    print("This tool helps diagnose issues with SMS reception and display")
    print()
    
    # Check service statuses
    backend_ok = check_backend_status()
    frontend_ok = check_frontend_status()
    
    if not backend_ok:
        print("\n🚨 Backend services are not running!")
        print("   Please start the backend services first:")
        print("   - Run start-fullstack.ps1 or start-fullstack.sh")
        return
    
    if not frontend_ok:
        print("\n🚨 Frontend is not accessible!")
        print("   Please start the frontend development server")
        return
    
    # Authenticate
    token = authenticate()
    if not token:
        print("\n🚨 Cannot proceed without authentication")
        return
    
    # Check messages
    messages = list_all_messages(token)
    
    # Check SS7 status
    check_ss7_status(token)
    
    # Test API endpoints
    test_api_endpoints(token)
    
    # Summary
    print("\n📋 Diagnostic Summary")
    print("=" * 40)
    print(f"Backend Status: {'✅ OK' if backend_ok else '❌ Error'}")
    print(f"Frontend Status: {'✅ OK' if frontend_ok else '❌ Error'}")
    print(f"Messages Found: {len(messages)}")
    
    if messages:
        print("\n💡 Recommendations:")
        print("   1. Check if your frontend is properly connecting to the backend")
        print("   2. Verify that the frontend is requesting messages from the correct API endpoint")
        print("   3. Check browser console for JavaScript errors")
        print("   4. Ensure CORS is properly configured")
    else:
        print("\n💡 Recommendations:")
        print("   1. Your SMS might not be reaching the system")
        print("   2. Check if your phone number is correctly configured in the system")
        print("   3. Verify SS7/SIGTRAN connection if using real telephony")
        print("   4. For testing, try sending an SMS through the web interface")

if __name__ == "__main__":
    main()
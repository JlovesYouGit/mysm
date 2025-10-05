import requests
import json

def verify_services():
    print("Verifying Telecom Services...")
    print("=" * 40)
    
    # Test main API
    try:
        print("1. Testing Main API (port 8083)...")
        response = requests.get("http://localhost:8083/health", timeout=3)
        if response.status_code == 200:
            print("   ✅ Main API is running")
        else:
            print(f"   ❌ Main API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Main API not accessible: {e}")
    
    # Test spectrum API
    try:
        print("2. Testing Spectrum API (port 8084)...")
        response = requests.get("http://localhost:8084/health", timeout=3)
        if response.status_code == 200:
            print("   ✅ Spectrum API is running")
        else:
            print(f"   ❌ Spectrum API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Spectrum API not accessible: {e}")
    
    # Test MongoDB connection through main API
    try:
        print("3. Testing MongoDB connectivity...")
        # This will test if the main API can connect to MongoDB
        response = requests.get("http://localhost:8083/api/numbers/available", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data:
                print(f"   ✅ MongoDB connected ({len(data['numbers'])} available numbers)")
            else:
                print("   ⚠️  MongoDB connection issue")
        else:
            print(f"   ❌ Numbers API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Numbers API not accessible: {e}")
    
    print("\n" + "=" * 40)
    print("Verification complete. Check results above.")

if __name__ == "__main__":
    verify_services()
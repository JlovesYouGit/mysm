import requests
import time

def test_main_api():
    """Test if the main API is running and responding"""
    try:
        print("Testing Main API connection...")
        response = requests.get("http://localhost:8083/health", timeout=5)
        if response.status_code == 200:
            print("✅ Main API is running and healthy")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Main API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Main API. Make sure the backend is running on port 8083")
        return False
    except requests.exceptions.Timeout:
        print("❌ Main API connection timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing Main API: {e}")
        return False

def test_spectrum_api():
    """Test if the spectrum API is running and responding"""
    try:
        print("\nTesting Spectrum API connection...")
        response = requests.get("http://localhost:8084/health", timeout=5)
        if response.status_code == 200:
            print("✅ Spectrum API is running and healthy")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Spectrum API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Spectrum API. Make sure the backend is running on port 8084")
        return False
    except requests.exceptions.Timeout:
        print("❌ Spectrum API connection timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing Spectrum API: {e}")
        return False

if __name__ == "__main__":
    print("Telecom System API Test")
    print("=" * 30)
    
    main_ok = test_main_api()
    spectrum_ok = test_spectrum_api()
    
    print("\n" + "=" * 30)
    if main_ok and spectrum_ok:
        print("🎉 All APIs are running!")
    else:
        print("⚠️  Some APIs are not running properly.")
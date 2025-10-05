import requests
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def test_api_connection():
    """Test if the API is running and responding"""
    try:
        print("Testing API connection...")
        response = requests.get("http://localhost:8083/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running on port 8083")
        return False
    except requests.exceptions.Timeout:
        print("❌ API connection timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_frontend_connection():
    """Test if the frontend server is running"""
    try:
        print("\nTesting frontend connection...")
        response = requests.get("http://localhost:8080/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend. Make sure the frontend is running on port 8080")
        return False
    except requests.exceptions.Timeout:
        print("❌ Frontend connection timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def test_auth():
    """Test authentication endpoint"""
    try:
        print("\nTesting authentication...")
        response = requests.post(
            "http://localhost:8083/api/auth/login",
            json={"username": "admin", "password": "telecom2025"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Authentication successful")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Authentication failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing authentication: {e}")
        return False

def test_mongodb_connection():
    """Test if MongoDB is running and accessible"""
    try:
        print("\nTesting MongoDB connection...")
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        
        # Try to access the telecom_service database
        db = client.telecom_service
        collection_names = db.list_collection_names()
        print(f"✅ Found telecom_service database with collections: {collection_names or 'None'}")
        client.close()
        return True
    except ServerSelectionTimeoutError:
        print("❌ MongoDB connection timed out. Make sure MongoDB is running on port 27017")
        return False
    except ConnectionFailure:
        print("❌ Cannot connect to MongoDB. Make sure MongoDB is running on port 27017")
        return False
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return False

if __name__ == "__main__":
    print("Telecom System Connection Test")
    print("=" * 40)
    
    api_ok = test_api_connection()
    frontend_ok = test_frontend_connection()
    mongo_ok = test_mongodb_connection()
    
    if api_ok:
        auth_ok = test_auth()
    
    print("\n" + "=" * 40)
    if api_ok and frontend_ok:
        if mongo_ok:
            print("🎉 All systems are running with database support!")
        else:
            print("⚠️  Core systems are running but database is not available.")
            print("   The application will work in mock mode.")
            print("   To enable persistent storage:")
            print("   1. Run '.\\install-mongodb.ps1' (automated) or")
            print("   2. Run '.\\setup-mongodb-manual.ps1' (manual setup)")
            print("   3. Then run '.\\init-database.ps1' to seed data")
        print("You can now access the application at http://localhost:8080/")
    else:
        print("⚠️  Some core services are not running properly.")
        print("Please check the PowerShell windows for error messages.")

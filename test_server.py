import subprocess
import time
import requests
import sys

def test_server():
    print("Testing server startup...")
    
    # Start server
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "main:app", 
        "--host", "0.0.0.0", "--port", "8081"
    ])
    
    # Wait for startup
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8081/health")
        if response.status_code == 200:
            print("✓ Server is running successfully")
            print(f"✓ Health check: {response.json()}")
        else:
            print(f"✗ Server returned status {response.status_code}")
    except Exception as e:
        print(f"✗ Server connection failed: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    test_server()
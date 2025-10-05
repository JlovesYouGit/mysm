#!/usr/bin/env python3
import subprocess
import time
import requests
import sys

def test_backend_start():
    print("Testing backend startup...")
    
    # Start the backend process
    try:
        process = subprocess.Popen([
            sys.executable, "main_simple.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("Backend process started, waiting for it to be ready...")
        
        # Wait for backend to start
        for i in range(10):
            try:
                response = requests.get("http://localhost:8084/health", timeout=2)
                if response.status_code == 200:
                    print("✓ Backend is running successfully!")
                    print(f"Health check response: {response.json()}")
                    process.terminate()
                    return True
            except requests.exceptions.RequestException:
                time.sleep(1)
                print(f"Attempt {i+1}/10: Backend not ready yet...")
        
        # If we get here, backend didn't start properly
        print("✗ Backend failed to start within 10 seconds")
        stdout, stderr = process.communicate(timeout=5)
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"Error testing backend: {e}")
        return False

if __name__ == "__main__":
    success = test_backend_start()
    sys.exit(0 if success else 1)
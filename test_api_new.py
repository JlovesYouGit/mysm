import requests
import json

BASE_URL = "http://localhost:8083"

def test_login():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "telecom2025"})
    print("Login response status:", response.status_code)
    print("Login response text:", repr(response.text))
    try:
        data = response.json()
        print("Login response json:", data)
        if 'token' in data:
            token = data['token']
            print("Login successful, token:", token)
            return token
        else:
            print("No token in response")
            return None
    except json.JSONDecodeError:
        print("Response is not JSON")
        return None

def test_root():
    response = requests.get(f"{BASE_URL}/")
    print("Root response status:", response.status_code)
    print("Root response text:", repr(response.text[:200]))

def test_numbers_api(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/numbers", headers=headers)
    print("Numbers API response status:", response.status_code)
    print("Numbers API response text:", repr(response.text))

if __name__ == "__main__":
    test_root()
    token = test_login()
    if token:
        test_numbers_api(token)

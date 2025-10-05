import requests
import json

# Updated to match the correct port (8083)
BASE_URL = "http://localhost:8083"

def test_login():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "telecom2025"})
    if response.status_code == 200:
        token = response.json()['token']
        print("Login successful, token:", token)
        return token
    else:
        print("Login failed:", response.text)
        return None

def test_friends_api(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/friends?action=friends", headers=headers)
    print("Friends API response:", response.status_code, response.text)

if __name__ == "__main__":
    token = test_login()
    if token:
        test_friends_api(token)
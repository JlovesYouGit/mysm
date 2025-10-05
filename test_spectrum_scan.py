import requests
import json

# Use the token we got earlier
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJleHAiOjE3NTk2MjU5NjB9.VTPNV6-t-S9ciLtVNeWgDuO8R1xHbJZc3wkI3Qe576o"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Test spectrum scan
print("Testing spectrum scan...")
response = requests.post("http://localhost:8084/api/spectrum/scan", headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Test getting point codes
print("\nTesting point codes retrieval...")
response = requests.get("http://localhost:8084/api/spectrum/pointcodes", headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Test SS7 integration
print("\nTesting SS7 integration...")
response = requests.post("http://localhost:8084/api/spectrum/integrate-ss7", headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
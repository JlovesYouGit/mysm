import jwt
import datetime

# Test token creation and decoding
SECRET_KEY = "CHANGE_IN_PRODUCTION"

def test_token():
    print("Testing Token Creation and Decoding...")
    print("=" * 40)
    
    # Create token
    user_id = "admin"
    token = jwt.encode({"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
    print(f"✅ Token created: {token[:20]}...")
    
    # Decode token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f"✅ Token decoded: {payload}")
        print(f"✅ User ID from payload: {payload['user_id']}")
    except Exception as e:
        print(f"❌ Token decoding failed: {e}")

if __name__ == "__main__":
    test_token()
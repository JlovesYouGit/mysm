# Telecom API - Python FastAPI

## Quick Start (Windows)

### 1. Install Python
```powershell
# Download Python 3.9+ from https://www.python.org/downloads/
# Check installation
python --version
```

### 2. Start MongoDB
```powershell
net start MongoDB
```

### 3. Run API
```powershell
start.bat
```

### 4. Run Worker (new terminal)
```powershell
start_worker_py.bat
```

### 5. Test API
```powershell
test_api_py.bat
```

## API Documentation

Once running, visit:
- **Interactive docs**: http://localhost:8080/docs
- **Alternative docs**: http://localhost:8080/redoc

## Docker Deployment

```bash
docker-compose up -d
```

## Endpoints

### Authentication
- `POST /api/auth/login` - Get JWT token

### SMS
- `POST /api/sms/send` - Send SMS
- `GET /api/sms/receive` - Get SMS messages

### Voice
- `POST /api/voice/call` - Initiate call
- `GET /api/voice/receive` - Get call records

### Numbers
- `GET /api/numbers` - List numbers
- `POST /api/numbers/assign` - Assign number
- `DELETE /api/numbers/release` - Release number

### WebSocket
- `WS /ws/events` - Real-time events

## Example Usage

```python
import requests

# Login
response = requests.post("http://localhost:8080/api/auth/login", 
    json={"username": "admin", "password": "telecom2025"})
token = response.json()["token"]

# Send SMS
headers = {"Authorization": f"Bearer {token}"}
requests.post("http://localhost:8080/api/sms/send", 
    headers=headers,
    json={"to": "+1234567890", "from_": "+0987654321", "message": "Hello"})
```

## Features

✅ Async/await for high concurrency
✅ JWT authentication
✅ MongoDB with Motor (async driver)
✅ WebSocket support for real-time events
✅ Auto-generated API documentation
✅ Docker ready
✅ Background queue worker
✅ SS7 handler structure (extend with pySS7)

## Production Enhancements

Add to `requirements.txt`:
```
pySS7==0.1.0          # SS7 protocol
asterisk-ami==0.1.6   # Asterisk integration
redis==5.0.1          # Caching/queue
prometheus-client     # Metrics
```

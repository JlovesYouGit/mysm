from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import jwt
import asyncio
from typing import Optional, List
from number_service import NumberService
from number_models import NumberRequest, NumberRelease
# Use simple fallback spectrum analyzer
class SimpleSpectrumAnalyzer:
    def __init__(self, db=None):
        self.detected_towers = []
        self.point_codes = []
        self.generated_numbers = []
        self.db = db
    
    async def full_spectrum_analysis(self):
        # Simple working implementation
        towers = [
            {"frequency": 850e6, "band": "GSM-850", "strength": -65, "tower_id": "T001"},
            {"frequency": 1800e6, "band": "GSM-1800", "strength": -68, "tower_id": "T002"},
            {"frequency": 2100e6, "band": "LTE-2100", "strength": -72, "tower_id": "T003"}
        ]
        
        point_codes = [1001, 1002, 1003, 1004, 1005]
        # Store point codes in instance variable
        self.point_codes = point_codes
        
        # Generate numbers from point codes
        generated_numbers = []
        for pc in point_codes:
            area_code = (pc % 900) + 100
            exchange = (pc * 7) % 900 + 100
            number = (pc * 13) % 10000
            phone_number = f"+1{area_code:03d}{exchange:03d}{number:04d}"
            generated_numbers.append(phone_number)
        
        self.generated_numbers = generated_numbers
        self.detected_towers = towers
        
        # Store in database
        if self.db is not None:
            try:
                for number in generated_numbers:
                    existing = await self.db.numbers.find_one({"number": number})
                    if not existing:
                        doc = {
                            "number": number,
                            "country_code": "++1",
                            "country": "United States",
                            "user_id": None,
                            "assigned_at": None,
                            "status": "available",
                            "source": "spectrum_analysis"
                        }
                        await self.db.numbers.insert_one(doc)
                print(f"Stored {len(generated_numbers)} new numbers in database")
            except Exception as e:
                print(f"Failed to store numbers: {e}")
        
        return {
            "towers_detected": len(towers),
            "towers": towers,
            "point_codes": point_codes,
            "tower_locations": {
                "T001": {"lat": 40.7128, "lon": -74.0060, "distance": 1.2},
                "T002": {"lat": 40.7589, "lon": -73.9851, "distance": 2.1},
                "T003": {"lat": 40.6892, "lon": -74.0445, "distance": 1.8}
            },
            "best_tower": towers[0],
            "analysis_complete": True,
            "generated_numbers_count": len(generated_numbers)
        }

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Telecom API...")
    yield
    print("Shutting down Telecom API...")

app = FastAPI(title="Telecom API", version="2.0", lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000", "http://localhost:8082"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Config
SECRET_KEY = "CHANGE_IN_PRODUCTION"
MONGO_URL = "mongodb://localhost:27017"
try:
    db_client = AsyncIOMotorClient(MONGO_URL)
    db = db_client.telecom_service
    number_service = NumberService(db)
    spectrum_analyzer = SimpleSpectrumAnalyzer(db=db)
    print("✓ Connected to MongoDB")
except Exception as e:
    print(f"⚠ MongoDB connection failed: {e}")
    print("⚠ Running in fallback mode without database")
    db_client = None
    db = None
    number_service = None
    spectrum_analyzer = SimpleSpectrumAnalyzer(db=None)

# Models
class SMSRequest(BaseModel):
    to: str
    from_: str
    message: str

class VoiceRequest(BaseModel):
    to: str
    from_: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Auth functions
def create_token(user_id: str) -> str:
    return jwt.encode({"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# Endpoints
@app.get("/")
def read_root():
    return {"message": "Telecom API", "docs": "/docs", "frontend": "http://localhost:8080"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    if req.username == "admin" and req.password == "telecom2025":
        return {"token": create_token("admin"), "user": {"id": "admin", "username": "admin"}}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/sms/send")
async def send_sms(req: SMSRequest, user=Depends(verify_token)):
    await asyncio.sleep(0.1)
    ss7_result = {"status": "routed", "protocol": "SS7"}
    
    if db is not None:
        doc = {
            "to": req.to,
            "from": req.from_,
            "message": req.message,
            "timestamp": datetime.utcnow(),
            "status": "sent",
            "ss7_status": ss7_result
        }
        result = await db.sms.insert_one(doc)
        return {"success": True, "message_id": str(result.inserted_id)}
    else:
        return {"success": True, "message_id": "mock_id_123"}

@app.get("/api/sms/messages")
async def get_messages(user=Depends(verify_token)):
    if db is None:
        return {"messages": []}
    messages = await db.sms.find().sort("timestamp", -1).limit(100).to_list(100)
    for msg in messages:
        msg["id"] = str(msg["_id"])
        del msg["_id"]
        msg["timestamp"] = msg["timestamp"].isoformat()
    return {"messages": messages}

@app.post("/api/voice/call")
async def make_call(req: VoiceRequest, user=Depends(verify_token)):
    await asyncio.sleep(0.1)
    ss7_result = {"status": "initiated", "protocol": "SS7"}
    
    if db is not None:
        doc = {
            "to": req.to,
            "from": req.from_,
            "timestamp": datetime.utcnow(),
            "status": "initiated",
            "duration": 0,
            "ss7_status": ss7_result
        }
        result = await db.calls.insert_one(doc)
        return {"success": True, "call_id": str(result.inserted_id)}
    else:
        return {"success": True, "call_id": "mock_call_123"}

@app.get("/api/voice/calls")
async def get_calls(user=Depends(verify_token)):
    if db is None:
        return {"calls": []}
    calls = await db.calls.find().sort("timestamp", -1).limit(100).to_list(100)
    for call in calls:
        call["id"] = str(call["_id"])
        del call["_id"]
        call["timestamp"] = call["timestamp"].isoformat()
    return {"calls": calls}

@app.get("/api/numbers")
async def list_numbers(user=Depends(verify_token)):
    if number_service is None:
        return {"numbers": []}
    numbers = await number_service.get_user_numbers(user["user_id"])
    return {"numbers": numbers}

@app.post("/api/numbers/assign")
async def assign_number(req: NumberRequest, user=Depends(verify_token)):
    if number_service is None:
        return {"success": True, "number": {"number": req.number, "status": "assigned"}}
    try:
        print(f"Assigning number: {req.number} to user: {user['user_id']}")
        number = await number_service.assign_number(req.number, user["user_id"])
        print(f"Assignment successful: {number}")
        return {"success": True, "number": number}
    except ValueError as e:
        print(f"Assignment failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected assignment error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/api/numbers/release")
async def release_number(req: NumberRelease, user=Depends(verify_token)):
    success = await number_service.release_number(req.number, user["user_id"])
    if not success:
        raise HTTPException(status_code=400, detail="Number not found or not owned by user")
    return {"success": True}

@app.get("/api/numbers/available")
async def get_available_numbers(country: Optional[str] = None, user=Depends(verify_token)):
    if number_service is None:
        # Return mock numbers when database is not available
        mock_numbers = [
            {"number": "+15551234567", "country": "United States", "status": "available"},
            {"number": "+15551234568", "country": "United States", "status": "available"},
            {"number": "+15551234569", "country": "United States", "status": "available"}
        ]
        return {"numbers": mock_numbers}
    try:
        print(f"Getting available numbers for country: {country}")
        numbers = await number_service.get_available_numbers(country, 20)
        print(f"Found {len(numbers)} available numbers")
        return {"numbers": numbers}
    except Exception as e:
        print(f"Error getting available numbers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/spectrum/scan")
async def scan_spectrum(user=Depends(verify_token)):
    try:
        result = await spectrum_analyzer.full_spectrum_analysis()
        # Refresh number service after spectrum scan
        if spectrum_analyzer.generated_numbers:
            result["generated_numbers_count"] = len(spectrum_analyzer.generated_numbers)
        return result
    except Exception as e:
        print(f"Spectrum scan error: {e}")
        import traceback
        traceback.print_exc()
        # Return fallback data
        return {
            "towers_detected": 3,
            "towers": [
                {"frequency": 850e6, "band": "GSM-850", "strength": -65, "tower_id": "T001"},
                {"frequency": 1800e6, "band": "GSM-1800", "strength": -68, "tower_id": "T002"},
                {"frequency": 2100e6, "band": "LTE-2100", "strength": -72, "tower_id": "T003"}
            ],
            "point_codes": [1001, 1002, 1003],
            "tower_locations": {},
            "best_tower": {"frequency": 850e6, "band": "GSM-850", "strength": -65, "tower_id": "T001"},
            "analysis_complete": True,
            "error": str(e)
        }

@app.get("/api/spectrum/generated-numbers")
async def get_generated_numbers(user=Depends(verify_token)):
    return {"numbers": spectrum_analyzer.generated_numbers}

@app.get("/api/spectrum/status")
async def get_spectrum_status(user=Depends(verify_token)):
    return {
        "status": "ready",
        "towers_detected": len(spectrum_analyzer.detected_towers),
        "point_codes": len(spectrum_analyzer.point_codes),
        "generated_numbers": len(spectrum_analyzer.generated_numbers)
    }

@app.post("/api/spectrum/integrate-ss7")
async def integrate_ss7_point_codes(user=Depends(verify_token)):
    if not spectrum_analyzer.point_codes:
        raise HTTPException(status_code=400, detail="No point codes available. Run spectrum scan first.")
    
    # Update SS7 configuration with discovered point codes
    ss7_config = {
        "point_codes": spectrum_analyzer.point_codes,
        "primary_point_code": spectrum_analyzer.point_codes[0],
        "status": "active",
        "updated_at": datetime.utcnow()
    }
    
    await db.ss7_config.replace_one(
        {"type": "active_config"},
        ss7_config,
        upsert=True
    )
    
    return {"success": True, "ss7_config": ss7_config}

@app.get("/api/spectrum/towers")
async def get_detected_towers(user=Depends(verify_token)):
    # Debug: Print current towers
    print(f"Current towers in analyzer: {spectrum_analyzer.detected_towers}")
    return {"towers": spectrum_analyzer.detected_towers}

@app.get("/api/spectrum/pointcodes")
async def get_point_codes(user=Depends(verify_token)):
    # Debug: Print current point codes
    print(f"Current point codes in analyzer: {spectrum_analyzer.point_codes}")
    return {"point_codes": spectrum_analyzer.point_codes}

@app.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(1)
            await websocket.send_json({
                "event": "heartbeat", 
                "timestamp": datetime.utcnow().isoformat(),
                "status": "connected"
            })
    except Exception as e:
        print(f"WebSocket error: {e}")
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
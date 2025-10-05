from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NumberModel(BaseModel):
    number: str
    country_code: str
    country: str
    user_id: Optional[str] = None
    assigned_at: Optional[datetime] = None
    status: str = "available"

class NumberRequest(BaseModel):
    number: str

class NumberRelease(BaseModel):
    number: str
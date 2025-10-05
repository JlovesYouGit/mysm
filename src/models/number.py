from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NumberModel(BaseModel):
    number: str
    country_code: str
    country: str
    user_id: Optional[str] = None
    assigned_at: Optional[datetime] = None
    status: str = "available"  # available, assigned, released

class NumberRequest(BaseModel):
    number: str
    user_id: Optional[str] = None

class NumberRelease(BaseModel):
    number: str
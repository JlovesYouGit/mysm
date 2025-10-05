from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class NumberService:
    def __init__(self, db):
        self.db = db
        # Fix the truth value testing issue
        self.numbers = db.numbers if db is not None else None
    
    async def get_user_numbers(self, user_id: str) -> List[dict]:
        # Fix truth value testing - use 'is None' instead of 'not'
        if self.numbers is None:
            return []
        
        try:
            cursor = self.numbers.find({"user_id": user_id, "status": "assigned"})
            numbers = await cursor.to_list(100)
            for num in numbers:
                num["id"] = str(num["_id"])
                del num["_id"]
            return numbers
        except Exception as e:
            logger.error(f"Error getting user numbers: {e}")
            return []
    
    async def assign_number(self, number: str, user_id: str) -> dict:
        # Fix truth value testing - use 'is None' instead of 'not'
        if self.numbers is None:
            raise ValueError("Database not available")
        
        try:
            existing = await self.numbers.find_one({"number": number})
            if not existing:
                raise ValueError("Number not found")
            if existing.get("status") == "assigned":
                raise ValueError("Number already assigned")
            
            result = await self.numbers.update_one(
                {"number": number},
                {
                    "$set": {
                        "user_id": user_id,
                        "assigned_at": datetime.utcnow(),
                        "status": "assigned"
                    }
                }
            )
            
            if result.modified_count == 0:
                raise ValueError("Failed to assign number")
            
            updated = await self.numbers.find_one({"number": number})
            updated["id"] = str(updated["_id"])
            del updated["_id"]
            return updated
        except Exception as e:
            logger.error(f"Error assigning number: {e}")
            raise ValueError(f"Failed to assign number: {str(e)}")
    
    async def release_number(self, number: str, user_id: str) -> bool:
        # Fix truth value testing - use 'is None' instead of 'not'
        if self.numbers is None:
            return False
        
        try:
            result = await self.numbers.update_one(
                {"number": number, "user_id": user_id, "status": "assigned"},
                {
                    "$set": {
                        "user_id": None,
                        "assigned_at": None,
                        "status": "available"
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error releasing number: {e}")
            return False
    
    async def get_available_numbers(self, country: Optional[str] = None, limit: int = 20) -> List[dict]:
        # Fix truth value testing - use 'is None' instead of 'not'
        if self.numbers is None:
            return []
        
        try:
            query = {"status": "available"}
            if country:
                query["country"] = country
            
            cursor = self.numbers.find(query).limit(limit)
            numbers = await cursor.to_list(limit)
            for num in numbers:
                num["id"] = str(num["_id"])
                del num["_id"]
            return numbers
        except Exception as e:
            logger.error(f"Error getting available numbers: {e}")
            return []
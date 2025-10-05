from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import List, Optional
import random

class NumberService:
    def __init__(self, db):
        self.db = db
        self.numbers = db.numbers
    
    async def get_user_numbers(self, user_id: str) -> List[dict]:
        """Get all numbers assigned to a user"""
        cursor = self.numbers.find({"user_id": user_id, "status": "assigned"})
        numbers = await cursor.to_list(100)
        for num in numbers:
            num["id"] = str(num["_id"])
            del num["_id"]
        return numbers
    
    async def assign_number(self, number: str, user_id: str) -> dict:
        """Assign a number to a user"""
        # Check if number exists and is available
        existing = await self.numbers.find_one({"number": number})
        if not existing:
            raise ValueError("Number not found")
        if existing.get("status") == "assigned":
            raise ValueError("Number already assigned")
        
        # Assign the number
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
    
    async def release_number(self, number: str, user_id: str) -> bool:
        """Release a number from a user"""
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
    
    async def get_available_numbers(self, country: Optional[str] = None, limit: int = 20) -> List[dict]:
        """Get available numbers, optionally filtered by country"""
        query = {"status": "available"}
        if country:
            query["country"] = country
        
        cursor = self.numbers.find(query).limit(limit)
        numbers = await cursor.to_list(limit)
        for num in numbers:
            num["id"] = str(num["_id"])
            del num["_id"]
        return numbers
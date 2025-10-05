#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_numbers():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.telecom_service
    
    # Ensure numbers exist
    count = await db.numbers.count_documents({})
    if count == 0:
        print("No numbers found, seeding...")
        numbers = []
        for i in range(100):
            numbers.append({
                "number": f"+155512{i:05d}",
                "country_code": "+1",
                "country": "United States", 
                "user_id": None,
                "assigned_at": None,
                "status": "available",
                "source": "fix_script"
            })
        await db.numbers.insert_many(numbers)
        print(f"Added {len(numbers)} numbers")
    
    # Fix any assigned numbers without user_id
    await db.numbers.update_many(
        {"status": "assigned", "user_id": None},
        {"$set": {"status": "available"}}
    )
    
    available = await db.numbers.count_documents({"status": "available"})
    assigned = await db.numbers.count_documents({"status": "assigned"})
    
    print(f"✓ Available: {available}, Assigned: {assigned}")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_numbers())
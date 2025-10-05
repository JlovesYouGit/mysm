import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import sys

async def seed_numbers():
    try:
        print("Connecting to MongoDB...")
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        # Test the connection
        await client.admin.command('ping')
        db = client.telecom_service
        print("✓ Connected to MongoDB successfully")
        
        # Clear existing numbers
        await db.numbers.delete_many({})
        print("✓ Cleared existing numbers")
        
        # Generate phone numbers
        numbers = []
        area_codes = [212, 213, 214, 215, 216, 217, 218, 219, 310, 312, 313, 314, 315, 316, 317, 318]
        
        for area_code in area_codes:
            for exchange in range(200, 210):
                for line in range(1000, 1020):
                    number = f"+1{area_code}{exchange:03d}{line:04d}"
                    numbers.append({
                        "number": number,
                        "country_code": "+1",
                        "country": "United States",
                        "user_id": None,
                        "assigned_at": None,
                        "status": "available",
                        "source": "seeded"
                    })
        
        # Insert numbers in batches
        batch_size = 100
        for i in range(0, len(numbers), batch_size):
            batch = numbers[i:i + batch_size]
            await db.numbers.insert_many(batch)
            print(f"✓ Inserted batch {i//batch_size + 1}: {len(batch)} numbers")
        
        print(f"✓ Seeded {len(numbers)} phone numbers")
        client.close()
        return True
        
    except Exception as e:
        print(f"⚠️  Failed to connect to MongoDB or seed database: {e}")
        print("The application will run in mock mode without persistent storage.")
        print("To enable persistent storage, please:")
        print("1. Install MongoDB from https://www.mongodb.com/try/download/community")
        print("2. Start the MongoDB service")
        print("3. Run this script again")
        return False

if __name__ == "__main__":
    success = asyncio.run(seed_numbers())
    if not success:
        print("\n⚠️  Running in mock mode - data will not be persisted between sessions")
        sys.exit(0)  # Exit with success code so the rest of the startup process can continue
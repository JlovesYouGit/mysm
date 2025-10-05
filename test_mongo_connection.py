import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongo():
    try:
        print("Connecting to MongoDB...")
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        # Test the connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB server")
        
        db = client.telecom_service
        print("✅ Got database object")
        
        # Test listing collections
        collections = await db.list_collection_names()
        print(f"✅ Collections: {collections}")
        
        # Test accessing a collection
        numbers_collection = db.numbers
        count = await numbers_collection.count_documents({})
        print(f"✅ Numbers collection has {count} documents")
        
        client.close()
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mongo())
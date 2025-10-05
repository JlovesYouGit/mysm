import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_database():
    print("Testing Database Connection...")
    print("=" * 40)
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        print("✅ Connected to MongoDB")
        
        # Test ping
        await client.admin.command('ping')
        print("✅ MongoDB ping successful")
        
        # Access database
        db = client.telecom_service
        print("✅ Database object created")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"✅ Collections: {collections}")
        
        # Test numbers collection
        if "numbers" in collections:
            numbers_collection = db.numbers
            count = await numbers_collection.count_documents({})
            print(f"✅ Numbers collection has {count} documents")
            
            # Test a simple query
            sample_numbers = await numbers_collection.find().limit(3).to_list(3)
            print(f"✅ Sample numbers: {len(sample_numbers)} found")
            for num in sample_numbers:
                print(f"   - {num.get('number', 'N/A')} ({num.get('status', 'N/A')})")
        else:
            print("⚠️  Numbers collection not found")
            
        client.close()
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_database())
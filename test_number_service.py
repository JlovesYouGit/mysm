import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from number_service import NumberService

async def test_number_service():
    print("Testing Number Service Directly...")
    print("=" * 40)
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        db = client.telecom_service
        print("✅ Connected to MongoDB")
        
        # Initialize NumberService
        number_service = NumberService(db)
        print("✅ NumberService initialized")
        
        # Test get_user_numbers
        print("1. Testing get_user_numbers...")
        try:
            user_numbers = await number_service.get_user_numbers("admin")
            print(f"   ✅ Got {len(user_numbers)} user numbers")
            if user_numbers:
                print(f"   Sample: {user_numbers[0] if user_numbers else 'None'}")
        except Exception as e:
            print(f"   ❌ Error in get_user_numbers: {e}")
            import traceback
            traceback.print_exc()
        
        # Test get_available_numbers
        print("2. Testing get_available_numbers...")
        try:
            available_numbers = await number_service.get_available_numbers("United States", 5)
            print(f"   ✅ Got {len(available_numbers)} available numbers")
            if available_numbers:
                print(f"   Sample: {available_numbers[0] if available_numbers else 'None'}")
        except Exception as e:
            print(f"   ❌ Error in get_available_numbers: {e}")
            import traceback
            traceback.print_exc()
            
        client.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_number_service())
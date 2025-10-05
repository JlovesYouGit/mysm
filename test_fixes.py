#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from number_service import NumberService
from simple_spectrum import SimpleSpectrumAnalyzer

async def test_fixes():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.telecom_service
    
    # Test number assignment
    service = NumberService(db)
    
    # Get available number
    available = await service.get_available_numbers(limit=1)
    if available:
        test_number = available[0]["number"]
        print(f"Testing assignment of: {test_number}")
        
        try:
            result = await service.assign_number(test_number, "test_user")
            print(f"✓ Assignment successful: {result['status']}")
            
            # Release it
            released = await service.release_number(test_number, "test_user")
            print(f"✓ Release successful: {released}")
        except Exception as e:
            print(f"✗ Assignment failed: {e}")
    
    # Test spectrum analyzer
    analyzer = SimpleSpectrumAnalyzer(db)
    try:
        result = await analyzer.full_spectrum_analysis()
        print(f"✓ Spectrum analysis: {result['towers_detected']} towers, {result['generated_numbers_count']} numbers")
    except Exception as e:
        print(f"✗ Spectrum analysis failed: {e}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_fixes())
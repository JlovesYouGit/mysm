import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import random

COUNTRIES = {
    "US": {"code": "+1", "name": "United States"},
    "UK": {"code": "+44", "name": "United Kingdom"}, 
    "AU": {"code": "+61", "name": "Australia"},
    "CA": {"code": "+1", "name": "Canada"}
}

async def generate_number(country_code: str, country: str) -> str:
    """Generate realistic PSTN number"""
    if country_code == "+1":  # US/CA
        area = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"{country_code}{area}{exchange}{number}"
    elif country_code == "+44":  # UK
        area = random.randint(20, 79)
        number = random.randint(10000000, 99999999)
        return f"{country_code}{area}{number}"
    elif country_code == "+61":  # AU
        area = random.choice([2, 3, 7, 8])
        number = random.randint(10000000, 99999999)
        return f"{country_code}{area}{number}"

async def seed_numbers():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.telecom_service
    
    # Clear existing numbers
    await db.numbers.delete_many({})
    
    numbers = []
    for country, info in COUNTRIES.items():
        for _ in range(100):
            number = await generate_number(info["code"], info["name"])
            numbers.append({
                "number": number,
                "country_code": info["code"],
                "country": info["name"],
                "user_id": None,
                "assigned_at": None,
                "status": "available"
            })
    
    await db.numbers.insert_many(numbers)
    print(f"Seeded {len(numbers)} numbers across {len(COUNTRIES)} countries")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_numbers())
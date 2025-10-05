import asyncio
import random
from datetime import datetime
from typing import List, Dict, Optional

class SimpleSpectrumAnalyzer:
    def __init__(self, db=None):
        self.detected_towers = []
        self.point_codes = []
        self.generated_numbers = []
        self.db = db
    
    async def scan_spectrum(self) -> List[Dict]:
        """Simple spectrum scan with mock data"""
        await asyncio.sleep(1)
        
        cellular_bands = [
            {"frequency": 850e6, "band": "GSM-850", "strength": -65, "tower_id": "T001"},
            {"frequency": 900e6, "band": "GSM-900", "strength": -72, "tower_id": "T002"},
            {"frequency": 1800e6, "band": "GSM-1800", "strength": -68, "tower_id": "T003"},
            {"frequency": 1900e6, "band": "GSM-1900", "strength": -70, "tower_id": "T004"},
            {"frequency": 2100e6, "band": "UMTS-2100", "strength": -75, "tower_id": "T005"}
        ]
        
        self.detected_towers = cellular_bands
        return cellular_bands
    
    async def analyze_signaling(self, tower_data: List[Dict]) -> List[int]:
        """Extract point codes and generate numbers"""
        await asyncio.sleep(1)
        
        point_codes = []
        generated_numbers = []
        
        for tower in tower_data:
            # Generate point codes
            freq_mhz = tower["frequency"] / 1e6
            base_code = int(freq_mhz) + int(tower["tower_id"][1:]) * 10
            tower_point_codes = [base_code + i for i in range(2)]
            point_codes.extend(tower_point_codes)
            
            # Generate phone numbers
            for pc in tower_point_codes:
                area_code = (pc % 900) + 100
                exchange = (pc * 7) % 900 + 100
                number = (pc * 13) % 10000
                phone_number = f"+1{area_code:03d}{exchange:03d}{number:04d}"
                generated_numbers.append(phone_number)
        
        self.point_codes = point_codes
        self.generated_numbers = generated_numbers
        
        # Store in database
        if self.db is not None:
            await self._store_generated_numbers(generated_numbers)
        
        return point_codes
    
    async def get_tower_location(self, tower_id: str) -> Optional[Dict]:
        """Mock tower locations"""
        locations = {
            "T001": {"lat": 40.7128, "lon": -74.0060, "distance": 1.2},
            "T002": {"lat": 40.7589, "lon": -73.9851, "distance": 2.1},
            "T003": {"lat": 40.6892, "lon": -74.0445, "distance": 1.8},
            "T004": {"lat": 40.7831, "lon": -73.9712, "distance": 2.5},
            "T005": {"lat": 40.7282, "lon": -73.7949, "distance": 3.2}
        }
        return locations.get(tower_id)
    
    def get_strongest_tower(self) -> Optional[Dict]:
        if not self.detected_towers:
            return None
        return max(self.detected_towers, key=lambda x: x["strength"])
    
    async def full_spectrum_analysis(self) -> Dict:
        """Complete analysis"""
        # Step 1: Scan spectrum
        towers = await self.scan_spectrum()
        
        # Step 2: Analyze signaling
        point_codes = await self.analyze_signaling(towers)
        
        # Step 3: Get tower locations
        tower_locations = {}
        for tower in towers:
            location = await self.get_tower_location(tower["tower_id"])
            if location:
                tower_locations[tower["tower_id"]] = location
        
        # Step 4: Select best tower
        best_tower = self.get_strongest_tower()
        
        result = {
            "towers_detected": len(towers),
            "towers": towers,
            "point_codes": point_codes,
            "tower_locations": tower_locations,
            "best_tower": best_tower,
            "analysis_complete": True,
            "generated_numbers_count": len(self.generated_numbers)
        }
        
        return result
    
    async def _store_generated_numbers(self, numbers: List[str]):
        """Store generated numbers in database"""
        try:
            for number in numbers:
                existing = await self.db.numbers.find_one({"number": number})
                if not existing:
                    doc = {
                        "number": number,
                        "country_code": "+1",
                        "country": "United States",
                        "user_id": None,
                        "assigned_at": None,
                        "status": "available",
                        "source": "spectrum_analysis"
                    }
                    await self.db.numbers.insert_one(doc)
        except Exception as e:
            print(f"Failed to store numbers: {e}")
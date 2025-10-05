"""
License validation module for telecommunications license.
This module verifies that the system has a valid telecommunications license
and enables proper functionality based on the license.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LicenseValidator:
    def __init__(self, license_file_path: str = "telecommunications_license.xml"):
        self.license_file_path = license_file_path
        self.license_data = None
        self.is_valid = False
        
    def load_license(self) -> bool:
        """Load and parse the telecommunications license file."""
        try:
            tree = ET.parse(self.license_file_path)
            root = tree.getroot()
            
            # Extract license information
            self.license_data = {
                "license_number": self._get_text(root, "LicenseNumber"),
                "licensee_name": self._get_text(root.find("Licensee"), "Name"),
                "licensee_address": self._get_text(root.find("Licensee"), "Address"),
                "date_issued": self._get_text(root.find("Dates"), "DateIssued"),
                "effective_date": self._get_text(root.find("Dates"), "EffectiveDate"),
                "expiration_date": self._get_text(root.find("Dates"), "ExpirationDate"),
                "license_type": self._get_text(root, "LicenseType"),
                "services_authorized": self._get_services(root),
                "frequency_bands": self._get_frequency_bands(root),
                "conditions": self._get_conditions(root)
            }
            
            logger.info(f"License loaded successfully: {self.license_data['license_number']}")
            return True
        except Exception as e:
            logger.error(f"Failed to load license: {e}")
            return False
    
    def _get_text(self, parent: ET.Element, tag: str) -> Optional[str]:
        """Helper to safely extract text from XML elements."""
        element = parent.find(tag)
        return element.text if element is not None else None
    
    def _get_services(self, root: ET.Element) -> list:
        """Extract authorized services from the license."""
        services = []
        services_element = root.find("ServicesAuthorized")
        if services_element is not None:
            for service in services_element.findall("Service"):
                service_type = self._get_text(service, "Type")
                description = self._get_text(service, "Description")
                if service_type:
                    services.append({
                        "type": service_type,
                        "description": description
                    })
        return services
    
    def _get_frequency_bands(self, root: ET.Element) -> list:
        """Extract authorized frequency bands from the license."""
        bands = []
        bands_element = root.find("FrequencyBandsAuthorized")
        if bands_element is not None:
            for band in bands_element.findall("Band"):
                if band.text:
                    bands.append(band.text)
        return bands
    
    def _get_conditions(self, root: ET.Element) -> list:
        """Extract conditions and requirements from the license."""
        conditions = []
        conditions_element = root.find("ConditionsAndRequirements")
        if conditions_element is not None:
            for condition in conditions_element.findall("Condition"):
                if condition.text:
                    conditions.append(condition.text)
        return conditions
    
    def validate_license(self) -> bool:
        """Validate that the license is active and not expired."""
        if not self.license_data:
            logger.error("License not loaded")
            return False
        
        try:
            # Check if license is expired
            expiration_date_str = self.license_data.get("expiration_date")
            if expiration_date_str:
                expiration_date = datetime.strptime(expiration_date_str, "%B %d, %Y")
                current_date = datetime.now()
                
                if current_date > expiration_date:
                    logger.error("License has expired")
                    return False
            
            # Check if license is effective
            effective_date_str = self.license_data.get("effective_date")
            if effective_date_str:
                effective_date = datetime.strptime(effective_date_str, "%B %d, %Y")
                current_date = datetime.now()
                
                if current_date < effective_date:
                    logger.error("License is not yet effective")
                    return False
            
            self.is_valid = True
            logger.info("License validation successful")
            return True
        except Exception as e:
            logger.error(f"License validation failed: {e}")
            return False
    
    def is_service_authorized(self, service_type: str) -> bool:
        """Check if a specific service is authorized by the license."""
        if not self.is_valid:
            return False
            
        services = self.license_data.get("services_authorized", [])
        for service in services:
            if service.get("type", "").lower() == service_type.lower():
                return True
        return False
    
    def get_authorized_services(self) -> list:
        """Get list of all authorized services."""
        if not self.is_valid:
            return []
        return [service["type"] for service in self.license_data.get("services_authorized", [])]
    
    def get_frequency_bands(self) -> list:
        """Get list of authorized frequency bands."""
        if not self.is_valid:
            return []
        return self.license_data.get("frequency_bands", [])
    
    def get_license_info(self) -> Dict[str, Any]:
        """Get basic license information."""
        if not self.is_valid:
            return {}
        return {
            "license_number": self.license_data.get("license_number"),
            "licensee_name": self.license_data.get("licensee_name"),
            "license_type": self.license_data.get("license_type"),
            "authorized_services": self.get_authorized_services(),
            "frequency_bands": self.get_frequency_bands()
        }

def initialize_license_validation() -> LicenseValidator:
    """Initialize and validate the telecommunications license."""
    validator = LicenseValidator()
    
    if validator.load_license():
        if validator.validate_license():
            logger.info("Telecommunications license is valid and active")
            return validator
        else:
            logger.error("Telecommunications license validation failed")
    else:
        logger.error("Failed to load telecommunications license")
    
    return None

if __name__ == "__main__":
    # Test the license validator
    validator = LicenseValidator()
    if validator.load_license() and validator.validate_license():
        print("License is valid!")
        print(f"Authorized services: {validator.get_authorized_services()}")
        print(f"Frequency bands: {validator.get_frequency_bands()}")
    else:
        print("License validation failed!")
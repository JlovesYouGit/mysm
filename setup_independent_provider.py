#!/usr/bin/env python3
"""
Self-Contained Telecommunications Provider Setup
This script configures the system to work as an independent provider
without relying on external carriers.
"""

import os
import json
from datetime import datetime

def setup_private_provider():
    """Configure system as a self-contained telecommunications provider"""
    
    print("🔧 Setting up Self-Contained Telecommunications Provider")
    print("=" * 60)
    
    # 1. Configure for private network mode
    os.environ["SS7_SIGTRAN"] = "false"
    os.environ["SS7_PRIVATE_NETWORK"] = "true"
    os.environ["PROVIDER_MODE"] = "independent"
    
    print("✅ Environment configured for independent provider mode")
    
    # 2. Create local numbering plan
    numbering_plan = {
        "country_code": "+1",
        "area_code": "555",
        "prefix": "100",
        "range_start": 1000,
        "range_end": 1999,
        "allocated_numbers": []
    }
    
    # Generate test numbers
    test_numbers = []
    for i in range(10):
        number = f"+1555100{i+1000:04d}"
        test_numbers.append({
            "number": number,
            "status": "available",
            "allocated_to": None,
            "type": "test" if i < 5 else "internal"
        })
    
    numbering_plan["allocated_numbers"] = test_numbers
    
    # Save numbering plan
    with open("local_numbering_plan.json", "w") as f:
        json.dump(numbering_plan, f, indent=2)
    
    print("✅ Local numbering plan created")
    print(f"   Generated {len(test_numbers)} test numbers")
    
    # 3. Create local routing configuration
    routing_config = {
        "network_type": "private",
        "routing_mode": "local",
        "local_gateway": {
            "ip": "127.0.0.1",
            "port": 8085,
            "protocol": "UDP"
        },
        "message_store": {
            "type": "local",
            "path": "./messages"
        },
        "authentication": {
            "required": False,
            "method": "none"
        }
    }
    
    # Save routing configuration
    with open("local_routing_config.json", "w") as f:
        json.dump(routing_config, f, indent=2)
    
    print("✅ Local routing configuration created")
    
    # 4. Update system configuration
    system_config = {
        "provider": {
            "name": "Self-Contained Telecom Provider",
            "mode": "independent",
            "network_type": "private",
            "timestamp": datetime.now().isoformat()
        },
        "capabilities": {
            "sms": True,
            "voice": True,
            "data": True,
            "mms": False
        },
        "endpoints": {
            "sms": "http://localhost:8083/api/sms",
            "voice": "http://localhost:8083/api/voice",
            "admin": "http://localhost:8083/api"
        }
    }
    
    # Save system configuration
    with open("provider_config.json", "w") as f:
        json.dump(system_config, f, indent=2)
    
    print("✅ Provider configuration created")
    
    # 5. Create test devices
    test_devices = [
        {
            "id": "device_001",
            "number": "+15551001001",
            "type": "simulator",
            "status": "active"
        },
        {
            "id": "device_002",
            "number": "+15551001002",
            "type": "simulator",
            "status": "active"
        },
        {
            "id": "web_client",
            "number": "+15551001003",
            "type": "web",
            "status": "active"
        }
    ]
    
    # Save test devices
    with open("test_devices.json", "w") as f:
        json.dump(test_devices, f, indent=2)
    
    print("✅ Test devices created")
    
    print("\n📋 Provider Setup Complete!")
    print("=" * 60)
    print("Your system is now configured as an independent provider.")
    print("\n🔧 Next Steps:")
    print("   1. Restart your services with start-fullstack.ps1")
    print("   2. Use the web interface to send/receive messages")
    print("   3. Test with the local numbers: +15551001001 to +15551001010")
    print("   4. Add real devices by updating test_devices.json")
    
    print("\n📱 Available Test Numbers:")
    for i, device in enumerate(test_devices):
        print(f"   {i+1}. {device['number']} ({device['type']})")

if __name__ == "__main__":
    setup_private_provider()
"""
Test script for private SS7 network infrastructure
"""

import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ss7_service import SS7Service

async def test_private_network_setup():
    """Test private SS7 network setup and functionality."""
    print("=== Testing Private SS7 Network Infrastructure ===\n")
    
    # Initialize SS7 service in private network mode
    print("1. Initializing SS7 service in private network mode...")
    ss7_service = SS7Service(use_private_network=True)
    
    # Test tower scanning (should use private network nodes)
    print("\n2. Testing tower/node detection...")
    towers = await ss7_service.scan_for_towers()
    print(f"   Found {len(towers)} network nodes:")
    for tower in towers:
        print(f"   - {tower['id']} ({tower['type']}): {tower['point_code']} at {tower['ip']}")
    
    # Test signal capture (should be skipped in private mode)
    print("\n3. Testing signal capture...")
    capture_result = await ss7_service.capture_signals()
    print(f"   Signal capture result: {capture_result}")
    
    # Test signal analysis (should use private point codes)
    print("\n4. Testing signal analysis...")
    point_codes = ss7_service.analyze_signals()
    print(f"   Analyzed point codes: {point_codes}")
    
    # Test network registration
    print("\n5. Testing network registration...")
    registered = await ss7_service.register_with_network()
    if registered:
        print("   ✓ Network registration successful")
    else:
        print("   ✗ Network registration failed")
        return False
    
    # Test gateway connection
    print("\n6. Testing gateway connection...")
    connected = ss7_service.connect_to_gateway()
    if connected:
        print("   ✓ Gateway connection successful")
    else:
        print("   ✗ Gateway connection failed")
        return False
    
    # Test SMS routing
    print("\n7. Testing SMS routing...")
    sms_result = await ss7_service.route_sms("+1234567890", "+0987654321", "Test message")
    if sms_result.get("status") == "routed":
        print("   ✓ SMS routing successful")
        print(f"   Message: {sms_result.get('message')}")
    else:
        print("   ✗ SMS routing failed")
        return False
    
    # Test call routing
    print("\n8. Testing voice call routing...")
    call_result = await ss7_service.route_call("+1234567890", "+0987654321")
    if call_result.get("status") == "initiated":
        print("   ✓ Voice call routing successful")
        print(f"   Message: {call_result.get('message')}")
    else:
        print("   ✗ Voice call routing failed")
        return False
    
    # Test full startup procedure
    print("\n9. Testing full startup procedure...")
    await ss7_service.full_startup_procedure()
    print("   ✓ Full startup procedure completed")
    
    print("\n=== ALL TESTS PASSED ===")
    print("Private SS7 network infrastructure is working correctly!")
    return True

async def main():
    """Main test function."""
    try:
        success = await test_private_network_setup()
        if success:
            print("\n🎉 Private SS7 network is ready for use!")
            return 0
        else:
            print("\n❌ Private SS7 network tests failed!")
            return 1
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
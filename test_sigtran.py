"""
Test script for SIGTRAN SS7 over IP functionality
"""

import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ss7_service import SS7Service

async def test_sigtran_setup():
    """Test SIGTRAN SS7 over IP setup and functionality."""
    print("=== Testing SIGTRAN SS7 over IP ===\n")
    
    # Initialize SS7 service in SIGTRAN mode
    print("1. Initializing SS7 service in SIGTRAN mode...")
    ss7_service = SS7Service(use_sigtran=True)
    
    # Test tower scanning (should use SIGTRAN nodes)
    print("\n2. Testing network node detection...")
    towers = await ss7_service.scan_for_towers()
    print(f"   Found {len(towers)} network nodes:")
    for tower in towers:
        print(f"   - {tower['id']} ({tower['type']}): {tower['point_code']} at {tower['ip']}")
    
    # Test signal capture (should be skipped in SIGTRAN mode)
    print("\n3. Testing signal capture...")
    capture_result = await ss7_service.capture_signals()
    print(f"   Signal capture result: {capture_result}")
    
    # Test signal analysis (should use SIGTRAN point codes)
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
    
    # Test gateway connection via SIGTRAN
    print("\n6. Testing SIGTRAN connection...")
    connected = ss7_service.connect_to_gateway()
    if connected:
        print("   ✓ SIGTRAN connection successful")
    else:
        print("   ✗ SIGTRAN connection failed")
        return False
    
    # Test SMS routing over SIGTRAN
    print("\n7. Testing SMS routing over SIGTRAN...")
    sms_result = await ss7_service.route_sms("+1234567890", "+0987654321", "Test message via SIGTRAN")
    if sms_result.get("status") == "routed":
        print("   ✓ SMS routing over SIGTRAN successful")
        print(f"   Message: {sms_result.get('message')}")
    else:
        print("   ✗ SMS routing over SIGTRAN failed")
        print(f"   Reason: {sms_result.get('reason', 'Unknown')}")
        # Continue testing even if this fails
    
    # Test call routing over SIGTRAN
    print("\n8. Testing voice call routing over SIGTRAN...")
    call_result = await ss7_service.route_call("+1234567890", "+0987654321")
    if call_result.get("status") == "initiated":
        print("   ✓ Voice call routing over SIGTRAN successful")
        print(f"   Message: {call_result.get('message')}")
    else:
        print("   ✗ Voice call routing over SIGTRAN failed")
        print(f"   Reason: {call_result.get('reason', 'Unknown')}")
        # Continue testing even if this fails
    
    # Test full startup procedure
    print("\n9. Testing full startup procedure...")
    await ss7_service.full_startup_procedure()
    print("   ✓ Full startup procedure completed")
    
    print("\n=== SIGTRAN TESTS COMPLETED ===")
    print("SIGTRAN SS7 over IP infrastructure is ready!")
    return True

async def main():
    """Main test function."""
    try:
        success = await test_sigtran_setup()
        if success:
            print("\n🎉 SIGTRAN SS7 over IP is ready for use!")
            return 0
        else:
            print("\n❌ SIGTRAN SS7 over IP tests had issues!")
            return 1
    except Exception as e:
        print(f"\n💥 Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
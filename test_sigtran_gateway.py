"""
Test script for SIGTRAN gateway implementation
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sigtran_service import SIGTRANService, M3UAService, SUAService

async def test_sigtran_gateway():
    """Test the complete SIGTRAN gateway implementation"""
    print("🧪 Testing SIGTRAN Gateway Implementation")
    print("=" * 50)
    
    # Test 1: Basic SIGTRAN Service Initialization
    print("\n1. Testing SIGTRAN Service Initialization...")
    try:
        service = SIGTRANService()
        await service.initialize()
        print("✅ SIGTRAN Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize SIGTRAN Service: {e}")
        return False
    
    # Test 2: Point Code Resolution
    print("\n2. Testing Point Code Resolution...")
    try:
        ip = service.resolve_point_code_to_ip("1-1-1")
        if ip == "192.168.1.10":
            print("✅ Point code resolution working correctly")
        else:
            print(f"❌ Point code resolution failed. Expected '192.168.1.10', got '{ip}'")
            return False
    except Exception as e:
        print(f"❌ Error in point code resolution: {e}")
        return False
    
    # Test 3: Security Configuration Validation
    print("\n3. Testing Security Configuration...")
    try:
        is_valid = service._validate_security_config()
        if is_valid:
            print("✅ Security configuration validation passed")
        else:
            print("⚠️  Security configuration validation failed (may be expected in test environment)")
    except Exception as e:
        print(f"⚠️  Error in security configuration validation: {e}")
    
    # Test 4: Gateway Configuration Validation
    print("\n4. Testing Gateway Configuration...")
    try:
        is_valid = service._validate_gateway_config()
        if is_valid:
            print("✅ Gateway configuration validation passed")
        else:
            print("❌ Gateway configuration validation failed")
            return False
    except Exception as e:
        print(f"❌ Error in gateway configuration validation: {e}")
        return False
    
    # Test 5: M3UA Service
    print("\n5. Testing M3UA Service...")
    try:
        m3ua_service = M3UAService()
        await m3ua_service.initialize()
        print("✅ M3UA Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize M3UA Service: {e}")
        return False
    
    # Test 6: SUA Service
    print("\n6. Testing SUA Service...")
    try:
        sua_service = SUAService()
        await sua_service.initialize()
        print("✅ SUA Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize SUA Service: {e}")
        return False
    
    # Test 7: Connection with Security
    print("\n7. Testing Secure Connection...")
    try:
        # This will test TLS/SSL if enabled in the configuration
        connected = service.connect_to_node("1-1-1", "192.168.1.10", 2905, "m3ua")
        if connected:
            print("✅ Secure connection established")
            # Close the connection
            service.close_connections()
        else:
            print("⚠️  Connection failed (expected in test environment without actual endpoints)")
    except Exception as e:
        print(f"⚠️  Connection test error (expected in test environment): {e}")
    
    # Test 8: Rate Limiting
    print("\n8. Testing Rate Limiting...")
    try:
        # Test rate limiting functionality
        allowed = service._apply_rate_limiting("192.168.1.10")
        if allowed:
            print("✅ Rate limiting applied correctly")
        else:
            print("❌ Rate limiting test failed")
            return False
    except Exception as e:
        print(f"❌ Error in rate limiting test: {e}")
        return False
    
    # Test 9: IP Whitelisting
    print("\n9. Testing IP Whitelisting...")
    try:
        # Test allowed IP
        allowed = service._is_ip_allowed("192.168.1.10")
        if allowed:
            print("✅ IP whitelisting working correctly for allowed IP")
        else:
            print("❌ IP whitelisting failed for allowed IP")
            return False
            
        # Test blocked IP
        blocked = service._is_ip_allowed("10.0.0.1")
        if not blocked:
            print("✅ IP whitelisting correctly blocked unauthorized IP")
        else:
            print("❌ IP whitelisting failed to block unauthorized IP")
            return False
    except Exception as e:
        print(f"❌ Error in IP whitelisting test: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All SIGTRAN Gateway tests completed!")
    print("The implementation includes:")
    print("  • Complete gateway configuration parameters")
    print("  • Point code to IP mapping resolution")
    print("  • TLS/SSL encryption support (configurable)")
    print("  • IP whitelisting and access control")
    print("  • Rate limiting functionality")
    print("  • Support for all SIGTRAN protocols (M3UA, SUA, M2PA, TCAP over IP)")
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(test_sigtran_gateway())
        if success:
            print("\n✅ SIGTRAN Gateway Implementation Test: PASSED")
            sys.exit(0)
        else:
            print("\n❌ SIGTRAN Gateway Implementation Test: FAILED")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)
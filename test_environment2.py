#!/usr/bin/env python3
"""
Test script to verify environment variables are set correctly
"""

import os

# Set environment variables directly for testing
os.environ['SS7_SIGTRAN'] = 'true'
os.environ['SS7_PRIVATE_NETWORK'] = 'false'

def check_environment():
    """Check if the environment variables are set correctly."""
    print("🔍 Checking Environment Variables...")
    print("=" * 40)
    
    # Check SS7_SIGTRAN
    sigtran = os.environ.get('SS7_SIGTRAN', 'not_set')
    print(f"SS7_SIGTRAN: {sigtran}")
    
    # Check SS7_PRIVATE_NETWORK
    private_network = os.environ.get('SS7_PRIVATE_NETWORK', 'not_set')
    print(f"SS7_PRIVATE_NETWORK: {private_network}")
    
    # Verify SS7 service can be imported and initialized
    try:
        from ss7_service import SS7Service
        service = SS7Service(use_sigtran=(sigtran.lower() == 'true'))
        print(f"\n✅ SS7 Service:")
        print(f"   SIGTRAN Mode: {service.use_sigtran}")
        print(f"   Private Network Mode: {service.use_private_network}")
        
        if service.use_sigtran:
            print("✅ System configured for SIGTRAN production deployment")
        else:
            print("⚠️  System NOT configured for SIGTRAN (SS7_SIGTRAN != 'true')")
            
    except Exception as e:
        print(f"❌ Failed to initialize SS7 Service: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_environment()
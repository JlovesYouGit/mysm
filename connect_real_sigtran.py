"""
Script for connecting to real SIGTRAN endpoints with full security
"""

import asyncio
import sys
import os
import socket
import ssl

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sigtran_service import M3UAService, SUAService

async def connect_to_real_sigtran_endpoints():
    """Connect to real SIGTRAN endpoints with full security"""
    print("🌐 Connecting to Real SIGTRAN Endpoints with Full Security")
    print("=" * 60)
    
    # Create M3UA service
    print("\n1. Initializing M3UA Service...")
    m3ua_service = M3UAService()
    await m3ua_service.initialize()
    
    # Create SUA service
    print("\n2. Initializing SUA Service...")
    sua_service = SUAService()
    await sua_service.initialize()
    
    # Test connection to STP1 (Signaling Transfer Point 1)
    print("\n3. Attempting Connection to STP1 (1-1-1) at 192.168.1.10:2905...")
    stp1_credentials = {"key": "secret_key_stp1"}
    
    try:
        stp1_connected = m3ua_service.connect_to_node(
            remote_point_code="1-1-1",
            ip="192.168.1.10",
            port=2905,
            protocol="m3ua",
            credentials=stp1_credentials
        )
        
        if stp1_connected:
            print("✅ Successfully connected to STP1")
        else:
            print("⚠️  Connection to STP1 failed (endpoint may not be available)")
    except Exception as e:
        print(f"❌ Error connecting to STP1: {e}")
    
    # Test connection to MSC1 (Mobile Switching Center 1)
    print("\n4. Attempting Connection to MSC1 (3-3-1) at 192.168.1.30:2905...")
    msc1_credentials = {"key": "secret_key_msc1"}
    
    try:
        msc1_connected = m3ua_service.connect_to_node(
            remote_point_code="3-3-1",
            ip="192.168.1.30",
            port=2905,
            protocol="m3ua",
            credentials=msc1_credentials
        )
        
        if msc1_connected:
            print("✅ Successfully connected to MSC1")
        else:
            print("⚠️  Connection to MSC1 failed (endpoint may not be available)")
    except Exception as e:
        print(f"❌ Error connecting to MSC1: {e}")
    
    # Test connection to SG1 (Signaling Gateway 1)
    print("\n5. Attempting Connection to SG1 (2-2-1) at 192.168.1.20:2906...")
    sg1_credentials = {"key": "secret_key_sg1"}
    
    try:
        sg1_connected = sua_service.connect_to_node(
            remote_point_code="2-2-1",
            ip="192.168.1.20",
            port=2906,
            protocol="sua",
            credentials=sg1_credentials
        )
        
        if sg1_connected:
            print("✅ Successfully connected to SG1")
        else:
            print("⚠️  Connection to SG1 failed (endpoint may not be available)")
    except Exception as e:
        print(f"❌ Error connecting to SG1: {e}")
    
    # Display security features in use
    print("\n6. Security Features in Use:")
    security_config = m3ua_service.security_config
    encryption = security_config.get("encryption", {})
    access_control = security_config.get("access_control", {})
    
    print(f"   🔒 TLS Encryption: {'Enabled' if encryption.get('tls_enabled', False) else 'Disabled'}")
    if encryption.get('tls_enabled', False):
        print(f"      Certificate File: {encryption.get('cert_file', 'N/A')}")
        print(f"      Key File: {encryption.get('key_file', 'N/A')}")
        print(f"      CA File: {encryption.get('ca_file', 'N/A')}")
        print(f"      Peer Verification: {'Enabled' if encryption.get('verify_peer', False) else 'Disabled'}")
    
    print(f"   🛡️  Authentication: {'Required' if access_control.get('authentication_required', False) else 'Not Required'}")
    print(f"   🚦 Rate Limiting: {'Enabled' if access_control.get('rate_limiting', {}).get('enabled', False) else 'Disabled'}")
    if access_control.get('rate_limiting', {}).get('enabled', False):
        print(f"      Messages per Second: {access_control.get('rate_limiting', {}).get('messages_per_second', 0)}")
    
    print(f"   📋 IP Whitelisting: {len(access_control.get('ip_whitelisting', []))} addresses configured")
    print("      Whitelisted IPs:")
    for ip in access_control.get('ip_whitelisting', []):
        print(f"         - {ip}")
    
    # Display connection status
    print("\n7. Connection Status Summary:")
    try:
        stp1_status = "Connected" if 'stp1_connected' in locals() and stp1_connected else "Not Connected"
        msc1_status = "Connected" if 'msc1_connected' in locals() and msc1_connected else "Not Connected"
        sg1_status = "Connected" if 'sg1_connected' in locals() and sg1_connected else "Not Connected"
        
        print(f"   STP1 (1-1-1): {stp1_status}")
        print(f"   MSC1 (3-3-1): {msc1_status}")
        print(f"   SG1 (2-2-1): {sg1_status}")
    except:
        print("   Connection status: Unable to determine (script interrupted)")
    
    print("\n" + "=" * 60)
    print("🏁 Real SIGTRAN Endpoint Connection Attempt Completed!")
    print("Note: Connection failures are expected in test environments")
    print("where actual SIGTRAN endpoints are not available.")

if __name__ == "__main__":
    try:
        print("🚀 Starting Real SIGTRAN Endpoint Connection...")
        asyncio.run(connect_to_real_sigtran_endpoints())
        print("\n✅ Real SIGTRAN Endpoint Connection: ATTEMPT COMPLETED")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n⚠️  Connection attempt interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during connection attempt: {e}")
        sys.exit(1)
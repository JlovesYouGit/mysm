"""
Example script for connecting to actual SIGTRAN endpoints with security features
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sigtran_service import M3UAService, SUAService

async def connect_to_sigtran_endpoints():
    """Demonstrate connecting to actual SIGTRAN endpoints with security"""
    print("🔗 Connecting to SIGTRAN Endpoints with Security")
    print("=" * 50)
    
    # Create M3UA service
    print("\n1. Initializing M3UA Service...")
    m3ua_service = M3UAService()
    await m3ua_service.initialize()
    
    # Connect to STP1 (Signaling Transfer Point 1)
    print("\n2. Connecting to STP1 (1-1-1) at 192.168.1.10:2905...")
    stp1_credentials = {"key": "secret_key_stp1"}
    stp1_connected = m3ua_service.connect_to_node(
        remote_point_code="1-1-1",
        ip="192.168.1.10",
        port=2905,
        protocol="m3ua",
        credentials=stp1_credentials
    )
    
    if stp1_connected:
        print("✅ Connected to STP1 with TLS encryption and authentication")
    else:
        print("⚠️  Failed to connect to STP1 (expected in test environment without actual endpoints)")
    
    # Connect to MSC1 (Mobile Switching Center 1)
    print("\n3. Connecting to MSC1 (3-3-1) at 192.168.1.30:2905...")
    msc1_credentials = {"key": "secret_key_msc1"}
    msc1_connected = m3ua_service.connect_to_node(
        remote_point_code="3-3-1",
        ip="192.168.1.30",
        port=2905,
        protocol="m3ua",
        credentials=msc1_credentials
    )
    
    if msc1_connected:
        print("✅ Connected to MSC1 with TLS encryption and authentication")
    else:
        print("⚠️  Failed to connect to MSC1 (expected in test environment without actual endpoints)")
    
    # Create SUA service for SCCP messages
    print("\n4. Initializing SUA Service...")
    sua_service = SUAService()
    await sua_service.initialize()
    
    # Connect to SG1 (Signaling Gateway 1)
    print("\n5. Connecting to SG1 (2-2-1) at 192.168.1.20:2906...")
    sg1_credentials = {"key": "secret_key_sg1"}
    sg1_connected = sua_service.connect_to_node(
        remote_point_code="2-2-1",
        ip="192.168.1.20",
        port=2906,
        protocol="sua",
        credentials=sg1_credentials
    )
    
    if sg1_connected:
        print("✅ Connected to SG1 with TLS encryption and authentication")
    else:
        print("⚠️  Failed to connect to SG1 (expected in test environment without actual endpoints)")
    
    # Send test messages if connections were established
    if stp1_connected or msc1_connected:
        print("\n6. Sending Test Messages...")
        
        # Send M3UA message
        test_message = b"Test SS7 message over SIGTRAN with security"
        sent = m3ua_service.send_data_message(test_message, "2-2-1", "1-1-1")
        if sent:
            print("✅ Test M3UA message sent successfully")
        else:
            print("❌ Failed to send test M3UA message")
    
    if sg1_connected:
        # Send SUA message
        test_sccp_message = b"Test SCCP message over SUA with security"
        sent = sua_service.send_sccp_message(test_sccp_message, "2-2-1", "3-3-1")
        if sent:
            print("✅ Test SUA message sent successfully")
        else:
            print("❌ Failed to send test SUA message")
    
    # Display connection status
    print("\n7. Connection Status:")
    print(f"   STP1 (1-1-1): {'Connected' if stp1_connected else 'Not Connected'}")
    print(f"   MSC1 (3-3-1): {'Connected' if msc1_connected else 'Not Connected'}")
    print(f"   SG1 (2-2-1): {'Connected' if sg1_connected else 'Not Connected'}")
    
    # Start message receivers for active connections
    if stp1_connected or msc1_connected:
        print("\n8. Starting M3UA message receiver...")
        await m3ua_service.start_message_receiver()
    
    if sg1_connected:
        print("\n9. Starting SUA message receiver...")
        await sua_service.start_message_receiver()
    
    # Keep running for a bit to demonstrate receiver functionality
    print("\n10. Running for 10 seconds to demonstrate receiver functionality...")
    await asyncio.sleep(10)
    
    # Clean up connections
    print("\n11. Cleaning up connections...")
    m3ua_service.close_connections()
    sua_service.close_connections()
    
    print("\n" + "=" * 50)
    print("🏁 SIGTRAN Endpoint Connection Demo Completed!")
    print("The implementation demonstrates:")
    print("  • Secure connections with TLS encryption")
    print("  • Authentication with credentials")
    print("  • IP whitelisting access control")
    print("  • Rate limiting protection")
    print("  • Support for M3UA and SUA protocols")
    print("  • Message sending and receiving capabilities")

if __name__ == "__main__":
    try:
        print("🚀 Starting SIGTRAN Endpoint Connection Demo...")
        asyncio.run(connect_to_sigtran_endpoints())
        print("\n✅ SIGTRAN Endpoint Connection Demo: COMPLETED")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during demo: {e}")
        sys.exit(1)
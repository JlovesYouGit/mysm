# SIGTRAN Deployment Guide for SS7 over IP

## Overview
This guide provides instructions for deploying SS7 signaling over IP networks using SIGTRAN protocols. SIGTRAN enables the transport of SS7 messages over standard IP infrastructure, providing flexible and cost-effective telecommunications signaling.

## 1. SIGTRAN Protocols Overview

### 1.1 Supported Protocols
- **M3UA (MTP3 User Adaptation)** - Primary protocol for SS7 over IP
- **SUA (SCCP User Adaptation)** - For SCCP message transport
- **M2PA (MTP2 Peer-to-Peer Adaptation)** - For direct MTP2 link transport
- **TCAP over IP** - For transaction capabilities over IP

### 1.2 Protocol Stack
```
Application Layer (TCAP/SCCP/MTP3)
            ↓
    SIGTRAN Adaptation Layer (M3UA/SUA/M2PA)
            ↓
      Transport Layer (SCTP/TCP)
            ↓
       IP Network Layer
```

## 2. System Architecture with SIGTRAN

### 2.1 Components
```
[NETGEAR Adapter] → [Signal Detection] → [Point Code Extraction]
                                      ↓
                            [SIGTRAN Service] ←→ [IP Network]
                                      ↓
                            [Remote SS7 Nodes]
```

### 2.2 Network Nodes
- **Signaling Gateway (SG)** - Terminates SIGTRAN connections
- **STP (Signal Transfer Point)** - Routes SS7 messages
- **SCP (Service Control Point)** - Provides database services
- **SSP (Service Switching Point)** - Switches calls based on signaling

## 3. Configuration

### 3.1 SIGTRAN Configuration File (sigtran_config.py)
```python
SIGTRAN_CONFIG = {
    "protocols": {
        "m3ua": {
            "enabled": True,
            "port": 2905,
            "transport": "SCTP"
        },
        "sua": {
            "enabled": True,
            "port": 2906,
            "transport": "SCTP"
        },
        "m2pa": {
            "enabled": True,
            "port": 2904,
            "transport": "SCTP"
        },
        "tcap_over_ip": {
            "enabled": True,
            "port": 2907,
            "transport": "SCTP"
        }
    },
    "point_codes": {
        "local": "2-2-1",
        "remote": "1-1-1",
        "mask": "0-0-0"
    },
    "network_appearance": 100,
    "routing_context": 1000,
    "point_code_mapping": {
        "1-1-1": "192.168.1.10",
        "2-2-1": "192.168.1.20",
        "3-3-1": "192.168.1.30"
    }
}
```

### 3.2 Environment Setup
```bash
# Enable SIGTRAN mode
export SS7_SIGTRAN=true

# Start the application
python main.py
```

## 4. Implementation Details

### 4.1 M3UA Service
The M3UA service provides MTP3 User Adaptation for IP transport:

```python
from sigtran_service import M3UAService

# Initialize service
m3ua_service = M3UAService()
await m3ua_service.initialize()

# Connect to remote node
connected = m3ua_service.connect_to_node("1-1-1", "ss7-carrier.example.com", 2905, "m3ua")

# Send SS7 message
message = b"SS7 message payload"
sent = m3ua_service.send_data_message(message, "2-2-1", "1-1-1")
```

### 4.2 SUA Service
The SUA service provides SCCP User Adaptation for IP transport:

```python
from sigtran_service import SUAService

# Initialize service
sua_service = SUAService()
await sua_service.initialize()

# Send SCCP message
sccp_message = b"SCCP message payload"
sent = sua_service.send_sccp_message(sccp_message, "2-2-1", "1-1-1")
```

## 5. API Endpoints

### 5.1 Configure SIGTRAN
```
POST /api/ss7/configure-sigtran
{
    "enable_sigtran": true,
    "protocol": "m3ua",
    "nodes": [
        {
            "point_code": "1-1-1",
            "ip": "ss7-carrier.example.com",
            "port": 2905
        }
    ]
}
```

### 5.2 Transport Status
```
GET /api/ss7/transport-status
```

Response:
```json
{
    "status": "active",
    "mode": "sigtran",
    "transport": "SS7 over IP (SIGTRAN)",
    "protocols": ["M3UA", "SUA", "M2PA"],
    "message": "SS7 messages routed over IP network using SIGTRAN protocols"
}
```

## 6. Security Considerations

### 6.1 TLS/SSL Encryption
```python
SIGTRAN_SECURITY = {
    "encryption": {
        "tls_enabled": True,
        "cert_file": "/etc/ssl/certs/sigtran.crt",
        "key_file": "/etc/ssl/private/sigtran.key",
        "ca_file": "/etc/ssl/certs/ca.crt",
        "verify_peer": True
    },
    "access_control": {
        "ip_whitelisting": ["192.168.1.10", "192.168.1.20"],
        "authentication_required": True
    }
}
```

### 6.2 Network Security
- Implement IP whitelisting
- Use VPN for secure connections
- Apply firewall rules for SIGTRAN ports
- Monitor for unauthorized access attempts

## 7. Testing SIGTRAN Implementation

### 7.1 Unit Tests
```bash
python -m pytest tests/test_sigtran.py
```

### 7.2 Integration Tests
```bash
python test_sigtran.py
```

### 7.3 Manual Testing
```bash
# Set environment variable
export SS7_SIGTRAN=true

# Run the application
python main.py

# Test API endpoints
curl -X GET http://localhost:8083/api/ss7/transport-status
```

## 8. Production Deployment

### 8.1 Requirements
- Valid telecommunications license
- Commercial agreement with SS7 service provider
- Assigned point codes from regulatory authority
- Secure network connectivity to provider infrastructure

### 8.2 Configuration Steps
1. Obtain SIGTRAN connection details from service provider
2. Update [sigtran_config.py](file://n:/sms/sigtran_config.py) with provider information
3. Configure security certificates
4. Set environment variable: `SS7_SIGTRAN=true`
5. Start the application

### 8.3 Signaling Gateway Setup
For detailed instructions on setting up signaling gateways with full SIGTRAN protocol support, point code mapping, and security measures, see [SIGTRAN_GATEWAY_SETUP.md](file://n:/sms/SIGTRAN_GATEWAY_SETUP.md)

## 9. Troubleshooting

### 9.1 Common Issues

#### Connection Failures
- Check network connectivity to provider endpoints
- Verify point codes and IP addresses
- Confirm firewall rules allow SIGTRAN traffic
- Validate SSL/TLS certificate configuration

#### Message Transmission Errors
- Check message format and encoding
- Verify point code routing tables
- Review provider-specific requirements
- Confirm protocol compatibility

### 9.2 Diagnostic Commands
```bash
# Test network connectivity
telnet ss7-carrier.example.com 2905

# Check certificate validity
openssl x509 -in sigtran.crt -text -noout

# Monitor network traffic
tcpdump -i any port 2905
```

## 10. Performance Optimization

### 10.1 Network Optimization
- Use dedicated network interfaces for SIGTRAN traffic
- Implement quality of service (QoS) for signaling traffic
- Optimize TCP/SCTP buffer sizes
- Minimize network latency

### 10.2 Message Processing
- Batch SS7 messages when possible
- Implement message queuing for high-volume scenarios
- Use connection pooling for multiple destinations
- Monitor and optimize message processing time

## Conclusion

SIGTRAN provides a modern approach to SS7 signaling by enabling transport over IP networks. This implementation supports M3UA, SUA, M2PA, and TCAP over IP protocols, providing flexible connectivity options for telecommunications services. When combined with proper authorization and network access, SIGTRAN enables cost-effective and scalable SS7 deployments.

The system is ready for production use with SIGTRAN capabilities, maintaining full compliance with the telecommunications license while providing enhanced connectivity options.

For detailed signaling gateway setup instructions, see [SIGTRAN_GATEWAY_SETUP.md](file://n:/sms/SIGTRAN_GATEWAY_SETUP.md)
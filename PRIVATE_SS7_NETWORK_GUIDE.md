# Private SS7 Network Implementation Guide

## Overview
This guide provides instructions for setting up and using a private SS7 network infrastructure for testing and development purposes. The implementation includes Signaling Transfer Points (STPs), Signaling Gateways (SGs), and Mobile Switching Centers (MSCs) with proper point code allocation and routing.

## 1. System Requirements

### 1.1 Hardware
- Minimum 6 servers or VMs for network nodes
- NETGEAR A6210 WiFi USB3.0 Adapter (for licensed mode)
- 192.168.1.0/24 network segment (configurable)
- Reliable low-latency network connectivity

### 1.2 Software
- Python 3.8+
- Required Python packages (see requirements.txt)
- MongoDB (for number management)
- OpenSSL (for certificate generation)

## 2. Network Architecture

### 2.1 Node Configuration
```
[STP1] ←→ [SG1] ←→ [MSC1]
   ↑         ↑        ↑
   ↓         ↓        ↓
[STP2] ←→ [SG2] ←→ [MSC2]
```

### 2.2 Point Code Allocation
| Node Type | Node ID | Point Code | IP Address |
|-----------|---------|------------|------------|
| STP | STP1 | 1-1-1 | 192.168.1.10 |
| STP | STP2 | 1-1-2 | 192.168.1.11 |
| SG | SG1 | 2-2-1 | 192.168.1.20 |
| SG | SG2 | 2-2-2 | 192.168.1.21 |
| MSC | MSC1 | 3-3-1 | 192.168.1.30 |
| MSC | MSC2 | 3-3-2 | 192.168.1.31 |

## 3. Installation and Setup

### 3.1 Clone Repository
```bash
git clone <repository-url>
cd telecom-system
```

### 3.2 Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements_spectrum.txt
```

### 3.3 Configure Environment
Set environment variable to enable private network mode:
```bash
# Windows
set SS7_PRIVATE_NETWORK=true

# Linux/Mac
export SS7_PRIVATE_NETWORK=true
```

## 4. Configuration Files

### 4.1 STP Configuration (ss7_stp_config.py)
```python
STP_CONFIG = {
    "node1": {
        "point_code": "1-1-1",
        "ip_address": "192.168.1.10",
        "port": 2905,
        "adjacent_nodes": ["2-2-1", "1-1-2"],
        "linksets": [
            {
                "name": "linkset1",
                "links": [
                    {"ip": "192.168.1.20", "port": 2905},  # SG1
                    {"ip": "192.168.1.11", "port": 2905}   # STP2
                ]
            }
        ]
    }
    # ... node2 configuration
}
```

### 4.2 SG Configuration (ss7_sg_config.py)
```python
SG_CONFIG = {
    "sg1": {
        "point_code": "2-2-1",
        "ip_address": "192.168.1.20",
        "port": 2905,
        "adjacent_nodes": ["1-1-1", "3-3-1"],
        "linksets": [
            {
                "name": "sg1_linkset",
                "links": [
                    {"ip": "192.168.1.10", "port": 2905},  # STP1
                    {"ip": "192.168.1.30", "port": 2905}   # MSC1
                ]
            }
        ]
    }
    # ... sg2 configuration
}
```

### 4.3 MSC Configuration (ss7_msc_config.py)
```python
MSC_CONFIG = {
    "msc1": {
        "point_code": "3-3-1",
        "ip_address": "192.168.1.30",
        "port": 2905,
        "adjacent_nodes": ["2-2-1"],
        "services": {
            "voice": True,
            "sms": True,
            "data": True
        }
    }
    # ... msc2 configuration
}
```

## 5. Starting the Network

### 5.1 Start Individual Nodes
Each node type can be started separately:

```bash
# Start STP nodes
python ss7_stp.py

# Start SG nodes
python ss7_sg.py

# Start MSC nodes
python ss7_msc.py
```

### 5.2 Start Main Application
```bash
# Start the main telecom API with private network mode
SS7_PRIVATE_NETWORK=true python main.py
```

## 6. API Endpoints

### 6.1 Network Configuration
```
POST /api/ss7/configure-private-network
{
    "enable_private_network": true,
    "stp_nodes": [...],
    "sg_nodes": [...],
    "msc_nodes": [...]
}
```

### 6.2 Network Status
```
GET /api/ss7/network-status
```

Response:
```json
{
    "status": "active",
    "mode": "private_network",
    "nodes": [
        {
            "id": "stp1",
            "type": "STP",
            "point_code": "1-1-1",
            "status": "online"
        }
        // ... other nodes
    ]
}
```

## 7. Testing the Network

### 7.1 Run Unit Tests
```bash
python -m pytest tests/test_ss7_components.py
```

### 7.2 Run Integration Tests
```bash
python test_private_ss7_network.py
```

### 7.3 Test SMS Functionality
```bash
curl -X POST http://localhost:8083/api/sms/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "to": "+0987654321",
    "from_": "+1234567890",
    "message": "Hello from private SS7 network!"
  }'
```

### 7.4 Test Voice Call Functionality
```bash
curl -X POST http://localhost:8083/api/voice/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "to": "+0987654321",
    "from_": "+1234567890"
  }'
```

## 8. Security Configuration

### 8.1 Generate Certificates
```bash
# Generate certificates for each node
openssl req -x509 -newkey rsa:4096 -keyout stp1.key -out stp1.crt -days 365 -nodes
openssl req -x509 -newkey rsa:4096 -keyout sg1.key -out sg1.crt -days 365 -nodes
openssl req -x509 -newkey rsa:4096 -keyout msc1.key -out msc1.crt -days 365 -nodes
```

### 8.2 Configure IP Whitelisting
```python
SECURITY_CONFIG = {
    "ip_whitelisting": [
        "192.168.1.10",  # STP1
        "192.168.1.11",  # STP2
        "192.168.1.20",  # SG1
        "192.168.1.21",  # SG2
        "192.168.1.30",  # MSC1
        "192.168.1.31"   # MSC2
    ]
}
```

## 9. Monitoring and Maintenance

### 9.1 Network Monitoring
- Monitor message throughput
- Track latency between nodes
- Log error rates and failures
- Alert on node status changes

### 9.2 Regular Maintenance Tasks
- Update software packages
- Rotate security certificates
- Review access logs
- Perform backup operations

## 10. Troubleshooting

### 10.1 Common Issues

#### Connection Failures
- Check network connectivity between nodes
- Verify IP addresses and ports in configuration
- Ensure firewall rules allow SS7 traffic (port 2905)

#### Message Routing Issues
- Verify point code allocation
- Check routing tables
- Review linkset configurations

#### Performance Problems
- Monitor system resources
- Check network latency
- Review load balancing configuration

### 10.2 Diagnostic Commands
```bash
# Check network connectivity
ping 192.168.1.10

# Check port availability
telnet 192.168.1.10 2905

# View application logs
tail -f logs/ss7_network.log
```

## 11. Transitioning to Production

### 11.1 Production Requirements
- Obtain legitimate point codes from regulatory authority
- Connect to real SS7 service provider
- Implement proper security certificates
- Ensure regulatory compliance

### 11.2 Configuration Changes
1. Update point codes to assigned values
2. Configure real network endpoints
3. Implement production security measures
4. Set up monitoring and alerting

## Conclusion
This private SS7 network implementation provides a complete testing environment for SS7 telecommunications services. It includes all necessary components for routing SMS and voice calls through a simulated SS7 infrastructure while maintaining compliance with the licensed telecommunications system.
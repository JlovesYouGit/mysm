# Production Deployment Guide for SIGTRAN SS7 Implementation

## Overview
This guide provides step-by-step instructions for deploying the telecommunications system with actual SS7 connectivity through SIGTRAN protocols in a production environment.

## Prerequisites
1. Valid telecommunications license
2. Carrier relationship with SS7 network access
3. Assigned point codes from regulatory authority
4. Network infrastructure with SIGTRAN endpoint connectivity
5. SSL/TLS certificates for secure connections

## Step 1: Deploy SSL/TLS Certificates

### Certificate Requirements
The system requires three SSL/TLS certificate files:
- Server certificate: `/etc/ssl/certs/sigtran.crt`
- Private key: `/etc/ssl/private/sigtran.key`
- Certificate Authority (CA) certificate: `/etc/ssl/certs/ca.crt`

### Certificate Deployment Process

#### Option 1: Using Carrier-Provided Certificates
1. Obtain certificates from your carrier
2. Place the server certificate at `/etc/ssl/certs/sigtran.crt`
3. Place the private key at `/etc/ssl/private/sigtran.key`
4. Place the CA certificate at `/etc/ssl/certs/ca.crt`
5. Set appropriate file permissions:
   ```bash
   chmod 644 /etc/ssl/certs/sigtran.crt
   chmod 600 /etc/ssl/private/sigtran.key
   chmod 644 /etc/ssl/certs/ca.crt
   ```

#### Option 2: Generating Self-Signed Certificates (Testing Only)
For testing purposes, you can generate self-signed certificates:
```bash
# Create directory structure
sudo mkdir -p /etc/ssl/certs /etc/ssl/private

# Generate private key
openssl genrsa -out /etc/ssl/private/sigtran.key 2048

# Generate certificate signing request
openssl req -new -key /etc/ssl/private/sigtran.key -out sigtran.csr

# Generate self-signed certificate
openssl x509 -req -days 365 -in sigtran.csr -signkey /etc/ssl/private/sigtran.key -out /etc/ssl/certs/sigtran.crt

# Generate CA certificate (for testing)
openssl req -x509 -newkey rsa:4096 -keyout ca.key -out /etc/ssl/certs/ca.crt -days 1095 -nodes

# Set permissions
sudo chmod 644 /etc/ssl/certs/sigtran.crt
sudo chmod 600 /etc/ssl/private/sigtran.key
sudo chmod 644 /etc/ssl/certs/ca.crt
```

## Step 2: Configure Actual SIGTRAN Endpoints

### Update SIGTRAN Configuration
Edit `sigtran_config.py` to match your carrier's infrastructure:

```python
# SIGTRAN Protocol Configuration
SIGTRAN_CONFIG = {
    "protocols": {
        "m3ua": {
            "enabled": True,
            "port": 2905,  # Carrier's M3UA port
            "transport": "SCTP"
        },
        "sua": {
            "enabled": True,
            "port": 2906,  # Carrier's SUA port
            "transport": "SCTP"
        }
    },
    # Update with your assigned point codes
    "point_codes": {
        "local": "YOUR-SG-POINT-CODE",  # Your Signaling Gateway point code
        "remote": "CARRIER-STP-POINT-CODE",  # Carrier's STP point code
        "mask": "0-0-0"
    },
    # Update with carrier's IP addresses and your point codes
    "point_code_mapping": {
        "CARRIER-STP-POINT-CODE": "CARRIER-STP-IP-ADDRESS",  # Carrier's STP
        "YOUR-SG-POINT-CODE": "YOUR-SG-IP-ADDRESS",  # Your Signaling Gateway
        "CARRIER-MSC-POINT-CODE": "CARRIER-MSC-IP-ADDRESS"  # Carrier's MSC
    }
}

# Update with carrier's security requirements
SIGTRAN_SECURITY = {
    "encryption": {
        "tls_enabled": True,
        "ipsec_enabled": False,
        "cert_file": "/etc/ssl/certs/sigtran.crt",
        "key_file": "/etc/ssl/private/sigtran.key",
        "ca_file": "/etc/ssl/certs/ca.crt",
        "verify_peer": True,
        "cipher_suite": "ECDHE-RSA-AES256-GCM-SHA384"
    },
    "access_control": {
        "ip_whitelisting": [
            "CARRIER-STP-IP-ADDRESS",  # Carrier's STP IP
            "CARRIER-MSC-IP-ADDRESS"   # Carrier's MSC IP
        ],
        "authentication_required": True,
        "max_connections": 100,
        "rate_limiting": {
            "enabled": True,
            "messages_per_second": 1000
        }
    }
}
```

### Carrier Information Required
Contact your carrier to obtain:
1. STP (Signal Transfer Point) IP address and port
2. MSC (Mobile Switching Center) IP address and port
3. Assigned point codes for your infrastructure
4. Authentication credentials (pre-shared keys)
5. SSL/TLS certificates
6. Network routing information

## Step 3: Provision Real Telephone Numbers

### Number Management APIs
The system provides REST APIs for number management:

#### Assign a Number to a User
```http
POST /api/numbers/assign
Authorization: Bearer <token>
Content-Type: application/json

{
  "number": "+1234567890"
}
```

#### List User's Numbers
```http
GET /api/numbers
Authorization: Bearer <token>
```

#### Get Available Numbers
```http
GET /api/numbers/available
Authorization: Bearer <token>
```

### Carrier Number Provisioning Process
1. Request telephone numbers from your carrier
2. Obtain number ranges or individual numbers
3. Configure number routing with your carrier
4. Use the API to assign numbers to users in the system
5. Test end-to-end functionality

## Step 4: Configure Authentication Credentials

### Update Authentication Configuration
The system uses pre-shared keys for authentication. Update the authentication logic in `sigtran_service.py`:

```python
def _authenticate_connection(self, point_code: str, credentials: Dict = None) -> bool:
    """Authenticate connection based on point code and credentials."""
    access_control = self.security_config.get("access_control", {})
    
    if not access_control.get("authentication_required", False):
        return True
    
    # Update with actual credentials from your carrier
    valid_credentials = {
        "CARRIER-STP-POINT-CODE": "CARRIER-STP-SECRET-KEY",
        "CARRIER-MSC-POINT-CODE": "CARRIER-MSC-SECRET-KEY"
    }
    
    # Check if node is already authenticated
    if point_code in self.authenticated_nodes:
        return True
    
    # Authenticate with provided credentials
    if credentials and credentials.get("key") == valid_credentials.get(point_code):
        self.authenticated_nodes.add(point_code)
        logger.info(f"Authenticated connection for point code {point_code}")
        return True
    
    logger.error(f"Authentication failed for point code {point_code}")
    return False
```

## Step 5: Network Configuration

### Firewall Rules
Configure firewall to allow SIGTRAN traffic:
```bash
# Allow M3UA traffic
sudo iptables -A INPUT -p sctp --dport 2905 -j ACCEPT

# Allow SUA traffic
sudo iptables -A INPUT -p sctp --dport 2906 -j ACCEPT

# Allow M2PA traffic
sudo iptables -A INPUT -p sctp --dport 2904 -j ACCEPT

# Allow TCAP over IP traffic
sudo iptables -A INPUT -p sctp --dport 2907 -j ACCEPT
```

### Network Interface Configuration
Ensure your network interfaces are properly configured:
```bash
# Configure network interface for SIGTRAN
sudo ip addr add YOUR-SG-IP-ADDRESS/24 dev eth0
sudo ip link set eth0 up
```

## Step 6: Start Production Services

### Using the Production Startup Script
```bash
# Make the script executable
chmod +x start_sigtran_production.sh

# Run the production startup script
./start_sigtran_production.sh
```

### Manual Environment Setup
```bash
# Set environment variables
export SS7_SIGTRAN=true
export SS7_PRIVATE_NETWORK=false

# Start the main application
python main.py
```

## Step 7: Testing and Validation

### Verify SIGTRAN Connectivity
```http
GET /api/ss7/transport-status
Authorization: Bearer <token>
```

Expected response:
```json
{
  "status": "active",
  "mode": "sigtran",
  "transport": "SS7 over IP (SIGTRAN)",
  "protocols": ["M3UA", "SUA", "M2PA", "TCAP over IP"],
  "security": {
    "tls_enabled": true,
    "authentication_required": true,
    "ip_whitelisting": true,
    "rate_limiting": true
  },
  "message": "SS7 messages routed over IP network using SIGTRAN protocols with full security"
}
```

### Test SMS Functionality
```http
POST /api/sms/send
Authorization: Bearer <token>
Content-Type: application/json

{
  "to": "+1234567890",
  "from_": "+0987654321",
  "message": "Test message from production system"
}
```

### Monitor System Logs
```bash
# Monitor main application logs
tail -f /var/log/telecom-api.log

# Monitor SIGTRAN connection logs
tail -f /var/log/sigtran-service.log
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Certificate Validation Errors
- Verify certificate paths in `sigtran_config.py`
- Check certificate file permissions
- Ensure CA certificate is properly configured

#### 2. Connection Failures
- Verify IP addresses and ports with your carrier
- Check firewall rules
- Confirm network connectivity

#### 3. Authentication Failures
- Verify pre-shared keys with your carrier
- Check point code mappings
- Ensure authentication is enabled in configuration

#### 4. Performance Issues
- Monitor message rates and adjust rate limiting
- Check network latency
- Verify hardware resources

## Security Best Practices

1. **Certificate Management**
   - Regularly update certificates before expiration
   - Store private keys securely
   - Use strong encryption algorithms

2. **Access Control**
   - Maintain up-to-date IP whitelists
   - Regularly review authentication credentials
   - Implement network segmentation

3. **Monitoring**
   - Enable detailed logging
   - Set up alerts for security events
   - Regular security audits

## Maintenance

### Regular Tasks
1. Certificate renewal before expiration
2. Security patch updates
3. Performance monitoring and optimization
4. Log file rotation and analysis
5. Backup of configuration files

### Emergency Procedures
1. Immediate shutdown procedures
2. Incident response protocols
3. Recovery procedures
4. Contact information for carrier support

## Support

For production deployment support, contact:
- Carrier Technical Support
- System Administrator
- Security Team

Document all changes and maintain configuration backups.
# API Reference Documentation

## 🌐 Base URL
```
http://localhost:8083
https://your-domain.com (Production)
```

## 🔐 Authentication

All API endpoints (except `/` and `/health`) require JWT authentication.

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "telecom2025"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "admin",
    "username": "admin"
  }
}
```

### Using Authentication
Include the JWT token in the Authorization header:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📱 SMS Services

### Send SMS
Route SMS messages through the SS7 network.

```http
POST /api/sms/send
Authorization: Bearer {token}
Content-Type: application/json

{
  "to": "+1234567890",
  "from_": "+1987654321",
  "message": "Hello from SS7 network!"
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "64f8a1b2c3d4e5f6a7b8c9d0",
  "licensed": true
}
```

### Get Messages
Retrieve SMS message history.

```http
GET /api/sms/messages
Authorization: Bearer {token}
```

**Response:**
```json
{
  "messages": [
    {
      "id": "64f8a1b2c3d4e5f6a7b8c9d0",
      "to": "+1234567890",
      "from": "+1987654321",
      "message": "Hello from SS7 network!",
      "timestamp": "2024-01-15T10:30:00Z",
      "status": "sent"
    }
  ]
}
```

## 📞 Voice Services

### Make Call
Initiate voice calls through the SS7 network.

```http
POST /api/voice/call
Authorization: Bearer {token}
Content-Type: application/json

{
  "to": "+1234567890",
  "from_": "+1987654321"
}
```

**Response:**
```json
{
  "success": true,
  "call_id": "64f8a1b2c3d4e5f6a7b8c9d1",
  "licensed": true
}
```

### Get Calls
Retrieve call history.

```http
GET /api/voice/calls
Authorization: Bearer {token}
```

**Response:**
```json
{
  "calls": [
    {
      "id": "64f8a1b2c3d4e5f6a7b8c9d1",
      "to": "+1234567890",
      "from": "+1987654321",
      "timestamp": "2024-01-15T10:35:00Z",
      "duration": 0,
      "status": "initiated"
    }
  ]
}
```

## 📞 Number Management

### List Numbers
Get user's assigned phone numbers.

```http
GET /api/numbers
Authorization: Bearer {token}
```

**Response:**
```json
{
  "numbers": [
    {
      "id": "64f8a1b2c3d4e5f6a7b8c9d2",
      "number": "+1234567890",
      "country_code": "+1",
      "country": "United States",
      "assigned_at": "2024-01-15T09:00:00Z",
      "status": "assigned"
    }
  ],
  "licensed": true
}
```

### Assign Number
Assign a phone number to the user.

```http
POST /api/numbers/assign
Authorization: Bearer {token}
Content-Type: application/json

{
  "number": "+1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "number": {
    "id": "64f8a1b2c3d4e5f6a7b8c9d2",
    "number": "+1234567890",
    "country_code": "+1",
    "country": "United States",
    "assigned_at": "2024-01-15T10:40:00Z",
    "status": "assigned"
  },
  "licensed": true
}
```

### Release Number
Release a phone number.

```http
POST /api/numbers/release
Authorization: Bearer {token}
Content-Type: application/json

{
  "number": "+1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "licensed": true
}
```

### Get Available Numbers
Get available phone numbers for assignment.

```http
GET /api/numbers/available?country=US
Authorization: Bearer {token}
```

**Response:**
```json
{
  "numbers": [
    {
      "id": "64f8a1b2c3d4e5f6a7b8c9d3",
      "number": "+1234567891",
      "country_code": "+1",
      "country": "United States",
      "status": "available"
    }
  ],
  "licensed": true
}
```

## 📡 Spectrum Analysis

### Scan Spectrum
Perform real-time spectrum analysis using RTL-SDR hardware.

```http
POST /api/spectrum/scan
Authorization: Bearer {token}
Content-Type: application/json

{
  "scan_type": "cellular",
  "frequency_band": "GSM900"
}
```

**Response:**
```json
{
  "status": "completed",
  "towers": [
    {
      "id": "tower1",
      "location": "37.7749,-122.4194",
      "frequency": "850 MHz",
      "signal_strength": -75
    },
    {
      "id": "tower2",
      "location": "34.0522,-118.2437",
      "frequency": "1900 MHz",
      "signal_strength": -82
    }
  ],
  "point_codes": [12345, 67890, 24680],
  "timestamp": "2024-01-15T10:45:00Z",
  "licensed": true,
  "message": "Spectrum analysis completed using licensed equipment"
}
```

### Get Detected Towers
Retrieve information about detected cell towers.

```http
GET /api/spectrum/towers
Authorization: Bearer {token}
```

**Response:**
```json
{
  "towers": [
    {
      "id": "tower1",
      "location": "37.7749,-122.4194",
      "frequency": "850 MHz",
      "signal_strength": -75
    }
  ],
  "licensed": true
}
```

### Get Point Codes
Retrieve discovered SS7 point codes.

```http
GET /api/spectrum/pointcodes
Authorization: Bearer {token}
```

**Response:**
```json
{
  "point_codes": [12345, 67890, 24680],
  "licensed": true,
  "message": "Point codes obtained from licensed spectrum analysis"
}
```

### Integrate with SS7
Integrate discovered point codes with SS7 network.

```http
POST /api/spectrum/integrate-ss7
Authorization: Bearer {token}
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully integrated with SS7 network using licensed equipment",
  "point_codes_used": [12345, 67890],
  "licensed": true
}
```

## 🔐 License Management

### Get License Info
Retrieve telecommunications license information.

```http
GET /api/license/info
Authorization: Bearer {token}
```

**Response:**
```json
{
  "license_info": {
    "license_number": "WP-DOCKET-12345",
    "licensee_name": "Telecom Service Provider",
    "license_type": "Wireless Telecommunications",
    "authorized_services": [
      "SMS Messaging",
      "Voice Calls",
      "Spectrum Analysis",
      "SS7 Network Access"
    ],
    "frequency_bands": [
      "698-806 MHz",
      "824-849 MHz",
      "869-894 MHz",
      "1710-1755 MHz",
      "1850-1910 MHz",
      "1930-1990 MHz"
    ]
  },
  "valid": true,
  "authorized_services": [
    "SMS Messaging",
    "Voice Calls",
    "Spectrum Analysis",
    "SS7 Network Access"
  ],
  "authorized_bands": [
    "698-806 MHz",
    "824-849 MHz",
    "869-894 MHz",
    "1710-1755 MHz",
    "1850-1910 MHz",
    "1930-1990 MHz"
  ]
}
```

## 🌐 SS7 Network Configuration

### Configure Private Network
Set up private SS7 network infrastructure.

```http
POST /api/ss7/configure-private-network
Authorization: Bearer {token}
Content-Type: application/json

{
  "enable_private_network": true,
  "stp_nodes": [
    {
      "point_code": "1-1-1",
      "ip": "192.168.1.10",
      "type": "STP"
    }
  ],
  "sg_nodes": [
    {
      "point_code": "2-2-1",
      "ip": "192.168.1.20",
      "type": "SG"
    }
  ],
  "msc_nodes": [
    {
      "point_code": "3-3-1",
      "ip": "192.168.1.30",
      "type": "MSC"
    }
  ]
}
```

**Response:**
```json
{
  "status": "configured",
  "message": "Private SS7 network infrastructure configured",
  "nodes": {
    "stps": [
      {
        "point_code": "1-1-1",
        "ip": "192.168.1.10",
        "type": "STP"
      }
    ],
    "sgs": [
      {
        "point_code": "2-2-1",
        "ip": "192.168.1.20",
        "type": "SG"
      }
    ],
    "mscs": [
      {
        "point_code": "3-3-1",
        "ip": "192.168.1.30",
        "type": "MSC"
      }
    ]
  }
}
```

### Get Network Status
Check current SS7 network status.

```http
GET /api/ss7/network-status
Authorization: Bearer {token}
```

**Response:**
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
    },
    {
      "id": "sg1",
      "type": "SG",
      "point_code": "2-2-1",
      "status": "online"
    },
    {
      "id": "msc1",
      "type": "MSC",
      "point_code": "3-3-1",
      "status": "online"
    }
  ]
}
```

### Configure SIGTRAN
Set up SIGTRAN for SS7 over IP.

```http
POST /api/ss7/configure-sigtran
Authorization: Bearer {token}
Content-Type: application/json

{
  "enable_sigtran": true,
  "protocol": "m3ua",
  "nodes": [
    {
      "point_code": "1-1-1",
      "ip": "192.168.1.10",
      "port": 2905,
      "protocol": "m3ua",
      "type": "STP"
    }
  ]
}
```

**Response:**
```json
{
  "status": "configured",
  "message": "SIGTRAN SS7 over IP configured with production settings",
  "protocol": "m3ua",
  "nodes": [
    {
      "point_code": "1-1-1",
      "ip": "192.168.1.10",
      "port": 2905,
      "protocol": "m3ua",
      "type": "STP"
    }
  ],
  "security": {
    "tls_enabled": true,
    "authentication_required": true,
    "ip_whitelisting": true,
    "rate_limiting": true,
    "certificate_files": {
      "cert_file": "/etc/ssl/certs/sigtran.crt",
      "key_file": "/etc/ssl/private/sigtran.key",
      "ca_file": "/etc/ssl/certs/ca.crt"
    }
  }
}
```

### Get Transport Status
Check SS7 transport layer status.

```http
GET /api/ss7/transport-status
Authorization: Bearer {token}
```

**Response:**
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
  "endpoints": [
    {
      "name": "STP1",
      "point_code": "1-1-1",
      "ip": "192.168.1.10",
      "port": 2905,
      "protocol": "M3UA",
      "status": "configured"
    }
  ],
  "message": "SS7 messages routed over IP network using SIGTRAN protocols with full security"
}
```

## 🔌 WebSocket Events

### Real-time Events
Connect to WebSocket for real-time system events.

```javascript
const ws = new WebSocket('ws://localhost:8083/ws/events');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Event:', data);
};
```

**Event Types:**
- `heartbeat`: System health check
- `sms_received`: Incoming SMS message
- `call_initiated`: New voice call
- `spectrum_update`: Spectrum analysis update
- `network_status`: SS7 network status change

## 📊 System Information

### Root Endpoint
Get basic system information.

```http
GET /
```

**Response:**
```json
{
  "message": "Telecom API",
  "docs": "/docs",
  "frontend": "http://localhost:8080",
  "license_status": "active",
  "license_info": {
    "license_number": "WP-DOCKET-12345",
    "licensee_name": "Telecom Service Provider",
    "license_type": "Wireless Telecommunications",
    "authorized_services": [
      "SMS Messaging",
      "Voice Calls",
      "Spectrum Analysis",
      "SS7 Network Access"
    ],
    "frequency_bands": [
      "698-806 MHz",
      "824-849 MHz",
      "869-894 MHz"
    ]
  }
}
```

### Health Check
Check system health and status.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:50:00Z",
  "license_valid": true,
  "services": [
    "SMS Messaging",
    "Voice Calls",
    "Spectrum Analysis",
    "SS7 Network Access"
  ]
}
```

## ❌ Error Responses

### Authentication Errors
```json
{
  "detail": "Invalid token"
}
```
**Status Code:** 401

### License Errors
```json
{
  "detail": "Service unavailable - valid telecommunications license required"
}
```
**Status Code:** 503

### Validation Errors
```json
{
  "detail": "Number not found or already assigned"
}
```
**Status Code:** 400

### Server Errors
```json
{
  "detail": "Internal server error"
}
```
**Status Code:** 500

## 📝 Rate Limits

- **Authentication**: 10 requests/minute
- **SMS/Voice**: 1000 requests/minute
- **Spectrum Analysis**: 10 requests/minute
- **Configuration**: 100 requests/minute

## 🔒 Security Headers

All responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`

## 📚 Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation with request/response examples and testing capabilities.
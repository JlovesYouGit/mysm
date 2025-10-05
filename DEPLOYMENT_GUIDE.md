# Production Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB 4.4+
- Docker & Docker Compose
- RTL-SDR hardware (optional)
- Valid telecommunications license

### 1. Clone and Setup
```bash
git clone https://github.com/your-repo/telecom-system.git
cd telecom-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Environment Variables:**
```bash
# Database
MONGO_URL=mongodb://localhost:27017

# SS7 Configuration
SS7_PRIVATE_NETWORK=false
SS7_SIGTRAN=false

# Security
JWT_SECRET_KEY=your-super-secret-key-change-in-production
SSL_CERT_PATH=/etc/ssl/certs/
SSL_KEY_PATH=/etc/ssl/private/

# License
LICENSE_FILE=telecommunications_license.xml
```

### 3. Start Services
```bash
# Development mode
python main.py

# Production mode with Docker
docker-compose up -d
```

## 🏗️ Production Architecture

### Recommended Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (nginx)                    │
├─────────────────────────────────────────────────────────────┤
│  Telecom API (3 instances) │ WebSocket Server │ Frontend   │
├─────────────────────────────────────────────────────────────┤
│     MongoDB Cluster        │    Redis Cache   │ Monitoring │
├─────────────────────────────────────────────────────────────┤
│  RTL-SDR Hardware │ Network Adapters │ SS7 Infrastructure  │
└─────────────────────────────────────────────────────────────┘
```

### Hardware Requirements

**Minimum (Development):**
- CPU: 4 cores, 2.5GHz
- RAM: 8GB
- Storage: 100GB SSD
- Network: 100Mbps

**Recommended (Production):**
- CPU: 8+ cores, 3.0GHz+
- RAM: 32GB+
- Storage: 500GB+ NVMe SSD
- Network: 1Gbps+
- RTL-SDR: RTL2832U or NETGEAR A6210

## 🐳 Docker Deployment

### Production Docker Compose
```yaml
version: '3.8'

services:
  telecom-api:
    build: .
    ports:
      - "8083:8083"
    environment:
      - MONGO_URL=mongodb://mongo:27017
      - SS7_PRIVATE_NETWORK=false
      - SS7_SIGTRAN=true
    depends_on:
      - mongo
      - redis
    volumes:
      - ./ssl:/etc/ssl:ro
      - ./licenses:/app/licenses:ro
      - /dev/bus/usb:/dev/bus/usb  # RTL-SDR access
    devices:
      - /dev/bus/usb
    privileged: true
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G

  mongo:
    image: mongo:6.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=secure_password
    volumes:
      - mongo_data:/data/db
      - ./mongo-init:/docker-entrypoint-initdb.d:ro
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --requirepass secure_redis_password
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl:ro
    depends_on:
      - telecom-api
    restart: unless-stopped

volumes:
  mongo_data:
  redis_data:
```

### Build and Deploy
```bash
# Build production image
docker build -t telecom-api:latest .

# Deploy with compose
docker-compose -f docker-compose.prod.yml up -d

# Scale API instances
docker-compose -f docker-compose.prod.yml up -d --scale telecom-api=3
```

## 🔐 SSL/TLS Configuration

### Generate SSL Certificates
```bash
# Self-signed for development
openssl req -x509 -newkey rsa:4096 -keyout ssl/private/server.key \
  -out ssl/certs/server.crt -days 365 -nodes

# Let's Encrypt for production
certbot certonly --standalone -d your-domain.com
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/certs/
cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/private/
```

### NGINX Configuration
```nginx
upstream telecom_api {
    server telecom-api:8083;
    # Add more instances for load balancing
    # server telecom-api-2:8083;
    # server telecom-api-3:8083;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://telecom_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://telecom_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## 🗄️ Database Setup

### MongoDB Configuration
```javascript
// mongo-init/01-init.js
db = db.getSiblingDB('telecom_service');

db.createUser({
  user: 'telecom_user',
  pwd: 'secure_password',
  roles: [
    {
      role: 'readWrite',
      db: 'telecom_service'
    }
  ]
});

// Create indexes for performance
db.sms.createIndex({ "timestamp": -1 });
db.sms.createIndex({ "to": 1, "from": 1 });
db.calls.createIndex({ "timestamp": -1 });
db.numbers.createIndex({ "number": 1 }, { unique: true });
db.numbers.createIndex({ "user_id": 1 });
db.numbers.createIndex({ "status": 1 });
```

### Database Initialization
```bash
# Initialize database with seed data
python seed_database.py

# Verify database setup
python test_db.py
```

## 📡 Hardware Setup

### RTL-SDR Configuration
```bash
# Install RTL-SDR drivers (Linux)
sudo apt-get update
sudo apt-get install rtl-sdr librtlsdr-dev

# Windows - run as administrator
powershell -ExecutionPolicy Bypass -File install_rtlsdr_drivers.ps1

# Test RTL-SDR
rtl_test -t

# Configure for spectrum analysis
python setup_hardware.py
```

### Network Adapter Setup
```bash
# Configure NETGEAR A6210 (if using)
# Ensure proper drivers are installed
# Configure for monitor mode if needed

# Test network adapter
python test_network_adapter.py
```

## 🌐 SIGTRAN Configuration

### SIGTRAN Network Setup
```python
# sigtran_config.py
SIGTRAN_CONFIG = {
    "protocols": {
        "m3ua": {
            "port": 2905,
            "version": 1,
            "heartbeat_interval": 30
        }
    },
    "point_codes": {
        "local": "2-2-1",
        "remote": ["1-1-1", "3-3-1"]
    },
    "point_code_mapping": {
        "1-1-1": "10.0.1.10",  # Production STP
        "2-2-1": "10.0.1.20",  # Your SG
        "3-3-1": "10.0.1.30"   # Production MSC
    },
    "gateway": {
        "local_interfaces": [
            {
                "ip": "10.0.1.20",
                "port": 2905,
                "protocol": "m3ua"
            }
        ]
    }
}

SIGTRAN_SECURITY = {
    "encryption": {
        "tls_enabled": True,
        "cert_file": "/etc/ssl/certs/sigtran.crt",
        "key_file": "/etc/ssl/private/sigtran.key",
        "ca_file": "/etc/ssl/certs/ca.crt",
        "cipher_suite": "ECDHE-RSA-AES256-GCM-SHA384",
        "verify_peer": True
    },
    "access_control": {
        "authentication_required": True,
        "ip_whitelisting": [
            "10.0.1.0/24",
            "192.168.1.0/24"
        ],
        "rate_limiting": {
            "enabled": True,
            "messages_per_second": 1000,
            "burst_limit": 5000
        }
    }
}
```

### Start SIGTRAN Services
```bash
# Enable SIGTRAN mode
export SS7_SIGTRAN=true

# Start with SIGTRAN configuration
python -c "
import asyncio
from sigtran_service import M3UAService

async def main():
    service = M3UAService()
    await service.initialize()
    print('SIGTRAN service ready')

asyncio.run(main())
"
```

## 📊 Monitoring & Logging

### Logging Configuration
```python
# logging.conf
[loggers]
keys=root,telecom,ss7,sigtran,spectrum

[handlers]
keys=consoleHandler,fileHandler,rotatingFileHandler

[formatters]
keys=simpleFormatter,detailedFormatter

[logger_root]
level=INFO
handlers=consoleHandler,rotatingFileHandler

[logger_telecom]
level=INFO
handlers=fileHandler
qualname=telecom
propagate=0

[logger_ss7]
level=DEBUG
handlers=fileHandler
qualname=ss7
propagate=0

[handler_rotatingFileHandler]
class=handlers.RotatingFileHandler
level=INFO
formatter=detailedFormatter
args=('logs/telecom.log', 'a', 10485760, 5)

[formatter_detailedFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Monitoring Setup
```bash
# Install monitoring tools
pip install prometheus-client grafana-api

# Start monitoring
python monitoring/prometheus_exporter.py &
```

### Health Checks
```bash
# System health check
curl -f http://localhost:8083/health || exit 1

# Database connectivity
python test_mongo_connection.py

# SS7 system status
python test_ss7_system.py

# License validation
python test_licensed_functionality.py
```

## 🔧 Performance Tuning

### Application Optimization
```python
# main.py - Production settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8083,
        workers=4,  # CPU cores
        loop="uvloop",  # High-performance event loop
        http="httptools",  # Fast HTTP parser
        access_log=False,  # Disable for performance
        server_header=False,
        date_header=False
    )
```

### Database Optimization
```javascript
// MongoDB performance settings
db.adminCommand({
  setParameter: 1,
  internalQueryMaxBlockingSortMemoryUsageBytes: 335544320
});

// Connection pooling
db.runCommand({
  setParameter: 1,
  maxIncomingConnections: 1000
});
```

### System Limits
```bash
# /etc/security/limits.conf
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768

# /etc/sysctl.conf
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 5000
```

## 🚨 Troubleshooting

### Common Issues

**1. License Validation Failed**
```bash
# Check license file
ls -la telecommunications_license.xml
python license_validator.py

# Verify license content
python -c "
from license_validator import LicenseValidator
lv = LicenseValidator()
lv.load_license()
print(lv.license_data)
"
```

**2. RTL-SDR Not Detected**
```bash
# Check USB devices
lsusb | grep RTL

# Test RTL-SDR
rtl_test -t

# Check permissions
sudo usermod -a -G plugdev $USER
```

**3. MongoDB Connection Issues**
```bash
# Check MongoDB status
systemctl status mongod

# Test connection
python test_mongo_connection.py

# Check logs
tail -f /var/log/mongodb/mongod.log
```

**4. SIGTRAN Connection Failed**
```bash
# Check network connectivity
ping 192.168.1.10

# Verify certificates
openssl x509 -in /etc/ssl/certs/sigtran.crt -text -noout

# Test SIGTRAN service
python test_sigtran.py
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debug
python main.py --debug

# Check debug logs
tail -f logs/debug.log
```

## 📋 Production Checklist

### Pre-Deployment
- [ ] Valid telecommunications license installed
- [ ] SSL certificates configured
- [ ] Database initialized and secured
- [ ] Hardware (RTL-SDR) tested
- [ ] Network connectivity verified
- [ ] SIGTRAN configuration validated
- [ ] Security settings reviewed
- [ ] Performance testing completed
- [ ] Monitoring configured
- [ ] Backup procedures established

### Post-Deployment
- [ ] Health checks passing
- [ ] License validation working
- [ ] SS7 network connectivity confirmed
- [ ] Spectrum analysis functional
- [ ] API endpoints responding
- [ ] WebSocket connections stable
- [ ] Database performance optimal
- [ ] Logs being generated
- [ ] Monitoring alerts configured
- [ ] Documentation updated

### Security Verification
- [ ] JWT authentication working
- [ ] TLS encryption enabled
- [ ] IP whitelisting configured
- [ ] Rate limiting active
- [ ] Input validation implemented
- [ ] Error handling secure
- [ ] Audit logging enabled
- [ ] Access controls verified

## 🔄 Maintenance

### Regular Tasks
```bash
# Daily
./scripts/health_check.sh
./scripts/backup_database.sh

# Weekly
./scripts/update_certificates.sh
./scripts/performance_report.sh

# Monthly
./scripts/security_audit.sh
./scripts/license_renewal_check.sh
```

### Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Database migrations
python migrate_database.py

# Restart services
docker-compose restart telecom-api
```

This deployment guide provides comprehensive instructions for setting up a production-grade telecommunications system with proper security, monitoring, and performance optimization.
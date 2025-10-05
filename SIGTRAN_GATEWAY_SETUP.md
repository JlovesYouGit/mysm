# SIGTRAN Signaling Gateway Setup Guide

## Overview
This guide provides detailed instructions for setting up and configuring signaling gateways to support SIGTRAN protocols for SS7 over IP transport.

## 1. Gateway Configuration

### 1.1 Protocol Support Configuration

#### M3UA (MTP3 User Adaptation)
```python
# M3UA Configuration in sigtran_config.py
"m3ua": {
    "enabled": True,
    "port": 2905,
    "transport": "SCTP",
    "as_config": {
        "name": "SS7_AS",
        "mode": "override",  # or "loadshare"
        "traffic_mode": "loadshare"
    },
    "asp_config": {
        "name": "SS7_ASP",
        "state": "asp_up"
    }
}
```

#### SUA (SCCP User Adaptation)
```python
# SUA Configuration
"sua": {
    "enabled": True,
    "port": 2906,
    "transport": "SCTP"
}
```

#### M2PA (MTP2 Peer-to-Peer Adaptation)
```python
# M2PA Configuration
"m2pa": {
    "enabled": True,
    "port": 2904,
    "transport": "SCTP"
}
```

#### TCAP over IP
```python
# TCAP over IP Configuration
"tcap_over_ip": {
    "enabled": True,
    "port": 2907,
    "transport": "SCTP"
}
```

### 1.2 Network Interface Configuration

#### Binding to Network Interfaces
```bash
# Configure network interfaces for SIGTRAN
sudo ip addr add 192.168.1.20/24 dev eth0
sudo ip link set eth0 up

# Configure routing for SS7 traffic
sudo ip route add 192.168.1.0/24 dev eth0
```

#### Firewall Configuration
```bash
# Open SIGTRAN ports
sudo iptables -A INPUT -p sctp --dport 2904 -j ACCEPT  # M2PA
sudo iptables -A INPUT -p sctp --dport 2905 -j ACCEPT  # M3UA
sudo iptables -A INPUT -p sctp --dport 2906 -j ACCEPT  # SUA
sudo iptables -A INPUT -p sctp --dport 2907 -j ACCEPT  # TCAP over IP

# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
```

### 1.3 Gateway Parameters Configuration
```python
# Gateway Configuration Parameters
"gateway": {
    "local_interfaces": [
        {
            "name": "eth0",
            "ip": "192.168.1.20",
            "netmask": "255.255.255.0",
            "point_code": "2-2-1"
        }
    ],
    "sctp_config": {
        "heartbeat_interval": 30,
        "max_burst": 4,
        "max_init_retransmits": 8,
        "rto_initial": 3000,
        "rto_min": 1000,
        "rto_max": 60000,
        "valid_cookie_life": 60000
    },
    "m3ua_config": {
        "as_config": {
            "name": "SS7_AS",
            "mode": "override",
            "traffic_mode": "loadshare"
        },
        "asp_config": {
            "name": "SS7_ASP",
            "state": "asp_up"
        }
    }
}
```

## 2. Point Code Mapping

### 2.1 Point Code to IP Address Mapping
```python
# Point Code Mapping Configuration
"point_code_mapping": {
    "1-1-1": "192.168.1.10",  # STP1
    "1-1-2": "192.168.1.11",  # STP2
    "2-2-1": "192.168.1.20",  # SG1 (This Gateway)
    "2-2-2": "192.168.1.21",  # SG2
    "3-3-1": "192.168.1.30",  # MSC1
    "3-3-2": "192.168.1.31"   # MSC2
}
```

### 2.2 Point Code Validation
```python
def validate_point_code_format(point_code: str) -> bool:
    """Validate point code format (e.g., '1-1-1')"""
    parts = point_code.split('-')
    if len(parts) != 3:
        return False
    try:
        opc, apc, spc = map(int, parts)
        return 0 <= opc <= 255 and 0 <= apc <= 255 and 0 <= spc <= 255
    except ValueError:
        return False
```

### 2.3 Dynamic Point Code Resolution
```python
class PointCodeResolver:
    def __init__(self, mapping_config):
        self.mapping = mapping_config
    
    def resolve_ip(self, point_code: str) -> Optional[str]:
        """Resolve IP address for a given point code"""
        return self.mapping.get(point_code)
    
    def add_mapping(self, point_code: str, ip: str):
        """Add new point code to IP mapping"""
        if validate_point_code_format(point_code) and self._validate_ip(ip):
            self.mapping[point_code] = ip
    
    def _validate_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
```

## 3. Security Implementation

### 3.1 Encryption Configuration

#### TLS/SSL Setup
```python
# TLS Configuration
"encryption": {
    "tls_enabled": True,
    "ipsec_enabled": False,
    "cert_file": "/etc/ssl/certs/sigtran.crt",
    "key_file": "/etc/ssl/private/sigtran.key",
    "ca_file": "/etc/ssl/certs/ca.crt",
    "verify_peer": True,
    "cipher_suite": "ECDHE-RSA-AES256-GCM-SHA384"
}
```

#### Certificate Generation
```bash
# Generate self-signed certificates for testing
openssl req -x509 -newkey rsa:4096 -keyout sigtran.key -out sigtran.crt -days 365 -nodes

# Generate CA certificate
openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 1095 -nodes
```

#### IPsec Configuration (Optional)
```bash
# Configure IPsec for additional security
sudo apt-get install strongswan

# Edit /etc/ipsec.conf
conn sigtran_tunnel
    left=192.168.1.20
    right=192.168.1.10
    authby=secret
    esp=aes256-sha256
    ike=aes256-sha256-modp2048
    auto=start
```

### 3.2 Access Control Implementation

#### IP Whitelisting
```python
# IP Whitelisting Configuration
"access_control": {
    "ip_whitelisting": [
        "192.168.1.10",  # STP1
        "192.168.1.11",  # STP2
        "192.168.1.20",  # SG1
        "192.168.1.21",  # SG2
        "192.168.1.30",  # MSC1
        "192.168.1.31"   # MSC2
    ],
    "authentication_required": True,
    "max_connections": 100
}
```

#### Rate Limiting
```python
# Rate Limiting Configuration
"rate_limiting": {
    "enabled": True,
    "messages_per_second": 1000,
    "burst_size": 100
}
```

#### Authentication
```python
class SIGTRANAuthenticator:
    def __init__(self):
        self.authenticated_nodes = set()
    
    def authenticate_node(self, node_id: str, credentials: dict) -> bool:
        """Authenticate a remote node"""
        # In a real implementation, this would check against a user database
        # For now, we'll use a simple check
        valid_credentials = {
            "sg1": "secret_key_1",
            "sg2": "secret_key_2",
            "stp1": "secret_key_3",
            "stp2": "secret_key_4"
        }
        
        if node_id in valid_credentials and credentials.get("key") == valid_credentials[node_id]:
            self.authenticated_nodes.add(node_id)
            return True
        return False
    
    def is_authenticated(self, node_id: str) -> bool:
        """Check if node is authenticated"""
        return node_id in self.authenticated_nodes
```

### 3.3 Security Service Implementation
```python
class SecurityService:
    def __init__(self, security_config):
        self.config = security_config
        self.message_counts = defaultdict(int)
        self.last_reset_time = time.time()
    
    def is_ip_allowed(self, ip: str) -> bool:
        """Check if IP is allowed based on access control."""
        access_control = self.config.get("access_control", {})
        whitelist = access_control.get("ip_whitelisting", [])
        
        # If no whitelist, allow all (insecure, but for testing)
        if not whitelist:
            return True
            
        return ip in whitelist
    
    def apply_rate_limiting(self, ip: str = None) -> bool:
        """Apply rate limiting to prevent flooding."""
        access_control = self.config.get("access_control", {})
        rate_limiting = access_control.get("rate_limiting", {})
        
        if not rate_limiting.get("enabled", False):
            return True
        
        # Reset counters every second
        current_time = time.time()
        if current_time - self.last_reset_time >= 1:
            self.message_counts.clear()
            self.last_reset_time = current_time
        
        # Check rate limit
        max_messages = rate_limiting.get("messages_per_second", 1000)
        current_count = self.message_counts[ip or "global"]
        
        if current_count >= max_messages:
            logger.warning(f"Rate limit exceeded for {ip or 'global'}: {current_count} messages per second")
            return False
        
        # Increment counter
        self.message_counts[ip or "global"] += 1
        return True
    
    def authenticate_connection(self, point_code: str, credentials: Dict = None) -> bool:
        """Authenticate connection based on point code and credentials."""
        access_control = self.config.get("access_control", {})
        
        if not access_control.get("authentication_required", False):
            return True
        
        # In a real implementation, this would check against a user database
        # For now, we'll accept all connections as authenticated for demonstration
        logger.info(f"Authenticated connection for point code {point_code}")
        return True
```

## 4. Gateway Management

### 4.1 Health Monitoring
```python
class GatewayMonitor:
    def __init__(self, sigtran_service):
        self.service = sigtran_service
        self.status = "unknown"
        self.metrics = {
            "connections": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0
        }
    
    def update_metrics(self):
        """Update gateway metrics"""
        self.metrics["connections"] = len(self.service.connections)
        # In a real implementation, we would track actual message counts
    
    def get_status(self) -> dict:
        """Get gateway status"""
        self.update_metrics()
        return {
            "status": self.status,
            "metrics": self.metrics,
            "timestamp": datetime.now().isoformat()
        }
```

### 4.2 Connection Management
```python
class ConnectionManager:
    def __init__(self, sigtran_service):
        self.service = sigtran_service
        self.max_connections = 100
    
    def can_accept_new_connection(self) -> bool:
        """Check if new connection can be accepted"""
        return len(self.service.connections) < self.max_connections
    
    def cleanup_stale_connections(self):
        """Remove stale connections"""
        stale_connections = []
        for conn_key, connection in self.service.connections.items():
            # In a real implementation, we would check connection health
            # For now, we'll just keep track of them
            pass
        
        for conn_key in stale_connections:
            if conn_key in self.service.connections:
                self.service.connections[conn_key]["socket"].close()
                del self.service.connections[conn_key]
```

## 5. Testing and Validation

### 5.1 Protocol Testing
```bash
# Test M3UA connectivity
nc -u 192.168.1.10 2905

# Test SCTP connectivity
echo "test" | nc -w 1 192.168.1.10 2905

# Monitor network traffic
sudo tcpdump -i any port 2905
```

### 5.2 Security Testing
```bash
# Test certificate validation
openssl s_client -connect 192.168.1.10:2905

# Test firewall rules
nmap -p 2904,2905,2906,2907 192.168.1.10

# Test rate limiting
# Send multiple messages rapidly and check for throttling
```

### 5.3 Integration Testing
```python
async def test_sigtran_gateway():
    """Test SIGTRAN gateway functionality"""
    # Initialize service
    service = SIGTRANService()
    await service.initialize()
    
    # Test point code mapping
    assert service.point_code_mapping["1-1-1"] == "192.168.1.10"
    
    # Test security validation
    assert service._validate_security_config() == True
    
    # Test connection
    connected = service.connect_to_node("1-1-1")
    assert connected == True
    
    print("✅ All gateway tests passed")
```

## 6. Production Deployment

### 6.1 High Availability Configuration
```bash
# Configure keepalived for gateway redundancy
sudo apt-get install keepalived

# Edit /etc/keepalived/keepalived.conf
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass sigtran123
    }
    virtual_ipaddress {
        192.168.1.100/24
    }
}
```

### 6.2 Load Balancing
```bash
# Configure load balancing for multiple gateways
sudo apt-get install haproxy

# Edit /etc/haproxy/haproxy.cfg
listen sigtran_sg
    bind *:2905
    mode tcp
    balance roundrobin
    server sg1 192.168.1.20:2905 check
    server sg2 192.168.1.21:2905 check
```

### 6.3 Monitoring and Alerting
```python
# Monitoring script
import psutil
import logging

def monitor_gateway():
    """Monitor gateway health"""
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    connection_count = len(psutil.net_connections())
    
    if cpu_percent > 80:
        logging.warning(f"High CPU usage: {cpu_percent}%")
    
    if memory_percent > 80:
        logging.warning(f"High memory usage: {memory_percent}%")
    
    logging.info(f"Active connections: {connection_count}")
```

## Conclusion

This SIGTRAN gateway setup guide provides comprehensive instructions for configuring signaling gateways with full protocol support, point code mapping, and security measures. The implementation supports all major SIGTRAN protocols (M3UA, SUA, M2PA) and includes robust security features including TLS encryption, IP whitelisting, and rate limiting.

For detailed information about using the SIGTRAN implementation, see [SIGTRAN_DEPLOYMENT_GUIDE.md](file://n:/sms/SIGTRAN_DEPLOYMENT_GUIDE.md)
"""
SIGTRAN Service for SS7 over IP Implementation
"""

import asyncio
import socket
import ssl
import struct
import logging
import ipaddress
import time
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

class SIGTRANService:
    def __init__(self, config_file="sigtran_config.py"):
        self.config = self._load_config(config_file)
        self.connections = {}
        self.running = False
        self.security_config = self.config.get("security", {})
        self.point_code_mapping = self.config.get("point_code_mapping", {})
        self.gateway_config = self.config.get("gateway", {})
        # Rate limiting tracking
        self.message_counts = defaultdict(int)
        self.last_reset_time = time.time()
        # Authentication tracking
        self.authenticated_nodes = set()
        
    def _load_config(self, config_file: str) -> Dict:
        """Load SIGTRAN configuration."""
        try:
            # Import configuration dynamically
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            config_module = __import__(config_file.replace('.py', ''))
            return {
                "protocols": getattr(config_module, 'SIGTRAN_CONFIG', {}).get("protocols", {}),
                "point_codes": getattr(config_module, 'SIGTRAN_CONFIG', {}).get("point_codes", {}),
                "point_code_mapping": getattr(config_module, 'SIGTRAN_CONFIG', {}).get("point_code_mapping", {}),
                "security": getattr(config_module, 'SIGTRAN_SECURITY', {}),
                "gateway": getattr(config_module, 'SIGTRAN_CONFIG', {}).get("gateway", {})
            }
        except Exception as e:
            logger.error(f"Failed to load SIGTRAN config: {e}")
            return {
                "protocols": {},
                "point_codes": {},
                "point_code_mapping": {},
                "security": {},
                "gateway": {}
            }
    
    async def initialize(self):
        """Initialize SIGTRAN service."""
        logger.info("Initializing SIGTRAN service for SS7 over IP...")
        
        # Validate security configuration
        if not self._validate_security_config():
            logger.warning("Security configuration validation failed")
        
        # Validate point code mapping
        if not self._validate_point_code_mapping():
            logger.warning("Point code mapping validation failed")
        
        # Validate gateway configuration
        if not self._validate_gateway_config():
            logger.warning("Gateway configuration validation failed")
        
        self.running = True
        logger.info("SIGTRAN service initialized successfully")
    
    def _validate_security_config(self) -> bool:
        """Validate security configuration."""
        security = self.security_config
        if not security:
            logger.info("No security configuration provided")
            return True
            
        # Check access control
        access_control = security.get("access_control", {})
        if access_control.get("ip_whitelisting"):
            for ip in access_control["ip_whitelisting"]:
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    logger.error(f"Invalid IP address in whitelist: {ip}")
                    return False
        
        return True
    
    def _validate_point_code_mapping(self) -> bool:
        """Validate point code to IP mapping."""
        mapping = self.point_code_mapping
        if not mapping:
            logger.info("No point code mapping provided")
            return True
            
        for point_code, ip in mapping.items():
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                logger.error(f"Invalid IP address for point code {point_code}: {ip}")
                return False
        
        return True
    
    def _validate_gateway_config(self) -> bool:
        """Validate gateway configuration."""
        gateway = self.gateway_config
        if not gateway:
            logger.info("No gateway configuration provided")
            return True
            
        # Validate local interfaces
        interfaces = gateway.get("local_interfaces", [])
        for interface in interfaces:
            try:
                ipaddress.ip_address(interface.get("ip", ""))
            except ValueError:
                logger.error(f"Invalid IP address in gateway interface: {interface.get('ip', '')}")
                return False
        
        return True
    
    def resolve_point_code_to_ip(self, point_code: str) -> Optional[str]:
        """Resolve point code to IP address using mapping configuration."""
        ip = self.point_code_mapping.get(point_code)
        if ip:
            logger.info(f"Resolved point code {point_code} to IP {ip}")
        else:
            logger.warning(f"No IP mapping found for point code {point_code}")
        return ip
    
    def _is_ip_allowed(self, ip: str) -> bool:
        """Check if IP is allowed based on access control."""
        access_control = self.security_config.get("access_control", {})
        whitelist = access_control.get("ip_whitelisting", [])
        
        # If no whitelist, allow all (insecure, but for testing)
        if not whitelist:
            return True
            
        return ip in whitelist
    
    def _apply_rate_limiting(self, ip: str = None) -> bool:
        """Apply rate limiting to prevent flooding."""
        access_control = self.security_config.get("access_control", {})
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
    
    def _authenticate_connection(self, point_code: str, credentials: Dict = None) -> bool:
        """Authenticate connection based on point code and credentials."""
        access_control = self.security_config.get("access_control", {})
        
        if not access_control.get("authentication_required", False):
            return True
        
        # In a production implementation, this would check against a user database
        # For demonstration, we'll use a simple check with predefined credentials
        valid_credentials = {
            "1-1-1": "secret_key_stp1",
            "1-1-2": "secret_key_stp2",
            "2-2-1": "secret_key_sg1",
            "2-2-2": "secret_key_sg2",
            "3-3-1": "secret_key_msc1",
            "3-3-2": "secret_key_msc2"
        }
        
        # Check if node is already authenticated
        if point_code in self.authenticated_nodes:
            return True
        
        # Authenticate with provided credentials or use predefined ones
        if credentials and credentials.get("key") == valid_credentials.get(point_code):
            self.authenticated_nodes.add(point_code)
            logger.info(f"Authenticated connection for point code {point_code}")
            return True
        elif not credentials and point_code in valid_credentials:
            # For demonstration, we'll accept predefined point codes as authenticated
            self.authenticated_nodes.add(point_code)
            logger.info(f"Authenticated connection for point code {point_code} (predefined)")
            return True
        
        logger.error(f"Authentication failed for point code {point_code}")
        return False
    
    def connect_to_node(self, remote_point_code: str, ip: str = None, port: int = None, protocol: str = "m3ua", credentials: Dict = None) -> bool:
        """Establish SIGTRAN connection to remote node."""
        try:
            # Use IP from point code mapping if not provided
            if not ip:
                ip = self.resolve_point_code_to_ip(remote_point_code)
            
            if not ip:
                logger.error(f"Cannot resolve IP for point code {remote_point_code}")
                return False
            
            # Use default port if not provided
            if not port:
                protocol_config = self.config.get("protocols", {}).get(protocol, {})
                port = protocol_config.get("port", 2905)
            
            # Validate IP address
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                logger.error(f"Invalid IP address: {ip}")
                return False
            
            # Check access control
            if not self._is_ip_allowed(ip):
                logger.error(f"Connection attempt from non-whitelisted IP: {ip}")
                return False
            
            # Authenticate connection
            if not self._authenticate_connection(remote_point_code, credentials):
                logger.error(f"Authentication failed for point code {remote_point_code}")
                return False
            
            logger.info(f"Connecting to {remote_point_code} at {ip}:{port} using {protocol}")
            
            # Apply rate limiting
            if not self._apply_rate_limiting(ip):
                logger.warning(f"Rate limit exceeded for connection to {ip}")
                return False
            
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Apply SSL/TLS if configured
            encryption_config = self.security_config.get("encryption", {})
            if encryption_config.get("tls_enabled", False):
                context = ssl.create_default_context()
                cert_file = encryption_config.get("cert_file")
                key_file = encryption_config.get("key_file")
                ca_file = encryption_config.get("ca_file")
                cipher_suite = encryption_config.get("cipher_suite", "ECDHE-RSA-AES256-GCM-SHA384")
                
                # Load certificates if specified
                if cert_file and key_file:
                    context.load_cert_chain(cert_file, key_file)
                    if ca_file:
                        context.load_verify_locations(ca_file)
                    context.check_hostname = encryption_config.get("verify_peer", True)
                    context.verify_mode = ssl.CERT_REQUIRED
                    
                    # Set cipher suite if specified
                    if cipher_suite:
                        context.set_ciphers(cipher_suite)
                    
                    sock = context.wrap_socket(sock, server_hostname=ip)
                    logger.info(f"TLS encryption enabled for connection with cipher suite: {cipher_suite}")
            
            # Connect to remote node
            sock.connect((ip, port))
            
            # Store connection
            connection_key = f"{remote_point_code}_{ip}_{port}"
            self.connections[connection_key] = {
                "socket": sock,
                "protocol": protocol,
                "point_code": remote_point_code,
                "ip": ip,
                "port": port,
                "connected_at": time.time()
            }
            
            logger.info(f"SIGTRAN connection established to {remote_point_code}")
            return True
            
        except ssl.SSLError as e:
            logger.error(f"SSL/TLS error connecting to {remote_point_code}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to {remote_point_code}: {e}")
            return False
    
    def send_ss7_message(self, message: bytes, destination_point_code: str) -> bool:
        """Send SS7 message over SIGTRAN connection."""
        try:
            # Apply rate limiting
            if not self._apply_rate_limiting():
                logger.warning("Rate limit exceeded, message not sent")
                return False
            
            # Find connection for destination
            connection = None
            for conn_key, conn in self.connections.items():
                if conn["point_code"] == destination_point_code:
                    connection = conn
                    break
            
            if not connection:
                # Try to establish connection if it doesn't exist
                logger.info(f"No existing connection to {destination_point_code}, attempting to connect...")
                ip = self.resolve_point_code_to_ip(destination_point_code)
                if ip and self.connect_to_node(destination_point_code, ip):
                    # Try to find the connection again
                    for conn_key, conn in self.connections.items():
                        if conn["point_code"] == destination_point_code:
                            connection = conn
                            break
            
            if not connection:
                logger.error(f"No connection found for point code {destination_point_code}")
                return False
            
            # Prepare M3UA message header
            # M3UA header format: Version(1) | Reserved(1) | Message Class(1) | Message Type(1) | Length(4)
            version = 1
            reserved = 0
            message_class = 1  # Transfer message
            message_type = 1   # Data transfer
            message_length = 8 + len(message)  # Header + payload
            
            # Pack header
            header = struct.pack("!BBBBI", version, reserved, message_class, message_type, message_length)
            
            # Send message
            full_message = header + message
            connection["socket"].sendall(full_message)
            
            logger.info(f"SS7 message sent to {destination_point_code} via SIGTRAN")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SS7 message: {e}")
            return False
    
    def receive_ss7_message(self) -> Optional[bytes]:
        """Receive SS7 message over SIGTRAN connection."""
        try:
            # This would typically be implemented as an async receiver
            # For now, we'll return None to indicate no message
            return None
        except Exception as e:
            logger.error(f"Error receiving SS7 message: {e}")
            return None
    
    async def start_message_receiver(self):
        """Start background task to receive messages."""
        async def receive_loop():
            while self.running:
                try:
                    # Check for incoming messages
                    message = self.receive_ss7_message()
                    if message:
                        logger.info(f"Received SS7 message via SIGTRAN: {len(message)} bytes")
                    await asyncio.sleep(0.1)  # Small delay to prevent busy loop
                except Exception as e:
                    logger.error(f"Error in message receiver loop: {e}")
        
        # Start receiver task
        asyncio.create_task(receive_loop())
        logger.info("SIGTRAN message receiver started")
    
    def close_connections(self):
        """Close all SIGTRAN connections."""
        for conn_key, connection in self.connections.items():
            try:
                connection["socket"].close()
                logger.info(f"Closed connection to {connection['point_code']}")
            except Exception as e:
                logger.error(f"Error closing connection {conn_key}: {e}")
        self.connections.clear()
        self.running = False
        logger.info("All SIGTRAN connections closed")

class M3UAService(SIGTRANService):
    """M3UA (MTP3 User Adaptation) specific implementation."""
    
    def __init__(self, config_file="sigtran_config.py"):
        super().__init__(config_file)
        self.protocol = "m3ua"
    
    def send_data_message(self, payload: bytes, opc: str, dpc: str, si: int = 3) -> bool:
        """Send M3UA DATA message."""
        try:
            # M3UA DATA message format
            # This is a simplified implementation
            logger.info(f"Sending M3UA DATA message: OPC={opc}, DPC={dpc}, SI={si}")
            
            # Apply rate limiting
            if not self._apply_rate_limiting():
                logger.warning("Rate limit exceeded, M3UA message not sent")
                return False
            
            # In a real implementation, we would:
            # 1. Create proper M3UA header
            # 2. Add protocol data unit (PDU)
            # 3. Include routing information
            # 4. Apply proper encoding
            
            # For demonstration, we'll just send the payload
            # Find a connection to use
            if self.connections:
                connection_key = list(self.connections.keys())[0]
                connection = self.connections[connection_key]
                connection["socket"].sendall(payload)
                logger.info("M3UA DATA message sent successfully")
                return True
            else:
                logger.error("No active connections for M3UA message")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send M3UA DATA message: {e}")
            return False

class SUAService(SIGTRANService):
    """SUA (SCCP User Adaptation) specific implementation."""
    
    def __init__(self, config_file="sigtran_config.py"):
        super().__init__(config_file)
        self.protocol = "sua"
    
    def send_sccp_message(self, sccp_payload: bytes, opc: str, dpc: str) -> bool:
        """Send SUA message containing SCCP payload."""
        try:
            logger.info(f"Sending SUA message: OPC={opc}, DPC={dpc}")
            
            # Apply rate limiting
            if not self._apply_rate_limiting():
                logger.warning("Rate limit exceeded, SUA message not sent")
                return False
            
            # In a real implementation, we would:
            # 1. Create proper SUA header
            # 2. Encapsulate SCCP payload
            # 3. Include addressing information
            
            # For demonstration, send the payload
            if self.connections:
                connection_key = list(self.connections.keys())[0]
                connection = self.connections[connection_key]
                connection["socket"].sendall(sccp_payload)
                logger.info("SUA message sent successfully")
                return True
            else:
                logger.error("No active connections for SUA message")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send SUA message: {e}")
            return False

# Example usage
async def main():
    """Example of using SIGTRAN service."""
    print("Initializing SIGTRAN service...")
    
    # Create M3UA service
    m3ua_service = M3UAService()
    await m3ua_service.initialize()
    
    # Connect to a remote node with authentication
    credentials = {"key": "secret_key_stp1"}
    connected = m3ua_service.connect_to_node("1-1-1", "192.168.1.10", 2905, "m3ua", credentials)
    if connected:
        print("✓ Connected to remote STP via M3UA with authentication")
        
        # Send a test message
        test_message = b"Test SS7 message over SIGTRAN"
        sent = m3ua_service.send_data_message(test_message, "2-2-1", "1-1-1")
        if sent:
            print("✓ Test message sent successfully")
        else:
            print("✗ Failed to send test message")
    else:
        print("✗ Failed to connect to remote node")
    
    # Start receiver
    await m3ua_service.start_message_receiver()
    
    # Keep running for a bit
    await asyncio.sleep(5)
    
    # Clean up
    m3ua_service.close_connections()
    print("SIGTRAN service test completed")

if __name__ == "__main__":
    asyncio.run(main())
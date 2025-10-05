"""
SIGTRAN Configuration for SS7 over IP - Production Template

Update this file with information provided by your carrier.
"""

# SIGTRAN Protocol Configuration
SIGTRAN_CONFIG = {
    "protocols": {
        "m3ua": {
            "enabled": True,
            "port": 2905,  # Update with carrier's M3UA port
            "transport": "SCTP",
            "as_config": {
                "name": "SS7_AS",
                "mode": "override",
                "traffic_mode": "loadshare"
            },
            "asp_config": {
                "name": "SS7_ASP",
                "state": "asp_up"
            }
        },
        "sua": {
            "enabled": True,
            "port": 2906,  # Update with carrier's SUA port
            "transport": "SCTP"
        },
        "m2pa": {
            "enabled": True,
            "port": 2904,  # Update with carrier's M2PA port
            "transport": "SCTP"
        },
        "tcap_over_ip": {
            "enabled": True,
            "port": 2907,  # Update with carrier's TCAP over IP port
            "transport": "SCTP"
        }
    },
    "point_codes": {
        "local": "YOUR-SG-POINT-CODE",  # Update with your Signaling Gateway point code
        "remote": "CARRIER-STP-POINT-CODE",  # Update with carrier's STP point code
        "mask": "0-0-0"
    },
    "network_appearance": 100,  # Update with carrier's network appearance
    "routing_context": 1000,  # Update with carrier's routing context
    # Update with carrier's IP addresses and point codes
    "point_code_mapping": {
        "CARRIER-STP-POINT-CODE": "CARRIER-STP-IP-ADDRESS",  # Carrier's STP IP
        "YOUR-SG-POINT-CODE": "YOUR-SG-IP-ADDRESS",  # Your Signaling Gateway IP
        "CARRIER-MSC-POINT-CODE": "CARRIER-MSC-IP-ADDRESS"  # Carrier's MSC IP
    },
    # Gateway Configuration Parameters
    "gateway": {
        "local_interfaces": [
            {
                "name": "eth0",  # Update with your network interface
                "ip": "YOUR-SG-IP-ADDRESS",  # Update with your Signaling Gateway IP
                "netmask": "255.255.255.0",  # Update with your network mask
                "point_code": "YOUR-SG-POINT-CODE"  # Update with your point code
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
        }
    }
}

# SIGTRAN Node Configuration
# Update with your actual node configuration
SIGTRAN_NODES = {
    "sg1": {
        "point_code": "YOUR-SG-POINT-CODE",
        "ip_address": "YOUR-SG-IP-ADDRESS",
        "sigtran_protocols": ["m3ua", "sua"],
        "connections": [
            {
                "remote_point_code": "CARRIER-STP-POINT-CODE",
                "ip": "CARRIER-STP-IP-ADDRESS",
                "port": 2905,
                "protocol": "m3ua"
            },
            {
                "remote_point_code": "CARRIER-MSC-POINT-CODE",
                "ip": "CARRIER-MSC-IP-ADDRESS",
                "port": 2905,
                "protocol": "m3ua"
            }
        ]
    }
}

# SIGTRAN Security Configuration
# Update with your actual security requirements
SIGTRAN_SECURITY = {
    "encryption": {
        "tls_enabled": True,
        "ipsec_enabled": False,
        "cert_file": "/etc/ssl/certs/sigtran.crt",  # Path to server certificate
        "key_file": "/etc/ssl/private/sigtran.key",  # Path to private key
        "ca_file": "/etc/ssl/certs/ca.crt",  # Path to CA certificate
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

# Authentication Credentials
# Update with actual credentials provided by your carrier
AUTHENTICATION_CREDENTIALS = {
    "CARRIER-STP-POINT-CODE": "CARRIER-STP-SECRET-KEY",
    "CARRIER-MSC-POINT-CODE": "CARRIER-MSC-SECRET-KEY"
}
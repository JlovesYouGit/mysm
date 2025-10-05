"""
SS7 Protocol Configuration
"""

# Message Transfer Part (MTP) Configuration
MTP_CONFIG = {
    "mtp_level": 3,  # MTP-Level 3 for routing
    "linkset_redundancy": True,
    "load_balancing": True,
    "error_correction": {
        "crc_check": True,
        "retransmission": True,
        "sequence_check": True
    }
}

# Signaling Connection Control Part (SCCP) Configuration
SCCP_CONFIG = {
    "connection_oriented": True,
    "global_title_translation": True,
    "subsystem_multiplexing": True,
    "error_handling": {
        "timeout": 30,  # seconds
        "retry_attempts": 3
    }
}

# Transaction Capabilities Application Part (TCAP) Configuration
TCAP_CONFIG = {
    "transaction_timeout": 60,  # seconds
    "max_transactions": 1000,
    "dialog_handling": True,
    "component_handling": True
}

# Security Configuration
SECURITY_CONFIG = {
    "encryption": "TLSv1.2",
    "certificate_path": "/etc/ssl/certs/",
    "private_key_path": "/etc/ssl/private/",
    "ip_whitelisting": [
        "192.168.1.10",  # STP1
        "192.168.1.11",  # STP2
        "192.168.1.20",  # SG1
        "192.168.1.21",  # SG2
        "192.168.1.30",  # MSC1
        "192.168.1.31"   # MSC2
    ]
}
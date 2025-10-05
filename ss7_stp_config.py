"""
SS7 Signaling Transfer Point (STP) Configuration
"""

# STP Node Configuration
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
    },
    "node2": {
        "point_code": "1-1-2",
        "ip_address": "192.168.1.11",
        "port": 2905,
        "adjacent_nodes": ["2-2-2", "1-1-1"],
        "linksets": [
            {
                "name": "linkset2",
                "links": [
                    {"ip": "192.168.1.21", "port": 2905},  # SG2
                    {"ip": "192.168.1.10", "port": 2905}   # STP1
                ]
            }
        ]
    }
}

# Routing Table
ROUTING_TABLE = {
    "1-1-1": "192.168.1.10:2905",
    "1-1-2": "192.168.1.11:2905",
    "2-2-1": "192.168.1.20:2905",
    "2-2-2": "192.168.1.21:2905",
    "3-3-1": "192.168.1.30:2905",
    "3-3-2": "192.168.1.31:2905"
}
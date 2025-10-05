"""
SS7 Signaling Gateway (SG) Configuration
"""

# SG Node Configuration
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
    },
    "sg2": {
        "point_code": "2-2-2",
        "ip_address": "192.168.1.21",
        "port": 2905,
        "adjacent_nodes": ["1-1-2", "3-3-2"],
        "linksets": [
            {
                "name": "sg2_linkset",
                "links": [
                    {"ip": "192.168.1.11", "port": 2905},  # STP2
                    {"ip": "192.168.1.31", "port": 2905}   # MSC2
                ]
            }
        ]
    }
}
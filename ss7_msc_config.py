"""
SS7 Mobile Switching Center (MSC) Configuration
"""

# MSC Node Configuration
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
        },
        "linksets": [
            {
                "name": "msc1_linkset",
                "links": [
                    {"ip": "192.168.1.20", "port": 2905}   # SG1
                ]
            }
        ]
    },
    "msc2": {
        "point_code": "3-3-2",
        "ip_address": "192.168.1.31",
        "port": 2905,
        "adjacent_nodes": ["2-2-2"],
        "services": {
            "voice": True,
            "sms": True,
            "data": True
        },
        "linksets": [
            {
                "name": "msc2_linkset",
                "links": [
                    {"ip": "192.168.1.21", "port": 2905}   # SG2
                ]
            }
        ]
    }
}
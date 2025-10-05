#!/bin/bash
# SIGTRAN Production Startup Script

echo "🚀 Starting Telecom System with SIGTRAN Production Configuration"
echo "============================================================="

# Set environment variables for production SIGTRAN deployment
export SS7_SIGTRAN=true
export SS7_PRIVATE_NETWORK=false

echo "Environment Variables:"
echo "  SS7_SIGTRAN=$SS7_SIGTRAN"
echo "  SS7_PRIVATE_NETWORK=$SS7_PRIVATE_NETWORK"
echo ""

# Confirm SIGTRAN configuration
echo "SIGTRAN Configuration:"
echo "  Mode: Production SS7 over IP"
echo "  Protocols: M3UA, SUA, M2PA, TCAP over IP"
echo "  Security: TLS Encryption, Authentication, IP Whitelisting"
echo "  Endpoints:"
echo "    - STP1: 192.168.1.10:2905 (M3UA)"
echo "    - MSC1: 192.168.1.30:2905 (M3UA)"
echo ""

# Start the main application
echo "Starting main application..."
python main.py
#!/bin/bash
# Production Startup Script for Real Telephone Numbers and SS7 with SIGTRAN

echo "🚀 Starting Telecom System with Real SS7 Connectivity"
echo "==================================================="

# Set environment variables for production deployment
export SS7_SIGTRAN=true
export SS7_PRIVATE_NETWORK=false

echo "Environment Variables Set:"
echo "  SS7_SIGTRAN=$SS7_SIGTRAN"
echo "  SS7_PRIVATE_NETWORK=$SS7_PRIVATE_NETWORK"
echo ""

# Verify SSL/TLS certificates exist
echo "Verifying SSL/TLS Certificates..."
if [ -f "/etc/ssl/certs/sigtran.crt" ] && [ -f "/etc/ssl/private/sigtran.key" ] && [ -f "/etc/ssl/certs/ca.crt" ]; then
    echo "✅ SSL/TLS certificates found"
else
    echo "⚠️  SSL/TLS certificates not found"
    echo "   Please deploy certificates to:"
    echo "   - /etc/ssl/certs/sigtran.crt (server certificate)"
    echo "   - /etc/ssl/private/sigtran.key (private key)"
    echo "   - /etc/ssl/certs/ca.crt (CA certificate)"
    echo ""
    echo "Continuing without SSL/TLS (NOT RECOMMENDED FOR PRODUCTION)"
fi

# Verify SIGTRAN configuration
echo ""
echo "Verifying SIGTRAN Configuration..."
if python -c "import sigtran_config; print('✅ SIGTRAN configuration loaded successfully')"; then
    echo "SIGTRAN configuration verified"
else
    echo "❌ SIGTRAN configuration error"
    echo "Please update sigtran_config.py with carrier information"
    exit 1
fi

# Start the main application
echo ""
echo "Starting main application..."
python main.py
#!/bin/bash
# Certificate Deployment Helper Script

echo "🔐 SIGTRAN Certificate Deployment Helper"
echo "========================================"

# Create directory structure
echo "Creating SSL directory structure..."
sudo mkdir -p /etc/ssl/certs /etc/ssl/private

# Check if certificate files exist
if [ -f "sigtran.crt" ] && [ -f "sigtran.key" ] && [ -f "ca.crt" ]; then
    echo "Found certificate files in current directory:"
    echo "  - sigtran.crt (server certificate)"
    echo "  - sigtran.key (private key)"
    echo "  - ca.crt (CA certificate)"
    
    echo ""
    echo "Deploying certificates..."
    
    # Copy certificates to appropriate locations
    sudo cp sigtran.crt /etc/ssl/certs/
    sudo cp sigtran.key /etc/ssl/private/
    sudo cp ca.crt /etc/ssl/certs/
    
    # Set appropriate permissions
    echo "Setting file permissions..."
    sudo chmod 644 /etc/ssl/certs/sigtran.crt
    sudo chmod 600 /etc/ssl/private/sigtran.key
    sudo chmod 644 /etc/ssl/certs/ca.crt
    
    echo "✅ Certificates deployed successfully!"
    echo ""
    echo "Certificate locations:"
    echo "  Server Certificate: /etc/ssl/certs/sigtran.crt"
    echo "  Private Key: /etc/ssl/private/sigtran.key"
    echo "  CA Certificate: /etc/ssl/certs/ca.crt"
    
    # Verify certificates
    echo ""
    echo "Verifying certificates..."
    openssl x509 -in /etc/ssl/certs/sigtran.crt -text -noout > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Server certificate is valid"
    else
        echo "❌ Server certificate validation failed"
    fi
    
else
    echo "❌ Required certificate files not found in current directory."
    echo "Please place the following files in this directory:"
    echo "  - sigtran.crt (server certificate)"
    echo "  - sigtran.key (private key)"
    echo "  - ca.crt (CA certificate)"
    echo ""
    echo "Or generate self-signed certificates for testing:"
    echo "  openssl genrsa -out sigtran.key 2048"
    echo "  openssl req -new -key sigtran.key -out sigtran.csr"
    echo "  openssl x509 -req -days 365 -in sigtran.csr -signkey sigtran.key -out sigtran.crt"
    echo "  openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -days 1095 -nodes"
fi
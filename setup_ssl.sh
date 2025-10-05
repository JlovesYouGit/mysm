#!/bin/bash
# Generate self-signed certificate
openssl req -new -x509 -days 365 -nodes -out asterisk.pem -keyout asterisk.pem -subj "/C=US/ST=State/L=City/O=Globalcomm/CN=localhost"

# For production, use Let's Encrypt:
# sudo apt-get install certbot
# sudo certbot certonly --standalone -d yourdomain.com

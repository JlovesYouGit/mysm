# Deployment Guide - Globalcomm Solutions Telecom Service

## Prerequisites
- PHP 7.4+
- MongoDB 4.4+
- Apache/Nginx
- Asterisk 18+ (for SS7)
- OpenSS7 or DAHDI drivers

## Step 1: Install Dependencies
```bash
composer install
```

## Step 2: MongoDB Setup
```bash
# Download MongoDB from https://www.mongodb.com/try/download/community
mongod --dbpath=data
```

## Step 3: SS7 Library Integration (Asterisk)

### Install Asterisk
```bash
sudo apt-get install asterisk asterisk-dahdi
```

### Configure SS7
1. Copy `asterisk_ss7.conf` to `/etc/asterisk/chan_dahdi.conf`
2. Edit `/etc/asterisk/modules.conf`:
```
load => chan_dahdi.so
```
3. Restart Asterisk:
```bash
sudo systemctl restart asterisk
```
4. Verify SS7:
```bash
asterisk -rx "ss7 show links"
asterisk -rx "ss7 show pointcodes"
```

## Step 4: Redundancy/Failover Setup

### Install Heartbeat
```bash
sudo apt-get install heartbeat
```
Copy `heartbeat.conf` to `/etc/ha.d/ha.cf`

### Install DRBD
```bash
sudo apt-get install drbd-utils
```
Copy `drbd.conf` to `/etc/drbd.d/r0.res`

Initialize DRBD:
```bash
sudo drbdadm create-md r0
sudo drbdadm up r0
sudo drbdadm primary --force r0
```

## Step 5: HTTPS/SSL Certificates

### Generate Self-Signed (Testing)
```bash
bash setup_ssl.sh
```

### Production (Let's Encrypt)
```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /etc/asterisk/keys/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /etc/asterisk/keys/
```

Copy `http_ssl.conf` to `/etc/asterisk/http.conf`

## Step 6: Authentication

Authentication is enabled by default in `api_index.php`
- Username: `admin`
- Password: `telecom2025`

Change credentials in `auth_middleware.php`

## Step 7: Web Server Configuration

### Apache
```apache
<VirtualHost *:80>
    DocumentRoot "N:/sms gone"
    <Directory "N:/sms gone">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

### Nginx
```nginx
server {
    listen 80;
    root N:/sms gone;
    index index.html;
    
    location /api/ {
        rewrite ^/api/(.*)$ /api_index.php last;
    }
}
```

## Step 8: Start Services
```bash
sudo systemctl start apache2
sudo systemctl start mongodb
sudo systemctl start asterisk
```

## Step 9: Access Interface
Open browser: http://localhost

## Testing
```bash
vendor/bin/phpunit test_api.php
```

## API Authentication
All API requests require Basic Auth:
```bash
curl -u admin:telecom2025 http://localhost/api/numbers
```

## Monitoring
- Asterisk CLI: `asterisk -r`
- MongoDB logs: `/var/log/mongodb/mongod.log`
- Apache logs: `/var/log/apache2/error.log`

## Backup
```bash
mongodump --out=/backup/mongodb
tar -czf /backup/config.tar.gz /etc/asterisk
```

# 🚀 Installation & Setup Guide

> **Deploy Your Independent Communication Node** - Complete step-by-step instructions for setting up your own decentralized telecommunications infrastructure.

---

## 📋 **Prerequisites**

### **System Requirements**
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS 10.15+
- **RAM**: Minimum 4GB (8GB+ recommended for community hubs)
- **Storage**: 20GB+ free space (SSD recommended)
- **Network**: Internet connection (for initial setup and bridge mode)
- **USB Ports**: 2+ available USB 3.0 ports

### **Required Hardware**
- **Computer**: PC, Laptop, or Raspberry Pi 4+
- **RTL-SDR Device**: USB software-defined radio dongle
- **Network Adapter**: USB wireless adapter
- **Antenna**: Appropriate for your target frequency
- **Power Supply**: Adequate for your hardware configuration

### **Optional Hardware (Enhanced Performance)**
- **High-gain antennas** for extended range
- **RF amplifiers** for increased power (check local regulations)
- **UPS/Battery backup** for reliability
- **GPS module** for precise timing and location

---

## ⚙️ **Installation Methods**

Choose the method that best fits your technical comfort level:

### **🟢 Method 1: Automated Installer (Recommended for Beginners)**
- One-click installation script
- Automatic dependency management
- Pre-configured settings
- Guided setup wizard

### **🟡 Method 2: Manual Installation (Intermediate)**
- Step-by-step manual setup
- Full control over configuration
- Custom hardware optimization
- Better understanding of system

### **🔴 Method 3: Developer Setup (Advanced)**
- Source code compilation
- Development environment
- Custom modifications
- Contribution preparation

---

## 🟢 **Method 1: Automated Installation**

### **Windows Setup**

1. **Download Installer**
   ```powershell
   # Download the latest installer
   Invoke-WebRequest -Uri "https://github.com/yourusername/decentralized-telecom/releases/latest/download/install-windows.ps1" -OutFile "install.ps1"
   ```

2. **Run Installer**
   ```powershell
   # Run as Administrator
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\install.ps1
   ```

3. **Follow Setup Wizard**
   - Hardware detection and configuration
   - Network settings configuration  
   - License validation
   - Initial system test

### **Linux Setup (Ubuntu/Debian)**

1. **Download and Run Installer**
   ```bash
   # Download installer
   curl -fsSL https://github.com/yourusername/decentralized-telecom/raw/main/install-linux.sh -o install.sh
   
   # Make executable and run
   chmod +x install.sh
   sudo ./install.sh
   ```

2. **Configure System**
   ```bash
   # Follow interactive prompts
   sudo systemctl enable decentralized-telecom
   sudo systemctl start decentralized-telecom
   ```

### **Raspberry Pi Setup**

1. **Pre-built Image (Easiest)**
   ```bash
   # Download pre-configured Raspberry Pi image
   wget https://github.com/yourusername/decentralized-telecom/releases/latest/download/decentralized-comm-rpi.img.gz
   
   # Flash to SD card (use Raspberry Pi Imager)
   # Boot Pi and connect via SSH
   ssh pi@[PI_IP_ADDRESS]
   
   # Run initial configuration
   sudo raspi-config-decentralized
   ```

---

## 🟡 **Method 2: Manual Installation**

### **Step 1: System Preparation**

#### **Windows**
```powershell
# Install Windows Subsystem for Linux (if needed)
wsl --install

# Install Python 3.9+
# Download from python.org

# Install Node.js 16+
# Download from nodejs.org

# Install Git
# Download from git-scm.com
```

#### **Linux (Ubuntu/Debian)**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip nodejs npm git build-essential
sudo apt install -y libusb-1.0-0-dev librtlsdr-dev rtl-sdr

# Install MongoDB
curl -fsSL https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt update
sudo apt install -y mongodb-org
```

### **Step 2: Clone Repository**
```bash
# Clone the project
git clone https://github.com/yourusername/decentralized-telecom.git
cd decentralized-telecom

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### **Step 3: Install Dependencies**

#### **Backend Setup**
```bash
# Install Python dependencies
cd Backend/
pip install -r requirements.txt

# Install RTL-SDR Python library
pip install pyrtlsdr

# Test SDR hardware
python -c "from rtlsdr import RtlSdr; sdr = RtlSdr(); print('SDR detected:', sdr.get_device_serial_addresses())"
```

#### **Frontend Setup**
```bash
# Install Node.js dependencies
cd ../Frontend/nexus-dialer-hub/
npm install

# Build frontend
npm run build
```

### **Step 4: Database Setup**
```bash
# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Initialize database
cd ../../Backend/
python init_database.py
```

### **Step 5: Configuration**

#### **Environment Variables**
```bash
# Copy configuration template
cp Configuration/.env.template Configuration/.env.local

# Edit configuration
nano Configuration/.env.local
```

**Configuration file (.env.local):**
```bash
# Basic Settings
NODE_ID=NODE_$(openssl rand -hex 4)
NODE_NAME="My Communication Node"
LOCATION_LAT=0.0000    # Your latitude
LOCATION_LON=0.0000    # Your longitude

# Network Settings
API_PORT=8083
SPECTRUM_PORT=8084
WEB_PORT=8080

# Database
MONGODB_URL=mongodb://localhost:27017/decentralized_telecom

# RF Settings
SDR_DEVICE=rtlsdr
DEFAULT_FREQUENCY=433500000  # 433.5 MHz
SAMPLE_RATE=2048000

# Security
JWT_SECRET_KEY=$(openssl rand -base64 32)
ADMIN_PASSWORD=your_secure_password_here

# Network Mode
SS7_SIGTRAN=false
SS7_PRIVATE_NETWORK=true  # Start in private network mode
LICENSED_OPERATION=true
```

### **Step 6: Hardware Configuration**

#### **RTL-SDR Setup**
```bash
# Test RTL-SDR device
rtl_test

# Check device permissions
sudo usermod -aG plugdev $USER
# Log out and back in for group changes

# Create udev rules for RTL-SDR
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", GROUP="plugdev", MODE="0666", SYMLINK+="rtl_sdr"' | sudo tee /etc/udev/rules.d/20-rtlsdr.rules
sudo udevadm control --reload-rules
```

#### **Network Adapter Setup**
```bash
# Check wireless interfaces
iwconfig

# Configure wireless interface (if needed)
sudo nano /etc/netplan/01-netcfg.yaml

# Example netplan config:
# network:
#   version: 2
#   wifis:
#     wlan1:  # Your USB adapter
#       dhcp4: yes
#       access-points:
#         "YourNetworkSSID":
#           password: "YourPassword"

# Apply network configuration
sudo netplan apply
```

---

## 🟢 **Quick Start Guide**

### **Start Your Node**

#### **Development Mode (Testing)**
```bash
# Start all services
cd decentralized-telecom/
./Scripts/start-fullstack.sh  # Linux/Mac
# or
.\Scripts\start-fullstack.ps1  # Windows

# Services will start on:
# - Frontend: http://localhost:8080
# - Main API: http://localhost:8083  
# - Spectrum API: http://localhost:8084
```

#### **Production Mode**
```bash
# Install as system service
sudo ./Scripts/install-service.sh

# Start services
sudo systemctl start decentralized-telecom-backend
sudo systemctl start decentralized-telecom-frontend

# Enable auto-start
sudo systemctl enable decentralized-telecom-backend
sudo systemctl enable decentralized-telecom-frontend
```

### **Access Your Node**

1. **Open Web Interface**
   - Navigate to `http://localhost:8080`
   - Or `http://[YOUR_PI_IP]:8080` for Raspberry Pi

2. **Initial Login**
   - Username: `admin`
   - Password: (from your .env.local configuration)

3. **Complete Setup Wizard**
   - Verify hardware detection
   - Configure RF parameters
   - Test communication capabilities
   - Join or create network

---

## 🔧 **Advanced Configuration**

### **RF Parameter Tuning**

#### **Frequency Selection**
```python
# Edit Backend/rf_config.py

# ISM bands (license-free in most countries)
FREQUENCIES = {
    'ISM_433': 433500000,    # 433.5 MHz
    'ISM_915': 915000000,    # 915 MHz (US)
    'ISM_2400': 2450000000,  # 2.45 GHz
}

# Choose based on your region and requirements
DEFAULT_FREQUENCY = FREQUENCIES['ISM_433']
```

#### **Power Settings**
```python
# RF power configuration (stay within legal limits)
RF_POWER_SETTINGS = {
    'LOW': 0.1,      # 100mW
    'MEDIUM': 1.0,   # 1W
    'HIGH': 4.0,     # 4W (check local regulations)
}

# Default power level
DEFAULT_RF_POWER = 'LOW'  # Start conservatively
```

### **Network Topology Configuration**

#### **Node Types**
```python
# Backend/node_config.py

NODE_TYPES = {
    'PERSONAL': {
        'max_connections': 5,
        'routing_enabled': True,
        'power_limit': 1.0,  # Watts
    },
    'COMMUNITY_HUB': {
        'max_connections': 50,
        'routing_enabled': True,
        'power_limit': 10.0,
        'priority_routing': True,
    },
    'REGIONAL_HUB': {
        'max_connections': 200,
        'routing_enabled': True,
        'power_limit': 100.0,
        'mesh_coordinator': True,
    }
}

# Set your node type
NODE_TYPE = 'PERSONAL'  # Start here, upgrade as needed
```

### **Security Configuration**

#### **Encryption Settings**
```python
# Backend/security_config.py

ENCRYPTION_SETTINGS = {
    'algorithm': 'AES-256-GCM',
    'key_rotation_interval': 86400,  # 24 hours
    'auth_timeout': 3600,            # 1 hour
}

# Enable end-to-end encryption
E2E_ENCRYPTION_ENABLED = True
```

#### **Authentication**
```python
# Multi-factor authentication (optional but recommended)
MFA_ENABLED = False  # Enable for production
MFA_METHOD = 'TOTP'  # Time-based one-time passwords

# API rate limiting
RATE_LIMITING = {
    'requests_per_minute': 60,
    'requests_per_hour': 1000,
}
```

---

## 🧪 **Testing Your Installation**

### **System Health Check**
```bash
# Run comprehensive system test
cd Backend/
python system_health_check.py

# Expected output:
# ✅ Database connection: OK
# ✅ RTL-SDR device: OK
# ✅ Network adapter: OK  
# ✅ RF transmission: OK
# ✅ Web interface: OK
# ✅ API endpoints: OK
```

### **RF Hardware Test**
```bash
# Test spectrum analyzer
python test_spectrum_analyzer.py

# Test basic RF transmission (low power)
python test_rf_transmission.py --power 0.1 --freq 433500000

# Measure noise floor
python measure_noise_floor.py
```

### **Network Connectivity Test**
```bash
# Test local network
python test_local_network.py

# Test mesh routing (requires 2+ nodes)
python test_mesh_routing.py --target-node NODE_ABC123

# Performance benchmark
python benchmark_network.py
```

---

## 🌐 **Joining the Network**

### **Network Discovery**
```bash
# Scan for nearby nodes
python scan_network.py

# Example output:
# Found nodes:
# - NODE_ABC123 (Signal: -65dBm, Distance: ~2km)
# - NODE_DEF456 (Signal: -78dBm, Distance: ~5km)
```

### **Connect to Existing Network**
```python
# Backend/network_join.py
KNOWN_NODES = [
    {
        'id': 'NODE_ABC123',
        'frequency': 433500000,
        'location': {'lat': 40.7128, 'lon': -74.0060},
        'public_key': 'base64_encoded_key_here'
    }
]

# Request to join network
JOIN_REQUEST = {
    'node_id': YOUR_NODE_ID,
    'capabilities': ['SMS', 'SPECTRUM_ANALYSIS'],
    'location': {'lat': YOUR_LAT, 'lon': YOUR_LON},
    'public_key': YOUR_PUBLIC_KEY
}
```

### **Create New Network**
```bash
# Initialize as first node in area
python create_network.py --name "Local Community Network" --region "Your Area"

# Network will be assigned:
# - Network ID: NET_XYZ789
# - Frequency plan
# - Routing protocol
# - Security keys
```

---

## 🎯 **Optimization Tips**

### **Performance Tuning**

#### **Hardware Optimization**
```bash
# Optimize RTL-SDR performance
echo 'blacklist dvb_usb_rtl28xxu' | sudo tee -a /etc/modprobe.d/blacklist-rtl.conf

# Set CPU governor for performance
echo 'performance' | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Increase USB buffer sizes
echo 1000 | sudo tee /sys/module/usbcore/parameters/usbfs_memory_mb
```

#### **Network Optimization**
```bash
# Optimize network stack
echo 'net.core.rmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### **Power Management**
```bash
# For battery/solar powered nodes
echo 'powersave' | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Enable aggressive power saving
echo 1 | sudo tee /sys/module/rtl2832u/parameters/power_save
```

### **Storage Optimization**
```bash
# Use log rotation to prevent disk fill
sudo nano /etc/logrotate.d/decentralized-telecom

# Content:
# /var/log/decentralized-telecom/*.log {
#     daily
#     rotate 7
#     compress
#     delaycompress
#     missingok
#     notifempty
#     create 644 decentralized-telecom decentralized-telecom
# }
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **RTL-SDR Not Detected**
```bash
# Check USB connection
lsusb | grep Realtek

# Install drivers
sudo apt install rtl-sdr librtlsdr-dev

# Check permissions
sudo usermod -aG plugdev $USER
# Logout and login again

# Test device
rtl_test -t
```

#### **Web Interface Not Loading**
```bash
# Check if services are running
systemctl status decentralized-telecom-backend
systemctl status decentralized-telecom-frontend

# Check ports
sudo netstat -tlnp | grep -E ':(8080|8083|8084)'

# Check logs
tail -f /var/log/decentralized-telecom/backend.log
tail -f /var/log/decentralized-telecom/frontend.log
```

#### **No Network Connectivity**
```bash
# Check network adapter
iwconfig

# Test RF transmission
python test_rf_basic.py

# Check frequency settings
python check_frequency_config.py

# Verify antenna connection
python measure_swr.py  # If you have SWR meter capability
```

#### **Database Connection Issues**
```bash
# Check MongoDB status
systemctl status mongod

# Test database connection
python test_db_connection.py

# Reset database (if corrupted)
python reset_database.py  # WARNING: This deletes all data
```

### **Debug Mode**
```bash
# Enable verbose logging
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG

# Start with debug output
python main.py --debug --verbose

# Monitor real-time logs
tail -f logs/debug.log
```

### **Performance Issues**
```bash
# Check system resources
htop

# Monitor RF performance
python monitor_rf_performance.py

# Network latency test
ping -c 10 [TARGET_NODE_IP]

# Spectrum analyzer display
python spectrum_monitor.py --gui
```

---

## 📊 **Monitoring & Maintenance**

### **System Monitoring**
```bash
# Install monitoring dashboard
cd Tools/
python install_monitoring.py

# Access monitoring at: http://localhost:3000
# Default login: admin / admin (change immediately)
```

### **Regular Maintenance**
```bash
# Weekly maintenance script
#!/bin/bash
# backup_and_maintain.sh

# Backup configuration
cp Configuration/.env.local /backup/env.local.$(date +%Y%m%d)

# Update software (if available)
git pull origin main
pip install -r Backend/requirements.txt --upgrade

# Clean logs
find logs/ -name "*.log" -mtime +7 -delete

# Test system health
python system_health_check.py

# Restart services
sudo systemctl restart decentralized-telecom-backend
```

### **Security Updates**
```bash
# Check for security updates
python check_security_updates.py

# Update system packages
sudo apt update && sudo apt upgrade -y

# Rotate encryption keys (monthly)
python rotate_encryption_keys.py
```

---

## 🎉 **Success! Your Node is Running**

### **Verification Checklist**
- [ ] Web interface accessible at http://localhost:8080
- [ ] Can login with admin credentials
- [ ] RF hardware detected and functional
- [ ] Network adapter configured
- [ ] Database connection established
- [ ] System health check passes
- [ ] Can send/receive test messages
- [ ] Joined network or created new network

### **Next Steps**
1. **🔧 Optimize configuration** for your specific hardware
2. **📡 Connect with neighbors** to expand network
3. **🧪 Test real-world performance** with friends/family
4. **📚 Read advanced documentation** for additional features
5. **🤝 Join community** discussions and contribute feedback

### **Share Your Success**
- **📸 Share screenshots** of your working system
- **📍 Add your node** to the network map  
- **💬 Join community discussions** about your experience
- **📖 Contribute documentation** improvements
- **🐛 Report any issues** you encountered

---

## 🆘 **Getting Help**

### **Community Support**
- **📋 GitHub Issues** - For bugs and technical problems
- **💬 Community Forum** - For general questions and discussions
- **🔧 Developer Discord** - For real-time technical help
- **📧 Mailing List** - For announcements and updates

### **Documentation**
- **📚 Full Documentation** - Comprehensive guides and references
- **🎥 Video Tutorials** - Step-by-step visual guides  
- **📖 FAQ** - Frequently asked questions
- **🔗 External Resources** - Related projects and tools

### **Professional Support**
For organizations or critical deployments:
- **🏢 Commercial Support** - Professional deployment assistance
- **🎓 Training Programs** - Comprehensive technical training
- **🛠️ Custom Development** - Tailored solutions for specific needs

---

**🎊 Congratulations! You're now part of the decentralized communication revolution!**

*Your node contributes to a more resilient, private, and community-controlled communication infrastructure. Together, we're building the future of independent communications.*
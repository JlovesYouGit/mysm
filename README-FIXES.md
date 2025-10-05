# Telecom System - Fixed Configuration

## Issues Identified and Fixed

1. **Port Mismatch**: The frontend was trying to connect to port 8083, but the start script was launching the backend on port 8082.

2. **Multiple Backend Services**: There were two backend implementations (Node.js and Python) that could conflict with each other.

3. **Missing Environment Configuration**: The frontend didn't have a proper .env file to configure the API endpoint.

4. **Database Initialization**: Missing clear instructions for initializing the MongoDB database.

## Fixed Configuration

### 1. Updated Start Script
The [start-fullstack.ps1](file:///N:/sms/start-fullstack.ps1) script now:
- Properly kills processes on the correct ports (8080 for frontend, 8083 for backend)
- Starts the Python/FastAPI backend on port 8083
- Starts the React frontend on port 8080
- Provides clear status messages

### 2. Frontend Environment Configuration
Created [.env](file:///N:/sms/Frontend%20components/nexus-dialer-hub/.env) file in the frontend directory with:
```
VITE_API_BASE_URL=http://localhost:8083
VITE_WS_URL=ws://localhost:8083/ws/events
```

### 3. Database Initialization Script
Created [init-database.ps1](file:///N:/sms/init-database.ps1) to properly seed the MongoDB database with phone numbers.

## Prerequisites

1. **Node.js**: For the frontend
   - Download from: https://nodejs.org/

2. **Python 3.8+**: For the backend
   - Download from: https://www.python.org/downloads/

## Optional (for persistent storage)

3. **MongoDB**: For persistent data storage
   - Download from: https://www.mongodb.com/try/download/community
   - Install as a service

## Setup Instructions

1. **Install dependencies**:
   ```bash
   # In the root directory
   pip install -r requirements.txt
   
   # In the frontend directory
   cd "Frontend components/nexus-dialer-hub"
   npm install
   cd ../..
   ```

2. **(Optional) Install MongoDB**:
   You can either:
   - Run the automated installer: `.\install-mongodb.ps1` (requires Administrator privileges)
   - Follow manual instructions: `.\setup-mongodb-manual.ps1`

3. **(Optional) Initialize the database** (if MongoDB is installed):
   ```powershell
   .\init-database.ps1
   ```

4. **Start the full stack**:
   ```powershell
   .\start-fullstack.ps1
   ```

## API Endpoints

- **Frontend**: http://localhost:8080/
- **Backend API**: http://localhost:8083/
- **API Documentation**: http://localhost:8083/docs

## Login Credentials

- **Username**: admin
- **Password**: telecom2025

## System Modes

The application can run in two modes:

### 1. Mock Mode (Default)
- Works without MongoDB
- Data is not persisted between sessions
- All core features work (authentication, number management, etc.)
- Perfect for testing and development

### 2. Database Mode (With MongoDB)
- Requires MongoDB to be installed and running
- Data is persisted between sessions
- Full production-like experience

## Troubleshooting

### If you see "Connection refused" errors:
1. Check that no other processes are using ports 8080 or 8083
2. Run the test_connection.py script to diagnose issues:
   ```bash
   python test_connection.py
   ```

### If features still don't work:
1. Check the PowerShell windows for error messages
2. Verify all dependencies are installed:
   ```bash
   # In the root directory
   pip install -r requirements.txt
   
   # In the frontend directory
   npm install
   ```

### If you're seeing PostgreSQL errors:
The system uses MongoDB (or mock data), not PostgreSQL. If you're seeing PostgreSQL errors, they're likely from another service or application.

## Testing the System

You can run the built-in test script to verify all components are working:

```bash
python test_connection.py
```

This will check:
- API connectivity
- Frontend connectivity
- MongoDB connectivity (if available)
- Authentication
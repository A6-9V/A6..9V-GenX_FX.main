# Quickstart Guide - Start Now!

## ⚠️ IMPORTANT: Start Docker Desktop First!

Before running any commands, you **MUST** start Docker Desktop:

1. **Open Docker Desktop** from your Start Menu or Desktop
2. **Wait for it to fully start** - Look for the whale icon in your system tray
3. **Verify it's running** - The Docker Desktop window should show "Docker Desktop is running"

## Quick Start (3 Steps)

### Step 1: Start Docker Desktop
- Open Docker Desktop application
- Wait until you see "Docker Desktop is running" in the window

### Step 2: Run Quickstart Script

**Option A: Double-click (Easiest)**
```
Double-click: START-NOW.bat
```

**Option B: PowerShell**
```powershell
cd C:\Users\USER\OneDrive\exness-docker
.\quickstart.ps1
```

**Option C: Manual**
```powershell
cd C:\Users\USER\OneDrive\exness-docker
docker-compose up -d
```

### Step 3: Verify Services

```powershell
docker-compose ps
```

You should see 5 containers running:
- ✅ exness-trading-bridge
- ✅ exness-postgres
- ✅ exness-redis
- ✅ exness-influxdb
- ✅ exness-grafana

## Account Configuration

### Configure Your Account:

1. **Copy environment template**:
   ```powershell
   Copy-Item config\.env.example .env
   ```

2. **Edit `.env` file** with your EXNESS credentials:
   - `EXNESS_LOGIN` - Your MT5 account number
   - `EXNESS_PASSWORD` - Your MT5 account password
   - `EXNESS_SERVER` - Your MT5 server name
   - `EXNESS_IS_DEMO` - Set to `true` for demo, `false` for live

3. **See [Configuration Guide](CONFIGURATION.md)** for detailed setup instructions

### Connect to MT5:

1. **Open MetaTrader 5**
2. **File → Login to Trade Account**
3. Enter your credentials from `.env` file:
   - **Login**: Your `EXNESS_LOGIN` value
   - **Password**: Your `EXNESS_PASSWORD` value
   - **Server**: Your `EXNESS_SERVER` value
4. Click **Login**

### Attach EA to Chart:

1. Open any chart (e.g., EURUSD)
2. Drag `PythonBridgeEA` from Navigator to chart
3. Configure:
   - **BridgePort**: `5555`
   - **BrokerName**: `EXNESS_DEMO`
   - **AutoExecute**: `true`
4. Click **OK**

## Services URLs

Once running, access:

- **Bridge API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Grafana**: http://localhost:3000 (admin/admin)
- **InfluxDB**: http://localhost:8086

## Troubleshooting

### "Docker Desktop not running"
```
Error: unable to get image... The system cannot find the file specified
```
**Solution**: Start Docker Desktop first!

### "Port already in use"
```
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```
**Solution**: 
- Check what's using the port: `netstat -ano | findstr :8000`
- Stop the conflicting service
- Or change port in `docker-compose.yml`

### "Container keeps restarting"
```powershell
# Check logs
docker-compose logs trading-bridge

# Restart services
docker-compose restart
```

### Services not starting
```powershell
# Rebuild and start
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Quick Commands

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart a service
docker-compose restart trading-bridge
```

## What's Configured

✅ **Account**: Configure in `.env` file (see Configuration Guide)  
✅ **30+ Trading Symbols**: Major pairs, metals, crypto, indices  
✅ **5 Docker Services**: Bridge, PostgreSQL, Redis, InfluxDB, Grafana  
✅ **Risk Management**: 1% per trade, lot size limits  
✅ **Bridge Port**: 5555 for MT5 EA connection  

## Next Steps After Starting

1. ✅ Verify Docker services are running
2. ✅ Connect MT5 to demo account
3. ✅ Attach EA to chart
4. ✅ Test with a small demo trade
5. ✅ Monitor in Grafana dashboard

---

**Ready?** Start Docker Desktop, then run `START-NOW.bat`!


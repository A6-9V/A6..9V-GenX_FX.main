# Quick Start Guide - EXNESS Docker Setup

## Prerequisites Check

1. **Docker Desktop** must be installed and running
   - Download: https://www.docker.com/products/docker-desktop
   - Verify: Open Docker Desktop and ensure it shows "Running"

2. **MT5 Terminal** should be installed at:
   - `C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06`

## Step 1: Launch Docker Services

### Option A: Double-click (Easiest)
```
launch-docker.bat
```

### Option B: PowerShell
```powershell
cd exness-docker
.\launch-docker.ps1
```

### Option C: Manual
```powershell
cd exness-docker
docker-compose up -d
```

## Step 2: Verify Services

Check that all containers are running:
```powershell
docker-compose ps
```

You should see:
- ✅ exness-trading-bridge
- ✅ exness-postgres
- ✅ exness-redis
- ✅ exness-influxdb
- ✅ exness-grafana

## Step 3: Access Services

| Service | URL | Login |
|---------|-----|-------|
| **API Health** | http://localhost:8000/health | - |
| **Grafana** | http://localhost:3000 | admin/admin |
| **InfluxDB** | http://localhost:8086 | admin/adminpassword |

## Step 4: Connect MT5 EA

1. Open MetaTrader 5
2. Attach your EA (e.g., PythonBridgeEA) to a chart
3. Configure EA parameters:
   - **BridgePort**: `5555`
   - **BrokerName**: `EXNESS`
   - **AutoExecute**: `true`
4. Check EA logs in MT5 (View → Terminal → Experts tab)

## Troubleshooting

### "Docker is not running"
- Start Docker Desktop
- Wait for it to fully start
- Try again

### "Port already in use"
- Check what's using the port: `netstat -ano | findstr :5555`
- Stop the conflicting service or change port in `docker-compose.yml`

### "Cannot connect to MT5"
- Verify MT5 path in `docker-compose.yml` (line 18)
- Ensure Docker Desktop has file sharing enabled for C: drive
- Check Docker Desktop → Settings → Resources → File Sharing

### View Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f trading-bridge
```

## Stop Services

```powershell
.\stop-docker.ps1
# or
docker-compose down
```

## Next Steps

1. Configure EXNESS API credentials in `.env` file
2. Set up Grafana dashboards for monitoring
3. Configure your trading strategies
4. Monitor logs and metrics

---

**Need Help?** Check `README.md` for detailed documentation.


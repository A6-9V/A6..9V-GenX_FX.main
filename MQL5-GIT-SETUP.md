# MQL5 Git Repository Setup

## Repository Information

- **Repository URL**: https://forge.mql5.io/LengKundee/mql5.git
- **Username**: LengKundee
- **Location**: `C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06\MQL5`

## Configuration Status

✅ **Git repository configured with credentials**
- Remote URL set with authentication
- Ready for push/pull operations

## Quick Commands

### Check Status
```powershell
cd C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06\MQL5
git status
```

### Pull Latest Changes
```powershell
git pull origin main
```

### Push Changes
```powershell
git add .
git commit -m "Your commit message"
git push origin main
```

### View Remote
```powershell
git remote -v
```

## Integration with EXNESS Docker

The MQL5 repository contains Expert Advisors (EAs) that can connect to the EXNESS Docker bridge:

1. **EA Configuration**:
   - BridgePort: `5555`
   - BrokerName: `EXNESS_DEMO`
   - AutoExecute: `true`

2. **Connection Flow**:
   - MQL5 EA → Docker Bridge (port 5555) → Trading Services
   - Trading Services → PostgreSQL/Redis/InfluxDB → Grafana Dashboard

## Files in Repository

The repository should contain:
- Expert Advisors (`.mq5` files in `Experts/` directory)
- Indicators (`.mq5` files in `Indicators/` directory)
- Scripts (`.mq5` files in `Scripts/` directory)
- Include files (`.mqh` files in `Include/` directory)

## Setup Scripts

- `setup-mql5-git.ps1` - PowerShell setup script
- `setup-mql5-git.bat` - Batch launcher

## Security Note

⚠️ **Credentials are stored in Git remote URL**
- For production, consider using Git credential helper
- Or use SSH keys for authentication

## Next Steps

1. Pull latest code: `git pull origin main`
2. Compile EAs in MetaEditor
3. Attach EA to chart with bridge configuration
4. Connect to EXNESS demo account (279410452)

---

**Last Updated**: 2025-12-29


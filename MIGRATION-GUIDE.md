# Migration Guide - EXNESS Docker Project Restructure

This guide helps existing users migrate to the new project structure and configuration system.

## What Changed?

### ✅ Security Improvements
- **No more hardcoded credentials** in scripts or documentation
- All credentials now stored in `.env` file (git-ignored)
- Enhanced `.gitignore` to prevent accidental credential commits

### ✅ Directory Structure
The project now follows a cleaner, more organized structure:
```
exness-docker/
├── docker/trading-bridge/    # Docker build files
├── config/                    # Configuration files
├── scripts/                   # All PowerShell and batch scripts
├── docs/                      # All documentation
├── bridge/                    # Bridge service code
├── logs/                      # Log files
├── data/                      # Data files
└── docker-compose.yml         # Docker services definition
```

### ✅ Enhanced Symbols Support
- Support for **30+ trading symbols** (previously 20)
- Hybrid configuration: Environment variable + JSON config
- New symbols added: EURCAD, EURCHF, EURAUD, EURNZD, GBPCHF, GBPCAD, GBPAUD, GBPNZD, AUDJPY, CHFJPY, CADJPY, NZDJPY, AUDNZD

### ✅ Environment-Based Configuration
- All configuration moved to `.env` file
- Template file: `env.template` (copy to `.env`)
- Comprehensive documentation in `docs/CONFIGURATION.md`

## Migration Steps

### Step 1: Backup Your Current Configuration

**Important**: Before migrating, backup your existing setup:

```powershell
# Navigate to project directory
cd C:\Users\USER\OneDrive\exness-docker

# Create backup directory
$backupDir = "backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')"
New-Item -ItemType Directory -Path $backupDir

# Backup important files
Copy-Item docker-compose.yml "$backupDir\docker-compose.yml.backup"
if (Test-Path ".env") {
    Copy-Item .env "$backupDir\.env.backup"
}
```

Or use the migration script:
```powershell
.\scripts\migrate-to-new-structure.ps1
```

### Step 2: Update Your Environment Configuration

1. **Copy the template**:
   ```powershell
   Copy-Item env.template .env
   ```

2. **Edit `.env` file** with your credentials:
   ```powershell
   notepad .env
   ```

3. **Required values to update**:
   - `EXNESS_LOGIN` - Your MT5 account number
   - `EXNESS_PASSWORD` - Your MT5 account password
   - `EXNESS_SERVER` - Your MT5 server name
   - `EXNESS_IS_DEMO` - `true` for demo, `false` for live
   - `MT5_PATH` - Path to your MT5 terminal directory
   - `SYMBOLS` - Trading symbols (comma-separated)

### Step 3: Verify Docker Compose Configuration

The `docker-compose.yml` has been updated:
- ✅ Removed duplicate entries
- ✅ Fixed missing PostgreSQL image
- ✅ All credentials now use environment variables
- ✅ Enhanced health checks

**No action needed** - the file is already updated.

### Step 4: Update Script References

All scripts have been updated for the new structure. If you have custom scripts:

- Scripts are now in `scripts/` directory
- Environment template is `env.template` (root) or `.env.example` (if created)
- Configuration files are in `config/` directory

### Step 5: Test Your Setup

1. **Verify environment file**:
   ```powershell
   .\scripts\verify-setup.ps1
   ```

2. **Start services**:
   ```powershell
   .\scripts\launch-docker.ps1
   # Or
   docker-compose up -d
   ```

3. **Check service status**:
   ```powershell
   docker-compose ps
   ```

4. **Verify bridge connection**:
   ```powershell
   curl http://localhost:8000/health
   ```

## Breaking Changes

### ⚠️ Credentials Location
- **Before**: Credentials were hardcoded in scripts/docs
- **After**: All credentials must be in `.env` file

### ⚠️ Script Paths
- **Before**: Scripts might have been in root directory
- **After**: All scripts are in `scripts/` directory

### ⚠️ Environment Template
- **Before**: May have used `.env.example`
- **After**: Uses `env.template` (with fallback to `.env.example`)

## Rollback Instructions

If you need to rollback:

1. **Restore from backup**:
   ```powershell
   # Find your backup directory
   $backupDir = Get-ChildItem -Directory -Filter "backup_*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

   # Restore files
   Copy-Item "$backupDir\docker-compose.yml.backup" "docker-compose.yml" -Force
   if (Test-Path "$backupDir\.env.backup") {
       Copy-Item "$backupDir\.env.backup" ".env" -Force
   }
   ```

2. **Stop and remove containers**:
   ```powershell
   docker-compose down
   ```

3. **Restart with old configuration**:
   ```powershell
   docker-compose up -d
   ```

## Common Issues

### Issue: "Cannot find .env file"
**Solution**: 
```powershell
Copy-Item env.template .env
# Then edit .env with your credentials
```

### Issue: "Services fail to start"
**Solution**:
1. Check `.env` file exists and has all required variables
2. Verify Docker Desktop is running
3. Check logs: `docker-compose logs trading-bridge`

### Issue: "MT5 path not found"
**Solution**:
1. Verify MT5 installation path
2. Update `MT5_PATH` in `.env` file
3. Ensure path uses Windows format: `C:\Users\...`

### Issue: "Port already in use"
**Solution**:
1. Check what's using the port: `netstat -ano | findstr :5555`
2. Change port in `.env` file: `BRIDGE_PORT=5556`
3. Update docker-compose.yml if needed

## Verification Checklist

After migration, verify:

- [ ] `.env` file exists and contains your credentials
- [ ] `docker-compose.yml` has no hardcoded credentials
- [ ] All scripts are in `scripts/` directory
- [ ] Documentation is in `docs/` directory
- [ ] Docker services start successfully
- [ ] Bridge API responds: `curl http://localhost:8000/health`
- [ ] MT5 can connect to bridge on port 5555
- [ ] Grafana dashboard accessible at http://localhost:3000

## Getting Help

If you encounter issues:

1. **Check logs**: `docker-compose logs trading-bridge`
2. **Verify setup**: `.\scripts\verify-setup.ps1`
3. **Review documentation**: 
   - [Configuration Guide](CONFIGURATION.md)
   - [Quick Start Guide](QUICK-START.md)
   - [Architecture](ARCHITECTURE.md)

## Next Steps

After successful migration:

1. ✅ Configure your trading symbols in `config/symbols.json`
2. ✅ Set up Grafana dashboards for monitoring
3. ✅ Connect your MT5 EA to the bridge service
4. ✅ Test with a small demo trade
5. ✅ Review [Architecture Documentation](ARCHITECTURE.md) for system overview

---

**Migration Date**: 2025-12-29  
**Project Version**: 2.0 (Restructured)


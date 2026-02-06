# Workspace Maintenance Guide

**Date**: 2025-12-20  
**Status**: Maintenance Required

## 🔍 Current Situation

Many files appear to have been moved or deleted. This guide helps restore and maintain the workspace.

## 📋 Maintenance Steps

### Step 1: Check Workspace Locations

**Check if files moved to D: drive:**
```powershell
Test-Path "D:\OneDrive"
Get-ChildItem "D:\OneDrive" -File | Select-Object -First 20 Name
```

**Check current location:**
```powershell
Get-Location
Get-ChildItem -File | Select-Object Name
```

### Step 2: Run Maintenance Script

**Double-click:**
```
MAINTAIN-WORKSPACE.bat
```

**Or in PowerShell:**
```powershell
.\workspace-maintenance.ps1
```

This will:
- Check both C: and D: drive locations
- Identify missing essential files
- Verify git repository
- Count scripts and documentation
- Create maintenance summary

### Step 3: Restore from Backup (if needed)

If files were moved to D: drive, check backup:
```powershell
Get-ChildItem "D:\OneDrive-Backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### Step 4: Restore Essential Files

If essential files are missing, they may need to be restored from:
1. D: drive location (if migration completed)
2. Backup folder
3. Git repository (if pushed)

## 🔧 Essential Files to Restore

### Critical Files
- `README.md` - Project documentation
- `.gitignore` - Git exclusions
- `.cursorignore` - Cursor exclusions
- `setup-workspace.ps1` - Workspace setup
- `git-setup.ps1` - Git configuration

### Important Scripts
- `setup-github-credentials.ps1` - GitHub setup
- `setup-exness-professional.ps1` - Exness setup
- `clean-exness-terminal.ps1` - Terminal cleanup
- `manage-exness-terminal.ps1` - Terminal management
- `CHECK-SYMBOL-SETUP.ps1` - Symbol verification

### Configuration Files
- `vps-config.txt` - VPS configuration
- `git-credentials.txt` - GitHub credentials
- `Config/github-config.json` - GitHub config

## 🚀 Quick Restoration

### Option 1: Check D: Drive
```powershell
if (Test-Path "D:\OneDrive") {
    Set-Location "D:\OneDrive"
    Get-ChildItem -File | Select-Object Name
}
```

### Option 2: Restore from Git
```powershell
git status
git restore .
```

### Option 3: Check Backup
```powershell
$backup = Get-ChildItem "D:\OneDrive-Backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Write-Host "Latest backup: $($backup.FullName)"
}
```

## 📝 Maintenance Checklist

- [ ] Run maintenance script
- [ ] Check workspace location (C: or D:)
- [ ] Verify essential files exist
- [ ] Check git repository status
- [ ] Verify scripts are accessible
- [ ] Check documentation files
- [ ] Restore missing files if needed
- [ ] Update paths if on D: drive
- [ ] Test key scripts

## 🎯 Next Actions

1. **Run maintenance:**
   ```
   MAINTAIN-WORKSPACE.bat
   ```

2. **Check summary:**
   - Review `WORKSPACE-MAINTENANCE-SUMMARY.txt`

3. **Restore if needed:**
   - From D: drive if migration completed
   - From backup folder
   - From git repository

4. **Update workspace:**
   - If on D: drive, update Cursor workspace
   - Update GitHub Desktop path
   - Update OneDrive sync location

---

**Run maintenance script first to assess current state!**


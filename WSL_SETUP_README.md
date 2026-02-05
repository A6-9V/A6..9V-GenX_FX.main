# 🐧 WSL Setup for GenX FX on H: Drive

This directory contains all the necessary files and documentation for setting up GenX FX Trading Platform on Windows Subsystem for Linux (WSL) with Docker, specifically configured for H: drive usage with full IDE integration.

---

## 🚀 Quick Start

### For Windows Users (Recommended)

1. **Run PowerShell Setup** (as Administrator):
   ```powershell
   .\setup-windows-wsl.ps1
   ```
   
   This will:
   - Enable WSL and Virtual Machine Platform features
   - Install Ubuntu 22.04
   - Configure WSL settings
   - Check Docker Desktop installation
   - Prepare H: drive

2. **After Setup, Open WSL**:
   ```bash
   wsl
   ```

3. **Navigate to H: Drive and Clone Repository**:
   ```bash
   cd /mnt/h/Projects
   git clone https://github.com/A6-9V/A6..9V-GenX_FX.main.git GenX_FX
   cd GenX_FX
   ```

4. **Run Linux Setup Script**:
   ```bash
   ./setup-wsl.sh
   ```

### For Linux Users (in WSL)

If you already have WSL set up, just run:

```bash
./setup-wsl.sh
```

---

## 📁 Files Overview

### Configuration Files

- **`.wslconfig`** - WSL2 performance configuration (place in Windows user directory)
- **`docker-compose.wsl.yml`** - WSL-optimized Docker Compose configuration
- **`.vscode/`** - Visual Studio Code WSL integration
  - `settings.json` - VSCode settings for WSL
  - `genx-fx-wsl.code-workspace` - Complete workspace configuration
- **`.idea/`** - IntelliJ IDEA / PyCharm configuration
  - Project files and run configurations

### Setup Scripts

- **`setup-windows-wsl.ps1`** - Windows PowerShell script (run as Administrator)
- **`setup-wsl.sh`** - Linux bash script (run inside WSL)

### Documentation

- **`docs/WSL_H_DRIVE_SETUP.md`** - Complete setup guide (11KB, very detailed)
- **`docs/IDE_INTEGRATION_GUIDE.md`** - IDE-specific instructions
- **`WSL_QUICK_REFERENCE.md`** - Quick reference for common commands

---

## 🎯 What's Included

### WSL Configuration
✅ Optimized memory and CPU settings  
✅ Nested virtualization for Docker  
✅ Performance tuning for H: drive  
✅ DNS and network optimization  

### Docker Setup
✅ Docker Compose with WSL optimizations  
✅ Delegated volume mounts for performance  
✅ Named volumes for dependency caching  
✅ BuildKit enabled by default  

### IDE Integration
✅ **VSCode**: Remote-WSL with Python and Docker  
✅ **IntelliJ IDEA**: WSL Python interpreter and Docker  
✅ **PyCharm**: Complete WSL development environment  

### Features
✅ Pre-configured run configurations  
✅ Debug configurations for all IDEs  
✅ Git integration in WSL  
✅ Terminal integration  
✅ File watching optimizations  

---

## 📋 Prerequisites

- Windows 10/11 (version 2004 or higher)
- At least 16GB RAM (32GB recommended)
- 50GB+ free space on H: drive
- Administrator access on Windows

---

## 🔧 Step-by-Step Setup

### 1. Windows Setup (PowerShell as Admin)

```powershell
# Navigate to project directory
cd H:\Projects\GenX_FX

# Run Windows setup script
.\setup-windows-wsl.ps1

# Restart computer if prompted
```

### 2. WSL Setup

```bash
# Open WSL (Ubuntu)
wsl

# Navigate to H: drive
cd /mnt/h/Projects/GenX_FX

# Run Linux setup
./setup-wsl.sh

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

### 3. Build and Run

```bash
# Build Docker images
docker compose -f docker-compose.wsl.yml build

# Start all services
docker compose -f docker-compose.wsl.yml up -d

# Check status
docker compose -f docker-compose.wsl.yml ps

# View logs
docker compose -f docker-compose.wsl.yml logs -f
```

### 4. IDE Setup

Choose your preferred IDE:

#### Visual Studio Code
1. Install Remote-WSL extension
2. Press `Ctrl+Shift+P` → "WSL: Connect to WSL"
3. Open folder: `/mnt/h/Projects/GenX_FX`
4. Or open workspace: `.vscode/genx-fx-wsl.code-workspace`

#### IntelliJ IDEA / PyCharm
1. File → Open → `\\wsl$\Ubuntu-22.04\mnt\h\Projects\GenX_FX`
2. Configure Python Interpreter (Settings → Project → Python Interpreter)
3. Select WSL → Ubuntu-22.04 → `/usr/bin/python3`
4. Configure Docker (Settings → Docker → Add → Docker for Windows)

---

## 🌐 Service URLs

After starting services:

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc
- **Client (dev)**: http://localhost:3000

---

## 🔍 Troubleshooting

### Issue: WSL can't access H: drive

```bash
# Check if mounted
ls /mnt/h

# If not, restart WSL
wsl --shutdown
wsl
```

### Issue: Docker permission denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or restart WSL
```

### Issue: Port already in use

```bash
# Find and kill process
sudo lsof -i :8000
sudo kill -9 <PID>
```

### More Issues?

See detailed troubleshooting in:
- `docs/WSL_H_DRIVE_SETUP.md` - Section "Troubleshooting"
- `docs/IDE_INTEGRATION_GUIDE.md` - Section "Troubleshooting"

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [WSL_H_DRIVE_SETUP.md](docs/WSL_H_DRIVE_SETUP.md) | Complete WSL setup guide (very detailed) |
| [IDE_INTEGRATION_GUIDE.md](docs/IDE_INTEGRATION_GUIDE.md) | VSCode, IntelliJ, PyCharm integration |
| [WSL_QUICK_REFERENCE.md](WSL_QUICK_REFERENCE.md) | Quick command reference |
| [DOCKER_DEPLOYMENT_GUIDE.md](docs/DOCKER_DEPLOYMENT_GUIDE.md) | Docker deployment guide |

---

## ⚡ Quick Commands

```bash
# Start services
docker compose -f docker-compose.wsl.yml up -d

# Stop services
docker compose -f docker-compose.wsl.yml down

# View logs
docker compose -f docker-compose.wsl.yml logs -f

# Rebuild
docker compose -f docker-compose.wsl.yml build --no-cache

# Check status
docker compose -f docker-compose.wsl.yml ps
```

For more commands, see: `WSL_QUICK_REFERENCE.md`

---

## 🆘 Getting Help

1. **Check Documentation**: Start with `docs/WSL_H_DRIVE_SETUP.md`
2. **Quick Reference**: Use `WSL_QUICK_REFERENCE.md` for common commands
3. **IDE Help**: See `docs/IDE_INTEGRATION_GUIDE.md`
4. **GitHub Issues**: [Open an issue](https://github.com/A6-9V/A6..9V-GenX_FX.main/issues)

---

## 💡 Performance Tips

1. **Use delegated mounts** - Already configured in `docker-compose.wsl.yml`
2. **Enable BuildKit** - Set in environment: `export DOCKER_BUILDKIT=1`
3. **Keep .wslconfig updated** - Copy to `C:\Users\YourUsername\.wslconfig`
4. **Clean up regularly** - Run `docker system prune` weekly
5. **Monitor resources** - Use `docker stats` to check usage

---

## ✅ Success Checklist

- [ ] Windows WSL features enabled
- [ ] Ubuntu 22.04 installed in WSL
- [ ] Docker Desktop running with WSL backend
- [ ] H: drive accessible from WSL (`/mnt/h`)
- [ ] Repository cloned to H: drive
- [ ] Environment file configured (`.env`)
- [ ] Docker images built successfully
- [ ] Services running (`docker compose ps`)
- [ ] API responding (http://localhost:8000)
- [ ] IDE connected to WSL
- [ ] Python interpreter configured
- [ ] Docker integration working

---

## 🎉 Next Steps

After successful setup:

1. **Configure API Keys** - Edit `.env` with your keys
2. **Run Tests** - `python run_tests.py`
3. **Start Development** - Open in your favorite IDE
4. **Deploy** - See `docs/DOCKER_DEPLOYMENT_GUIDE.md`

---

**Happy Trading! 🚀📈**

For support, see: [GitHub Issues](https://github.com/A6-9V/A6..9V-GenX_FX.main/issues)

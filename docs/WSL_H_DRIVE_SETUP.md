# 🚀 Docker WSL Setup Guide for GenX FX on H: Drive

This guide provides comprehensive instructions for setting up the GenX FX Trading Platform using Docker on Windows Subsystem for Linux (WSL) on the H: drive, with full integration for VSCode, IntelliJ IDEA, and PyCharm.

---

## 📋 Prerequisites

### Required Software
- **Windows 10/11** (version 2004 or higher)
- **WSL 2** installed and configured
- **Docker Desktop for Windows** (with WSL 2 backend enabled)
- **At least one IDE**:
  - Visual Studio Code with Remote-WSL extension
  - IntelliJ IDEA Ultimate (or PyCharm Professional)
  - PyCharm Professional

### System Requirements
- **RAM**: 16GB minimum (32GB recommended)
- **Storage on H: Drive**: At least 50GB free space
- **CPU**: 4+ cores recommended

---

## 🔧 Step 1: Configure WSL 2 for H: Drive

### 1.1 Enable WSL 2
Open PowerShell as Administrator and run:

```powershell
wsl --install
wsl --set-default-version 2
```

### 1.2 Install Ubuntu on WSL
```powershell
wsl --install -d Ubuntu-22.04
```

### 1.3 Configure WSL to Use H: Drive

Create or edit the `.wslconfig` file in your Windows user directory:

**Option A: Windows User Directory (Recommended)**
```
C:\Users\YourUsername\.wslconfig
```

**Option B: H: Drive User Directory**
```
H:\Users\YourUsername\.wslconfig
```

Copy the `.wslconfig` file from this repository to the appropriate location:

```powershell
# From Windows PowerShell
copy .wslconfig C:\Users\YourUsername\.wslconfig
```

### 1.4 Configure WSL Mount Points

Create a `/etc/wsl.conf` file inside your WSL distribution:

```bash
# Inside WSL terminal
sudo nano /etc/wsl.conf
```

Add the following configuration:

```ini
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"
mountFsTab = true

[network]
generateHosts = true
generateResolvConf = true

[interop]
enabled = true
appendWindowsPath = true
```

Save and exit (Ctrl+X, Y, Enter).

### 1.5 Restart WSL

```powershell
# From PowerShell
wsl --shutdown
wsl
```

---

## 🐳 Step 2: Install Docker in WSL

### 2.1 Update Package Lists
```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2 Install Docker Dependencies
```bash
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### 2.3 Add Docker's Official GPG Key
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### 2.4 Add Docker Repository
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.5 Install Docker Engine
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 2.6 Add Your User to Docker Group
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 2.7 Enable Docker Service
```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### 2.8 Verify Docker Installation
```bash
docker --version
docker compose version
docker run hello-world
```

---

## 📁 Step 3: Set Up Project on H: Drive

### 3.1 Access H: Drive from WSL
```bash
cd /mnt/h
```

### 3.2 Create Project Directory
```bash
# Create a dedicated directory for the project
mkdir -p /mnt/h/Projects/GenX_FX
cd /mnt/h/Projects/GenX_FX
```

### 3.3 Clone Repository
```bash
git clone https://github.com/A6-9V/A6..9V-GenX_FX.main.git .
```

### 3.4 Create Environment File
```bash
cp .env.example .env
# Edit .env with your API keys
nano .env
```

---

## 💻 Step 4: IDE Configuration

### 4.1 Visual Studio Code Setup

#### Install Required Extensions
1. Open VSCode on Windows
2. Install the following extensions:
   - **Remote - WSL** (ms-vscode-remote.remote-wsl)
   - **Docker** (ms-azuretools.vscode-docker)
   - **Python** (ms-python.python)
   - **Pylance** (ms-python.vscode-pylance)
   - **Remote - Containers** (ms-vscode-remote.remote-containers)

#### Open Project in WSL
1. Open VSCode
2. Press `Ctrl+Shift+P` to open command palette
3. Type "WSL: Connect to WSL" and select it
4. Navigate to your project: `/mnt/h/Projects/GenX_FX`
5. Open the workspace: File → Open Workspace from File → Select `.vscode/genx-fx-wsl.code-workspace`

#### VSCode will automatically:
- Use the WSL Python interpreter
- Connect to Docker in WSL
- Configure terminal to use WSL bash
- Apply all WSL-optimized settings

### 4.2 IntelliJ IDEA Setup

#### Configure WSL Integration
1. Open IntelliJ IDEA
2. Go to **File** → **Settings** → **Build, Execution, Deployment** → **WSL**
3. Click **+** to add WSL distribution (Ubuntu-22.04)
4. Click **OK**

#### Configure Python Interpreter for WSL
1. Go to **File** → **Settings** → **Project: GenX_FX** → **Python Interpreter**
2. Click the gear icon → **Add**
3. Select **WSL**
4. Choose your WSL distribution (Ubuntu-22.04)
5. Set Python path: `/usr/bin/python3`
6. Click **OK**

#### Configure Docker for WSL
1. Go to **File** → **Settings** → **Build, Execution, Deployment** → **Docker**
2. Click **+** to add Docker configuration
3. Select **Docker for Windows**
4. Set connection to: `unix:///var/run/docker.sock`
5. Click **Apply** and **OK**

#### Open Project
1. **File** → **Open**
2. Navigate to: `\\wsl$\Ubuntu-22.04\mnt\h\Projects\GenX_FX`
3. Click **OK**

The `.idea` folder in the repository contains pre-configured settings for WSL.

### 4.3 PyCharm Setup

#### Configure WSL Python Interpreter
1. Open PyCharm
2. Go to **File** → **Settings** → **Project: GenX_FX** → **Python Interpreter**
3. Click the gear icon → **Add**
4. Select **WSL**
5. Choose distribution: Ubuntu-22.04
6. Set Python path: `/usr/bin/python3`
7. Click **OK**

#### Configure Docker
1. Go to **File** → **Settings** → **Build, Execution, Deployment** → **Docker**
2. Click **+** to add Docker
3. Select **Docker for Windows**
4. Use WSL socket: `unix:///var/run/docker.sock`
5. Click **OK**

#### Open Project in WSL
1. **File** → **Open**
2. Navigate to: `\\wsl$\Ubuntu-22.04\mnt\h\Projects\GenX_FX`
3. Click **OK**

PyCharm will use the `.idea` configuration files from the repository.

---

## 🚀 Step 5: Build and Run with Docker

### 5.1 Install Project Dependencies

```bash
# Python dependencies
pip3 install -r requirements.txt

# Node.js dependencies
npm install
cd client && npm install && cd ..
```

### 5.2 Build Docker Images
```bash
docker compose -f docker-compose.wsl.yml build
```

### 5.3 Start Services
```bash
docker compose -f docker-compose.wsl.yml up -d
```

### 5.4 View Running Containers
```bash
docker compose -f docker-compose.wsl.yml ps
```

### 5.5 View Logs
```bash
# All services
docker compose -f docker-compose.wsl.yml logs -f

# Specific service
docker compose -f docker-compose.wsl.yml logs -f api
```

### 5.6 Stop Services
```bash
docker compose -f docker-compose.wsl.yml down
```

---

## 🎯 Step 6: Verify Installation

### 6.1 Check API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 6.2 Access Services
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Client** (if running): http://localhost:3000

### 6.3 Test Docker Commands from IDE

#### VSCode
1. Open integrated terminal (WSL)
2. Run: `docker ps`
3. You should see running containers

#### IntelliJ / PyCharm
1. Open terminal (bottom panel)
2. Ensure it's using WSL bash
3. Run: `docker ps`

---

## 🔍 Troubleshooting

### Issue 1: WSL Can't Access H: Drive
**Solution:**
```bash
# Check if H: is mounted
ls /mnt/h

# If not mounted, restart WSL
wsl --shutdown
wsl
```

### Issue 2: Docker Permission Denied
**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
# Or restart WSL
```

### Issue 3: Docker Build is Slow on H: Drive
**Solution:**
The `docker-compose.wsl.yml` file uses `delegated` mount mode for better performance:
```yaml
volumes:
  - .:/app:delegated
```

### Issue 4: IDE Can't Find Python Interpreter
**Solution for all IDEs:**
1. Ensure Python is installed in WSL: `which python3`
2. Path should be: `/usr/bin/python3`
3. Re-configure interpreter in IDE settings

### Issue 5: Port Already in Use
**Solution:**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port in docker-compose.wsl.yml
```

### Issue 6: File Watching Issues in VSCode
**Solution:**
Already configured in `.vscode/settings.json`:
```json
"remote.WSL.fileWatcher.polling": true,
"remote.WSL.fileWatcher.pollingInterval": 5000
```

---

## ⚡ Performance Optimization Tips

### 1. Use Docker BuildKit
Already configured in VSCode workspace:
```bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```

### 2. Keep Source Code on WSL Filesystem
For best performance, consider moving the project to WSL's native filesystem:
```bash
# Instead of /mnt/h/Projects/GenX_FX
# Use: ~/Projects/GenX_FX
```

Then access from Windows via:
```
\\wsl$\Ubuntu-22.04\home\yourusername\Projects\GenX_FX
```

### 3. Configure .dockerignore
Already included in the repository to exclude:
- node_modules
- venv
- .git
- __pycache__
- etc.

### 4. Use Named Volumes for Dependencies
The `docker-compose.wsl.yml` uses named volumes for pip cache:
```yaml
volumes:
  pip-cache:
    driver: local
```

---

## 🔐 Security Considerations

### 1. Environment Variables
- Never commit `.env` file to Git
- Use `.env.example` as a template
- Keep API keys secure

### 2. WSL Security
- Keep WSL updated: `sudo apt update && sudo apt upgrade`
- Don't run services as root
- Use strong passwords for databases

### 3. Docker Security
- Don't expose sensitive ports externally
- Use Docker secrets for production
- Regularly update Docker images

---

## 📚 Additional Resources

### Documentation
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Docker Desktop WSL 2 Backend](https://docs.docker.com/desktop/windows/wsl/)
- [VSCode Remote Development](https://code.visualstudio.com/docs/remote/wsl)
- [IntelliJ WSL Support](https://www.jetbrains.com/help/idea/how-to-use-wsl-development-environment-in-product.html)

### GenX FX Documentation
- [Getting Started Guide](GETTING_STARTED.md)
- [API Documentation](API_KEY_SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)

---

## 🎉 Success Checklist

- [ ] WSL 2 installed and configured
- [ ] Docker running in WSL
- [ ] H: drive accessible from WSL (`/mnt/h`)
- [ ] Project cloned to H: drive
- [ ] IDE(s) connected to WSL
- [ ] Python interpreter configured
- [ ] Docker integration working in IDE
- [ ] Docker Compose services running
- [ ] API responding at http://localhost:8000
- [ ] All tests passing

---

## 🤝 Support

If you encounter issues not covered in this guide:
1. Check the [GitHub Issues](https://github.com/A6-9V/A6..9V-GenX_FX.main/issues)
2. Review the [Troubleshooting section](#-troubleshooting)
3. Create a new issue with:
   - Your OS version
   - WSL version (`wsl --version`)
   - Docker version (`docker --version`)
   - IDE and version
   - Error messages and logs

---

**Happy Trading! 🚀📈**

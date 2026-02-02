# 🎯 IDE Integration Guide for WSL Development

This guide covers the integration of Visual Studio Code, IntelliJ IDEA, and PyCharm with the GenX FX project running on WSL with Docker.

---

## 📑 Table of Contents

1. [Visual Studio Code](#-visual-studio-code)
2. [IntelliJ IDEA](#-intellij-idea)
3. [PyCharm](#-pycharm)
4. [Common Tasks](#-common-tasks)
5. [Troubleshooting](#-troubleshooting)

---

## 💙 Visual Studio Code

### Prerequisites
- VSCode installed on Windows
- Remote-WSL extension installed

### Quick Setup

1. **Install Required Extensions:**
   ```
   Remote - WSL (ms-vscode-remote.remote-wsl)
   Docker (ms-azuretools.vscode-docker)
   Python (ms-python.python)
   Pylance (ms-python.vscode-pylance)
   ```

2. **Connect to WSL:**
   - Press `F1` or `Ctrl+Shift+P`
   - Type: "WSL: Connect to WSL"
   - Select your WSL distribution

3. **Open Project:**
   - File → Open Folder
   - Navigate to: `/mnt/h/Projects/GenX_FX` (or your project path)
   - Or use the workspace: File → Open Workspace → `.vscode/genx-fx-wsl.code-workspace`

### Features Enabled

- ✅ WSL Python interpreter auto-detected
- ✅ Docker integration with WSL backend
- ✅ Git operations in WSL
- ✅ Integrated terminal (WSL bash)
- ✅ File watching optimized for WSL
- ✅ Debug configurations for Python
- ✅ Docker Compose tasks

### Available Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

- **Start GenX API (WSL)** - Run the FastAPI backend
- **Start Client Dev Server (WSL)** - Run the React frontend
- **Docker Build (WSL)** - Build Docker image
- **Docker Compose Up (WSL)** - Start all services
- **Docker Compose Down (WSL)** - Stop all services
- **Install Python Dependencies (WSL)** - Install requirements.txt
- **Install Node Dependencies (WSL)** - Install package.json

### Debug Configurations

Press `F5` to start debugging with:

- **Debug GenX API (WSL)** - Debug FastAPI backend
- **Debug Main Script (WSL)** - Debug main.py
- **Docker: Python (WSL)** - Debug in Docker container

---

## 🔷 IntelliJ IDEA

### Prerequisites
- IntelliJ IDEA Ultimate installed on Windows
- Python plugin installed

### Quick Setup

1. **Enable WSL Support:**
   - File → Settings → Build, Execution, Deployment → WSL
   - Click **+** to add your WSL distribution
   - Select Ubuntu (or your distribution)

2. **Configure Python Interpreter:**
   - File → Settings → Project → Python Interpreter
   - Click gear icon → Add → WSL
   - Select your WSL distribution
   - Python path: `/usr/bin/python3`
   - Apply and OK

3. **Configure Docker:**
   - File → Settings → Build, Execution, Deployment → Docker
   - Click **+** → Docker for Windows
   - Connect via: `unix:///var/run/docker.sock`
   - Apply and OK

4. **Open Project:**
   - File → Open
   - Navigate to: `\\wsl$\Ubuntu-22.04\mnt\h\Projects\GenX_FX`
   - Click OK

### Pre-configured Settings

The repository includes `.idea` folder with:

- ✅ WSL Python interpreter configuration
- ✅ Source folders marked correctly
- ✅ Test runner set to pytest
- ✅ Docker Compose run configurations
- ✅ Python script run configurations

### Run Configurations

Available in the Run menu:

- **Docker Compose WSL** - Start all services
- **GenX API (WSL)** - Run API directly in WSL

### Using Docker in IntelliJ

1. Open **Services** tab (View → Tool Windows → Services)
2. Expand **Docker** → **Containers**
3. Right-click on docker-compose.wsl.yml
4. Select "Deploy"

---

## 🐍 PyCharm

### Prerequisites
- PyCharm Professional installed on Windows

### Quick Setup

1. **Configure WSL Interpreter:**
   - File → Settings → Project → Python Interpreter
   - Click gear icon → Add → WSL
   - Distribution: Ubuntu-22.04
   - Python: `/usr/bin/python3`
   - OK

2. **Configure Docker:**
   - File → Settings → Build, Execution, Deployment → Docker
   - Click **+** → Docker for Windows
   - Connect to: `unix:///var/run/docker.sock`
   - OK

3. **Open Project:**
   - File → Open
   - Navigate to: `\\wsl$\Ubuntu-22.04\mnt\h\Projects\GenX_FX`
   - OK

### Features

- ✅ WSL Python interpreter with full IntelliSense
- ✅ Docker integration
- ✅ Remote debugging in WSL
- ✅ Git operations in WSL
- ✅ Terminal uses WSL bash
- ✅ Database tools (if using SQL)

### Docker Compose in PyCharm

1. Open **Services** tab
2. Find docker-compose.wsl.yml
3. Right-click → "Run"
4. View logs and manage containers

---

## 🔧 Common Tasks

### Start Development Environment

**VSCode:**
```bash
# Open terminal in VSCode (Ctrl+`)
docker compose -f docker-compose.wsl.yml up -d
```

**IntelliJ/PyCharm:**
1. Open Services tab
2. Right-click docker-compose.wsl.yml
3. Select "Deploy" or "Run"

### Run Tests

**VSCode:**
```bash
# In WSL terminal
python run_tests.py
```

**IntelliJ/PyCharm:**
1. Right-click on `run_tests.py`
2. Select "Run 'pytest in run_tests.py'"

### Debug Python Code

**VSCode:**
1. Set breakpoints in Python files
2. Press `F5`
3. Select "Debug GenX API (WSL)"

**IntelliJ/PyCharm:**
1. Set breakpoints
2. Right-click file
3. Select "Debug 'filename'"

### Access Docker Logs

**VSCode:**
```bash
# In terminal
docker compose -f docker-compose.wsl.yml logs -f service_name
```

**IntelliJ/PyCharm:**
1. Services tab → Docker → Containers
2. Right-click container
3. Select "Show Logs"

### Rebuild Docker Images

**All IDEs:**
```bash
docker compose -f docker-compose.wsl.yml build --no-cache
docker compose -f docker-compose.wsl.yml up -d
```

---

## 🔍 Troubleshooting

### IDE Can't Find Python Interpreter

**Solution:**
1. Open WSL terminal
2. Run: `which python3`
3. Copy the path (should be `/usr/bin/python3`)
4. Manually set this path in IDE settings

### Docker Connection Failed

**Solution:**
1. Ensure Docker Desktop is running
2. Check WSL integration in Docker Desktop settings
3. Restart Docker Desktop
4. Restart IDE

### File Watching Not Working (VSCode)

**Solution:**
Already configured in `.vscode/settings.json`:
```json
"remote.WSL.fileWatcher.polling": true
```

If still not working:
1. Reload VSCode window: `Ctrl+Shift+P` → "Reload Window"
2. Or restart VSCode

### Slow Performance on H: Drive

**Recommendations:**

1. **Use WSL Native Filesystem:**
   ```bash
   # Move project to WSL home
   cp -r /mnt/h/Projects/GenX_FX ~/Projects/GenX_FX
   ```
   
   Then access from Windows:
   ```
   \\wsl$\Ubuntu-22.04\home\yourusername\Projects\GenX_FX
   ```

2. **Enable Docker BuildKit:**
   Already configured in docker-compose.wsl.yml with `delegated` mounts

3. **Increase WSL Memory:**
   Edit `.wslconfig` in Windows user directory

### Port Already in Use

**Solution:**
```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Git Operations Slow

**Solution:**
```bash
# Disable file watching for git
git config core.fsmonitor false
```

---

## 📊 IDE Comparison

| Feature | VSCode | IntelliJ IDEA | PyCharm |
|---------|--------|---------------|---------|
| WSL Support | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| Docker Integration | ✅ Good | ✅ Excellent | ✅ Excellent |
| Python IntelliSense | ✅ Good (Pylance) | ✅ Good | ✅ Excellent |
| Debugging | ✅ Good | ✅ Excellent | ✅ Excellent |
| Database Tools | ⚠️ Limited | ✅ Excellent | ✅ Excellent |
| Free/Open Source | ✅ Free | ⚠️ Paid | ⚠️ Paid |
| Resource Usage | 🟢 Light | 🟡 Medium | 🟡 Medium |
| Learning Curve | 🟢 Easy | 🟡 Moderate | 🟢 Easy |

---

## 🎯 Best Practices

### 1. Use WSL Terminal
Always use WSL bash terminal in your IDE for consistency

### 2. Keep Dependencies Updated
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt --upgrade
```

### 3. Use Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Enable Auto-Save
In your IDE settings, enable auto-save to avoid losing changes

### 5. Use Docker BuildKit
Already enabled in the workspace settings for better build performance

---

## 📚 Additional Resources

- [VSCode Remote Development](https://code.visualstudio.com/docs/remote/wsl)
- [IntelliJ WSL Support](https://www.jetbrains.com/help/idea/how-to-use-wsl-development-environment-in-product.html)
- [PyCharm WSL Guide](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html)
- [Docker Desktop WSL 2](https://docs.docker.com/desktop/windows/wsl/)

---

## 💡 Tips for Productive Development

1. **Use IDE's built-in terminal** - It's already configured for WSL
2. **Learn keyboard shortcuts** - Speeds up development significantly
3. **Use Docker Compose** - Simplifies multi-service management
4. **Enable auto-import** - Automatically imports modules
5. **Set up code formatters** - Black for Python, Prettier for JS/TS
6. **Use version control panel** - Built-in Git GUI in all IDEs

---

**Happy Coding! 🚀**

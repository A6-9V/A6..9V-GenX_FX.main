# 🚀 GenX FX - WSL Quick Reference

Quick reference for common commands and operations when using GenX FX on WSL with Docker.

---

## 📁 File System Navigation

```bash
# Access H: drive from WSL
cd /mnt/h

# Access project directory
cd /mnt/h/Projects/GenX_FX

# Access from Windows File Explorer
\\wsl$\Ubuntu-22.04\mnt\h\Projects\GenX_FX

# WSL home directory
cd ~
```

---

## 🐳 Docker Commands

### Docker Compose (WSL Optimized)

```bash
# Build all images
docker compose -f docker-compose.wsl.yml build

# Build without cache
docker compose -f docker-compose.wsl.yml build --no-cache

# Start all services
docker compose -f docker-compose.wsl.yml up -d

# Start specific service
docker compose -f docker-compose.wsl.yml up -d api

# View logs (all services)
docker compose -f docker-compose.wsl.yml logs -f

# View logs (specific service)
docker compose -f docker-compose.wsl.yml logs -f api

# Stop all services
docker compose -f docker-compose.wsl.yml down

# Stop and remove volumes
docker compose -f docker-compose.wsl.yml down -v

# Check service status
docker compose -f docker-compose.wsl.yml ps

# Restart a service
docker compose -f docker-compose.wsl.yml restart api
```

### Docker Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# List images
docker images

# Remove an image
docker rmi <image_id>

# Clean up unused resources
docker system prune -a

# View disk usage
docker system df
```

---

## 🐍 Python Commands

### Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Deactivate
deactivate
```

### Dependencies

```bash
# Install requirements
pip3 install -r requirements.txt

# Upgrade pip
pip3 install --upgrade pip

# Install specific package
pip3 install package_name

# List installed packages
pip3 list

# Freeze requirements
pip3 freeze > requirements.txt
```

### Running Python Scripts

```bash
# Run main application
python3 main.py

# Run API server
python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python3 run_tests.py

# Or use pytest directly
pytest tests/
```

---

## 📦 Node.js / NPM Commands

### Dependencies

```bash
# Install all dependencies
npm install

# Install specific package
npm install package_name

# Install dev dependency
npm install --save-dev package_name

# Update dependencies
npm update
```

### Running Scripts

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

### Client-specific Commands

```bash
# Navigate to client directory
cd client

# Install client dependencies
npm install

# Run client dev server
npm run dev

# Build client
npm run build
```

---

## 🔧 WSL Management

```bash
# Check WSL version
wsl --version

# List installed distributions
wsl --list --verbose

# Set default distribution
wsl --set-default Ubuntu-22.04

# Shutdown WSL
wsl --shutdown

# Restart WSL distribution
wsl --terminate Ubuntu-22.04
wsl

# Update WSL
wsl --update
```

---

## 🛠️ System Maintenance

### Update System

```bash
# Update package lists
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Full upgrade
sudo apt full-upgrade -y

# Clean up
sudo apt autoremove -y
sudo apt autoclean
```

### Check System Resources

```bash
# Disk usage
df -h

# Memory usage
free -h

# CPU info
lscpu

# Running processes
top
# or
htop  # (install with: sudo apt install htop)
```

---

## 🔍 Debugging & Troubleshooting

### Check Service Status

```bash
# Check if API is running
curl http://localhost:8000/health

# Check if Docker daemon is running
docker info

# Check service logs
docker compose -f docker-compose.wsl.yml logs api
```

### Find Process on Port

```bash
# Find what's using port 8000
sudo lsof -i :8000

# Kill process by PID
sudo kill -9 <PID>

# Or use fuser
sudo apt install psmisc
sudo fuser -k 8000/tcp
```

### Check Network

```bash
# Test connectivity
ping google.com

# Check DNS
nslookup google.com

# Check listening ports
sudo netstat -tulpn | grep LISTEN
```

---

## 🔐 Environment & Configuration

```bash
# Edit environment file
nano .env

# View environment variables
env | grep GENX

# Export environment variable
export VARIABLE_NAME=value

# Make script executable
chmod +x script.sh

# Run setup script
./setup-wsl.sh
```

---

## 📊 Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push origin branch-name

# Pull latest
git pull

# Create new branch
git checkout -b feature/new-feature

# View branches
git branch -a

# Switch branch
git checkout branch-name
```

---

## 🎯 IDE Integration

### Open in VSCode

```bash
# From WSL, open current directory in VSCode
code .

# Open specific file
code filename.py
```

### Open in Windows File Explorer

```bash
# Open current directory in Explorer
explorer.exe .
```

---

## ⚡ Performance Tips

```bash
# Enable Docker BuildKit
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Add to .bashrc for persistence
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bashrc

# Reload .bashrc
source ~/.bashrc
```

---

## 🆘 Emergency Commands

```bash
# Kill all Docker containers
docker kill $(docker ps -q)

# Remove all Docker containers
docker rm $(docker ps -a -q)

# Remove all Docker images
docker rmi $(docker images -q)

# Complete Docker cleanup
docker system prune -a --volumes -f

# Restart Docker service in WSL
sudo service docker restart
```

---

## 📱 Service URLs

```
API:              http://localhost:8000
API Docs:         http://localhost:8000/docs
API Redoc:        http://localhost:8000/redoc
Client (dev):     http://localhost:3000
Client (prod):    http://localhost:5173
```

---

## 🔗 Useful Aliases

Add to `~/.bashrc` for quick access:

```bash
# Add these to ~/.bashrc
alias dc='docker compose -f docker-compose.wsl.yml'
alias dcup='docker compose -f docker-compose.wsl.yml up -d'
alias dcdown='docker compose -f docker-compose.wsl.yml down'
alias dclogs='docker compose -f docker-compose.wsl.yml logs -f'
alias dcps='docker compose -f docker-compose.wsl.yml ps'
alias genx='cd /mnt/h/Projects/GenX_FX'

# Reload .bashrc
source ~/.bashrc

# Now you can use:
# dc up -d
# dc logs -f
# dcps
# genx
```

---

## 💡 Pro Tips

1. **Always use docker-compose.wsl.yml** for better WSL performance
2. **Keep dependencies cached** - use named volumes
3. **Use BuildKit** - faster builds
4. **Monitor resources** - `docker stats` shows resource usage
5. **Clean up regularly** - `docker system prune` removes unused data
6. **Use aliases** - save time with custom shortcuts
7. **Check logs often** - `docker compose logs -f` helps debugging
8. **Backup .env** - but never commit it!

---

For detailed documentation, see: [docs/WSL_H_DRIVE_SETUP.md](docs/WSL_H_DRIVE_SETUP.md)

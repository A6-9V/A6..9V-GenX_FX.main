#!/bin/bash
set -e

# GenX FX - Exness VPS Setup Script

echo "========================================"
echo "GenX FX - Exness VPS Setup"
echo "========================================"

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# 1. System Update
echo "[1/7] Updating system..."
apt-get update && apt-get upgrade -y
apt-get install -y curl git ufw software-properties-common build-essential

# 2. Install Python 3.12
echo "[2/7] Installing Python 3.12..."
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip

# 3. Install Node.js (v20)
echo "[3/7] Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g pnpm pm2

# 4. Setup Project Directory
echo "[4/7] Setting up project..."
INSTALL_DIR="/opt/genx-trading"
mkdir -p "$INSTALL_DIR"

# If we are currently in the repo, copy it. Otherwise clone.
if [ -f "requirements.txt" ]; then
    echo "Copying current directory to $INSTALL_DIR..."
    cp -r . "$INSTALL_DIR/"
else
    echo "Cloning repository..."
    # Replace with your actual repo URL if different
    git clone https://github.com/Mouy-leng/GenX_FX.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"
chown -R $SUDO_USER:$SUDO_USER "$INSTALL_DIR" || true

# 5. Install Dependencies
echo "[5/7] Installing dependencies..."
# Create venv
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
pnpm install
pnpm build

# 6. Setup Firewall
echo "[6/7] Configuring firewall..."
ufw allow 22
ufw allow 8000
ufw allow 9090
ufw --force enable

# 7. Create Startup Script (PM2)
echo "[7/7] Configuring startup..."
cat <<EOF > start_system.sh
#!/bin/bash
source venv/bin/activate
pm2 start "uvicorn api.main:app --host 0.0.0.0 --port 8000" --name genx-api
pm2 start "npx serve client/dist -p 3000" --name genx-frontend
pm2 save
pm2 startup
EOF
chmod +x start_system.sh

echo "========================================"
echo "Setup Complete!"
echo "Directory: $INSTALL_DIR"
echo "To start the system:"
echo "  cd $INSTALL_DIR"
echo "  ./start_system.sh"
echo "========================================"

#!/bin/bash

# GenX FX - WSL H: Drive Setup Script
# This script automates the setup process for Docker on WSL with H: drive

set -e

echo "🚀 GenX FX - WSL H: Drive Setup Script"
echo "========================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running in WSL
if ! grep -qi microsoft /proc/version; then
    print_error "This script must be run in WSL (Windows Subsystem for Linux)"
    exit 1
fi
print_success "Running in WSL environment"

# Update system packages
echo ""
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_success "System packages updated"

# Install essential tools
echo ""
echo "🔧 Installing essential tools..."
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release
print_success "Essential tools installed"

# Check if Docker is installed
echo ""
echo "🐳 Checking Docker installation..."
if command -v docker &> /dev/null; then
    print_success "Docker is already installed ($(docker --version))"
else
    print_warning "Docker not found. Installing Docker..."
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    
    print_success "Docker installed successfully"
    print_warning "Please log out and log back in for group changes to take effect"
fi

# Check if H: drive is accessible
echo ""
echo "💾 Checking H: drive accessibility..."
if [ -d "/mnt/h" ]; then
    print_success "H: drive is accessible at /mnt/h"
else
    print_error "H: drive not found at /mnt/h"
    print_warning "Please ensure H: drive is properly mounted in WSL"
    exit 1
fi

# Install Node.js (if not installed)
echo ""
echo "📦 Checking Node.js installation..."
if command -v node &> /dev/null; then
    print_success "Node.js is already installed ($(node --version))"
else
    print_warning "Node.js not found. Installing Node.js 20.x..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
    print_success "Node.js installed successfully ($(node --version))"
fi

# Install Python packages
echo ""
echo "🐍 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_warning "requirements.txt not found in current directory"
fi

# Install Node packages
echo ""
echo "📦 Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    npm install
    print_success "Node.js dependencies installed"
else
    print_warning "package.json not found in current directory"
fi

# Check if client directory exists and install its dependencies
if [ -d "client" ] && [ -f "client/package.json" ]; then
    echo ""
    echo "📦 Installing client dependencies..."
    cd client
    npm install
    cd ..
    print_success "Client dependencies installed"
fi

# Create .env file if it doesn't exist
echo ""
echo "🔐 Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env file from .env.example"
        print_warning "Please edit .env file and add your API keys"
    else
        print_warning ".env.example not found"
    fi
else
    print_success ".env file already exists"
fi

# Docker BuildKit setup
echo ""
echo "⚡ Configuring Docker BuildKit..."
if ! grep -q "DOCKER_BUILDKIT" ~/.bashrc; then
    echo "export DOCKER_BUILDKIT=1" >> ~/.bashrc
    echo "export COMPOSE_DOCKER_CLI_BUILD=1" >> ~/.bashrc
    print_success "Docker BuildKit environment variables added to ~/.bashrc"
else
    print_success "Docker BuildKit already configured"
fi

# Summary
echo ""
echo "=========================================="
echo "🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys: nano .env"
echo "2. Log out and log back in (for Docker group changes)"
echo "3. Build Docker images: docker compose -f docker-compose.wsl.yml build"
echo "4. Start services: docker compose -f docker-compose.wsl.yml up -d"
echo ""
echo "For detailed instructions, see: docs/WSL_H_DRIVE_SETUP.md"
echo ""
echo "To verify Docker: docker run hello-world"
echo "To check services: docker compose -f docker-compose.wsl.yml ps"
echo ""
print_success "Setup script completed successfully!"

#!/usr/bin/env bash
# -------------------------------------------
#  Ultima – full dev-environment bootstrap
# -------------------------------------------

set -euo pipefail

echo "🔧 1/7  Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 2/7  Installing core packages..."
sudo apt install -y git curl wget unzip build-essential \
  software-properties-common jq libfuse2

echo "🐳 3/7  Installing Docker & nvidia-docker2..."
if ! command -v docker &> /dev/null; then
  sudo apt install -y docker.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker $USER
fi
if ! dpkg -l | grep -q nvidia-docker2; then
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
  curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
  curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list
  sudo apt update && sudo apt install -y nvidia-docker2
  sudo systemctl restart docker
fi

echo "🌐 4/7  Installing Node via NVM..."
if [ ! -d "$HOME/.nvm" ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
fi
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"
nvm install --lts
nvm use --lts

echo "🐍 5/7  Setting up Python venv..."
python3 -m venv ~/ultima-venv
source ~/ultima-venv/bin/activate
pip install --upgrade pip

echo "🔐 6/7  Checking SSH key..."
if [ ! -f "$HOME/.ssh/id_ed25519.pub" ]; then
  ssh-keygen -t ed25519 -C "$USER@$(hostname)"
  echo "👉  Add this key to GitHub:"
  cat ~/.ssh/id_ed25519.pub
fi

echo "📁 7/7  Confirming folder structure..."
tree -d -L 2 ~/Ultima || true

echo "✅  SETUP COMPLETE.  Run:  source ~/ultima-venv/bin/activate" 
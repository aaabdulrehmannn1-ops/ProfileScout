#!/bin/bash
# ===========================================================================
#  ProfileScout Setup Script for macOS/Linux
#  Complete installation and dependency setup
# ===========================================================================

echo ""
echo "==========================================================================="
echo "         ProfileScout - OSINT Reconnaissance Tool Setup"
echo "==========================================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[✗] Python 3 is not installed"
    echo ""
    echo "Please install Python 3:"
    echo "  macOS:  brew install python3"
    echo "  Ubuntu: sudo apt-get install python3 python3-pip"
    echo "  CentOS: sudo yum install python3 python3-pip"
    echo ""
    exit 1
fi

# Display Python version
echo "[+] Python found:"
python3 --version
echo ""

# Install pip if needed
echo "[*] Installing dependencies..."
echo "    Installing: requests..."
pip3 install requests

if [ $? -ne 0 ]; then
    echo "[✗] Failed to install requests"
    exit 1
fi

echo "    Installing: colorama..."
pip3 install colorama

if [ $? -ne 0 ]; then
    echo "[✗] Failed to install colorama"
    exit 1
fi

echo ""
echo "[+] All dependencies installed successfully!"
echo ""

# Verify installation
echo "[*] Verifying installation..."
python3 -c "import requests; print('[+] requests version: ' + requests.__version__)"
python3 -c "import colorama; print('[+] colorama version: ' + colorama.__version__)"

echo ""
echo "==========================================================================="
echo "         Setup Complete! You're ready to run ProfileScout"
echo "==========================================================================="
echo ""
echo "Quick Start:"
echo "  python3 profilescout.py"
echo ""
echo "For more information, see:"
echo "  README.md - Comprehensive documentation"
echo "  QUICKSTART.md - Quick start guide"
echo "  examples.py - Usage examples"
echo ""
